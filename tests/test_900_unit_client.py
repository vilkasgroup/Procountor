"""Offline unit tests for :mod:`procountor.client`.

These tests mock every network interaction, so they run without Procountor
credentials and form the regression gate exercised in CI.
"""

import unittest
from unittest import mock

from procountor.client import Client
from tests.test_client import build_mock_client, TEST_ACCESS_TOKEN


class ClientUrlTests(unittest.TestCase):
    def setUp(self):
        self.client = build_mock_client()

    def test_init_sets_attributes_and_token(self):
        self.assertIsInstance(self.client, Client)
        self.assertEqual(self.client.client_id, "test-client-id")
        self.assertEqual(self.client.client_secret, "test-client-secret")
        self.assertEqual(self.client.redirect_uri, "https://example.com/callback")
        self.assertTrue(self.client.test_mode)
        self.assertEqual(self.client.access_token, TEST_ACCESS_TOKEN)

    def test_api_host_test_mode(self):
        self.client.test_mode = True
        self.assertEqual(self.client.api_host, "https://pts-api.procountor.com")

    def test_api_host_production(self):
        self.client.test_mode = False
        self.assertEqual(self.client.api_host, "https://api.procountor.com")

    def test_api_url_supported(self):
        self.client.api_version = "supported"
        self.assertEqual(
            self.client.api_url, "https://pts-api.procountor.com/supported/api/"
        )

    def test_api_url_latest(self):
        self.client.api_version = "latest"
        self.assertEqual(
            self.client.api_url, "https://pts-api.procountor.com/latest/api/"
        )

    def test_api_url_specified_version(self):
        self.client.api_version = "20.01"
        self.assertEqual(
            self.client.api_url, "https://pts-api.procountor.com/v2001/api/"
        )

    def test_api_url_invalid_version_raises(self):
        self.client.api_version = "not-a-version"
        with self.assertRaises(ValueError):
            _ = self.client.api_url

    def test_dict_to_url_query_empty(self):
        self.assertEqual(self.client._dict_to_url_query({}), "")

    def test_dict_to_url_query_with_values(self):
        self.assertEqual(
            self.client._dict_to_url_query({"size": 5}), "?size=5"
        )

    def test_dict_to_url_query_non_dict_raises(self):
        with self.assertRaises(Exception):
            self.client._dict_to_url_query("nope")

    def test_create_endpoint(self):
        self.assertEqual(self.client._create_endpoint("invoices"), "invoices")
        self.assertEqual(
            self.client._create_endpoint("invoices", {"startDate": "2024-01-01"}),
            "invoices?startDate=2024-01-01",
        )


class ClientHeaderTests(unittest.TestCase):
    def setUp(self):
        self.client = build_mock_client()

    def test_headers_default_endpoint(self):
        headers = self.client._headers("GET", "users")
        self.assertEqual(headers["content-type"], "application/json")
        self.assertEqual(
            headers["authorization"], "Bearer {}".format(TEST_ACCESS_TOKEN)
        )

    def test_headers_attachment_get_is_multipart(self):
        headers = self.client._headers("GET", "attachments/1")
        self.assertEqual(headers["content-type"], "multipart/mixed")

    def test_headers_attachment_post_omits_content_type(self):
        headers = self.client._headers("POST", "attachments")
        self.assertNotIn("content-type", headers)
        self.assertIn("authorization", headers)

    def test_headers_attachment_other_method_is_json(self):
        headers = self.client._headers("DELETE", "attachments/1")
        self.assertEqual(headers["content-type"], "application/json")


class GetTokenTests(unittest.TestCase):
    def _make_response(self, status_code, json_data=None, text=""):
        response = mock.Mock()
        response.status_code = status_code
        response.text = text
        response.json.return_value = json_data or {}
        return response

    @mock.patch("procountor.transport.requests.post")
    def test_successful_token(self, mock_post):
        mock_post.return_value = self._make_response(
            200, {"access_token": "real-token"}
        )
        client = build_mock_client()
        # call the real implementation now that requests.post is mocked
        token = Client._get_token(client)
        self.assertEqual(token, "real-token")
        self.assertEqual(client.access_token, "real-token")

    @mock.patch("procountor.transport.requests.post")
    def test_401_raises_runtime_error(self, mock_post):
        mock_post.return_value = self._make_response(401, text="unauthorized")
        client = build_mock_client()
        with self.assertRaises(RuntimeError):
            Client._get_token(client)

    @mock.patch("procountor.transport.requests.post")
    def test_404_raises_runtime_error(self, mock_post):
        mock_post.return_value = self._make_response(404, text="not found")
        client = build_mock_client()
        with self.assertRaises(RuntimeError):
            Client._get_token(client)

    @mock.patch("procountor.transport.requests.post")
    def test_unexpected_status_raises_runtime_error(self, mock_post):
        mock_post.return_value = self._make_response(500, text="boom")
        client = build_mock_client()
        with self.assertRaises(RuntimeError):
            Client._get_token(client)

    @mock.patch("procountor.transport.requests.post")
    def test_missing_access_token_raises_runtime_error(self, mock_post):
        mock_post.return_value = self._make_response(200, {"something_else": 1})
        client = build_mock_client()
        with self.assertRaises(RuntimeError):
            Client._get_token(client)


