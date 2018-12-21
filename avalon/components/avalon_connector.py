import re
import json
import logging

from circuits.core.handlers import handler
from resilient_circuits.actions_component import ResilientComponent, ActionMessage, StatusMessage, FunctionError_

from avalon.lib import resilient_api as res
from avalon.lib.errors import IntegrationError
from avalon.lib import avalon_api as av

logger = logging.getLogger(__name__)

class AvalonConnector(ResilientComponent):
    # Subscribe to the message destination named "avalon_connector"
    channel = "actions.avalon_connector"
    
    def __init__(self, opts):
        """constructor provides access to the configuration options"""
        super(AvalonConnector, self).__init__(opts)
        
        self.res_options = opts.get("resilient", {})

        self.options = opts.get("avalon", {})
        res.validateFields(["api_token"], self.options)

        self.api_token = self.options["api_token"]


    @handler("reload")
    def _reload(self, event, opts):
        """Configuration options have changed, save new values"""
        self.res_options = opts.get("resilient", {})
        
        self.options = opts.get("avalon", {})
        res.validateFields(["api_token"], self.options)

        self.api_token = self.options["api_token"]

    # Handles avalon_create_workspace action 
    @handler("avalon_create_workspace")
    def _avalon_create_workspace(self, event, *args, **kwargs):
        # This function is called with the action message,
        # In the message we find the whole incident data (and other context)
        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        try:
            # TODO: Eventually we might allow user to specify the name and the summary 
            # for the new Avalon workspace in IBM Resilient and pass those values 
            # validateFields([u"avalon_workspace_title", u"avalon_workspace_summary"], kwargs)

            # workspace_title = clean_html(kwargs.get(u"avalon_workspace_title"))  # text
            # workspace_summary = clean_html(kwargs.get(u"avalon_workspace_summary"))  # text

            # The message also contains information about the user who triggered the action
            who = event.message["user"]["email"]

            workspace_title = "{} (IBM Resilient)".format(incident["name"])
            workspace_summary = "Created from IBM Resilient by {}. IBM Resilient Incident ID: {}".format(who, incident["id"])

            # call API
            data = {
                "Title": workspace_title, 
                "Summary": workspace_summary, 
                "TLP": "r", 
                "ShareWithMyOrganization": False
            }

            resp = av.workspace_create(self.api_token, data, logger)
            (error, msg) = av.check_error(resp, logger)
            if error:
                return msg

            # Post a new artifact to the incident, using the provided REST API client
            # workspace data looks like: {"data": {"path": "https://example.com...aces/22/ "}}
            result = resp.json()
            workspace_data = result["data"]
            workspace_url = workspace_data["path"].strip() 
            workspace_id = av.workspace_id_from_url(workspace_url)

            res.incident_add_workspace_artifact(self.rest_client(), incident["id"], workspace_id, workspace_title, workspace_url)

            # Any string returned by the handler function is shown to the Resilient user in the Action Status dialog
            return "Avalon workspace created successfully."
        except Exception as err:
            # This will still mark the action as complete
            return "Error: {}".format(str(err))

            # TODO: Find out how we can return errors from custom action handlers    
            # see: https://10.1.0.151/docs/rest-api/json_AcknowledgementDTO.html
            
            # return json.dumps({ 
            #     "message_type": { "id": 1, "name": "error" },
            #     "message": str(err), 
            #     "complete": True,
            #     "results" : { }
            # })
            



