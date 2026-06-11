from __future__ import annotations

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
