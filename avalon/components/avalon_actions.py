import json
import logging

from circuits.core.handlers import handler
from resilient_circuits.actions_component import ResilientComponent, ActionMessage, StatusMessage

from actions import Actions

logger = logging.getLogger(__name__)

class AvalonActions(ResilientComponent):
    # Subscribe to the message destination named "avalon_actions"
    channel = "actions.avalon_actions"
    
    def __init__(self, opts):
        """constructor provides access to the configuration options"""
        super(AvalonActions, self).__init__(opts)
        
        self.res_options = opts.get("resilient", {})

        self.options = opts.get("avalon", {})
        Actions.validate_fields(["base_url", "api_token"], self.options)

        base_url = self.options["base_url"]
        api_token = self.options["api_token"]
        rest_client = self.rest_client()

        self.actions = Actions(base_url, api_token, rest_client, logger)


    @handler("reload")
    def handle_reload(self, event, opts):
        """Configuration options have changed, save new values"""
        self.res_options = opts.get("resilient", {})
        
        self.options = opts.get("avalon", {})
        Actions.validate_fields(["base_url", "api_token"], self.options)

        base_url = self.options["base_url"]
        api_token = self.options["api_token"]
        self.actions.reload(base_url, api_token)


    # Handles Avalon: Create Workspace action 
    @handler("avalon_create_workspace")
    def handle_avalon_create_workspace(self, event, *args, **kwargs):
        # Any string returned by the handler function is shown to the Resilient user in the Action Status dialog

        # incident data
        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        # the user who triggered the action
        who = event.message["user"]["email"]

        # TODO: Eventually we might allow user to specify the name and the summary 
        # for the new Avalon workspace in IBM Resilient and pass those values 
        # res.validate_fields([u"avalon_workspace_title", u"avalon_workspace_summary"], kwargs)

        # workspace_title = clean_html(kwargs.get(u"avalon_workspace_title"))  # text
        # workspace_summary = clean_html(kwargs.get(u"avalon_workspace_summary"))  # text

        return self.actions.create_avalon_workspace(incident, who)


    # Handles "Avalon: Pull Nodes" action 
    @handler("avalon_pull_nodes")
    def handle_avalon_pull_nodes(self, event, *args, **kwargs):
        # Any string returned by the handler function is shown to the Resilient user in the Action Status dialog
        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        return self.actions.pull_avalon_nodes(incident)


    # Handles "Avalon: Push Artifacts" action. This is called for artifacts only 
    @handler("avalon_push_artifacts")
    def handle_avalon_push_all_artifact(self, event, *args, **kwargs):
        # Any string returned by the handler function is shown to the Resilient user in the Action Status dialog
        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        return self.actions.push_resilient_artifacts(incident)


    # Handles "Avalon: Push Artifact" action. This is called for artifacts only 
    @handler("avalon_push_artifact")
    def handle_avalon_push_artifact(self, event, *args, **kwargs):
        # Any string returned by the handler function is shown to the Resilient user in the Action Status dialog
        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        artifact = event.message["artifact"]
        logger.info("Called from artifact {}: {}".format(artifact["id"], artifact["value"]))

        return self.actions.push_one_resilient_artifact(incident, artifact)


   