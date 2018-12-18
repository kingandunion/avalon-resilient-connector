# Simple example component for resilient-circuits
import json
import logging
from circuits.core.handlers import handler
from resilient_circuits.actions_component import ResilientComponent, ActionMessage

logger = logging.getLogger(__name__)

class AvalonComponent(ResilientComponent):
    # Subscribe to the Action Module message destination named "avalon"
    channel = "actions.avalon_create_workspace"
    
    @handler("avalon_create_workspace")
    def _avalon_create_workspace(self, event, *args, **kwargs):
        # This function is called with the action message,
        # In the message we find the whole incident data (and other context)
        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        # The message also contains information about the user who triggered the action
        who = event.message["user"]["email"]
    
        # Post a new artifact to the incident, using the provided REST API client 
        new_artifact = {
            "type": "String",
            "value": "Test artifact from {}".format(who)
        }

        new_artifact_uri = "/incidents/{}/artifacts".format(incident["id"])
        self.rest_client().post(new_artifact_uri, new_artifact)

        # Any string returned by the handler function is shown to the Resilient user in the Action Status dialog
        return "Workspace created successfully."
    