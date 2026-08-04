import db

def check_answer(user_answer, correct_answer):
    return user_answer.strip().lower() == correct_answer.strip().lower()

def get_feedback(is_correct, correct_answer):
    if is_correct:
        return "✅ Correct! Well done!"
    else:
        return f"❌ Not quite. The correct answer is: {correct_answer}"

def load_sample_math():
    # Add your PDF questions here later
    db.add_question("math", "Solve: 2x + 5 = 15", "5")
    db.add_question("math", "What is 12 * 8?", "96")
    db.add_question("math", "What is the square root of 144?", "12")
