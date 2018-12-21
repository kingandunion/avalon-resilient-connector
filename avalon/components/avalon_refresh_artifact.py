# -*- coding: utf-8 -*-
# pragma pylint: disable=unused-argument, no-self-use
"""Function implementation"""

import logging
from resilient_circuits import ResilientComponent, function, handler, StatusMessage, FunctionResult, FunctionError
import avalon.util.selftest as selftest


class FunctionComponent(ResilientComponent):
    """Component that implements Resilient function 'avalon_refresh_artifact"""

    def __init__(self, opts):
        """constructor provides access to the configuration options"""
        super(FunctionComponent, self).__init__(opts)
        self.options = opts.get("avalon", {})
        selftest.selftest_function(opts)

    @handler("reload")
    def _reload(self, event, opts):
        """Configuration options have changed, save new values"""
        self.options = opts.get("avalon", {})

    @function("avalon_refresh_artifact")
    def _avalon_refresh_artifact_function(self, event, *args, **kwargs):
        """Function: Refreshes artifact data from artifact linked Avalon workspace"""
        try:
            # Get the function parameters:

            log = logging.getLogger(__name__)

            # PUT YOUR FUNCTION IMPLEMENTATION CODE HERE
            #  yield StatusMessage("starting...")
            #  yield StatusMessage("done...")

            results = {
                "value": "xyz"
            }

            # Produce a FunctionResult with the results
            yield FunctionResult(results)
        except Exception:
            yield FunctionError()