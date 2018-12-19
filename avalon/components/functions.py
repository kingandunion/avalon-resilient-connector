import json
import logging

from circuits.core.handlers import handler
from resilient_circuits.actions_component import ResilientComponent, ActionMessage, StatusMessage

from avalon.lib.resilient_common import validateFields
from avalon.lib.errors import IntegrationError

from .common import create_workspace

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

        self.api_token = self.options['api_token']


    @handler("reload")
    def _reload(self, event, opts):
        """Configuration options have changed, save new values"""
        self.res_options = opts.get("resilient", {})
        
        self.options = opts.get("avalon", {})
        validateFields(["api_token"], self.options)

        self.api_token = self.options['api_token']

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
            workspace_summary = "Created from IBM Resilient by {}. IBM Resilient Incident ID: {}".format(who, incident["id"])

            # call API
            data = {
                "Title": workspace_title, 
                "Summary": workspace_summary, 
                "TLP": "r", 
                "ShareWithMyOrganization": False
            }

            resp = create_workspace(logger, self.api_token, data)

            result = resp.json()

            if resp.status_code >= 300:
                # handle results such as this:
                # {"errors":[{"detail":"Incorrect type. Expected resource identifier object, received str.","source":{"pointer":"/data/attributes/Owners"},"status":"400"}]}
               
                if 'errors' in result:
                    msg = json.dumps(result, indent=4, separators=(',', ': '))
                    logger.error(msg)
                    return msg 
                
                raise IntegrationError(resp.text)

            # Post a new artifact to the incident, using the provided REST API client
            # workspace data looks like: {'data': {'path': 'https://example.com...aces/22/ '}}
            workspace_data = result['data']
            workspace_url = workspace_data['path'].strip() 
            new_artifact = {
                "type": "String",
                "value": "Avalon Workspace",
                "description": {
                    "format" : "text", 
                    "content" : 'Avalon Workspace Address: {}'.format(workspace_url)
                }                    
            }

            new_artifact_uri = "/incidents/{}/artifacts".format(incident["id"])
            self.rest_client().post(new_artifact_uri, new_artifact)

            # Any string returned by the handler function is shown to the Resilient user in the Action Status dialog
            return "Avalon workspace created successfully."
        except Exception as err:
            raise err
            
        