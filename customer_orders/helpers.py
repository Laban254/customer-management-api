import africastalking
from django.conf import settings

# Initialize Africa's Talking SDK
username = settings.AFRICAS_TALKING_USERNAME
api_key = settings.AFRICAS_TALKING_API_KEY
africastalking.initialize(username, api_key)

# Initialize the SMS service
sms_service = africastalking.SMS

def send_sms(phone_number, message):
    """
    Sends an SMS using Africa's Talking API.

    Args:
        phone_number (str): The recipient's phone number.
        message (str): The message content to be sent.
        sender_id (str): The sender ID for the SMS (default is '65446').

    Returns:
        dict: A dictionary containing the status and response from Africa's Talking.
    """
    try:
        response = sms_service.send(message, [phone_number])
        return {"status": "success", "response": response}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
