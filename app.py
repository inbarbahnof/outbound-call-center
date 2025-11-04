import os
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
import re
from word2number import w2n
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import my_calendar

app = Flask(__name__)

load_dotenv()

is_start = True

# OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ---- Flask endpoints ---- #

@app.route("/voice", methods=["POST"])
def voice():
    """Initial call greeting and offer slots"""
    global is_start

    resp = VoiceResponse()
    slots = my_calendar.get_available_slots()
    if not slots:
        resp.say("Sorry, no slots are available at the moment.", voice="Polly.Amy")
        return Response(str(resp), mimetype="text/xml")

    # Offer first 3 slots
    options = slots[:3]
    slot_msg = ""

    if is_start:
        slot_msg += "Hi! This is your AI assistant. Here are the available slots. "
        is_start = False

    for i, s in enumerate(options, start=1):
        slot_msg += f"Option {i}: {format_slot(s)}. "
    slot_msg += "Please say the option number you prefer."

    resp.say(slot_msg, voice="Polly.Amy")
    resp.gather(input="speech", action="/process_speech", timeout=5)
    return Response(str(resp), mimetype="text/xml")


@app.route("/process_speech", methods=["POST"])
def process_speech():
    """Handle caller response, book slot or ask if they want to repeat"""
    user_text = request.form.get("SpeechResult", "")
    caller_number = request.form.get("From", "")
    print(f"Caller said: {user_text}")

    resp = VoiceResponse()
    option = parse_option(user_text)

    if option is None:
        # Not understood → ask for keypad input instead of speech
        resp.say("Sorry, I didn’t catch that.", voice="Polly.Amy")
        resp.say("If you’d like me to repeat the available options, please press 1.", voice="Polly.Amy")

        gather = resp.gather(
            input="dtmf",
            num_digits=1,
            action="/handle_repeat",
            timeout=3
        )
        return Response(str(resp), mimetype="text/xml")

    # --- Valid option ---
    slots = my_calendar.get_available_slots()
    chosen_slot = slots[option - 1] if 0 < option <= len(slots) else None

    if chosen_slot and my_calendar.book_slot(chosen_slot, caller_number):
        resp.say(f"Great! You’re booked for {chosen_slot}. See you then!", voice="Polly.Amy")
    else:
        resp.say("Sorry, that slot is no longer available. Please try again.", voice="Polly.Amy")
        resp.gather(input="speech", action="/process_speech", timeout=5)

    return Response(str(resp), mimetype="text/xml")


@app.route("/handle_repeat", methods=["POST"])
def handle_repeat():
    """Handle if user pressed 1 to repeat"""
    digits = request.form.get("Digits", "")
    resp = VoiceResponse()

    if digits == "1":
        resp.say("Sure, let me repeat the available options.", voice="Polly.Amy")
        resp.redirect("/voice")
    else:
        resp.say("Alright. Please say the option number you prefer.", voice="Polly.Amy")
        resp.gather(input="speech", action="/process_speech", timeout=5)

    return Response(str(resp), mimetype="text/xml")


def parse_option(user_text):
    match = re.search(r'\d+', user_text)
    if match:
        return int(match.group())

    try:
        return w2n.word_to_num(user_text.lower())
    except:
        return None


def format_slot(slot):
    """
    Convert '2025-11-05 10:00' → 'Tuesday, November 5th at 10 AM'
    """
    dt = datetime.strptime(slot, "%Y-%m-%d %H:%M")
    day_suffix = lambda d: 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')
    return dt.strftime(f"%A, %B {dt.day}{day_suffix(dt.day)} at %I:%M %p")


if __name__ == "__main__":
    # 1) Start Flask server
    # 2) Trigger calls manually
    app.run(host="0.0.0.0", port=5000)


