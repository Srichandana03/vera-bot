# Vera Bot 🤖

A conversational AI assistant that handles appointment scheduling using natural language input.
Built as a stateful, rule-based system with multi-turn dialogue support.

---

## 🚀 Live Demo

👉 https://vera-bot-1.onrender.com

---

## 🧠 Overview

Vera Bot allows users to book, cancel, and reschedule appointments through conversational interactions.
It intelligently extracts date and time from flexible user input and manages dialogue state across multiple turns.

---

## ✨ Features

### 🗓️ Appointment Booking

* Supports multi-step conversations
* Accepts flexible inputs like:

  * "tomorrow evening"
  * "next monday 6pm"
  * "book appointment 5 nov 9pm"

---

### 🔁 Rescheduling

* Modify existing appointments:

  * "change my appointment to friday 8pm"

---

### ❌ Cancellation

* Cancel existing bookings:

  * "cancel my booking"

---

### 🧠 Context Awareness

* Maintains state across conversation turns
* Handles:

  * partial inputs (only date / only time)
  * flexible order (time → date or date → time)

---

### ✏️ Correction Handling

* Supports user corrections:

  * "actually make it tuesday 6pm"

---

### ✅ Validation

* Prevents invalid bookings:

  * past dates are rejected

---

## 🧱 Tech Stack

| Layer             | Technology   |
| ----------------- | ------------ |
| Language          | Python       |
| Backend Framework | Flask        |
| NLP Utility       | dateparser   |
| Deployment        | Render       |
| Version Control   | Git + GitHub |

---

## ⚙️ Architecture

```text
User Input → Intent Detection → Action Handler → State Update → Response
```

### Components:

* `intent.py` → detects user intent (booking, cancel, reschedule)
* `actions.py` → core logic & state management
* `utils.py` → date/time extraction
* `app.py` → Flask API wrapper

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
Bot: You're all set! I've booked your appointment for May 05 at 6:00 PM.
```

---

## ⚠️ Limitations

* Rule-based intent detection (no ML/NLP model)
* No persistent storage (data resets on restart)
* Limited handling of:

  * ambiguous inputs
  * multiple intents in one message
* Single-user state (not scalable for multi-user systems)

---

## 🚀 Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/Srichandana03/vera-bot.git
cd vera-bot
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run Locally

```bash
python app.py
```

---

### 4. Access

```
http://localhost:10000
```

---

## 🌐 Deployment

Deployed using **Render** as a web service.

* Flask API exposed via `/chat`
* Uses dynamic port binding for cloud hosting

---

## 🔮 Future Improvements

* Replace rule-based intent detection with ML/NLP model
* Add persistent storage (database)
* Support multi-user sessions
* Handle ambiguous and multi-intent inputs
* Build frontend UI for better interaction

---

## 👩‍💻 Author

**Srichandana**
B.Tech – Artificial Intelligence & Machine Learning

---
