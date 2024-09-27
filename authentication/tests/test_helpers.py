from django.test import TestCase
from django.contrib.auth import get_user_model
from authentication.helpers import authenticate_or_create_user

User = get_user_model()

class AuthenticateOrCreateUserTest(TestCase):
    def setUp(self):
        # Create an initial user with a specific username
        self.email = 'testuser@example.com'
        self.user_info = {
            'sub': '1234567890',
            'given_name': 'Test',
            'family_name': 'User',
        }
        self.user = User.objects.create(
            email=self.email,
            username=self.user_info['sub'],
            first_name=self.user_info['given_name'],
            last_name=self.user_info['family_name']
        )
    
    def test_create_new_user(self):
        """
        Test that a new user is created if no user with the given email exists.
        """
        new_email = 'newuser@example.com'
        new_user_info = {
            'sub': '0987654321',
            'given_name': 'New',
            'family_name': 'User',
        }
        user = authenticate_or_create_user(new_email, new_user_info)
        self.assertEqual(user.email, new_email)
        self.assertEqual(user.username, new_user_info['sub'])
        self.assertEqual(user.first_name, new_user_info['given_name'])
        self.assertEqual(user.last_name, new_user_info['family_name'])

    def test_existing_user(self):
        """
        Test that an existing user is returned if a user with the given email already exists.
        """
        user = authenticate_or_create_user(self.email, self.user_info)
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.username, self.user_info['sub'])

    def test_unique_username_generation(self):
        """
        Test that the username is made unique by appending a number if the username already exists.
        """
        duplicate_email = 'duplicate@example.com'
        duplicate_user_info = {
            'sub': self.user_info['sub'],
            'given_name': 'Duplicate',
            'family_name': 'User',
        }
        
        user = authenticate_or_create_user(duplicate_email, duplicate_user_info)
        
        # Since '1234567890' is taken, the username should be '12345678901'
        self.assertEqual(user.username, '12345678901')
        self.assertEqual(user.email, duplicate_email)
        self.assertEqual(user.first_name, duplicate_user_info['given_name'])
        self.assertEqual(user.last_name, duplicate_user_info['family_name'])