# Vera Bot 🤖

A conversational AI assistant for booking, canceling, and rescheduling appointments using natural language.

---

## 🌐 Live Endpoint

👉 https://vera-bot-1-ldar.onrender.com

---

## 🧠 Overview

Vera Bot is a stateful conversational system that supports multi-turn dialogue for appointment management.
It processes natural language input and extracts structured date/time information to perform actions.

---

## ✨ Features

* Multi-turn booking flow
* Handles partial inputs (date-only / time-only)
* Flexible phrasing ("tomorrow evening", "next monday 6pm")
* Cancel booking
* Reschedule booking
* Correction handling ("actually make it tuesday")
* Basic validation (prevents past dates)

---

## 🧱 Tech Stack

* Python
* Flask (API backend)
* dateparser (NLP for date/time extraction)
* Render (deployment)
* GitHub (version control)

---

## ⚙️ API Endpoints

Base URL:

```id="bp9r0a"
https://vera-bot-1-ldar.onrender.com
```

---

### 🔹 POST `/v1/reply`

Handles user messages and returns bot response.

#### Request

```json id="ev2pf6"
{
  "message": "book appointment tomorrow 7pm"
}
```

#### Response

```json id="0sm4ij"
{
  "action": "book_appointment",
  "body": "You're all set! I've booked your appointment..."
}
```

---

### 🔹 POST `/v1/context`

Used to initialize or reset conversation state.

```json id="j5sf0c"
{
  "reset": true
}
```

---

### 🔹 POST `/v1/tick`

Heartbeat / no-op endpoint.

---

### 🔹 GET `/v1/healthz`

```json id="wdlhpn"
{
  "status": "ok"
}
```

---

### 🔹 GET `/v1/metadata`

```json id="lb0v3n"
{
  "name": "Vera Bot",
  "version": "1.0",
  "capabilities": ["booking", "cancel", "reschedule"]
}
```

---

## 🧪 Example Interaction

```id="r0t9nr"
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

```bash id="zv0q2r"
pip install -r requirements.txt
python app.py
```

---

## 👩‍💻 Author

Srichandana
B.Tech – Artificial Intelligence & Machine Learning
