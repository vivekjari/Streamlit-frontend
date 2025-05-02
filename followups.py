import random

def generate_followups(user_input, df):
    generic_questions = [
        "What was the best-performing campaign?",
        "Which day had the highest CTR?",
        "How does sentiment affect conversions?",
        "Can you show me trend over time?",
        "Which ads had high engagement but low conversions?"
    ]
    return random.sample(generic_questions, 3)
