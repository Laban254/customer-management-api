from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.conf import settings
from django.contrib.auth import get_user_model
from authentication.helpers import authenticate_or_create_user

User = get_user_model()

class GoogleCallbackViewTest(TestCase):
    """
    Test suite for Google OAuth callback view.

    This test class covers various scenarios for handling the Google OAuth callback,
    including successful authentication, missing authorization code, failed token exchange,
    and failed user information retrieval.

    The test class uses the `unittest.mock.patch` decorator to mock the external requests
    (for token exchange and fetching user info from Google) and the helper method
    `authenticate_or_create_user` that handles user creation or authentication.
    """

    def setUp(self):
        """
        Set up the test client for API requests.
        """
        self.client = APIClient()

    @patch('requests.post')
    @patch('requests.get')
    @patch('authentication.helpers.authenticate_or_create_user')
    def test_google_callback_success(self, mock_authenticate_or_create_user, mock_get, mock_post):
        """
        Test successful Google OAuth callback with valid authorization code.

        Mocks:
        - The token exchange with Google is successful, returning an access token.
        - The request for user information is successful, returning a user's email.
        - User creation or authentication is mocked to return a valid user.

        Assertions:
        - The status code is 200 OK.
        - The response contains access and refresh tokens.
        """
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'access_token': 'mock_access_token'}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'email': 'testuser@gmail.com'}

        mock_user = User(email='testuser@gmail.com', username='testuser')
        mock_authenticate_or_create_user.return_value = mock_user

        response = self.client.get(reverse('google-callback'), {'code': 'mock_code'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    @patch('requests.post')
    @patch('requests.get')
    def test_google_callback_no_code(self, mock_get, mock_post):
        """
        Test Google OAuth callback when no authorization code is provided.

        Simulates the scenario where Google does not return an authorization code in the callback.

        Assertions:
        - The status code is 400 Bad Request.
        - The error message indicates the missing authorization code.
        """
        response = self.client.get(reverse('google-callback'))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Authorization code not provided by Google')

    @patch('requests.post')
    def test_google_callback_failed_token_exchange(self, mock_post):
        """
        Test Google OAuth callback with a failed token exchange.

        Simulates a scenario where the authorization code is invalid, and the token exchange with Google fails.

        Assertions:
        - The status code is 400 Bad Request.
        - The error message indicates the failure to obtain an access token.
        """
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {}

        response = self.client.get(reverse('google-callback'), {'code': 'invalid_code'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Failed to obtain access token')

    @patch('requests.post')
    @patch('requests.get')
    def test_google_callback_failed_user_info(self, mock_get, mock_post):
        """
        Test Google OAuth callback with a failed user info request.

        Simulates a successful token exchange but a failure when fetching user information from Google.

        Assertions:
        - The status code is 400 Bad Request.
        - The error message indicates the failure to retrieve user info.
        """
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'access_token': 'mock_access_token'}

        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = {}

        response = self.client.get(reverse('google-callback'), {'code': 'mock_code'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Google did not return an email address') 