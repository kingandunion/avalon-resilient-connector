# -*- coding: utf-8 -*-

"""Generate a default configuration-file section for Avalon"""

from __future__ import print_function


def config_section_data():
    """Produce the default configuration section for app.config,
       when called by `resilient-circuits config [-c|-u]`
    """
    config_data = u"""[avalon]
avalon_api_token=<avalon-api-token>
    """
    return config_data

