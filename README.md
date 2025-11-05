# Call Center AI

This project is an AI-powered outbound call system with a simple web interface built using **React** and **Flask**. The AI interacts with the user via **Twilio** calls and allows them to select available slots.

## What I Did

- Created a **React frontend** where users can enter a phone number and press "Call".
- Built a **Flask backend** to serve the React app and handle API requests.
- Integrated **Twilio** to make outbound calls.
- Implemented a simple **AI assistant** that:
  - Greets the user on the call.
  - Offers the first few available slots.
  - Accepts user input via speech or keypad and books the slot.
- Handled slot booking with a **mock calendar system** (`my_calendar`) for demonstration.
- Deployed the app in a way that serves the React build from Flask.

## Future Improvements

If I had more time, I would:

1. **Validate user input** to ensure proper phone numbers before making a call.
2. Allow **calling multiple numbers at once**.
3. Integrate a **real calendar system** and automatically send a Google Calendar invitation to the person the AI called, and track the available slots.
