# -*- coding: utf-8 -*-
# pragma pylint: disable=unused-argument, no-self-use
"""Function implementation
   test with: resilient-circuits selftest -l avalon
"""

import logging

from ..components.actions import Actions
from ..lib.avalon_api import Avalon

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def selftest_function(opts):
    """
    Placeholder for selftest function. An example use would be to test package api connectivity.
    Suggested return values are be unimplemented, success, or failure.
    """
    try:
        options = opts.get("avalon", {})
        Actions.validate_fields(["base_url", "api_token"], options)

        base_url = options["base_url"]
        api_token = options["api_token"]

        av = Avalon(base_url, api_token, logger)
        resp = av.ping_get()
        if resp.status_code != 200:
            return {"state": "failure"}       

    except Exception as err:
        logger.error(str(err))
        return {"state": "failure"}       

    return {"state": "success"}