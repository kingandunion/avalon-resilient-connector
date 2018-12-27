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

    # Handles avalon_refresh action 
    @handler("avalon_refresh")
    def _avalon_refresh(self, event, *args, **kwargs):
        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        # Any string returned by the handler function is shown to the Resilient user in the Action Status dialog
        return "Error: Not implemented."

    # Handles avalon_add_node action. This is called for artifacts only 
    @handler("avalon_add_node")
    def _avalon_add_node(self, event, *args, **kwargs):
        # the user who triggered the action
        who = event.message["user"]["email"]

        # incident data (and other context)
        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        # artifact data (and other context)
        artifact = event.message["artifact"]
        logger.info("Called from artifact {}: {}".format(artifact["id"], artifact["value"]))

        try:
            # Add Avalon node
            self._add_node(incident, artifact, who)
            return "{} added to Avalon.".format(artifact["value"])

        except Exception as err:
            # NOTE: This will still mark the action as complete in IBM Resilient
            return "Error: {}".format(str(err))

    def _add_node(self, incident, artifact, who):
        # check whether Avalon workspace has been created for this incident already
        workspace_artifact = res.incident_get_workspace_artifact(self.rest_client(), incident["id"])
        if workspace_artifact is None:
            raise Exception("Please create Avalon workspace for this incident first.")   

        workspace_id = res.get_artifact_property(workspace_artifact, "id")    

        # Any string returned by the handler function is shown to the Resilient user in the Action Status dialog
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




