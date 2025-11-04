import asyncio
import websockets
import json
from openai import OpenAI
import base64
import speech_capabilities

client = OpenAI()


async def handle_media(websocket):
    print("Twilio connected to /media stream")

    async for message in websocket:
        data = json.loads(message)
        if data.get("event") == "media":
            audio_chunk = base64.b64decode(data["media"]["payload"])

            # 1. Send audio to speech-to-text model
            text = speech_capabilities.transcribe_audio(audio_chunk)

            if text:
                print("User said:", text)

                # 2. Generate AI reply
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system",
                         "content": "You are a friendly call assistant scheduling meetings."},
                        {"role": "user", "content": text},
                    ],
                )
                reply = response.choices[0].message.content
                print("AI says:", reply)

                # 3. Convert AI reply to speech (TTS)
                audio_reply = speech_capabilities.synthesize_speech(reply)

                # 4. Send audio back to Twilio stream
                await websocket.send(json.dumps({
                    "event": "media",
                    "media": {"payload": base64.b64encode(audio_reply).decode("utf-8")}
                }))


async def main():
    async with websockets.serve(handle_media, "0.0.0.0", 8000):
        print("Listening for Twilio media streams on ws://0.0.0.0:8000")
        await asyncio.Future()  # run forever


asyncio.run(main())
