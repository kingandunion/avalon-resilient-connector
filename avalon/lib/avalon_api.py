import json
import re
import requests

from .errors import IntegrationError

HEADERS = { 
    "Content-Type": "application/json",
    "Authorization": "Token {}"
}

class Avalon:
    def __init__(self, base_url, api_token, logger):
        self.reload(base_url, api_token)
        self.logger = logger


    def reload(self, base_url, api_token):
        self.base_url = base_url
        self.api_token = api_token 


    def ping_get(self):
        """
        Get API ping endpoint.
        """

        # url
        path = "api/ping/token"
        url = "/".join((self.base_url, path))

        # headers
        headers = self._build_headers()

        try:
            resp = requests.get(url, verify=True, headers=headers)
            if resp is None:
                raise IntegrationError("no response returned")

            return resp 
        except Exception as err:
            self.logger and self.logger.error(err)
            raise IntegrationError(err)


    def workspace_id_from_url(self, workspace_url):
        m = re.search(r'workspaces/(?P<graphid>\d+)/$', workspace_url)
        if m is None:
            raise IntegrationError("Could not find workspace ID in Avalon response.")

        workspace_id = int(m.group("graphid"))
        return workspace_id

    def workspace_create(self, data):
        """
        Create a new Avalon workspace / graph
        :param data: Dict with post data. It will be converted to JSON  
        :return: the responsefrom the Avalon API
        """

        # url
        path = "api/graph/new/token"
        url = "/".join((self.base_url, path))

        # headers
        headers = self._build_headers()

        # payload
        payload = json.dumps(data)

        try:
            resp = requests.post(url, verify=True, headers=headers, data=payload)

            if resp is None:
                raise IntegrationError("no response returned")

            return resp 
        except Exception as err:
            self.logger and self.logger.error(err)
            raise IntegrationError(err)

    def workspace_get(self, workspace_id):
        """
        Get Avalon workspace / graph details
        :param api_token: Avalon API token
        :param workspace_id: Workspace / Graph ID
        :return: the responsefrom the Avalon API
        """

        # url
        path = "api/graph/{}/token".format(workspace_id)
        url = "/".join((self.base_url, path))

        # headers
        headers = self._build_headers()

        try:
            resp = requests.get(url, verify=True, headers=headers)
            if resp is None:
                raise IntegrationError("no response returned")

            return resp 
        except Exception as err:
            self.logger and self.logger.error(err)
            raise IntegrationError(err)

    def workspace_export(self, workspace_id, workspace_uuid, export_format):
        """
        Export Avalon workspace / graph 
        :param workspace_id: Workspace / Graph ID
        :param workspace_uuid: Workspace / Graph UUID
        :param export_format: string, one of csv | json | jsonedge | cb-json | stix | stix-json | bro-intel
        :return: the responsefrom the Avalon API
        """

        # url
        path = "export/graph/{}/{}/{}".format(workspace_id, workspace_uuid, export_format)
        url = "/".join((self.base_url, path))

        try:
            resp = requests.get(url)
            if resp is None:
                raise IntegrationError("no response returned")

            return resp 
        except Exception as err:
            self.logger and self.logger.error(err)
            raise IntegrationError(err)


    def workspace_add_node(self, workspace_id, data):
        """
        Create a new Avalon workspace
        :param api_token: Avalon API token
        :param workspace_id: Workspace / Graph ID
        :param data: Dict with post data. It will be converted to JSON  
        :return: the responsefrom the Avalon API
        """

        # url
        path = "api/graph/{}/bulkimport/token".format(workspace_id)
        url = "/".join((self.base_url, path))

        # headers
        headers = self._build_headers()

        # payload
        payload = json.dumps(data)

        try:
            resp = requests.post(url, verify=True, headers=headers, data=payload)
            if resp is None:
                raise IntegrationError("no response returned")

            return resp 
        except Exception as err:
            self.logger and self.logger.error(err)
            raise IntegrationError(err)

    @staticmethod
    def check_error(resp):
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

        if resp.status_code == 500:
            raise IntegrationError(resp.text)

        if resp.status_code >= 300:
            result = resp.json()
            if "errors" in result:
                msg = json.dumps(result, indent=4, separators=(",", ": "))
                return (True, msg) 
            
            raise IntegrationError(resp.text)

        return (False, "")         

    def _build_headers(self):
        """
        build the header needed for API calls
        :param api_token:
        :return: https headers
        """
        headers = HEADERS.copy()
        headers["Authorization"] = headers["Authorization"].format(self.api_token)

        return headers


