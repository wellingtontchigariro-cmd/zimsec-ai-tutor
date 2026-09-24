import db

# --- For simple tutoring ---
def get_ai_response(user_text):
    user_text = user_text.lower().strip()

    if "hello" in user_text or "hie" in user_text or "hi" in user_text:
        return "Hello! 👋 I am your ZIMSEC O-Level AI Tutor. \n\nSend me a question from Maths, Science, English, etc. Or type *quiz math* to start a quiz."

    if "quiz math" in user_text:
        q = db.get_random_question("math")
        if q:
            # q format: (id, subject, question, answer)
            return f"📝 QUIZ: {q[2]}\n\nReply with your answer."
        else:
            db.add_question("math", "Solve: 2x + 5 = 15", "5")
            return "📝 QUIZ: Solve: 2x + 5 = 15"

    # For now, simple answer checking if they just sent a number
    # Later we will make this smarter
    return f"You said: '{user_text}'\n\nI am your O-Level tutor. Ask me any question or type *quiz math*."

# --- Your old functions, keep them ---
def check_answer(user_answer, correct_answer):
    return user_answer.strip().lower() == correct_answer.strip().lower()

def get_feedback(is_correct, correct_answer):
    if is_correct:
        return "✅ Correct! Well done!"
    else:
        return f"❌ Not quite. The correct answer is: {correct_answer}"

def load_sample_math():
    db.add_question("math", "Solve: 2x + 5 = 15", "5")
    db.add_question("math", "What is 12 * 8?", "96")
    db.add_question("math", "What is the square root of 144?", "12")
