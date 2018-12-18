import requests
from .errors import IntegrationError

def execute_call(log, url, verb, headers, payload, verifyFlag, callback):
    """Function: perform the http API call. Different types of http operations are supported:
        GET, POST, PUT
        Errors raise IntegrationError
        If a callback method is provided, then it's called to handle the error
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
            raise IntegrationError("unknown verb {}".format(verb))

        if resp is None:
            raise IntegrationError('no response returned')

        if resp.status_code >= 300:
            log and log.warning(resp)
            if callback:
                return callback(resp)
            else:
                # get the result
                raise IntegrationError(resp.text)

        # check if anything returned
        log and log.debug(resp.text)
        if resp.text is None or len(resp.text) == 0:
            return {}          # make sure to always return a dictionary

        # get the result
        r = resp.json()

        return r      # json object needed, not a string representation
    except Exception as err:
        log and log.error(err)
        raise IntegrationError(err)