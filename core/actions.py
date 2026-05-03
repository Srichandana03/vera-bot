from core.utils import extract_datetime
from datetime import datetime


def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d")
    except:
        return date_str


def format_time(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M").strftime("%I:%M %p").lstrip("0")
    except:
        return time_str


def is_past_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d") < datetime.now()
    except:
        return False


def handle_action(intent, text, state):

    text_lower = text.lower()

    # -------------------------------
    # 1. STOP
    # -------------------------------
    if intent == "stop_intent":
        state.clear()
        return {
            "action": "end",
            "response": "Got it. I won’t message you further."
        }

    # -------------------------------
    # 2. CANCEL
    # -------------------------------
    if intent == "cancel_request":
        state.clear()
        return {
            "action": "cancel_booking",
            "response": "Your booking has been cancelled. Let me know if you'd like to book another slot."
        }

    # -------------------------------
    # 3. RESCHEDULE
    # -------------------------------
    if intent == "reschedule_request":
        date, time = extract_datetime(text)

        if date and time:
            if is_past_date(date):
                return {
                    "action": "invalid_date",
                    "response": "That date is in the past. Please choose a future date."
                }

            return {
                "action": "reschedule_booking",
                "response": f"Your appointment has been moved to {format_date(date)} at {format_time(time)}. Need anything else?"
            }

        return {
            "action": "ask_details",
            "response": "Sure — what new date and time would you like?"
        }

    # -------------------------------
    # 4. FOLLOW-UP (BOOKING FLOW)
    # -------------------------------
    if state.get("pending") == "booking":

        # correction handling
        if any(x in text_lower for x in ["actually", "instead", "change it"]):
            state.pop("date", None)
            state.pop("time", None)

        date, time = extract_datetime(text)

        if date:
            state["date"] = date
        if time:
            state["time"] = time

        if state.get("date") and state.get("time"):
            final_date = state.pop("date")
            final_time = state.pop("time")
            state.pop("pending")

            # 🔥 validation (safe upgrade)
            if is_past_date(final_date):
                return {
                    "action": "invalid_date",
                    "response": "That date is in the past. Please choose a future date."
                }

            return {
                "action": "book_appointment",
                "response": f"You're all set! I've booked your appointment for {format_date(final_date)} at {format_time(final_time)}. Need anything else?"
            }

        if state.get("date") and not state.get("time"):
            return {
                "action": "ask_time",
                "response": "Got the date. What time should I book?"
            }

        if state.get("time") and not state.get("date"):
            return {
                "action": "ask_date",
                "response": "Got the time. Which date should I book?"
            }

        return {
            "action": "ask_details",
            "response": "I still need both date and time."
        }

    # -------------------------------
    # 5. GREETING
    # -------------------------------
    if intent == "greeting":
        return {
            "action": "none",
            "response": "Hi! How can I help you today?"
        }

    # -------------------------------
    # 6. BOOKING REQUEST
    # -------------------------------
    if intent == "booking_request":

        if any(x in text_lower for x in ["actually", "instead", "change it"]):
            state.pop("date", None)
            state.pop("time", None)

        date, time = extract_datetime(text)

        if date:
            state["date"] = date
        if time:
            state["time"] = time

        if state.get("date") and state.get("time"):
            final_date = state.pop("date")
            final_time = state.pop("time")

            # 🔥 validation
            if is_past_date(final_date):
                return {
                    "action": "invalid_date",
                    "response": "That date is in the past. Please choose a future date."
                }

            return {
                "action": "book_appointment",
                "response": f"You're all set! I've booked your appointment for {format_date(final_date)} at {format_time(final_time)}. Need anything else?"
            }

        state["pending"] = "booking"

        if state.get("date") and not state.get("time"):
            return {
                "action": "ask_time",
                "response": "Got the date. What time should I book?"
            }

        if state.get("time") and not state.get("date"):
            return {
                "action": "ask_date",
                "response": "Got the time. Which date should I book?"
            }

        return {
            "action": "ask_details",
            "response": "Sure — what date and time should I book?"
        }

    # -------------------------------
    # 7. FALLBACK
    # -------------------------------
    return {
        "action": "none",
        "response": "I’m not sure I understood that. Could you rephrase?"
    }