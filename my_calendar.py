import json
import os

CALENDAR_FILE = "calendar.json"

# Initialize calendar if it doesn't exist
if not os.path.exists(CALENDAR_FILE):
    with open(CALENDAR_FILE, "w") as f:
        json.dump({
            "available": {
                "2025-11-05": ["10:00", "14:00", "16:30"],
                "2025-11-06": ["09:30", "11:00", "15:00"]
            },
            "booked": []
        }, f)


def load_calendar():
    with open(CALENDAR_FILE, "r") as f:
        return json.load(f)


def save_calendar(calendar):
    with open(CALENDAR_FILE, "w") as f:
        json.dump(calendar, f, indent=2)


def get_available_slots():
    calendar = load_calendar()
    slots = []
    for date, times in calendar["available"].items():
        for t in times:
            slots.append(f"{date} {t}")
    return slots


def book_slot(slot, caller_number):
    calendar = load_calendar()
    date, time = slot.split(" ")
    if slot in [f"{date} {t}" for t in calendar["available"].get(date, [])]:
        # Remove from available
        calendar["available"][date].remove(time)
        # Add to booked
        calendar["booked"].append({"caller": caller_number, "slot": slot})
        save_calendar(calendar)
        return True
    return False
