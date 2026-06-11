from __future__ import annotations

import os
import json
import re
from typing import Any

import requests
from requests_toolbelt.multipart import decoder

from urllib.parse import urlencode

#: Shape of every value returned by the API helper methods.
ResponseDict = dict[str, Any]


class BaseClient:
    """HTTP transport and authentication for the Procountor REST API.

    This base class holds everything that talks to the network -- building
    URLs, fetching and refreshing the OAuth token, and turning ``requests``
    responses into plain dictionaries. The high-level endpoint helpers live in
    :class:`procountor.api_methods.ApiMethods`, which builds on this class.
    """

    access_token: str

    _endpoints = {
        "hosts": {
            "production": os.getenv("PROCOUNTOR_HOST_PRODUCTION", "https://api.procountor.com"),
            "test": os.getenv("PROCOUNTOR_HOST_TEST", "https://pts-api.procountor.com"),
        },
        "version": {
            "latest": "latest/api",
            "supported": "supported/api",
            "specified": "v{}/api",
        },
    }

    def __init__(
        self,
        api_key: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        test_mode: bool = True,
        api_version: str = "supported",
    ) -> None:
        self.api_key = api_key
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.test_mode = test_mode
        self.api_version = api_version
        self._get_token()

    @property
    def api_url(self) -> str:
        if self.api_version in ["latest", "supported"]:
            version = BaseClient._endpoints["version"][self.api_version]
        elif re.match(r"^2[0-9]\.[0-9]{2}$", self.api_version):
            version_number = "{}{}".format(self.api_version[0:2], self.api_version[3:5])
            version = BaseClient._endpoints["version"]["specified"].format(version_number)
        else:
            raise ValueError(
                "Given value for api version {} is not valid. Valid values are latest, supported or Api version >= 20.01".format(
                    self.api_version
                )
            )

        return "{}/{}/".format(self.api_host, version)

    @property
    def api_host(self) -> str:
        host = BaseClient._endpoints["hosts"]["test" if self.test_mode else "production"]
        return host

    def _create_endpoint(self, endpoint: str, queries: dict[str, Any] | None = None) -> str:
        """

        :return: url, string
        """
        if queries is None:
            queries = {}
        return "{}{}".format(endpoint, self._dict_to_url_query(queries))

    def _dict_to_url_query(self, url_dict: dict[str, Any]) -> str:
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

    def invalidate_token(self) -> ResponseDict:
        """Method invalidates the access token"""

        method = "POST"
        endpoint = "logout"
        headers = {"authorization": "Bearer " + self.access_token}
        url = "{}/{}".format(self.api_host, endpoint)

        return self.request(method, endpoint, headers, url)

    def _get_token(self) -> str:
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
                + str(json_content)
            )

        self.access_token = access_token
        return access_token

    def _handleResponse(self, response: requests.Response) -> ResponseDict:
        """Convert a ``requests`` response into a plain result dict.

        The returned dict always has a ``status`` key with the HTTP status code.
        On a successful (200/202) response the parsed JSON body is placed under
        ``content``; for multipart responses the file bytes are under
        ``content`` and the parsed metadata under ``metadata``. On any error, or
        when the body cannot be parsed, the raw response text is placed under
        ``message``.

        :param response: the ``requests`` response to interpret
        :return: dict with ``status`` plus ``content`` (and ``metadata``) or ``message``
        """

        answer: ResponseDict = {"status": response.status_code}

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
            except Exception:
                answer["message"] = response.text
        else:
            answer["message"] = response.text

        return answer

    def request(
        self,
        method: str,
        endpoint: str,
        headers: dict[str, str] | None = None,
        url: str | None = None,
        files: Any = None,
        *args: Any,
        json: Any = None,
        **kwargs: Any,
    ) -> ResponseDict:
        """Method to make HTTP requests over Procountor REST API

        :param method: wanted request method, uppercase string
        :param endpoint: wanted REST API endpoint, string
        :param headers: Overwrite HTTP-headers, dict
        :param json: explicit JSON body (dict or list). Takes precedence over
                     ``kwargs``; use this to send a top-level JSON array.
        :param kwargs: JSON body fields to pass to Procountor, dict
        :return: response from rest server, dict
        """
        headers = headers or self._headers(method, endpoint)
        url = url or self.api_url + endpoint

        # Test environment (Microsoft-Azure-Application-Gateway)
        # doesn't like if there is a json body in (for ex.) GET method.
        if json is None:
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

    # Generic verbs -- call any Procountor endpoint without a dedicated helper.
    # The Procountor API surface is large; these reach everything the named
    # methods do not, while the client keeps handling auth and token refresh.

    def get(self, path: str, **params: Any) -> ResponseDict:
        """GET any endpoint. Keyword arguments become query parameters.

        Example::

            client.get("invoices", startDate="2024-01-01", endDate="2024-01-31")
        """
        return self.request("GET", self._create_endpoint(path, params))

    def post(self, path: str, json: Any = None) -> ResponseDict:
        """POST any endpoint with an optional JSON body (dict or list)."""
        return self.request("POST", path, json=json)

    def put(self, path: str, json: Any = None) -> ResponseDict:
        """PUT any endpoint with an optional JSON body (dict or list)."""
        return self.request("PUT", path, json=json)

    def delete(self, path: str) -> ResponseDict:
        """DELETE any endpoint."""
        return self.request("DELETE", path)

    def _headers(self, method: str, endpoint: str) -> dict[str, str]:
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
