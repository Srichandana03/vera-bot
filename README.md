# Vera Bot 🤖

A conversational AI assistant for booking, canceling, and rescheduling appointments using natural language.

---

## 🌐 Live Demo

👉 https://vera-bot-1-ldar.onrender.com

---

## 🧠 Overview

Vera Bot enables users to interact conversationally to manage appointments.
It supports flexible inputs like:

* "tomorrow evening"
* "next monday 6pm"
* "book appointment 5 nov 9pm"

The system maintains conversational state and handles multi-step interactions.

---

## ✨ Features

* ✅ Multi-turn booking flow (date + time collection)
* ✅ Handles partial inputs (only date / only time)
* ✅ Flexible input order (time → date or date → time)
* ✅ Cancellation support ("cancel my booking")
* ✅ Rescheduling ("change my appointment to friday 8pm")
* ✅ Correction handling ("actually make it tuesday 6pm")
* ✅ Date validation (prevents past bookings)

---

## 🧱 Tech Stack

* Python
* Flask (Backend API)
* dateparser (Natural language date/time parsing)
* Render (Deployment)
* Git & GitHub (Version control)

---

## ⚙️ Architecture

```
User Input → Intent Detection → Action Handler → State Update → Response
```

### Components:

* `intent.py` → detects user intent
* `actions.py` → handles logic + state
* `utils.py` → extracts date/time
* `app.py` → Flask API

---

## 🔌 API Usage

### Endpoint

```
POST /chat
```

### Request

```json
{
  "message": "book appointment tomorrow 7pm"
}
```

### Response

```json
{
  "action": "book_appointment",
  "response": "You're all set! I've booked your appointment..."
}
```

---

## 🧪 Example Conversation

```
User: book appointment
Bot: Sure — what date and time should I book?

User: next monday
Bot: Got the date. What time should I book?

User: 6pm
Bot: You're all set! I've booked your appointment...
```

---

## ⚠️ Limitations

* Rule-based intent detection (no ML model)
* No persistent storage (state resets on restart)
* Single-user state (not scalable)
* Limited handling of ambiguous or multi-intent inputs

---

## 🚀 Run Locally

```bash
pip install -r requirements.txt
python app.py
```

---

## 👩‍💻 Author

Srichandana
B.Tech – Artificial Intelligence & Machine Learning
