import json
import re
import requests

from .errors import IntegrationError

AVALON_BASE_URL = "http://localhost:8000/api"

HEADERS = { 
    "Content-Type": "application/json",
    "Authorization": "Token {}"
}

def workspace_id_from_url(workspace_url):
    m = re.search(r'workspaces/(?P<graphid>\d+)/$', workspace_url)
    if m is None:
        raise IntegrationError("Could not find workspace ID in Avalon response.")

    workspace_id = int(m.group("graphid"))
    return workspace_id

def workspace_create_empty(api_token, data, log):
    """
    Create a new Avalon workspace
    :param log: logger
    :param api_token: Avalon API token
    :param data: Dict with post data. It will be converted to JSON  
    :return: the responsefrom the Avalon API
    """

    # url
    path = "graph/new/token"
    url = "/".join((AVALON_BASE_URL, path))

    # headers
    headers = _build_headers(api_token)

    # payload
    payload = json.dumps(data)

    try:
        resp = requests.post(url, verify=True, headers=headers, data=payload)
        # resp = requests.get(url, verify=verifyFlag, headers=headers, params=payload)
        # resp = requests.put(url, verify=verifyFlag, headers=headers, data=payload)

        if resp is None:
            raise IntegrationError("no response returned")

        return resp 
    except Exception as err:
        log and log.error(err)
        raise IntegrationError(err)

def workspace_add_node(api_token, workspace_id, data, log):
    """
    Create a new Avalon workspace
    :param log: logger
    :param api_token: Avalon API token
    :param data: Dict with post data. It will be converted to JSON  
    :return: the responsefrom the Avalon API
    """

    # url
    path = "graph/{}/bulkimport/token".format(workspace_id)
    url = "/".join((AVALON_BASE_URL, path))

    # headers
    headers = _build_headers(api_token)

    # payload
    payload = json.dumps(data)

    try:
        resp = requests.post(url, verify=True, headers=headers, data=payload)
        if resp is None:
            raise IntegrationError("no response returned")

        return resp 
    except Exception as err:
        log and log.error(err)
        raise IntegrationError(err)

def check_error(resp, log):
    # handle results such as this:

    #   {
    #       "errors":[
    #           {
    #               "detail":"Incorrect type. Expected resource identifier object, received str.",
    #               "source": {
    #                   "pointer":"/data/attributes/Owners"
    #               },
    #               "status": "400"
    #           }
    #       ]
    #   }

    if resp.status_code >= 300:
        result = resp.json()
        if "errors" in result:
            msg = json.dumps(result, indent=4, separators=(",", ": "))
            log.error(msg)
            return (True, msg) 
        
        raise IntegrationError(resp.text)

    return (False, "")         

def _build_headers(api_token):
    """
    build the header needed for API calls
    :param api_token:
    :return: https headers
    """
    headers = HEADERS.copy()
    headers["Authorization"] = headers["Authorization"].format(api_token)

    return headers


