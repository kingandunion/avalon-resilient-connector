import re
import json
import logging

from circuits.core.handlers import handler
from resilient_circuits.actions_component import ResilientComponent, ActionMessage, StatusMessage

from avalon.lib import resilient_api as res
from avalon.lib.errors import IntegrationError, WorkspaceLinkError
from avalon.lib import avalon_api as av

logger = logging.getLogger(__name__)

# maps Avalon Node type to IBM Resilient Artifact type
node_to_artifact_type = dict(
    ip = res.ArtifactType.ip_address,
    domain = res.ArtifactType.dns_name,
    url = res.ArtifactType.url,
    email = res.ArtifactType.email_sender,
)

# maps IBM Resilient Artifact type to Avalon Node type
artifact_to_node_type = dict(reversed(item) for item in node_to_artifact_type.items())

class AvalonActions(ResilientComponent):
    # Subscribe to the message destination named "avalon_actions"
    channel = "actions.avalon_actions"
    
    def __init__(self, opts):
        """constructor provides access to the configuration options"""
        super(AvalonActions, self).__init__(opts)
        
        self.res_options = opts.get("resilient", {})

        self.options = opts.get("avalon", {})
        res.validate_fields(["api_token"], self.options)

        self.api_token = self.options["api_token"]


    @handler("reload")
    def handle_reload(self, event, opts):
        """Configuration options have changed, save new values"""
        self.res_options = opts.get("resilient", {})
        
        self.options = opts.get("avalon", {})
        res.validate_fields(["api_token"], self.options)

        self.api_token = self.options["api_token"]


    # Handles Avalon: Create Workspace action 
    @handler("avalon_create_workspace")
    def handle_avalon_create_workspace(self, event, *args, **kwargs):
        return self._avalon_create_workspace(event, args, kwargs)


    # Handles "Avalon: Pull All Nodes" action 
    @handler("avalon_pull_all_nodes")
    def handle_avalon_pull_nodes(self, event, *args, **kwargs):
        return self._avalon_pull_all_nodes(event, args, kwargs)


    # Handles "Avalon: Push All Artifacts" action. This is called for artifacts only 
    @handler("avalon_push_all_artifacts")
    def handle_avalon_push_all_artifact(self, event, *args, **kwargs):
        return self._avalon_push_all_artifacts(event, args, kwargs)


    # Handles "Avalon: Push Artifact" action. This is called for artifacts only 
    @handler("avalon_push_artifact")
    def handle_avalon_push_artifact(self, event, *args, **kwargs):
        return self._avalon_push_artifact(event, args, kwargs)


    def _avalon_create_workspace(self, event, *args, **kwargs):
        # Any string returned by the handler function is shown to the Resilient user in the Action Status dialog

        # the user who triggered the action
        who = event.message["user"]["email"]

        # incident data (and other context)
        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        # TODO: Eventually we might allow user to specify the name and the summary 
        # for the new Avalon workspace in IBM Resilient and pass those values 
        # res.validate_fields([u"avalon_workspace_title", u"avalon_workspace_summary"], kwargs)

        # workspace_title = clean_html(kwargs.get(u"avalon_workspace_title"))  # text
        # workspace_summary = clean_html(kwargs.get(u"avalon_workspace_summary"))  # text

        try:
            # create Avalon workspace
            self._create_workspace(incident, who)
            return "Avalon workspace created successfully."
        except WorkspaceLinkError:
            return "Avalon workspace already exists for this incident."
        except Exception as err:
            # TODO: Find out how we can return errors from custom action handlers    
            # see: https://10.1.0.151/docs/rest-api/json_AcknowledgementDTO.html
            
            # return json.dumps({ 
            #     "message_type": { "id": 1, "name": "error" },
            #     "message": str(err), 
            #     "complete": True,
            #     "results" : { }
            # })

            # NOTE: This will still mark the action as complete in IBM Resilient
            return "Error: {}".format(str(err))


    def _create_workspace(self, incident, who):
        # check whether Avalon workspace has been created for this incident already
        if incident["properties"]["avalon_workspace_id"]:
            raise WorkspaceLinkError("Already linked to Avalon Workspace ID: {}.".format(incident["avalon_workspace_id"]))   

        workspace_title = "{} (IBM Resilient)".format(incident["name"])
        workspace_summary = "Created from IBM Resilient by {}. IBM Resilient Incident ID: {}".format(who, incident["id"])
        
        data = {
            "Title": workspace_title, 
            "Summary": workspace_summary, 
            "TLP": "r", 
            "ShareWithMyOrganization": False
        }

        resp = av.workspace_create_empty(self.api_token, data, logger)
        (error, msg) = av.check_error(resp, logger)
        if error:
            raise IntegrationError(msg)

        # workspace data looks like: {"data": {"path": "https://example.com...aces/22/ "}}
        result = resp.json()
        workspace_data = result["data"]
        workspace_url = workspace_data["path"].strip() 
        workspace_id = av.workspace_id_from_url(workspace_url)

        # Set the workspace id field
        res.incident_set_avalon_workspace_id(self.rest_client(), incident["id"], workspace_id)

        # Add a new artifact to the incident
        artifact_title = "Avalon Workspace"
        artifact_description = "Avalon workspace address: {}".format(workspace_url)
        res.incident_add_workspace_artifact(self.rest_client(), 
                                                incident["id"], 
                                                artifact_title, artifact_description, 
                                                workspace_id, workspace_url)


    def _avalon_pull_all_nodes(self, event, *args, **kwargs):
        # Any string returned by the handler function is shown to the Resilient user in the Action Status dialog

        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        try:
            incident_id = incident["id"]
            artifacts = res.incident_get_artifacts(self.rest_client(), incident_id)

            # get workspace ID
            workspace_id = incident["properties"].get("avalon_workspace_id", None)
            if not workspace_id:
                raise Exception("Please create Avalon workspace for this incident first.") 

            # Call to get workspace / graph object. We need the graph UUID
            workspace_uuid = self._get_avalon_workspace_uuid(workspace_id)

            # Get all avalon nodes
            nodes = self._get_avalon_workspace_nodes(workspace_id, workspace_uuid)
            if nodes is None:
                return "Avalon workspace does not contains any nodes."

            # import the nodes into the IBM resilient incident
            self._resilient_add_artifacts(incident_id, artifacts, nodes)

            return "Successfully pulled all nodes from Avalon."
        except Exception as err:
            # NOTE: This will still mark the action as complete in IBM Resilient
            return "Error: {}".format(str(err))


    # matches nodes to artifacts by type and value 
    # imports only the nodes that are new  
    def _resilient_add_artifacts(self, incident_id, artifacts, nodes):
        for node in nodes:
            node_value = node[0]
            node_type = node[1]

            # check whether it is a supported artifact            
            artifact_type = node_to_artifact_type.get(node_type)
            if artifact_type is None:
                continue

            # check whether artifact with the same type and value already exists 
            artifact_value = node_value   
            matching_artifacts = [
                a for a in artifacts 
                if a["type"] == artifact_type and a["value"] == artifact_value
            ]

            if len(matching_artifacts) > 0:
                continue

            # add new artifact to incident
            artifact_description = "Created from Avalon workspace node."
            res.incident_add_artifact(self.rest_client(), incident_id, artifact_type, artifact_value, artifact_description)


    def _avalon_push_all_artifacts(self, event, *args, **kwargs):
        # Any string returned by the handler function is shown to the Resilient user in the Action Status dialog

        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        try:
            incident_id = incident["id"]
            artifacts = res.incident_get_artifacts(self.rest_client(), incident_id)

            # get workspace ID
            workspace_id = incident["properties"].get("avalon_workspace_id", None)
            if not workspace_id:
                raise Exception("Please create Avalon workspace for this incident first.") 

            # Call to get workspace / graph object. We need the graph UUID
            workspace_uuid = self._get_avalon_workspace_uuid(workspace_id)

            # Get all avalon nodes
            nodes = self._get_avalon_workspace_nodes(workspace_id, workspace_uuid)

            # Push all artifacts
            total_success = True            
            for artifact in artifacts:
                # ignore the special Avalon Workspace artifact
                artifact_type = res.get_artifact_property(artifact, "type")
                if artifact_type and artifact_type == "avalon_workspace":
                    continue

                # add only if node does not exist 
                if not self._find_node_for_artifact(nodes, artifact):
                   success = self._add_workspace_node(artifact, workspace_id)
                   total_success = total_success and success 

            if not total_success:
                return "Some artifacts could not be pushed to Avalon."
    
            return "Successfully pushed all artifacts to Avalon."
        except Exception as err:
            # NOTE: This will still mark the action as complete in IBM Resilient
            return "Error: {}".format(str(err))


    def _avalon_push_artifact(self, event, *args, **kwargs):
        # incident data (and other context)
        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        # artifact data (and other context)
        artifact = event.message["artifact"]
        logger.info("Called from artifact {}: {}".format(artifact["id"], artifact["value"]))

        try:
            # Add Avalon node
            self._push_artifact(incident, artifact)
            return "{} added to Avalon.".format(artifact["value"])
        except Exception as err:
            # NOTE: This will still mark the action as complete in IBM Resilient
            return "Error: {}".format(str(err))


    def _push_artifact(self, incident, artifact):
        # get workspace ID
        workspace_id = incident["properties"].get("avalon_workspace_id", None)
        if not workspace_id:
            raise Exception("Please create Avalon workspace for this incident first.") 

        # Call to get workspace / graph object. We need the graph UUID
        workspace_uuid = self._get_avalon_workspace_uuid(workspace_id)

        # Get all avalon nodes
        nodes = self._get_avalon_workspace_nodes(workspace_id, workspace_uuid)
        
        if self._find_node_for_artifact(nodes, artifact):
            raise Exception("Could not add Avalon node. A node with value {} already exists.".format(artifact["value"]))

        if self._add_workspace_node(artifact, workspace_id):
            return

        # We should never reach this line if action conditions are properly set
        raise IntegrationError("Unsupported artifact.")


    def _add_workspace_node(self, artifact, workspace_id):
        if artifact["type"] != res.ArtifactType.dns_name:
            return False    

        data = {
            "nodes": [ 
                { 
                    "term": artifact["value"],
                    "type": "domain" 
                } 
            ]
        }

        resp = av.workspace_add_node(self.api_token, workspace_id, data, logger)
        (error, msg) = av.check_error(resp, logger)
        if error:
            raise IntegrationError(msg)

        return True


    def _find_node_for_artifact(self, nodes, artifact):
        # check whether node with the same type and value already exists in the workspace
        if not nodes:
            return False

        for node in nodes:
            node_value = node[0]
            node_type = node[1]

            artifact_value = node_value                      

            artifact_type = node_to_artifact_type.get(node_type)
            if not artifact_type:
                continue

            if artifact["type"] == artifact_type and artifact["value"] == artifact_value:
                return True

        return False


    def _get_avalon_workspace_uuid(self, workspace_id):
        # Call to get workspace / graph object. We need the graph UUID
        resp = av.workspace_get(self.api_token, workspace_id, logger)
        (error, msg) = av.check_error(resp, logger)
        if error:
            raise IntegrationError(msg)

        result = resp.json()

        # get UUID
        return result["data"]["attributes"]["UUID"]


    def _get_avalon_workspace_nodes(self, workspace_id, workspace_uuid):
        # export the nodes from the Avalon workspace 
        resp = av.workspace_export(workspace_id, workspace_uuid, "json", logger)
        (error, msg) = av.check_error(resp, logger)
        if error:
            raise IntegrationError(msg)

        result = resp.json()
        nodes = result["data"]

        return nodes





