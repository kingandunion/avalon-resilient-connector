import requests
from .errors import IntegrationError

def call_avalon_api(log, verb, url, payload, verifyFlag, headers):
    """Function: perform the http API call. Different types of http operations are supported:
        GET, POST, PUT
        Errors raise IntegrationError
    """

    try:
        (payload and log) and log.debug(payload)

        if verb == 'get':
            resp = requests.get(url, verify=verifyFlag, headers=headers, params=payload)
        elif verb == 'post':
            resp = requests.post(url, verify=verifyFlag, headers=headers, data=payload)
        elif verb == 'put':
            resp = requests.put(url, verify=verifyFlag, headers=headers, data=payload)
        else:
            raise ValueError("unknown verb {}".format(verb))

        if resp is None:
            raise IntegrationError('no response returned')

        return resp 
    except Exception as err:
        log and log.error(err)
        raise IntegrationError(err)