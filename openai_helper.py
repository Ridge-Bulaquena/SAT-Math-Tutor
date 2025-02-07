
import os
import json
import google.generativeai as genai

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def analyze_answer(question, student_answer, correct_answer):
    """Analyze student's answer using Google Gemini Pro API"""
    prompt = f"""
    Analyze this SAT Math question and the student's answer:
    Question: {question}
    Student's Answer: {student_answer}
    Correct Answer: {correct_answer}
    
    Provide feedback in JSON format with the following structure:
    {{
        "is_correct": boolean,
        "explanation": "detailed explanation",
        "improvement_tips": "specific tips for improvement if wrong"
    }}
    """
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.3}
        )
        return json.loads(response.text)
    except Exception as e:
        return {
            "is_correct": student_answer == correct_answer,
            "explanation": "Unable to generate detailed explanation.",
            "improvement_tips": "Please try again later."
        }
