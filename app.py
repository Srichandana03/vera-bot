from fastapi import FastAPI
import time

app = FastAPI()

store = {}
last_sent = {}

SUPPRESSION_WINDOW = 1800  # 30 min


# ------------------ BASIC ROUTES ------------------

@app.get("/v1/healthz")
def health():
    return {"status": "ok"}


@app.get("/v1/metadata")
def metadata():
    return {"bot_name": "vera-engine", "version": "7.0"}


@app.post("/v1/context")
def context(data: dict):
    store[data["context_id"]] = data["payload"]
    return {"accepted": True}


# ------------------ DECISION ENGINE ------------------

def get_cta(action_type):
    return {
        "push_offer": "Yes, run targeted offer",
        "optimize_existing_offer": "Improve current offer",
        "scale_visibility": "Boost listing visibility",
        "fix_reputation": "Improve listing now",
        "activate_offer": "Create an offer",
        "nudge": "View suggestions"
    }.get(action_type, "Proceed")


def decide_action(category, merchant, trigger):
    perf = merchant.get("performance", {})

    views = perf.get("views", 0)
    orders = perf.get("orders", 0)
    rating = perf.get("rating", 4.5)

    conversion = orders / max(views, 1)

    scores = []

    if rating < 4.0:
        scores.append(("fix_reputation", 10, "Low rating hurting conversions"))

    if trigger.get("type") == "search_spike" and conversion < 0.1:
        if merchant.get("offers"):
            scores.append(("optimize_existing_offer", 9, "Existing offers not converting"))
        else:
            scores.append(("push_offer", 9, "High demand but low conversion"))

    if conversion > 0.15:
        scores.append(("scale_visibility", 8, "Good conversion, scale reach"))

    if not merchant.get("offers"):
        scores.append(("activate_offer", 6, "No active offers"))

    if not scores:
        return {
            "type": "nudge",
            "reason": "No strong signal",
            "cta": "View suggestions"
        }

    best = sorted(scores, key=lambda x: x[1], reverse=True)[0]

    return {
        "type": best[0],
        "reason": best[2],
        "cta": get_cta(best[0])
    }


# ------------------ CATEGORY CONTEXT ------------------

def category_line(category):
    if category == "restaurant":
        return "Food decisions are highly time-sensitive."
    elif category == "dentist":
        return "Patients prioritize trust and hygiene."
    elif category == "gym":
        return "Consistency and motivation drive signups."
    elif category == "salon":
        return "Visual appeal and quick wins drive bookings."
    elif category == "pharmacy":
        return "Customers expect quick and reliable service."
    return ""


# ------------------ MESSAGE ------------------

def generate_message(decision, merchant, trigger, category, customer=None):
    perf = merchant.get("performance", {})

    views = perf.get("views", 0)
    orders = perf.get("orders", 0)

    conversion = (orders / max(views, 1)) * 100
    keyword = trigger.get("keyword", "").lower()
    search_count = trigger.get("count", 100)

    cat_line = category_line(category)

    if "lunch" in keyword:
        offer_text = "₹149 lunch combo"
        timing = "in the next 90 minutes"
        context_line = "Lunch demand is peaking right now."
    elif "dinner" in keyword:
        offer_text = "₹199 dinner special"
        timing = "tonight"
        context_line = "Dinner demand will peak soon."
    else:
        offer_text = "limited-time deal"
        timing = "today"
        context_line = "Demand is active right now."

    customer_line = ""
    if customer:
        relation = customer.get("relationship", "")
        if relation == "repeat":
            customer_line = "Your repeat customers are already familiar with you."
        else:
            customer_line = "You have potential new customers in this demand."

    if decision["type"] == "push_offer":
        return (
            f"{search_count} people nearby searched '{trigger.get('keyword', 'your service')}'. "
            f"You had {views} visits but only {orders} orders "
            f"({round(conversion,1)}% conversion).\n"
            f"You're capturing only a small share of active demand.\n"
            f"{context_line}\n"
            f"{cat_line}\n"
            f"{customer_line}\n"
            f"I recommend running a {offer_text} to improve conversions {timing}. "
            f"Should I go ahead?"
        )

    if decision["type"] == "optimize_existing_offer":
        return (
            f"You’re getting traffic ({views} visits) but only {orders} orders "
            f"({round(conversion,1)}% conversion).\n"
            f"Your current offers aren’t converting effectively.\n"
            f"{cat_line}\n"
            f"I recommend improving your offer structure.\n"
            f"Should I optimize your existing offer?"
        )

    if decision["type"] == "scale_visibility":
        return (
            f"Your conversion rate is strong at {round(conversion,1)}% "
            f"({orders}/{views}).\n"
            f"{cat_line}\n"
            f"I recommend scaling visibility instead of discounting.\n"
            f"Should I boost your listing now?"
        )

    if decision["type"] == "fix_reputation":
        return (
            f"Your rating is limiting customer trust and conversions.\n"
            f"{cat_line}\n"
            f"I recommend improving listing quality and reviews.\n"
            f"Should I help fix your profile?"
        )

    if decision["type"] == "activate_offer":
        return (
            f"You currently don’t have any active offers.\n"
            f"{cat_line}\n"
            f"I recommend launching a simple starter deal.\n"
            f"Should I create one for you?"
        )

    return "Want help improving your performance today?"


# ------------------ SUPPRESSION ------------------

def should_suppress(merchant_id, trigger_type, action_type):
    key = f"{merchant_id}_{trigger_type}_{action_type}"
    now = time.time()

    if key in last_sent:
        if now - last_sent[key] < SUPPRESSION_WINDOW:
            return True

    last_sent[key] = now
    return False


# ------------------ MAIN ENDPOINT ------------------

@app.post("/v1/tick")
def tick(data: dict):
    merchant = store.get(data.get("merchant_id"), {})
    trigger = data.get("trigger", {})
    category = data.get("category", "")
    customer = data.get("customer")

    # ✅ FIX: handle missing merchant properly
    if not merchant:
        return {
            "message": "I need the latest merchant data to make a recommendation.",
            "cta": "Refresh context",
            "send_as": "vera_growth_assistant",
            "suppression_key": "no_context",
            "rationale": "Missing merchant context"
        }

    decision = decide_action(category, merchant, trigger)

    if should_suppress(
        merchant.get("id", "m"),
        trigger.get("type", "t"),
        decision["type"]
    ):
        return {
            "message": "No new update right now.",
            "cta": "None",
            "send_as": "vera_growth_assistant",
            "suppression_key": "suppressed",
            "rationale": "Recently sent similar message"
        }

    message = generate_message(decision, merchant, trigger, category, customer)

    return {
        "message": message,
        "cta": decision["cta"],
        "send_as": "vera_growth_assistant",
        "suppression_key": f"{merchant.get('id','m')}_{trigger.get('type','t')}",
        "rationale": decision["reason"]
    }


@app.post("/v1/reply")
def reply(data: dict):
    return {"message": "Action noted."}