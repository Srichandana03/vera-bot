# Vera Message Engine

A deterministic message engine built for the Magicpin Vera AI Challenge.

This system generates high-quality, context-aware merchant messages by combining trigger signals, merchant performance, category tone, and optional customer context.

---

## 🚀 What it does

Implements a `compose()`-style engine via API endpoints:

- `/v1/context` → stores merchant data
- `/v1/tick` → generates next best message
- `/v1/reply` → handles responses (basic)
- `/v1/healthz` → health check
- `/v1/metadata` → bot info

---

## 🧠 Core Idea

Instead of template-based messaging, this engine:

- Evaluates multiple possible actions  
- Scores them based on impact  
- Selects the best decision  
- Generates a grounded, specific message  

---

## ⚙️ Decision Engine

The system considers:

- Conversion rate (orders / views)  
- Demand signals (search spikes)  
- Merchant rating (trust factor)  
- Offer availability  

### Example logic:
- Low rating → fix reputation first  
- High demand + low conversion → push/optimize offer  
- High conversion → scale visibility  
- No offers → activate offer  

---

## ✍️ Message Design

Messages are:

- Specific (real numbers, % conversion)  
- Context-aware (lunch/dinner timing)  
- Category-aligned (restaurant, gym, etc.)  
- Action-driven (single clear CTA)  

No fake claims or inflated metrics are used.

---

## 🧩 Category Awareness

Each vertical has tailored messaging tone:

- Restaurant → time-sensitive decisions  
- Dentist → trust & hygiene  
- Gym → consistency & motivation  
- Salon → visual appeal  
- Pharmacy → speed & reliability  

---

## 👤 Customer Awareness

If customer context is present:

- Repeat users → familiarity messaging  
- New users → acquisition-focused messaging  

---

## 🔕 Anti-Spam Logic

Prevents repeated messages using:

- Merchant ID  
- Trigger type  
- Action type  
- Time window (30 mins)  

---

## 🧪 Deterministic Behavior

Given the same input:

- Output remains consistent  
- No randomness or LLM dependency  

Designed to pass judge replay scenarios reliably.

---

## 🛠 Tech Stack

- **Language:** Python 3  
- **Framework:** FastAPI (API development)  
- **Server:** Uvicorn (ASGI server)  
- **Architecture:** Rule-based + scoring decision engine  
- **State Management:** In-memory store (dictionary-based)  
- **Deployment:** Render (cloud hosting)  
- **Version Control:** Git + GitHub  

---

## ▶️ Running Locally

```bash
uvicorn app:app --reload
