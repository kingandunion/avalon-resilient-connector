# -*- coding: utf-8 -*-
# pragma pylint: disable=unused-argument, no-self-use
"""Function implementation"""

import logging
from datetime import datetime
import pytz
import tzlocal

from resilient_circuits import ResilientComponent, function, handler, StatusMessage, FunctionResult, FunctionError

from .actions import Actions
from avalon.lib.resilient_api import Resilient
import avalon.util.selftest as selftest


logger = logging.getLogger(__name__)

class AvalonRefreshFunction(ResilientComponent):
    """Component that implements Resilient function 'avalon_refresh"""

    def __init__(self, opts):
        """constructor provides access to the configuration options"""
        super(AvalonRefreshFunction, self).__init__(opts)

        selftest.selftest_function(opts)

        self.options = opts.get("avalon", {})
        Actions.validate_fields(["base_url", "api_token"], self.options)

        base_url = self.options["base_url"]
        api_token = self.options["api_token"]
        rest_client = self.rest_client()

        self.actions = Actions(base_url, api_token, rest_client, logger)
        self.res = Resilient(self.rest_client())


    @handler("reload")
    def _reload(self, event, opts):
        """Configuration options have changed, save new values"""
        self.options = opts.get("avalon", {})
        Actions.validate_fields(["base_url", "api_token"], self.options)

        base_url = self.options["base_url"]
        api_token = self.options["api_token"]
        self.actions.reload(base_url, api_token)


    @function("avalon_refresh")
    def _avalon_refresh_function(self, event, *args, **kwargs):
        """Function: Pulls data from a linked Avalon workspace. 
        Requires an Avalon Workspace to have been associated with the incident. 
        Avalon Workspace can be created with the "Avalon: Create Workspace" custom menu command."""

        incident_id = event.message["inputs"]["incident_id"]
        incident_name = event.message["inputs"]["incident_name"]
        logger.info("Called from incident {}: {}".format(incident_id, incident_name))

        incident = self.res.incident_get(incident_id)

        try:
            new_pull_time = datetime.now(tz=tzlocal.get_localzone())
            old_pull_time = self.res.incident_get_avalon_last_pull_time(incident)

            # pull every 60 minutes
            if old_pull_time:
                minute_delta = (new_pull_time - old_pull_time).seconds / 60.0 
                if minute_delta < 60:
                    # return empty dict (no particular result)
                    yield FunctionResult({})
                    return

            # pull nodes from Avalon
            yield StatusMessage("Starting...")

            result = self.actions.pull_avalon_nodes(incident)            
            
            yield StatusMessage(result)

            yield StatusMessage("Done.")

            # set the last pull time
            self.res.incident_set_avalon_last_pull_time(incident_id, new_pull_time, old_pull_time)

            # return empty dict (no particular result)
            yield FunctionResult({})
        except Exception as err:
            yield FunctionError(str(err))