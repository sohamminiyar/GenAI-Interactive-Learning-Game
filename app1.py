import streamlit as st
import os
from dotenv import load_dotenv
from db import create_tables, update_user_score, get_user_score, get_badges, assign_badge
from recommendation import generate_questions
import matplotlib.pyplot as plt
import random


# Set page config FIRST
st.set_page_config(page_title="GenAI Adaptive Aptitude Game", layout="wide")

# Load environment variables
load_dotenv()

# Initialize database tables
create_tables()

# Title
st.title("🎮 GenAI Adaptive Aptitude Game")

# Sidebar
st.sidebar.title("🚀 Progress & Badges")
user_name = st.sidebar.text_input("Enter your name:", "Player")

if "round" not in st.session_state:
    st.session_state.round = 1
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Easy"
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "questions" not in st.session_state:
    st.session_state.questions = []

badges = get_badges(user_name)
st.sidebar.markdown("🏅 **Your Badges:**")
for b in badges:
    st.sidebar.write(f"- {b}")

st.sidebar.markdown(f"🔢 **Current Round:** {st.session_state.round}")
st.sidebar.markdown(f"🎚️ **Current Difficulty:** {st.session_state.difficulty}")

next_difficulty = {
    "Easy": "Medium",
    "Medium": "Hard",
    "Hard": "Hard"
}
prev_difficulty = {
    "Hard": "Medium",
    "Medium": "Easy",
    "Easy": "Easy"
}

# Mixed category logic
categories = ["Verbal", "Logical", "Mathematics"]

if st.button("🚀 Start New Quiz"):
    st.session_state.submitted = False
    st.session_state.questions = []
    st.session_state.round += 1

    for cat in categories:
        qs = generate_questions(cat, st.session_state.difficulty, 3)
        st.session_state.questions.extend(qs[:3])

    # Add one extra random category question
    extra_cat = random.choice(categories)
    st.session_state.questions.append(generate_questions(extra_cat, st.session_state.difficulty, 1)[0])

    random.shuffle(st.session_state.questions)

if st.session_state.questions and not st.session_state.submitted:
    score = 0
    user_answers = []
    correct_answers = []
    categories_list = []

    for idx, q in enumerate(st.session_state.questions):
        st.write(f"**Q{idx + 1}:** {q['question']}")
        answer = st.radio(f"Choose your answer for Q{idx + 1}:", q["options"], key=f"q{idx}")
        user_answers.append(answer)
        correct_answers.append(q["answer"])
        # Smart: store category for later analysis
        if "category" in q:
            categories_list.append(q["category"])
        else:
            categories_list.append(random.choice(categories))

    if st.button("✅ Submit Answers"):
        for i in range(len(user_answers)):
            if user_answers[i].strip().lower() == correct_answers[i].strip().lower():
                score += 1

        st.session_state.submitted = True
        st.write(f"### 🎯 Your Score: {score}/10")

        update_user_score(user_name, score)

        # Difficulty adaptation
        current = st.session_state.difficulty
        if score >= 8:
            st.session_state.difficulty = next_difficulty[current]
            st.success(f"📈 Leveling Up! Next round will be **{st.session_state.difficulty}**.")
        elif score < 4:
            st.session_state.difficulty = prev_difficulty[current]
            st.warning(f"📉 Dropping difficulty. Next round will be **{st.session_state.difficulty}**.")
        else:
            st.info(f"➡️ Staying on **{current}** difficulty.")

        # Badges
        if score == 10:
            assign_badge(user_name, "🏅 Perfect Score!")
        elif score >= 8:
            assign_badge(user_name, "🔥 Pro Gamer!")
        elif score >= 5:
            assign_badge(user_name, "🎯 Good Effort!")

        badges = get_badges(user_name)
        st.sidebar.markdown("🏅 **Your Badges:**")
        for b in badges:
            st.sidebar.write(f"- {b}")

        # Category-wise analysis
        cat_scores = {"Verbal": 0, "Logical": 0, "Mathematics": 0}
        cat_total = {"Verbal": 0, "Logical": 0, "Mathematics": 0}

        for i in range(len(user_answers)):
            cat = categories_list[i]
            cat_total[cat] += 1
            if user_answers[i].strip().lower() == correct_answers[i].strip().lower():
                cat_scores[cat] += 1

        st.subheader("📊 Performance Analysis by Category")
        fig, ax = plt.subplots()
        ax.bar(cat_scores.keys(), cat_scores.values(), color=["#FF6384", "#36A2EB", "#FFCE56"])
        ax.set_ylabel("Correct Answers")
        ax.set_ylim(0, max(cat_total.values()))
        st.pyplot(fig)

        # Button for next test
        st.markdown("### Ready for next round?")
        st.button("🔁 Next Test Round", on_click=lambda: st.session_state.update({"questions": [], "submitted": False}))
else:
    if not st.session_state.questions:
        st.info("👆 Click **Start New Quiz** to begin.")