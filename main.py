import streamlit as st
import json
import random
from streamlit_lottie import st_lottie
from utils import (
    load_questions,
    get_filtered_questions,
    get_topics,
    get_difficulties,
    save_attempt
)
from openai_helper import analyze_answer
from analytics import (
    calculate_performance_metrics,
    create_progress_chart,
    create_topic_performance_chart
)

# Initialize session state
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "history" not in st.session_state:
    st.session_state.history = []
if "questions" not in st.session_state:
    st.session_state.questions = load_questions()

# Page configuration
st.set_page_config(page_title="SAT Math Tutor", layout="wide")

# Load and display the Lottie animation
def load_lottie_file(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)

# Title and description with Lottie animation
title_col1, title_col2 = st.columns([0.15, 0.85])
with title_col1:
    lottie_animation = load_lottie_file('attached_assets/92435.json')
    st_lottie(lottie_animation, height=100, key="title_animation")
with title_col2:
    st.title("SAT Math Tutor")

st.markdown("""
    Welcome to your personalized SAT Math tutor! Practice questions, get instant feedback,
    and track your progress with AI-powered explanations.
""")

# Sidebar for navigation and filters
with st.sidebar:
    side_col1, side_col2 = st.columns([0.3, 0.7])
    with side_col1:
        lottie_animation = load_lottie_file('attached_assets/92435.json')
        st_lottie(lottie_animation, height=60, key="sidebar_animation")
    with side_col2:
        st.header("Study Options")
    
    # Topic and difficulty selection
    selected_topic = st.selectbox(
        "Select Topic",
        ["All Topics"] + get_topics(st.session_state.questions)
    )
    
    selected_difficulty = st.selectbox(
        "Select Difficulty",
        ["All Difficulties"] + get_difficulties(st.session_state.questions)
    )
    
    # Filter questions
    topic = None if selected_topic == "All Topics" else selected_topic
    difficulty = None if selected_difficulty == "All Difficulties" else selected_difficulty
    
    if st.button("New Question"):
        filtered_questions = get_filtered_questions(
            st.session_state.questions,
            topic,
            difficulty
        )
        if filtered_questions:
            st.session_state.current_question = random.choice(filtered_questions)
        else:
            st.error(f"No questions available for Topic: {selected_topic}, Difficulty: {selected_difficulty}. Try different filters.")
            available_topics = get_topics(st.session_state.questions)
            available_difficulties = get_difficulties(st.session_state.questions)
            st.info(f"Available topics: {', '.join(available_topics)}\nAvailable difficulties: {', '.join(available_difficulties)}")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    if st.session_state.current_question:
        st.subheader("Question")
        st.markdown(f"""
            **Topic:** {st.session_state.current_question['topic']}  
            **Difficulty:** {st.session_state.current_question['difficulty']}
            
            {st.session_state.current_question['question']}
        """)
        
        # Answer input
        user_answer = st.radio(
            "Select your answer:",
            st.session_state.current_question["options"],
            key="answer"
        )
        
        if st.button("Submit Answer"):
            # Check answer and get AI analysis
            analysis = analyze_answer(
                st.session_state.current_question["question"],
                user_answer,
                st.session_state.current_question["correct_answer"]
            )
            
            # Save attempt
            st.session_state.history = save_attempt(
                st.session_state.history,
                st.session_state.current_question,
                user_answer,
                analysis["is_correct"]
            )
            
            # Display feedback
            if analysis["is_correct"]:
                st.success("Correct! 🎉")
            else:
                st.error("Incorrect. Keep practicing!")
            
            with st.expander("See Solution"):
                st.markdown(st.session_state.current_question["solution"])
                st.markdown("**AI Explanation:**")
                st.markdown(analysis["explanation"])
                if not analysis["is_correct"]:
                    st.markdown("**Tips for Improvement:**")
                    st.markdown(analysis["improvement_tips"])

with col2:
    st.subheader("Your Progress")
    if st.session_state.history:
        metrics = calculate_performance_metrics(st.session_state.history)

        # Animated metrics display
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric(
                "Questions Attempted",
                metrics["total_questions"],
                delta=1 if len(st.session_state.history) > 0 else None,
                delta_color="normal"
            )
        with col_b:
            st.metric(
                "Correct Answers",
                metrics["correct_answers"],
                delta=1 if st.session_state.history and st.session_state.history[-1]["correct"] else None,
                delta_color="normal"
            )
        with col_c:
            previous_accuracy = 0 if len(st.session_state.history) <= 1 else \
                round((metrics["correct_answers"] - (1 if st.session_state.history[-1]["correct"] else 0)) / 
                      (len(st.session_state.history) - 1) * 100, 2)
            st.metric(
                "Accuracy",
                f"{metrics['accuracy']}%",
                delta=f"{metrics['accuracy'] - previous_accuracy:.1f}%" if len(st.session_state.history) > 1 else None,
                delta_color="normal"
            )

        # Animated progress charts
        st.plotly_chart(create_progress_chart(st.session_state.history), use_container_width=True)
        st.plotly_chart(create_topic_performance_chart(st.session_state.history), use_container_width=True)
    else:
        st.info("Start answering questions to see your progress!")

# Footer
st.markdown("---")
st.markdown("""
    💡 **Tip:** Regular practice is key to improving your SAT Math score.
    Try questions from different topics and difficulty levels to build well-rounded skills.
""")
