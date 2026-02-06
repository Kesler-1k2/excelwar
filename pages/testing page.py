import streamlit as st
import pandas as pd

st.set_page_config(page_title="Excel Learning App", page_icon="📊")

# -------------------------
# Session State (Progress Tracking)
# -------------------------
if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = {"Lesson 1": 0, "Lesson 2": 0, "Lesson 3": 0}

# -------------------------
# Mode Selection
# -------------------------
mode = st.sidebar.selectbox("Select Mode", ["Student", "Teacher"])

st.title("📊 Excel Learning App")

# -------------------------
# Example Dataset
# -------------------------
data = pd.DataFrame({
    "Student": ["Alex", "Ben", "Chloe", "Daniel", "Emma"],
    "Math": [78, 85, 92, 66, 88],
    "Science": [82, 79, 95, 70, 90]
})

# -------------------------
# Download Dataset
# -------------------------
csv = data.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    "Download Practice Dataset",
    csv,
    "excel_practice_data.csv",
    "text/csv"
)

# -------------------------
# Tabs for Lessons
# -------------------------
lesson1, lesson2, lesson3 = st.tabs(["Lesson 1", "Lesson 2", "Lesson 3"])

# =====================================================
# LESSON 1
# =====================================================
with lesson1:
    st.header("Lesson 1: Introduction to Excel")

    st.write("""
    Learn Excel basics, interface navigation, data entry, and formulas.
    """)

    st.subheader("Example Dataset")
    st.dataframe(data)

    # Quiz
    st.subheader("Quiz")

    q1 = st.radio(
        "Which formula adds numbers together?",
        ["AVERAGE", "SUM", "MAX"],
        key="l1q1"
    )

    if st.button("Submit Lesson 1 Quiz"):
        score = 0
        if q1 == "SUM":
            score += 1

        st.session_state.quiz_scores["Lesson 1"] = score
        st.success(f"Score: {score}/1")


# =====================================================
# LESSON 2
# =====================================================
with lesson2:
    st.header("Lesson 2: Data Organisation")

    st.write("""
    Learn sorting, filtering, and conditional formatting.
    """)

    st.subheader("Try Sorting Data")

    sorted_data = st.checkbox("Sort by Math Score")
    if sorted_data:
        st.dataframe(data.sort_values("Math"))

    # Quiz
    st.subheader("Quiz")

    q2 = st.radio(
        "What does filtering do?",
        [
            "Deletes data",
            "Shows selected data only",
            "Changes data values"
        ],
        key="l2q1"
    )

    if st.button("Submit Lesson 2 Quiz"):
        score = 0
        if q2 == "Shows selected data only":
            score += 1

        st.session_state.quiz_scores["Lesson 2"] = score
        st.success(f"Score: {score}/1")


# =====================================================
# LESSON 3
# =====================================================
with lesson3:
    st.header("Lesson 3: Charts & Projects")

    st.write("Learn how to create charts from data.")

    if st.button("Generate Chart"):
        st.bar_chart(data.set_index("Student"))

    # Quiz
    st.subheader("Quiz")

    q3 = st.radio(
        "Which chart is best for showing proportions?",
        ["Pie Chart", "Line Chart", "Scatter Plot"],
        key="l3q1"
    )

    if st.button("Submit Lesson 3 Quiz"):
        score = 0
        if q3 == "Pie Chart":
            score += 1

        st.session_state.quiz_scores["Lesson 3"] = score
        st.success(f"Score: {score}/1")


# =====================================================
# PROGRESS TRACKING
# =====================================================
st.sidebar.subheader("📈 Progress")

progress_total = sum(st.session_state.quiz_scores.values())
st.sidebar.write(f"Total Score: {progress_total}/3")

# =====================================================
# TEACHER MODE
# =====================================================
if mode == "Teacher":
    st.sidebar.subheader("👩‍🏫 Teacher Dashboard")

    st.sidebar.write("Quiz Scores:")
    st.sidebar.write(st.session_state.quiz_scores)

    st.sidebar.write("Dataset Preview:")
    st.sidebar.dataframe(data)