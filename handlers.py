from whatsapp_api import send_message
import db
import ai_logic

# Simple memory for who is doing quiz: phone -> {answer}
user_sessions = {}

def handle_message(data, access_token, phone_number_id):
    try:
        # Check if data has WhatsApp messages
        if "entry" not in data:
            return
        entry = data["entry"][0]
        if "changes" not in entry:
            return
        value = entry["changes"][0].get("value", {})
        if "messages" not in value:
            return

        msg = value["messages"][0]
        phone = msg.get("from")
        text_body = msg.get("text", {}).get("body", "")

        if not phone or not text_body:
            return

        text = text_body.lower().strip()
        print(f"From {phone}: {text}")

        db.add_user(phone)

        # If user is answering a quiz
        if phone in user_sessions and "current_a" in user_sessions[phone]:
            correct_ans = user_sessions[phone]["current_a"]
            is_correct = ai_logic.check_answer(text, correct_ans)
            feedback = ai_logic.get_feedback(is_correct, correct_ans)
            if is_correct:
                db.update_score(phone, 10)
                feedback += f"\nYour score: {db.get_score(phone)}"
            send_message(phone, feedback, access_token, phone_number_id)
            user_sessions.pop(phone, None)
            return

        # Commands
        if text in ["hi", "hello", "hie", "start"]:
            send_message(phone, "Hi! I'm your ZIMSEC O-Level AI Tutor 📚\n\nType *quiz math* to start Maths quiz\nOr ask me any O-Level question.", access_token, phone_number_id)

        elif text.startswith("quiz"):
            parts = text.split()
            subject = parts[1] if len(parts) > 1 else "math"
            q = db.get_random_question(subject)
            if q:
                # q = (id, subject, question, answer)
                user_sessions[phone] = {"current_a": q[3], "current_q": q[2]}
                send_message(phone, f"📝 QUIZ ({subject}): {q[2]}", access_token, phone_number_id)
            else:
                # Load samples if empty
                ai_logic.load_sample_math()
                q = db.get_random_question(subject)
                if q:
                    user_sessions[phone] = {"current_a": q[3], "current_q": q[2]}
                    send_message(phone, f"📝 QUIZ ({subject}): {q[2]}", access_token, phone_number_id)
                else:
                    send_message(phone, f"No questions for {subject} yet.", access_token, phone_number_id)

        else:
            # Normal tutor chat
            reply = ai_logic.get_ai_response(text_body)
            send_message(phone, reply, access_token, phone_number_id)

    except Exception as e:
        print(f"Error in handle_message: {e}")
