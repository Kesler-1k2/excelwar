# ===============================================================
# EXCEL LEARNING STUDIO - EXTENDED EDITION (~1000 LINE PROJECT)
# ===============================================================

import streamlit as st
import pandas as pd
import numpy as np
import random
import math
import time
from datetime import datetime

# ===============================================================
# PAGE CONFIG
# ===============================================================
st.set_page_config(
    page_title="Excel Learning Studio Pro",
    page_icon="📊",
    layout="wide"
)

# ===============================================================
# GLOBAL CONSTANTS
# ===============================================================

APP_VERSION = "2.0"
XP_PER_LESSON = 50

# ===============================================================
# SESSION STATE INITIALIZATION
# ===============================================================

def init_session():

    if "student_name" not in st.session_state:
        st.session_state.student_name = "Guest"

    if "xp" not in st.session_state:
        st.session_state.xp = 0

    if "level" not in st.session_state:
        st.session_state.level = 1

    if "badges" not in st.session_state:
        st.session_state.badges = []

    if "lesson_completion" not in st.session_state:
        st.session_state.lesson_completion = {
            "Lesson 1": False,
            "Lesson 2": False,
            "Lesson 3": False
        }

    if "quiz_scores" not in st.session_state:
        st.session_state.quiz_scores = {}

    if "activity_log" not in st.session_state:
        st.session_state.activity_log = []

init_session()

# ===============================================================
# LOGGING SYSTEM
# ===============================================================

def log_activity(action):
    st.session_state.activity_log.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "action": action
    })

# ===============================================================
# LEVEL SYSTEM
# ===============================================================

