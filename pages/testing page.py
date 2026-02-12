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
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(page_title="Excel Learning Studio", page_icon="📊", layout="wide")

APP_VERSION = "3.0"
XP_PER_LESSON = 50

# ------------------------------------------------
# SESSION INIT
# ------------------------------------------------
def init_session():
    defaults = {
        "xp": 0,
        "level": 1,
        "completed": {"Lesson 1": False, "Lesson 2": False, "Lesson 3": False},
        "log": []
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ------------------------------------------------
# LOGGING
# ------------------------------------------------
def log(msg):
    st.session_state.log.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "event": msg
    })

# ------------------------------------------------
# LEVEL SYSTEM
# ------------------------------------------------
def update_level():
    st.session_state.level = 1 + st.session_state.xp // 150

# ------------------------------------------------
# AI FUNCTION DATABASE (EXPANDED)
# ------------------------------------------------
AI_FUNCTIONS = {

    "SUM": {
        "desc": "Adds numbers together from selected cells.",
        "syntax": "=SUM(A1:A5)",
        "example": "Adds values from A1 to A5 to get total marks."
    },

    "AVERAGE": {
        "desc": "Finds the average value of numbers.",
        "syntax": "=AVERAGE(A1:A5)",
        "example": "Used to calculate average student score."
    },

    "MIN": {
        "desc": "Returns the smallest number in a dataset.",
        "syntax": "=MIN(A1:A5)",
        "example": "Finds lowest test score."
    },

    "MAX": {
        "desc": "Returns the largest number in a dataset.",
        "syntax": "=MAX(A1:A5)",
        "example": "Finds highest test score."
    },

    "COUNT": {
        "desc": "Counts number of numeric cells.",
        "syntax": "=COUNT(A1:A5)",
        "example": "Counts how many students have marks."
    },

    "IF": {
        "desc": "Performs logical testing.",
        "syntax": '=IF(A1>50,"Pass","Fail")',
        "example": "Checks whether student passed."
    }
}

# ------------------------------------------------
# SIDEBAR AI TUTOR
# ------------------------------------------------
st.sidebar.title("🤖 Excel AI Tutor")

func = st.sidebar.selectbox("Choose Function", list(AI_FUNCTIONS.keys()))

st.sidebar.write("### Description")
st.sidebar.info(AI_FUNCTIONS[func]["desc"])

st.sidebar.write("### Syntax")
st.sidebar.code(AI_FUNCTIONS[func]["syntax"])

st.sidebar.write("### Example")
st.sidebar.success(AI_FUNCTIONS[func]["example"])

# ------------------------------------------------
# MINICEXCEL BUILDER
# ------------------------------------------------
def mini_excel(key):

    rows = st.slider("Rows", 3, 15, 5, key=f"{key}_rows")
    cols = st.slider("Columns", 3, 8, 5, key=f"{key}_cols")

    df = pd.DataFrame(
        np.random.randint(1, 100, (rows, cols)),
        columns=[f"Col {i+1}" for i in range(cols)]
    )

    edited = st.data_editor(df, key=f"{key}_editor")
    return edited

# ------------------------------------------------
# SAFE FORMULA SIMULATION
# ------------------------------------------------
def simulate_formula(formula, values):

    try:
        arr = np.array(values).astype(float)

        if arr.size == 0:
            return "No data available"

        if formula == "SUM":
            return arr.sum()

        if formula == "AVERAGE":
            return arr.mean()

        if formula == "MIN":
            return arr.min()

        if formula == "MAX":
            return arr.max()

        if formula == "COUNT":
            return len(arr)

        return "Unsupported"

    except:
        return "Invalid data"

# ------------------------------------------------
# QUIZ ENGINE
# ------------------------------------------------
def quiz(q, options, answer, key):

    user = st.radio(q, options, key=f"{key}_radio")

    if st.button("Submit Quiz", key=f"{key}_btn"):

        if user == answer:
            st.success("Correct!")
            st.session_state.xp += 20
            update_level()
        else:
            st.error("Incorrect")

# ------------------------------------------------
# LESSON COMPLETION
# ------------------------------------------------
def complete_lesson(name, key):

    if st.button("Complete Lesson", key=key):

        if not st.session_state.completed[name]:
            st.session_state.completed[name] = True
            st.session_state.xp += XP_PER_LESSON
            update_level()
            st.success("Lesson Completed!")

