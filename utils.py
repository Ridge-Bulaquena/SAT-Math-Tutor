import json
import random
from datetime import datetime

def load_questions():
    """Load questions from JSON file"""
    try:
        with open("questions.json", "r") as f:
            questions = json.load(f)["questions"]
            print(f"Loaded {len(questions)} questions")  # Debug log
            return questions
    except Exception as e:
        print(f"Error loading questions: {e}")  # Debug log
        return []

def get_filtered_questions(questions, topic=None, difficulty=None):
    """Filter questions by topic and difficulty"""
    if not questions:
        print("Warning: No questions loaded")
        return []
        
    filtered = questions
    print(f"Initial questions count: {len(filtered)}")
    
    if topic and topic != "All Topics":
        filtered = [q for q in filtered if q["topic"].lower() == topic.lower()]
        print(f"After topic filter '{topic}': {len(filtered)}")
        if not filtered:
            print(f"No questions found for topic: {topic}")
            return []
            
    if difficulty and difficulty != "All Difficulties":
        filtered = [q for q in filtered if q["difficulty"].lower() == difficulty.lower()]
        print(f"After difficulty filter '{difficulty}': {len(filtered)}")
        if not filtered:
            print(f"No questions found for difficulty: {difficulty}")
            return []
            
    return filtered

def get_topics(questions):
    """Get unique topics from questions"""
    return sorted(list(set(q["topic"] for q in questions)))

def get_difficulties(questions):
    """Get unique difficulty levels from questions"""
    return sorted(list(set(q["difficulty"] for q in questions)))

def save_attempt(history, question, student_answer, is_correct):
    """Save question attempt to history"""
    history.append({
        "timestamp": datetime.now().isoformat(),
        "question_id": question["id"],
        "topic": question["topic"],
        "difficulty": question["difficulty"],
        "correct": is_correct,
        "student_answer": student_answer
    })
    return history