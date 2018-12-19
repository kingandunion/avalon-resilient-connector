# (c) Copyright IBM Corp. 2010, 2018. All Rights Reserved.
import json
from avalon.lib.requests_common import call_avalon_api

GRAPH_FRAGMENT      = 'graph'
NEW_GPAPH_FRAGMENT  = '/'.join((GRAPH_FRAGMENT, 'new', 'token'))

HEADERS = { 
    'Content-Type': 'application/json',
    'Authorization': 'Token {}'
}

AVALON_BASE_URL = 'http://localhost:8000/api'

def create_workspace(log, api_token, data):
    """
    Create a PagerDuty note
    :param log:
    :param appDict:
    :param incident_id:
    :param note:
    :return: the json string from the PD API
    """
    # build url
    url = '/'.join((AVALON_BASE_URL, NEW_GPAPH_FRAGMENT))

    # headers
    headers = _build_headers(api_token)

    # payload
    payload = json.dumps(data)

    return call_avalon_api(log, 'post', url, payload, True, headers)

def _build_headers(api_token):
    """
    build the header needed for API calls
    :param api_token:
    :return: https headers
    """
    headers = HEADERS.copy()
    headers['Authorization'] = headers['Authorization'].format(api_token)

    return headers