# ------------------------------------------------
# MAIN UI
# ------------------------------------------------
st.title("📊 Excel Learning Studio")

st.write(f"XP: {st.session_state.xp} | Level: {st.session_state.level}")

tabs = st.tabs(["Lesson 1", "Lesson 2", "Lesson 3", "Teacher Dashboard"])

# =================================================
# LESSON 1 (VERY DETAILED)
# =================================================
with tabs[0]:

    st.header("Lesson 1 — Excel Basics & Mathematical Functions")

    with st.expander("📘 Teaching Section", True):

        st.markdown("""
### What is Excel?

Excel is a spreadsheet software used to organise, calculate, and analyse data.

### Understanding Structure
- Rows run horizontally
- Columns run vertically
- Cells store information

### Function: SUM
SUM adds values together.

Used when:
- Calculating totals
- Adding expenses
- Finding total scores

### Function: AVERAGE
Calculates mean value.

Used when:
- Finding average grades
- Analysing performance

### Function: MIN
Finds smallest value.

### Function: MAX
Finds largest value
""")

    st.subheader("🧪 Guided Practice")

    df = mini_excel("l1")

    formula = st.selectbox("Choose Function", ["SUM", "AVERAGE", "MIN", "MAX"], key="l1_formula")

    result = simulate_formula(formula, df.values.flatten())

    st.write("Result:", result)

    quiz(
        "Which function finds average?",
        ["SUM", "AVERAGE", "MIN"],
        "AVERAGE",
        "l1_quiz"
    )

    complete_lesson("Lesson 1", "l1_complete")

# =================================================
# LESSON 2 (VERY DETAILED)
# =================================================
with tabs[1]:

    st.header("Lesson 2 — Sorting, Filtering & Data Organisation")

    with st.expander("📘 Teaching Section", True):

        st.markdown("""
### Sorting
Sorting arranges information in order.

Examples:
- Alphabetical sorting
- Sorting marks from highest to lowest

### Filtering
Filtering shows only selected data.

Example:
- Show only students who passed

### Why Organisation Matters
- Makes analysis easier
- Helps find patterns
- Helps decision making
""")

    df2 = mini_excel("l2")

    if "Col 1" in df2.columns:
        if st.checkbox("Sort Column 1", key="l2_sort"):
            st.dataframe(df2.sort_values("Col 1"))

    quiz(
        "Filtering does what?",
        ["Deletes data", "Shows selected data", "Changes numbers"],
        "Shows selected data",
        "l2_quiz"
    )

    complete_lesson("Lesson 2", "l2_complete")

# =================================================
# LESSON 3 (VERY DETAILED)
# =================================================
with tabs[2]:

    st.header("Lesson 3 — Charts & Visual Data Analysis")

    with st.expander("📘 Teaching Section", True):

        st.markdown("""
### Why Charts Are Important
Charts help people understand data visually.

### Bar Chart
Used for comparing categories.

### Line Chart
Used for trends over time.

### Pie Chart
Used for showing proportions.

### Good Chart Practices
- Always label axes
- Use correct chart type
- Keep charts simple
""")

    df3 = mini_excel("l3")

    numeric_df = df3.select_dtypes(include=np.number)

    if not numeric_df.empty:
        chart = st.selectbox("Chart Type", ["Bar", "Line", "Area"], key="l3_chart")

        if chart == "Bar":
            st.bar_chart(numeric_df)
        elif chart == "Line":
            st.line_chart(numeric_df)
        else:
            st.area_chart(numeric_df)
    else:
        st.warning("No numeric data")

    quiz(
        "Which chart shows trends?",
        ["Line", "Pie", "Bar"],
        "Line",
        "l3_quiz"
    )

    complete_lesson("Lesson 3", "l3_complete")

# =================================================
# TEACHER DASHBOARD
# =================================================
with tabs[3]:

    st.header("Teacher Dashboard")

    st.write("Lesson Completion:")
    st.write(st.session_state.completed)

    st.subheader("Activity Log")
    if st.session_state.log:
        st.dataframe(pd.DataFrame(st.session_state.log))
    else:
        st.info("No activity yet")

# ------------------------------------------------
# FOOTER
# ------------------------------------------------
st.markdown("---")
st.caption(f"Version {APP_VERSION}")