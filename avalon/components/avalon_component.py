import logging

from circuits.core.handlers import handler
from circuits import Event, Timer
from resilient_circuits.actions_component import ResilientComponent, ActionMessage, StatusMessage

from avalon.components.actions import Actions

logger = logging.getLogger(__name__)

class auto_refresh(Event):
    """auro_refresh"""

    def __init__(self, incident_id):
        super(auto_refresh, self).__init__()
        self.incident_id = incident_id

class AvalonComponent(ResilientComponent):
    # Subscribe to the message destination named "avalon_actions"
    channel = "actions.avalon_actions"
    
    def __init__(self, opts):
        """constructor provides access to the configuration options"""
        super(AvalonComponent, self).__init__(opts)
        
        self.res_options = opts.get("resilient", {})

        self.options = opts.get("avalon", {})
        Actions.validate_fields(["base_url", "api_token"], self.options)

        base_url = self.options["base_url"]
        api_token = self.options["api_token"]
        rest_client = self.rest_client()

        self.actions = Actions(base_url, api_token, rest_client, logger)
        self.incident_timer = {}

        # start auto refresh for all inicidents which are connected to Avalon workspace 
        # and which have auto-refresh ON 
        auto_refresh_incidents = self.actions.get_auto_refresh_incidents()
        for incident in auto_refresh_incidents:
            self._start_auto_refresh(incident)


    @handler("reload")
    def handle_reload(self, event, opts):
        """Configuration options have changed, save new values"""
        self.res_options = opts.get("resilient", {})
        
        self.options = opts.get("avalon", {})
        Actions.validate_fields(["base_url", "api_token"], self.options)

        base_url = self.options["base_url"]
        api_token = self.options["api_token"]
        self.actions.reload(base_url, api_token)


    # Any string returned by the handler function is shown to the Resilient user in the Action Status dialog

    # Handles Avalon: Create Workspace action 
    @handler("avalon_create_workspace")
    def handle_avalon_create_workspace(self, event, *args, **kwargs):
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
        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        return self.actions.pull_avalon_nodes(incident)


    # Handles "Avalon: Push Artifacts" action. This is called for artifacts only 
    @handler("avalon_push_artifacts")
    def handle_avalon_push_all_artifact(self, event, *args, **kwargs):
        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        return self.actions.push_resilient_artifacts(incident)


    # Handles "Avalon: Push Artifact" action. This is called for artifacts only 
    @handler("avalon_push_artifact")
    def handle_avalon_push_artifact(self, event, *args, **kwargs):
        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        artifact = event.message["artifact"]
        logger.info("Called from artifact {}: {}".format(artifact["id"], artifact["value"]))

        return self.actions.push_single_resilient_artifact(incident, artifact)

    # Handles "Avalon: Start Auto-refresh" action.
    @handler("avalon_start_auto_refresh")
    def handle_avalon_start_auto_refresh_workflow(self, event, *args, **kwargs):
        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        incident_id = incident["id"]

        self._start_auto_refresh(incident)

        # set the auto refresh field to false
        old_value = self.actions.res.incident_get_avalon_auto_refresh(incident) 
        self.actions.res.incident_set_avalon_auto_refresh(incident_id, True, old_value)

        return "Avalon Auto-refresh started successfully."


    # Handles "Avalon: Stop Auto-refresh Workflow" action.
    @handler("avalon_stop_auto_refresh")
    def handle_avalon_stop_auto_refresh(self, event, *args, **kwargs):
        incident = event.message["incident"]
        logger.info("Called from incident {}: {}".format(incident["id"], incident["name"]))

        # remove timer the incident map
        incident_id = incident["id"]
        timer = self.incident_timer.pop(incident_id, None)
        
        # stop ticking
        if timer:
            timer.unregister()    

        # set the auto refresh field to false
        old_value = self.actions.res.incident_get_avalon_auto_refresh(incident) 
        self.actions.res.incident_set_avalon_auto_refresh(incident_id, False, old_value)

        return "Avalon Auto-refresh stopped successfully."

    # Handles the auto refresh timer events
    @handler("auto_refresh")
    def handle_auto_refresh(self, event, *args, **kwargs):
        incident_id = event.incident_id
        incident = self.actions.res.incident_get(incident_id)

        logger.info("handle_auto_refresh called for incident {}: {}".format(incident["id"], incident["name"]))

        self.actions.refresh_nodes(incident)


    def _start_auto_refresh(self, incident):
        # Get the interval from the avalon_auto_refresh_time field 
        refresh_interval_minutes = self.actions.res.incident_get_avalon_auto_refresh_time(incident)
        
        # default to 60 minutes if not set in IBM Resilient
        if not refresh_interval_minutes:
            refresh_interval_minutes = 60

        # create timer
        incident_id = incident["id"]
        auto_refresh_event = auto_refresh(incident_id)
        timer = Timer(60 * refresh_interval_minutes, auto_refresh_event, self.channel, persist=True)

        # keep timer in the incident map
        self.incident_timer[incident_id] = timer

        # start ticking
        timer.register(self)    

        # fire event once to refresh nodes now
        self.fire(auto_refresh_event)
