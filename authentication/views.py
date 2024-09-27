import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from urllib.parse import urlencode
import requests
from django.conf import settings
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from .helpers import authenticate_or_create_user
from rest_framework.permissions import AllowAny

logger = logging.getLogger('auth')  

class GoogleLoginView(APIView):
    """
    Handles OAuth2 login flow for Google authentication.
    This view is publicly accessible and redirects unauthenticated users 
    to Google's OAuth2 login page.
    """

    def get(self, request):
        """
        Initiates the OAuth2 login process by redirecting the user to the 
        Google authentication page with required parameters.
        """
        params = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'response_type': 'code',
            'scope': 'openid email profile',
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
            'state': 'random_string_for_csrf_protection',
            'access_type': 'offline',  
            'prompt': 'consent', 
        }
        google_auth_url = 'https://accounts.google.com/o/oauth2/auth?' + urlencode(params)
        logger.debug('Redirecting to Google Auth URL: %s', google_auth_url)
        return redirect(google_auth_url)

class GoogleCallbackView(APIView):
    """
    Handles the Google OAuth2 callback to exchange the authorization code 
    for an access token, retrieve user information, and authenticate or create 
    the user in the system.
    """

    def get(self, request):
        """
        Handles the GET request to process Google's OAuth2 callback.
        Expects an authorization code and exchanges it for user information.
        """
        # Retrieve authorization code from request
        code = request.GET.get('code')
        if not code:
            logger.warning('Authorization code not provided by Google')
            return Response({'error': 'Authorization code not provided by Google'}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange authorization code for access token
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        }

        try:
            token_response = requests.post(token_url, data=token_data, timeout=10)
            token_response.raise_for_status()  # Raise an exception for 4XX/5XX errors
            token_json = token_response.json()
            logger.info('Successfully exchanged authorization code for access token')
        except requests.exceptions.RequestException as e:
            logger.error('Failed to exchange authorization code: %s', str(e))
            return Response({'error': f'Failed to exchange authorization code: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        if 'access_token' not in token_json:
            logger.error('Failed to obtain access token')
            return Response({'error': 'Failed to obtain access token'}, status=status.HTTP_400_BAD_REQUEST)

        user_info_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        try:
            user_info_response = requests.get(user_info_url, headers={
                'Authorization': f"Bearer {token_json['access_token']}"
            }, timeout=10)
            user_info_response.raise_for_status()  # catch 4XX/5XX errors
            user_info = user_info_response.json()
            logger.info('Successfully retrieved user info from Google')
        except requests.exceptions.RequestException as e:
            logger.error('Failed to retrieve user info: %s', str(e))
            return Response({'error': f'Failed to retrieve user info: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        email = user_info.get('email')
        if not email:
            logger.error('Google did not return an email address')
            return Response({'error': 'Google did not return an email address'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate_or_create_user(email, user_info)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        login(request, user)
        logger.info('User %s logged in successfully', email)

        return Response({
            'access': access_token,
            'refresh': refresh_token
        }, status=status.HTTP_200_OK)