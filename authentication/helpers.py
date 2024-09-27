from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

def authenticate_or_create_user(email, user_info):
    """
    Retrieves an existing user by email, or creates a new one if it doesn't exist.

    Args:
        email (str): Email address of the user.
        user_info (dict): Dictionary containing user information.

    Returns:
        User: An instance of the User model, either existing or newly created.
    """
    username = user_info.get('sub') or slugify(email.split('@')[0])
    
    # Ensure username is unique by appending a number if necessary
    base_username = username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    # Create or get user with a unique username
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': username,
            'first_name': user_info.get('given_name', ''),
            'last_name': user_info.get('family_name', ''),
        }
    )
    
    return user