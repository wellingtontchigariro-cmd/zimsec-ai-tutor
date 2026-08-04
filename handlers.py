import whatsapp_api, db, ai_logic, os

user_sessions = {} # phone: {subject, current_q, current_a}

async def handle_whatsapp_message(data):
    try:
        entry = data['entry'][0]['changes'][0]['value']
        if 'messages' not in entry:
            return

        msg = entry['messages'][0]
        phone = msg['from']
        text = msg['text']['body'].lower()

        db.add_user(phone)

        if phone not in user_sessions:
            user_sessions[phone] = {}

        if text == "hi" or text == "start":
            await whatsapp_api.send_message(phone, "Hi! I'm your ZIMSEC AI Tutor 📚\nType 'quiz math' to start a math question")

        elif text.startswith("quiz "):
            subject = text.split(" ")[1]
            q = db.get_random_question(subject)
            if q:
                user_sessions[phone] = {"subject": subject, "current_q": q[2], "current_a": q[3]}
                await whatsapp_api.send_message(phone, f"Q: {q[2]}")
            else:
                await whatsapp_api.send_message(phone, f"No questions for {subject} yet. Add some first!")

        elif "current_q" in user_sessions[phone]:
            user_ans = text
            correct_ans = user_sessions[phone]["current_a"]
            is_correct = ai_logic.check_answer(user_ans, correct_ans)
            feedback = ai_logic.get_feedback(is_correct, correct_ans)
            if is_correct:
                db.update_score(phone, 10)
            await whatsapp_api.send_message(phone, feedback)
            user_sessions[phone] = {}

        else:
            await whatsapp_api.send_message(phone, "Type 'quiz math' to start")

    except Exception as e:
        print("Error:", e)
