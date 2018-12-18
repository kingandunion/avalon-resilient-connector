# Simple example component for resilient-circuits
import json
import logging

from circuits.core.handlers import handler
from resilient_circuits.actions_component import ResilientComponent, ActionMessage, StatusMessage

from avalon.lib.resilient_common import validateFields
from avalon.lib.errors import IntegrationError

# TODO:
# from .common import create_workspace

logger = logging.getLogger(__name__)

class AvalonFunctions(ResilientComponent):
    # Subscribe to the Action Module message destination named "avalon"
    channel = "actions.avalon_create_workspace"
    
    def __init__(self, opts):
        """constructor provides access to the configuration options"""
        super(AvalonFunctions, self).__init__(opts)
        
        self.res_options = opts.get("resilient", {})
        self.options = opts.get("avalon", {})
        validateFields(["api_token"], self.options)

    @handler("reload")
    def _reload(self, event, opts):
        """Configuration options have changed, save new values"""
        self.res_options = opts.get("resilient", {})
        
        self.options = opts.get("avalon", {})
        validateFields(["api_token"], self.options)

    @handler("avalon_create_workspace")
    def _avalon_create_workspace(self, event, *args, **kwargs):
        # This function is called with the action message,
        # In the message we find the whole incident data (and other context)
        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        try:
            # TODO: Eventually we might allow user to specify the name and the summary 
            # for the new Avalon workspace in IBM Resilient and pass those values 
            # validateFields([u'avalon_workspace_title', u'avalon_workspace_summary'], kwargs)

            # workspace_title = clean_html(kwargs.get(u'avalon_workspace_title'))  # text
            # workspace_summary = clean_html(kwargs.get(u'avalon_workspace_summary'))  # text

            # The message also contains information about the user who triggered the action
            who = event.message["user"]["email"]

            workspace_title = "{} (IBM Resilient)".format(incident["name"])
            workspace_summary = "Created by {} from IBM Resilient Incident ID: {}, c".format(who, incident["id"])

            logger.info(workspace_title)
            logger.info(workspace_summary)

            # TODO:
            # resp = create_workspace(self.log, self.options, workspace_title, workspace_summary, self.create_workspace_callback)
            
            # Post a new artifact to the incident, using the provided REST API client 
            new_artifact = {
                "type": "String",
                "value": "Test artifact from {}".format(who)
            }

            new_artifact_uri = "/incidents/{}/artifacts".format(incident["id"])
            self.rest_client().post(new_artifact_uri, new_artifact)

            # Any string returned by the handler function is shown to the Resilient user in the Action Status dialog
            return "Avalon workspace created successfully."
        except Exception as err:
            raise err
            
    def create_workspace_callback(self, resp):
        """ handle results such as this
            {"error":{"message":"Invalid Input Provided","code":2001,"errors":["Content cannot be empty."]}}
        """
        result = resp.json()
        if 'error' in result and result['error']['code'] == 2001:
            msg = ": ".join((result['error']['message'], str(result['error']['errors'])))
            logger.warning(msg)
            StatusMessage(msg)
            return {}
        else:
            raise IntegrationError(resp.text)