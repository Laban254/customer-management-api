from django.test import TestCase
from django.conf import settings
from django.urls import reverse

class GoogleLoginViewTest(TestCase):
    """
    Test suite for Google login functionality.
    
    This test checks the behavior of the Google login view by ensuring that
    the user is redirected to the correct Google OAuth URL with the appropriate
    parameters.
    """

    def test_google_login_redirect(self):
        """
        Test that the Google login view redirects to the Google OAuth endpoint.

        This test performs the following steps:
        1. Sends a GET request to the 'google-login' view.
        2. Asserts that the response status code is 302 (redirect).
        3. Asserts that the response URL contains the Google OAuth authorization URL.
        4. Asserts that the response URL contains the correct `client_id` parameter.
        """
        response = self.client.get(reverse('google-login'))

        self.assertEqual(response.status_code, 302)

        google_auth_url = 'https://accounts.google.com/o/oauth2/auth'
        self.assertIn(google_auth_url, response.url)
        self.assertIn('client_id=' + settings.GOOGLE_CLIENT_ID, response.url)
        # self.assertIn('redirect_uri=' + settings.GOOGLE_REDIRECT_URI, response.url)