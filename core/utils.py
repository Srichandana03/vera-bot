import dateparser
import re
from dateparser.search import search_dates

def extract_datetime(text):
    original_text = text.lower()

    # -------------------------------
    # 1. FUZZY TIME HANDLING
    # -------------------------------
    text = original_text.replace("evening", "7pm")
    text = text.replace("morning", "9am")
    text = text.replace("afternoon", "2pm")

    # -------------------------------
    # 2. EXTRACT TIME (ROBUST)
    # -------------------------------
    time = None

    matches = re.findall(r'\b\d{1,2}(?::\d{2})?\s?(?:am|pm)\b', text)

    if matches:
        raw_time = matches[0]
        parsed_time = dateparser.parse(raw_time)

        if parsed_time:
            time = parsed_time.strftime("%H:%M")

    # -------------------------------
    # 3. EXTRACT DATE
    # -------------------------------
    cleaned = re.sub(r'\b(book|appointment|schedule)\b', '', text)

    results = search_dates(cleaned, settings={"PREFER_DATES_FROM": "future"})

    date = None

    if results:
        dt = results[0][1]

        # Only accept date if user actually mentioned date words
        if any(word in original_text for word in [
            "tomorrow", "today", "next",
            "monday", "tuesday", "wednesday", "thursday",
            "friday", "saturday", "sunday",
            "jan", "feb", "mar", "apr", "may", "jun",
            "jul", "aug", "sep", "oct", "nov", "dec"
        ]):
            date = dt.strftime("%Y-%m-%d")

    return date, time