class GenericVerbTests(unittest.TestCase):
    """The generic get/post/put/delete verbs that reach any endpoint."""

    def setUp(self):
        self.client = build_mock_client()
        patcher = mock.patch.object(
            self.client, "request", return_value={"status": 200, "content": {}}
        )
        self.mock_request = patcher.start()
        self.addCleanup(patcher.stop)

    def test_get_builds_query_string(self):
        self.client.get("invoices", startDate="2024-01-01")
        self.mock_request.assert_called_once_with(
            "GET", "invoices?startDate=2024-01-01"
        )

    def test_get_without_params(self):
        self.client.get("company")
        self.mock_request.assert_called_once_with("GET", "company")

    def test_post_sends_json_body(self):
        self.client.post("products", json={"name": "Widget"})
        self.mock_request.assert_called_once_with(
            "POST", "products", json={"name": "Widget"}
        )

    def test_post_supports_list_body(self):
        self.client.post("payments", json=[{"id": 1}, {"id": 2}])
        self.mock_request.assert_called_once_with(
            "POST", "payments", json=[{"id": 1}, {"id": 2}]
        )

    def test_put_sends_json_body(self):
        self.client.put("invoices/7", json={"status": "PAID"})
        self.mock_request.assert_called_once_with(
            "PUT", "invoices/7", json={"status": "PAID"}
        )

    def test_delete(self):
        self.client.delete("attachments/5")
        self.mock_request.assert_called_once_with("DELETE", "attachments/5")


class RequestBodyTests(unittest.TestCase):
    """The explicit ``json`` body argument added to request()."""

    def setUp(self):
        self.client = build_mock_client()

    @mock.patch("procountor.transport.requests.request")
    def test_explicit_json_list_body_is_sent(self, mock_request):
        response = mock.Mock()
        response.status_code = 200
        response.headers = {"Content-Type": "application/json"}
        response.json.return_value = {}
        mock_request.return_value = response

        self.client.request("POST", "payments", json=[{"id": 1}])

        _, kwargs = mock_request.call_args
        self.assertEqual(kwargs["json"], [{"id": 1}])

    @mock.patch("procountor.transport.requests.request")
    def test_kwargs_still_become_body(self, mock_request):
        response = mock.Mock()
        response.status_code = 200
        response.headers = {"Content-Type": "application/json"}
        response.json.return_value = {}
        mock_request.return_value = response

        self.client.request("POST", "invoices", name="Acme")

        _, kwargs = mock_request.call_args
        self.assertEqual(kwargs["json"], {"name": "Acme"})


class HandleResponseTests(unittest.TestCase):
    def setUp(self):
        self.client = build_mock_client()

    def _response(self, status_code, json_data=None, text="", content_type="application/json"):
        response = mock.Mock()
        response.status_code = status_code
        response.text = text
        response.headers = {"Content-Type": content_type}
        if json_data is None:
            response.json.side_effect = ValueError("no json")
        else:
            response.json.return_value = json_data
        return response

    def test_json_content_on_200(self):
        result = self.client._handleResponse(self._response(200, {"id": 1}))
        self.assertEqual(result, {"status": 200, "content": {"id": 1}})

    def test_error_status_returns_message(self):
        result = self.client._handleResponse(self._response(400, text="bad request"))
        self.assertEqual(result, {"status": 400, "message": "bad request"})

    def test_invalid_json_falls_back_to_message(self):
        result = self.client._handleResponse(
            self._response(200, json_data=None, text="not json")
        )
        self.assertEqual(result, {"status": 200, "message": "not json"})


class RequestTests(unittest.TestCase):
    def setUp(self):
        self.client = build_mock_client()

    @mock.patch("procountor.transport.requests.request")
    def test_request_returns_handled_response(self, mock_request):
        response = mock.Mock()
        response.status_code = 200
        response.headers = {"Content-Type": "application/json"}
        response.json.return_value = {"ok": True}
        mock_request.return_value = response

        result = self.client.request("GET", "users")

        self.assertEqual(result, {"status": 200, "content": {"ok": True}})
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "GET")
        self.assertEqual(args[1], "https://pts-api.procountor.com/supported/api/users")

    @mock.patch.object(Client, "_get_token", return_value="refreshed-token")
    @mock.patch("procountor.transport.requests.request")
    def test_request_refreshes_token_on_401(self, mock_request, mock_get_token):
        unauthorized = mock.Mock()
        unauthorized.status_code = 401
        ok = mock.Mock()
        ok.status_code = 200
        ok.headers = {"Content-Type": "application/json"}
        ok.json.return_value = {"ok": True}
        mock_request.side_effect = [unauthorized, ok]

        result = self.client.request("GET", "users")

        self.assertEqual(result, {"status": 200, "content": {"ok": True}})
        self.assertEqual(mock_request.call_count, 2)
        mock_get_token.assert_called_once()


if __name__ == "__main__":
    unittest.main()
