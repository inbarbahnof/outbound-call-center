from twilio.rest import Client
from dotenv import load_dotenv
from urllib.parse import quote
import os

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()

BASE_URL = os.getenv("BASE_URL")  # ngrok HTTPS URL, e.g. https://abc123.ngrok.io
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")  # your Twilio number, e.g. +18005550199

if not all([BASE_URL, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER]):
    raise ValueError("Missing one or more environment variables in .env")

# Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# ----------------------------
# Call functions
# ----------------------------
def make_call(to_number, message):
    """Make an outbound call to `to_number` with a message"""
    encoded_message = quote(message)  # URL-encode special characters
    call = twilio_client.calls.create(
        to=to_number,
        from_=TWILIO_NUMBER,
        url=f"{BASE_URL}/voice?message={encoded_message}"
    )
    print(f"Call started to {to_number}. SID: {call.sid}")


def call_leads(numbers, message):
    """Call multiple leads sequentially"""
    for number in numbers:
        make_call(number, message)

if __name__ == "__main__":
    leads = ["+972 54 943 1226"]  # Replace with your test numbers
    message = "Hi! This is Inbar’s AI assistant. Are you available for a quick meeting tomorrow?"

    # Call all leads
    call_leads(leads, message)