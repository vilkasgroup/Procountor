import json
import re
import requests
from requests_toolbelt.multipart import decoder

try:
    from urllib.parse import urlparse, parse_qs, urlencode
except ImportError:
    from urlparse import urlparse, parse_qs
    from urllib import urlencode

from .api_methods import ApiMethods


class Client(ApiMethods):
    """Class for Procountor accounting API

    Following packages need to be installed:
     - requests

    :param api_key: Procountor API Key, string
    :param client_id: Procountor REST API client id, string
    :param client_secret: Procountor REST API client secret, string
    :param redirect_uri: URI where redirected after authentication, string
    :param test_mode: Wether to use test api or real api, bool
    :param api_version: Cen be latest, supported or >= 20.01, string
    """

    _endpoints = {
        "hosts": {
            "production": "https://api.procountor.com",
            "test": "https://pts-procountor.pubdev.azure.procountor.com",
        },
        "version": {
            "latest": "latest/api",
            "supported": "supported/api",
            "specified": "v{}/api",
        },
    }

    def __init__(
        self,
        api_key,
        client_id,
        client_secret,
        redirect_uri,
        test_mode=True,
        api_version="supported",
    ):
        self.api_key = (api_key,)
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.test_mode = test_mode
        self.api_version = api_version
        self._get_token()

    @property
    def api_url(self):
        if self.api_version in ["latest", "supported"]:
            version = Client._endpoints["version"][self.api_version]
        elif re.match("^2[0-9]\.[0-9]{2}$", self.api_version):
            version_number = "{}{}".format(self.api_version[0:2], self.api_version[3:5])
            version = Client._endpoints["version"]["specified"].format(version_number)
        else:
            raise ValueError(
                "Given value for api version {} is not valid. Valid values are latest, supported or Api version >= 20.01".format(
                    self.api_version
                )
            )

        return "{}/{}/".format(self.api_host, version)

    @property
    def api_host(self):
        host = Client._endpoints["hosts"]["test" if self.test_mode else "production"]
        return host

    def _create_endpoint(self, endpoint, queries={}):
        """

        :return: url, string
        """
        return "{}{}".format(endpoint, self._dict_to_url_query(queries))

    def _dict_to_url_query(self, url_dict):
        """
        :return: url s
        """

        if isinstance(url_dict, dict):
            if len(url_dict) > 0:
                return "?{}".format(urlencode(url_dict))
            else:
                return ""
        else:
            raise Exception(
                "Given params are not dict. The type was {}".format(type(url_dict))
            )

    def invalidate_token(self):
        """Method invalidates the access token"""

        method = "POST"
        endpoint = "logout"
        headers = {"authorization": "Bearer " + self.access_token}
        url = "{}/{}".format(self.api_host, endpoint)

        return self.request(method, endpoint, headers, url)

    def _get_token(self):
        """Makes a request and returns an access token. Access token is valid for
        3600 seconds.

        :return: granted tokens, str
        """

        params = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "api_key": self.api_key,
        }

        headers = {"content-type": "application/x-www-form-urlencoded"}

        url = self.api_url + "oauth/token/"
        response = requests.post(url, data=params, headers=headers)
        status_code = response.status_code

        if status_code != 200:
            if status_code == 404:
                raise RuntimeError(
                    "Not found api endpoint. Please, check your API version."
                )

            if status_code == 401:
                raise RuntimeError(
                    "Authentication failed. Please, check your credentials."
                )

            raise RuntimeError(
                "Authentication got an unexpected HTTP Status code: "
                + str(status_code)
                + ". Content: " + response.text
            )

        json_content = response.json()

        access_token = json_content.get("access_token", None)

        if access_token is None:
            raise RuntimeError(
                "Cannot read the access_token from the response. Response was: "
                + json_content
            )

        self.access_token = access_token
        return access_token

    def _handleResponse(self, response):
        """
        TODO: This text

        :return: response as dict. Dict has a key named status for HTTP-status code. In error case there is string
        """

        answer = {"status": response.status_code}

        if response.status_code in (200, 202):
            try:
                if response.headers["Content-Type"].startswith("multipart/"):
                    meta, filebytes = decoder.MultipartDecoder.from_response(
                        response
                    ).parts
                    answer["content"] = filebytes.content
                    answer["metadata"] = json.loads(meta.content.decode("utf-8"))
                else:
                    answer["content"] = response.json()
            except:
                answer["message"] = response.text
        else:
            answer["message"] = response.text

        return answer

    def request(
        self, method, endpoint, headers=None, url=None, files=None, *args, **kwargs
    ):
        """Method to make HTTP requests over Procountor REST API

        :param method: wanted request method, uppercase string
        :param endpoint: wanted REST API endpoint, string
        :param headers: Overwrite HTTP-headers, dict
        :param kwargs: query parameters to pass to Procountor, dict
        :return: response from rest server, dict
        """
        headers = headers or self._headers(method, endpoint)
        url = url or self.api_url + endpoint

        # Test environment (Microsoft-Azure-Application-Gateway)
        # doesn't like if there is a json body in (for ex.) GET method.
        json = None if len(kwargs) == 0 else kwargs

        response = requests.request(
            method, url, headers=headers, files=files, json=json
        )

        # refresh token if out of date
        if response.status_code == 401:
            self.access_token = self._get_token()
            response = requests.request(
                method, url, headers=headers, files=files, json=json
            )

        return self._handleResponse(response)

    def _headers(self, method, endpoint):
        """Method returns correct headers for request

        :param method: request method, string
        :param endpoint: request endpoint, string
        :return: headers for request, dict
        """

        if "attachments" in endpoint:
            if method == "GET":
                headers = {
                    "content-type": "multipart/mixed",
                    "authorization": "Bearer {}".format(self.access_token),
                }
            elif method == "POST":
                headers = {
                    # can't put 'content-type': 'multipart/form-data' here as documentation says. Requests generates it
                    # automatically.
                    "authorization": "Bearer {}".format(self.access_token),
                }
            else:
                headers = {
                    "content-type": "application/json",
                    "authorization": "Bearer {}".format(self.access_token),
                }
        else:
            headers = {
                "content-type": "application/json",
                "authorization": "Bearer {}".format(self.access_token),
            }

        return headers
