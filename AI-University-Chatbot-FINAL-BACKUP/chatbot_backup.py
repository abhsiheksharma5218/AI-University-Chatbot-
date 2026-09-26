from university_data import UNIVERSITY_DATA


def get_response(user_message):
    user_message = user_message.lower().strip()

    if not user_message:
        return "Please type your question."


    # Check greetings first
    greeting_data = UNIVERSITY_DATA["greeting"]

    for keyword in greeting_data["keywords"]:
        if keyword in user_message:
            return greeting_data["response"]


    # Check all university topics
    for topic, data in UNIVERSITY_DATA.items():

        if topic == "greeting":
            continue

        for keyword in data["keywords"]:

            if keyword in user_message:
                return data["response"]


    # Smart fallback response
    return """
I'm sorry, I couldn't understand your question. 🤔

You can ask me about:

🎓 Admission
📚 Courses
💻 ECE
💰 Fees
💼 Placements
🏠 Hostel
📖 Library
📍 Contact

Example:
"What is the admission process?"
"""