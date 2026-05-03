from core.intent import detect_intent
from core.actions import handle_action

def process_message(user_input, state={}):
    intent = detect_intent(user_input)
    result = handle_action(intent, user_input, state)
    return result


if __name__ == "__main__":
    state = {}

    while True:
        user_input = input("User: ")
        response = process_message(user_input, state)
        print("Bot:", response["response"])

        if response["action"] == "end":
            break