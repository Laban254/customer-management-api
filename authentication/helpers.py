from django.contrib.auth.models import User

def authenticate_or_create_user(email, user_info):
    """
    Authenticates an existing user by email or creates a new user if none exists.

    Args:
        email (str): The email address of the user.
        user_info (dict): A dictionary containing user information from Google, 
                          including the user's Google ID and names

    Returns:
        User: An instance of the User model, either existing or newly created.
    """
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create(
            username=user_info.get('sub'), 
            email=email,
            first_name=user_info.get('given_name', ''), 
            last_name=user_info.get('family_name', ''),
        )
    
    return user
