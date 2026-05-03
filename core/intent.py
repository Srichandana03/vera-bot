def detect_intent(text):
    text = text.lower()

    # 🔴 priority first
    if any(x in text for x in ["stop", "unsubscribe", "no more"]):
        return "stop_intent"

    if any(x in text for x in ["cancel", "remove", "delete"]):
        return "cancel_request"

    if any(x in text for x in ["change", "reschedule", "modify", "move"]):
        return "reschedule_request"

    # 🟡 improved booking coverage (safe expansion)
    if any(x in text for x in [
        "book", "appointment", "schedule", "slot", "visit",
        "come", "meet", "plan"
    ]):
        return "booking_request"

    if any(x in text for x in ["hi", "hello", "hey"]):
        return "greeting"

    return "fallback"