def update_level():
    st.session_state.level = 1 + (st.session_state.xp // 150)

# ===============================================================
# BADGE SYSTEM
# ===============================================================

def award_badge(badge_name):
    if badge_name not in st.session_state.badges:
        st.session_state.badges.append(badge_name)

# ===============================================================
# SIDEBAR PROFILE
# ===============================================================

st.sidebar.title("👤 Student Profile")

name = st.sidebar.text_input("Enter Name", st.session_state.student_name)
st.session_state.student_name = name

st.sidebar.write(f"XP: {st.session_state.xp}")
st.sidebar.write(f"Level: {st.session_state.level}")

st.sidebar.write("Badges:")
for badge in st.session_state.badges:
    st.sidebar.write(f"🏅 {badge}")

# ===============================================================
# AI FUNCTION DATABASE
# ===============================================================

AI_FUNCTIONS = {
    "SUM": "Adds numbers together across selected cells.",
    "AVERAGE": "Calculates the mean value.",
    "MIN": "Returns the smallest number.",
    "MAX": "Returns the largest number.",
    "COUNT": "Counts numerical cells.",
    "COUNTA": "Counts non-empty cells.",
    "IF": "Returns value depending on logical test.",
    "VLOOKUP": "Searches vertically in table.",
    "HLOOKUP": "Searches horizontally.",
    "ROUND": "Rounds number to specified digits.",
    "TODAY": "Returns current date.",
    "LEN": "Counts characters in text.",
    "LEFT": "Extracts text from left.",
    "RIGHT": "Extracts text from right.",
    "CONCAT": "Joins text values."
}

# ===============================================================
# AI HELPER PANEL
# ===============================================================

st.sidebar.title("🤖 Excel AI Tutor")

func_choice = st.sidebar.selectbox(
    "Select Excel Function",
    list(AI_FUNCTIONS.keys())
)

st.sidebar.info(AI_FUNCTIONS[func_choice])

# ===============================================================
# FORMULA SIMULATOR
# ===============================================================

def simulate_formula(formula, data):

    try:
        if formula == "SUM":
            return np.sum(data)

        if formula == "AVERAGE":
            return np.mean(data)

        if formula == "MIN":
            return np.min(data)

        if formula == "MAX":
            return np.max(data)

        return "Unsupported Formula"

    except:
        return "Error in calculation"

# ===============================================================
# DATASET GENERATORS
# ===============================================================

def generate_student_scores():

    names = ["Alex","Ben","Chloe","Daniel","Emma","Felix","Grace","Hannah"]

    df = pd.DataFrame({
        "Name": names,
        "Math": np.random.randint(60,100,len(names)),
        "Science": np.random.randint(60,100,len(names)),
        "English": np.random.randint(60,100,len(names))
    })

    return df

# ===============================================================
# MINICEXCEL BUILDER
# ===============================================================

def mini_excel(title):

    st.subheader(title)

    rows = st.slider("Rows", 3, 20, 5)
    cols = st.slider("Columns", 3, 10, 5)

    df = pd.DataFrame(
        np.random.randint(0,50,(rows,cols)),
        columns=[f"Col {i+1}" for i in range(cols)]
    )

    edited = st.data_editor(df, num_rows="dynamic")

    return edited

# ===============================================================
# CHART LAB
# ===============================================================

def chart_lab(df):

    st.subheader("📊 Chart Lab")

    chart_type = st.selectbox("Chart Type", ["Bar","Line","Area"])

    if chart_type == "Bar":
        st.bar_chart(df)

    elif chart_type == "Line":
        st.line_chart(df)

    elif chart_type == "Area":
        st.area_chart(df)

# ===============================================================
# WORKSHEET GENERATOR
# ===============================================================

def worksheet_generator():

    st.subheader("📄 Worksheet Generator")

    difficulty = st.selectbox("Difficulty", ["Easy","Medium","Hard"])

    if difficulty == "Easy":
        numbers = np.random.randint(1,20,5)

    elif difficulty == "Medium":
        numbers = np.random.randint(1,100,8)

    else:
        numbers = np.random.randint(1,500,12)

    st.write("Use SUM on this dataset:")
    st.write(numbers)

# ===============================================================
# QUIZ ENGINE
# ===============================================================

def run_quiz(lesson_name, question, options, correct):

    answer = st.radio(question, options)

    if st.button(f"Submit {lesson_name} Quiz"):

        if answer == correct:
            st.success("Correct!")
            st.session_state.xp += 20
            award_badge("Quiz Master")
            log_activity(f"{lesson_name} Quiz Passed")
        else:
            st.error("Try Again")

        update_level()

# ===============================================================
# LESSON COMPLETION
# ===============================================================

def complete_lesson(name):

    if not st.session_state.lesson_completion[name]:

        st.session_state.lesson_completion[name] = True
        st.session_state.xp += XP_PER_LESSON
        award_badge("Lesson Completed")
        update_level()

# ===============================================================
# FILE UPLOAD SANDBOX
# ===============================================================

def upload_excel():

    st.subheader("📂 Upload Excel File")

    file = st.file_uploader("Upload CSV or Excel", type=["csv","xlsx"])

    if file:

        try:
            df = pd.read_csv(file)
        except:
            df = pd.read_excel(file)

        st.dataframe(df)
        chart_lab(df.select_dtypes(include=np.number))

# ===============================================================
# TEACHER DASHBOARD
# ===============================================================

def teacher_dashboard():

    st.header("👩‍🏫 Teacher Analytics")

    st.write("Lesson Completion")
    st.write(st.session_state.lesson_completion)

    st.write("XP:", st.session_state.xp)
    st.write("Level:", st.session_state.level)

    st.subheader("Activity Log")
    st.dataframe(pd.DataFrame(st.session_state.activity_log))

# ===============================================================
# MAIN NAVIGATION
# ===============================================================

st.title("📊 Excel Learning Studio Pro")

mode = st.radio("Mode", ["Student","Teacher"])

tabs = st.tabs([
    "Lesson 1",
    "Lesson 2",
    "Lesson 3",
    "Chart Lab",
    "Worksheet Lab",
    "Upload Lab"
])

# ===============================================================
# LESSON 1
# ===============================================================

with tabs[0]:

    st.header("Lesson 1 - Excel Basics")

    with st.expander("📘 Teaching"):
        st.write("""
        Excel stores data in rows and columns.
        Cells hold individual values.

        Basic Formulas:
        SUM, AVERAGE, MIN, MAX
        """)

    practice_df = mini_excel("🧪 MiniExcel Practice")

    st.subheader("🔬 Formula Simulator")

    selected = st.selectbox("Choose Formula", ["SUM","AVERAGE","MIN","MAX"])
    result = simulate_formula(selected, practice_df.values.flatten())

    st.write("Result:", result)

    run_quiz(
        "Lesson 1",
        "Which formula adds numbers?",
        ["SUM","IF","LEN"],
        "SUM"
    )

    if st.button("Complete Lesson 1"):
        complete_lesson("Lesson 1")

# ===============================================================
# LESSON 2
# ===============================================================

with tabs[1]:

    st.header("Lesson 2 - Sorting & Filtering")

    with st.expander("📘 Teaching"):
        st.write("""
        Sorting arranges values.
        Filtering hides unwanted data.
        """)

    df = mini_excel("MiniExcel Sorting Lab")

    if st.checkbox("Sort Column 1"):
        st.dataframe(df.sort_values("Col 1"))

    run_quiz(
        "Lesson 2",
        "Filtering does what?",
        ["Deletes Data","Shows Selected Data","Changes Numbers"],
        "Shows Selected Data"
    )

    if st.button("Complete Lesson 2"):
        complete_lesson("Lesson 2")

# ===============================================================
# LESSON 3
# ===============================================================

with tabs[2]:

    st.header("Lesson 3 - Charts")

    with st.expander("📘 Teaching"):
        st.write("""
        Charts help visualise patterns.
        Bar → Compare
        Line → Trends
        Pie → Proportions
        """)

    df = mini_excel("MiniExcel Chart Lab")
    chart_lab(df)

    run_quiz(
        "Lesson 3",
        "Which chart shows trends?",
        ["Line","Pie","Scatter"],
        "Line"
    )

    if st.button("Complete Lesson 3"):
        complete_lesson("Lesson 3")

# ===============================================================
# EXTRA LABS
# ===============================================================

with tabs[3]:
    st.header("📊 Free Chart Lab")
    df = generate_student_scores()
    st.dataframe(df)
    chart_lab(df.set_index("Name"))

with tabs[4]:
    worksheet_generator()

with tabs[5]:
    upload_excel()

# ===============================================================
# TEACHER MODE
# ===============================================================

if mode == "Teacher":
    teacher_dashboard()

# ===============================================================
# FOOTER
# ===============================================================

st.markdown("---")
st.caption(f"Excel Learning Studio Pro v{APP_VERSION}")