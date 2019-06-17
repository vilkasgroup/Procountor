import json
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

    :param username: Procountor username, string
    :param password: Procountor password, string
    :param company_id: Procountor environment company id, string
    :param client_id: Procountor REST API client id, string
    :param client_secret: Procountor REST API client secret, string
    :param redirect_uri: URI where redirected after authentication, string
    :param test_mode: Wether to use test api or real api, bool
    """

    _api_host = "https://api.procountor.com"
    _test_api_host = "https://api-test.procountor.com"

    _api_host_version = "https://api.procountor.com/procountor.api.v{}"
    _test_api_host_version = "https://api-test.procountor.com/procountor.api.v{}"

    def __init__(self, username, password, company_id, client_id, client_secret, redirect_uri, test_mode=True, api_version=None):
        self.username = username
        self.password = password
        self.company_id = company_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.test_mode = test_mode
        self.api_version = api_version
        self._get_tokens()

    @property
    def api_url(self):
        return self.api_host + "/api/"

    @property
    def api_host(self):
        if self.test_mode:
            if self.api_version:
                return Client._test_api_host_version.format(self.api_version)
            else:
                return Client._test_api_host
        else: # Production
            if self.api_version:
                return Client._api_host_version.format(self.api_version)
            else:
                return Client._api_host

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
            if (len(url_dict) > 0):
                return "?{}".format(urlencode(url_dict))
            else:
                return ""
        else:
            raise Exception("Given params are not dict. The type was {}".format(type(url_dict)))

    def _get_auth_code(self):
        """Makes post request and returns authorization code which is used for getting access token and refresh token

        :return: auth_code, string or raise error if delentians are not corrects
        """

        params = {
            'response_type': 'code',
            'username': self.username,
            'password': self.password,
            'company': self.company_id,
            'redirect_uri': self.redirect_uri,
        }

        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }

        auth_code = None

        url_params = {
            "response_type": 'code',
            "client_id": self.client_id,
            "state": '123456',  # state parameter may be chosen arbitrarily or omitted
        }

        url = '{}oauth/authz/{}'.format(self.api_url, self._dict_to_url_query(url_params))

        response = requests.post(url, params=params, headers=headers, allow_redirects=False)

        # have to get value of query parameter named 'code'
        if response.status_code == 302:
            auth_code = parse_qs(urlparse(response.headers['Location']).query)['code'][0]
        else:
            messages = response.json()
            raise Exception(messages['error_description'])

        return auth_code

    def invalidate_token(self):
        """Method invalidates the access token"""

        method = "POST"
        endpoint = "logout"
        headers = {
            'authorization': 'Bearer ' + self.access_token
        }
        url = "{}/{}".format(self.api_host, endpoint)

        return self.request(method, endpoint, headers, url)

    def _get_tokens(self):
        """Makes a request and returns access token and refresh token for coming requests. Access token is valid for
        3600 seconds and has to be refreshed after that with refresh token. Refresh token is valid always.

        :return: granted tokens, dict
        """

        auth_code = self._get_auth_code()

        params = {
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
            'code': auth_code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }

        r = requests.post(self.api_url + 'oauth/token/', params=params, headers=headers)

        self.access_token = r.json()['access_token']
        self.refresh_token = r.json()['refresh_token']

        tokens = {'access_token': self.access_token, 'refresh_token': self.refresh_token}
        return tokens

    def refresh_access_token(self):
        """If the access token is expired (3600 seconds), new access token is granted with refresh token

        :param refresh_token: token to get new access token, string
        :return: refreshed access_token, string
        """

        params = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }

        r = requests.post(self.api_url + 'oauth/token/', params=params, headers=headers)
        self.access_token = r.json().get('access_token')

        return self.access_token

    def _handleResponse(self, response):
        """
        TODO: This text

        :return: response as dict. Dict has a key named status for HTTP-status code. In error case there is string
        """

        answer = {'status': response.status_code}

        if response.status_code in (200, 202):
            try:
                if response.headers['Content-Type'].startswith("multipart/"):
                    meta, filebytes = decoder.MultipartDecoder.from_response(response).parts
                    answer['content'] = filebytes.content
                    answer['metadata'] = json.loads(meta.content.decode('utf-8'))
                else:
                    answer['content'] = response.json()
            except:
                answer['message'] = response.text
        else:
            answer['message'] = response.text

        return answer

    def request(self, method, endpoint, headers=None, url=None, files=None, *args, **kwargs):
        """Method to make HTTP requests over Procountor REST API

        :param method: wanted request method, uppercase string
        :param endpoint: wanted REST API endpoint, string
        :param headers: Overwrite HTTP-headers, dict
        :param kwargs: query parameters to pass to Procountor, dict
        :return: response from rest server, dict
        """
        headers = headers or self._headers(method, endpoint)
        url = url or self.api_url + endpoint

        response = requests.request(method, url, headers=headers, files=files, json=kwargs)

        # refresh token if out of date
        if response.status_code == 401:
            self.access_token = self.refresh_access_token()
            response = requests.request(method, url, headers=headers, files=files, json=kwargs)

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
                    'content-type': 'multipart/mixed',
                    'authorization': 'Bearer {}'.format(self.access_token),
                }
            elif method == "POST":
                headers = {
                    # can't put 'content-type': 'multipart/form-data' here as documentation says. Requests generates it
                    # automatically.
                    'authorization': 'Bearer {}'.format(self.access_token),
                }
            else:
                headers = {
                    'content-type': 'application/json',
                    'authorization': 'Bearer {}'.format(self.access_token),
                }
        else:
            headers = {
                'content-type': 'application/json',
                'authorization': 'Bearer {}'.format(self.access_token),
            }

        return headers
