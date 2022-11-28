from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from ..msb import MSBService


class APIServiceTest(SimpleTestCase):
    def test_instanciate_service(self):
        """
        Tests if the a sub class of APIService can be instatiated
        """

        mock_endpoint = "mock_endpoint"
        msb_api_service = MSBService(mock_endpoint)

        self.assertEquals(msb_api_service.__class__.__name__, "MSBService")
        self.assertEquals(msb_api_service.__class__.__mro__[1].__name__, "APIService")

    @patch("apps.services.base.cache")
    @patch("apps.services.base.requests")
    def test_get_list(self, mock_requests, mock_cache):
        """
        Tests get_list
        """

        mock_cache.get.return_value = None

        mock_token = "mock_token"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "result": [
                {
                    "mock_key": "mock_result",
                }
            ],
        }

        mock_requests.post.return_value.status_code = 200
        mock_requests.post.headers = {
            "Authorization": f"Bearer {mock_token}",
        }
        mock_requests.post.return_value = mock_response

        mock_endpoint = "mock_endpoint"
        msb_api_service = MSBService(mock_endpoint)
        response = msb_api_service.get_list(mock_token)

        self.assertEquals(len(response), 1)
        self.assertEquals(response[0].get("mock_key"), "mock_result")

    @patch("apps.services.base.cache")
    @patch("apps.services.base.requests")
    def test_get_list_from_cache(self, mock_requests, mock_cache):
        """
        Tests get_list from cache
        """

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "result": [
                {
                    "mock_key": "mock_result",
                }
            ],
        }
        mock_cache.get.return_value = mock_response
        mock_token = "mock_token"
        mock_endpoint = "mock_endpoint"
        msb_api_service = MSBService(mock_endpoint)
        response = msb_api_service.get_list(mock_token)

        self.assertEquals(len(response), 1)
        self.assertEquals(response[0].get("mock_key"), "mock_result")
