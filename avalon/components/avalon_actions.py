import re
import json
import logging

from circuits.core.handlers import handler
from resilient_circuits.actions_component import ResilientComponent, ActionMessage, StatusMessage

from avalon.lib import resilient_api as res
from avalon.lib.errors import IntegrationError, WorkspaceExistsError
from avalon.lib import avalon_api as av

logger = logging.getLogger(__name__)

class AvalonActions(ResilientComponent):
    # Subscribe to the message destination named "avalon_actions"
    channel = "actions.avalon_actions"

    # maps Avalon Graph Node type to IBM Resilient Incident Artifact type
    node_artifact_type = {
        "ip": res.ArtifactType.ip_address,
        "domain" : res.ArtifactType.dns_name
    } 
    
    def __init__(self, opts):
        """constructor provides access to the configuration options"""
        super(AvalonActions, self).__init__(opts)
        
        self.res_options = opts.get("resilient", {})

        self.options = opts.get("avalon", {})
        res.validate_fields(["api_token"], self.options)

        self.api_token = self.options["api_token"]


    @handler("reload")
    def _reload(self, event, opts):
        """Configuration options have changed, save new values"""
        self.res_options = opts.get("resilient", {})
        
        self.options = opts.get("avalon", {})
        res.validate_fields(["api_token"], self.options)

        self.api_token = self.options["api_token"]


    # Handles avalon_create_workspace action 
    @handler("avalon_create_workspace")
    def _avalon_create_workspace(self, event, *args, **kwargs):
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
            self._create_empty_workspace(incident, who)

            # Any string returned by the handler function is shown to the Resilient user in the Action Status dialog
            return "Avalon workspace created successfully."
        except WorkspaceExistsError:
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


    # Handles the avalon_pull_workspace_nodes action 
    @handler("avalon_pull_workspace_nodes")
    def _avalon_pull_workspace_nodes(self, event, *args, **kwargs):
        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        try:
            incident_id = incident["id"]
            artifacts = res.incident_get_artifacts(self.rest_client(), incident_id)
            workspace_artifact = res.incident_get_workspace_artifact(self.rest_client(), incident_id, artifacts)

            if not workspace_artifact:
                raise Exception("Please create Avalon workspace for this incident first.")   

            # get workspace ID
            workspace_id = res.get_artifact_property(workspace_artifact, "id")    

            # Call to get workspace / graph object. We need the graph UUID
            resp = av.workspace_get(self.api_token, workspace_id, logger)
            (error, msg) = av.check_error(resp, logger)
            if error:
                raise IntegrationError(msg)

            result = resp.json()

            # get UUID
            workspace_uuid = result["data"]["attributes"]["UUID"]

            # export the nodes from the Avalon workspace 
            resp = av.workspace_export(workspace_id, workspace_uuid, "json", logger)
            (error, msg) = av.check_error(resp, logger)
            if error:
                raise IntegrationError(msg)

            result = resp.json()
            nodes = result["data"]
            if nodes is None:
                return "Avalon workspace does not contains any nodes."

            # import the nodes into the IBM resilient incident
            self._import_avalon_nodes(incident_id, artifacts, nodes)

            # Any string returned by the handler function is shown to the Resilient user in the Action Status dialog
            return "Successfully refreshed all artifacts from Avalon."
        except Exception as err:
            # NOTE: This will still mark the action as complete in IBM Resilient
            return "Error: {}".format(str(err))

    # matches nodes to artifacts by type and value 
    # and adds the nodes that are new  
    def _import_avalon_nodes(self, incident_id, artifacts, nodes):
        for node in nodes:
            node_value = node[0]
            node_type = node[1]

            # check whether it is a supported artifact            
            artifact_type = self.node_artifact_type.get(node_type)
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

    # Handles avalon_add_node action. This is called for artifacts only 
    @handler("avalon_add_node")
    def _avalon_add_node(self, event, *args, **kwargs):
        # incident data (and other context)
        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        # artifact data (and other context)
        artifact = event.message["artifact"]
        logger.info("Called from artifact {}: {}".format(artifact["id"], artifact["value"]))

        try:
            # Add Avalon node
            self._add_node(incident, artifact)
            return "{} added to Avalon.".format(artifact["value"])
        except Exception as err:
            # NOTE: This will still mark the action as complete in IBM Resilient
            return "Error: {}".format(str(err))


    def _add_node(self, incident, artifact):
        # check whether Avalon workspace has been created for this incident already
        workspace_artifact = res.incident_get_workspace_artifact(self.rest_client(), incident["id"])
        if not workspace_artifact:
            raise Exception("Please create Avalon workspace for this incident first.")   

        # Any string returned by the handler function is shown to the Resilient user in the Action Status dialog
        workspace_id = res.get_artifact_property(workspace_artifact, "id")    

        # Call to get workspace / graph object. We need the graph UUID
        if self._check_for_existing_node(workspace_id, artifact):
            raise Exception("Could not add Avalon node. A node with value {} already exists.".format(artifact["value"]))

        if artifact["type"] == res.ArtifactType.dns_name:
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

            return

        # We should never reach this line if action conditions are properly set
        raise IntegrationError("Unsupported artifact.")

    def _check_for_existing_node(self, workspace_id, artifact):
        # check whether node with the same type and value already exists in the workspace

        # Call to get workspace / graph object. We need the graph UUID
        resp = av.workspace_get(self.api_token, workspace_id, logger)
        (error, msg) = av.check_error(resp, logger)
        if error:
            raise IntegrationError(msg)

        result = resp.json()

        # get UUID
        workspace_uuid = result["data"]["attributes"]["UUID"]

        # export the nodes from the Avalon workspace 
        resp = av.workspace_export(workspace_id, workspace_uuid, "json", logger)
        (error, msg) = av.check_error(resp, logger)
        if error:
            raise IntegrationError(msg)

        result = resp.json()
        nodes = result["data"]
        if not nodes:
            return False

        for node in nodes:
            node_value = node[0]
            node_type = node[1]

            artifact_value = node_value                      

            artifact_type = self.node_artifact_type.get(node_type)
            if not artifact_type:
                continue

            if artifact["type"] == artifact_type and artifact["value"] == artifact_value:
                return True

        return False


    def _create_empty_workspace(self, incident, who):
        # check whether Avalon workspace has been created for this incident already
        artifact = res.incident_get_workspace_artifact(self.rest_client(), incident["id"])
        if not artifact is None:
            existing_workspace_url = res.get_artifact_property(artifact, "url")
            raise WorkspaceExistsError(existing_workspace_url)   

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

        # Add a new artifact to the incident, using the provided REST API client
        artifact_title = "Avalon Workspace"
        artifact_description = "Avalon workspace address: {}".format(workspace_url)
        res.incident_add_workspace_artifact(self.rest_client(), 
                                                incident["id"], 
                                                artifact_title, artifact_description, 
                                                workspace_id, workspace_url)



