# -*- coding: utf-8 -*-
# pragma pylint: disable=unused-argument, no-self-use
"""Function implementation"""

import logging
from resilient_circuits import ResilientComponent, function, handler, StatusMessage, FunctionResult, FunctionError
import avalon.util.selftest as selftest


class AvalonRefreshFunction(ResilientComponent):
    """Component that implements Resilient function 'avalon_refresh"""

    def __init__(self, opts):
        """constructor provides access to the configuration options"""
        super(AvalonRefreshFunction, self).__init__(opts)
        self.options = opts.get("avalon", {})
        selftest.selftest_function(opts)

    @handler("reload")
    def _reload(self, event, opts):
        """Configuration options have changed, save new values"""
        self.options = opts.get("avalon", {})

    @function("avalon_refresh")
    def _avalon_refresh_function(self, event, *args, **kwargs):
        """Function: Pulls data from a linked Avalon workspace. 
        Requires an Avalon Workspace to have been associated with the incident. 
        Avalon Workspace can be created with the "Avalon: Create Workspace" custom menu command."""
        try:
            # Get the function parameters:

            log = logging.getLogger(__name__)

            # PUT YOUR FUNCTION IMPLEMENTATION CODE HERE
            yield StatusMessage("starting...")
            yield StatusMessage("done...")

            results = {
                "value": "xyz"
            }

            # Produce a FunctionResult with the results
            yield FunctionResult(results)
            # yield FunctionError()
        except Exception:
            yield FunctionError()