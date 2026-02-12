from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st

APP_VERSION = "3.1"
XP_PER_LESSON = 50
LEVEL_STEP = 150
LESSON_NAMES = ("Lesson 1", "Lesson 2", "Lesson 3")

AI_FUNCTIONS = {
    "SUM": {
        "desc": "Adds numbers together from selected cells.",
        "syntax": "=SUM(A1:A5)",
        "example": "Use this to calculate total marks.",
    },
    "AVERAGE": {
        "desc": "Calculates the mean value.",
        "syntax": "=AVERAGE(A1:A5)",
        "example": "Use this to find average score.",
    },
    "MIN": {
        "desc": "Returns the smallest number.",
        "syntax": "=MIN(A1:A5)",
        "example": "Use this to find the lowest score.",
    },
    "MAX": {
        "desc": "Returns the largest number.",
        "syntax": "=MAX(A1:A5)",
        "example": "Use this to find the highest score.",
    },
    "COUNT": {
        "desc": "Counts numeric cells in a range.",
        "syntax": "=COUNT(A1:A5)",
        "example": "Use this to count filled numeric marks.",
    },
    "IF": {
        "desc": "Returns one value for true and another for false.",
        "syntax": '=IF(A1>=50, "Pass", "Fail")',
        "example": "Use this to label pass/fail outcomes.",
    },
}

LESSON_NOTES = {
    "Lesson 1": """
### Excel Basics
- Rows run horizontally.
- Columns run vertically.
- Cells store values or formulas.

### Core formulas
- `SUM` for totals
- `AVERAGE` for means
- `MIN` and `MAX` for range checks
""",
    "Lesson 2": """
### Sorting and Filtering
- Sorting arranges data by a chosen order.
- Filtering shows only rows matching conditions.
- Organized data is faster to analyze.
""",
    "Lesson 3": """
### Charts and Visual Analysis
- Bar charts compare categories.
- Line charts show trends over time.
- Area charts emphasize overall magnitude.
""",
}

st.set_page_config(page_title="Excel Learning Studio", page_icon="📊", layout="wide")


def init_session() -> None:
    defaults = {
        "student_name": "Guest",
        "xp": 0,
        "level": 1,
        "completed": {lesson: False for lesson in LESSON_NAMES},
        "badges": [],
        "log": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def log_event(message: str) -> None:
    st.session_state.log.append(
        {
            "time": datetime.now().strftime("%H:%M:%S"),
            "event": message,
        }
    )


def update_level() -> None:
    st.session_state.level = 1 + st.session_state.xp // LEVEL_STEP


def add_xp(amount: int, reason: str) -> None:
    st.session_state.xp += amount
    update_level()
    log_event(f"+{amount} XP ({reason})")


def award_badge(badge_name: str) -> None:
    if badge_name not in st.session_state.badges:
        st.session_state.badges.append(badge_name)
        log_event(f"Badge unlocked: {badge_name}")


def complete_lesson(lesson_name: str, key_prefix: str) -> None:
    if st.button("Complete Lesson", key=f"{key_prefix}_complete"):
        if st.session_state.completed[lesson_name]:
            st.info("You already completed this lesson.")
            return

        st.session_state.completed[lesson_name] = True
        add_xp(XP_PER_LESSON, f"{lesson_name} completion")
        award_badge("Lesson Finisher")
        st.success(f"{lesson_name} completed.")


def mini_excel(key_prefix: str) -> pd.DataFrame:
    rows = st.slider("Rows", min_value=3, max_value=15, value=5, key=f"{key_prefix}_rows")
    cols = st.slider("Columns", min_value=3, max_value=8, value=5, key=f"{key_prefix}_cols")

    dataframe = pd.DataFrame(
        np.random.randint(1, 100, (rows, cols)),
        columns=[f"Col {index + 1}" for index in range(cols)],
    )
    return st.data_editor(dataframe, key=f"{key_prefix}_editor")


def simulate_formula(formula: str, values) -> str | float:
    try:
        numeric_values = np.array(values, dtype=float)
    except (TypeError, ValueError):
        return "Invalid data"

    if numeric_values.size == 0:
        return "No data"

    if formula == "SUM":
        return float(numeric_values.sum())
    if formula == "AVERAGE":
        return float(numeric_values.mean())
    if formula == "MIN":
        return float(numeric_values.min())
    if formula == "MAX":
        return float(numeric_values.max())
    if formula == "COUNT":
        return int(numeric_values.size)

    return "Unsupported formula"


def render_chart_lab(dataframe: pd.DataFrame, key_prefix: str) -> None:
    numeric_df = dataframe.select_dtypes(include=np.number)
    if numeric_df.empty:
        st.warning("No numeric data available for charting.")
        return

    chart_type = st.selectbox("Chart Type", ["Bar", "Line", "Area"], key=f"{key_prefix}_chart")

    if chart_type == "Bar":
        st.bar_chart(numeric_df)
    elif chart_type == "Line":
        st.line_chart(numeric_df)
    else:
        st.area_chart(numeric_df)


def run_quiz(question: str, options: list[str], answer: str, key_prefix: str) -> None:
    selected = st.radio(question, options, key=f"{key_prefix}_radio")
    if st.button("Submit Quiz", key=f"{key_prefix}_submit"):
        if selected == answer:
            add_xp(20, f"{key_prefix} quiz")
            award_badge("Quiz Master")
            st.success("Correct.")
        else:
            st.error("Incorrect. Try again.")


def worksheet_generator() -> None:
    st.subheader("Worksheet Generator")
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

    if difficulty == "Easy":
        numbers = np.random.randint(1, 20, 5)
    elif difficulty == "Medium":
        numbers = np.random.randint(1, 100, 8)
    else:
        numbers = np.random.randint(1, 500, 12)

    st.write("Use `SUM` on this dataset:")
    st.write(numbers)


def upload_lab() -> None:
    st.subheader("Upload Lab")
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

    if uploaded_file is None:
        return

    try:
        dataframe = pd.read_csv(uploaded_file)
    except UnicodeDecodeError:
        dataframe = pd.read_excel(uploaded_file)
    except pd.errors.ParserError:
        dataframe = pd.read_excel(uploaded_file)

    st.dataframe(dataframe)
    render_chart_lab(dataframe, "upload")


def teacher_dashboard() -> None:
    st.header("Teacher Dashboard")
    st.write("Lesson completion:")
    st.json(st.session_state.completed)

    metric_col_1, metric_col_2 = st.columns(2)
    metric_col_1.metric("Total XP", st.session_state.xp)
    metric_col_2.metric("Current Level", st.session_state.level)

    st.subheader("Badges")
    if st.session_state.badges:
        for badge in st.session_state.badges:
            st.write(f"🏅 {badge}")
    else:
        st.info("No badges earned yet.")

    st.subheader("Activity Log")
    if st.session_state.log:
        st.dataframe(pd.DataFrame(st.session_state.log))
    else:
        st.info("No activity recorded yet.")


def render_sidebar() -> None:
    st.sidebar.title("Student Profile")
    name = st.sidebar.text_input("Name", value=st.session_state.student_name)
    if name != st.session_state.student_name:
        st.session_state.student_name = name
        log_event(f"Student name set to {name}")

    st.sidebar.metric("XP", st.session_state.xp)
    st.sidebar.metric("Level", st.session_state.level)

    st.sidebar.write("Badges")
    if st.session_state.badges:
        for badge in st.session_state.badges:
            st.sidebar.write(f"- {badge}")
    else:
        st.sidebar.write("- None")

    st.sidebar.title("Excel AI Tutor")
    function_name = st.sidebar.selectbox("Choose Function", list(AI_FUNCTIONS.keys()))
    details = AI_FUNCTIONS[function_name]
    st.sidebar.info(details["desc"])
    st.sidebar.code(details["syntax"])
    st.sidebar.caption(details["example"])


def render_lesson(lesson_name: str, lesson_key: str) -> None:
    st.header(f"{lesson_name}")
    with st.expander("Teaching Notes", expanded=True):
        st.markdown(LESSON_NOTES[lesson_name])

    dataframe = mini_excel(lesson_key)

    st.subheader("Formula Simulator")
    formula = st.selectbox("Choose Function", ["SUM", "AVERAGE", "MIN", "MAX", "COUNT"], key=f"{lesson_key}_formula")
    result = simulate_formula(formula, dataframe.values.flatten())
    st.write("Result:", result)

    if lesson_name == "Lesson 1":
        run_quiz(
            "Which function adds values together?",
            ["SUM", "IF", "LEN"],
            "SUM",
            "lesson1",
        )
    elif lesson_name == "Lesson 2":
        run_quiz(
            "Filtering does what?",
            ["Deletes data", "Shows selected data", "Changes numbers"],
            "Shows selected data",
            "lesson2",
        )
    else:
        run_quiz(
            "Which chart best shows trends?",
            ["Line", "Pie", "Bar"],
            "Line",
            "lesson3",
        )

    complete_lesson(lesson_name, lesson_key)


def main() -> None:
    init_session()
    render_sidebar()

    st.title("📊 Excel Learning Studio")
    mode = st.radio("Mode", ["Student", "Teacher"], horizontal=True)

    lesson_1_tab, lesson_2_tab, lesson_3_tab, chart_tab, worksheet_tab, upload_tab = st.tabs(
        ["Lesson 1", "Lesson 2", "Lesson 3", "Chart Lab", "Worksheet Lab", "Upload Lab"]
    )

    with lesson_1_tab:
        render_lesson("Lesson 1", "l1")

    with lesson_2_tab:
        render_lesson("Lesson 2", "l2")

    with lesson_3_tab:
        render_lesson("Lesson 3", "l3")

    with chart_tab:
        st.header("Free Chart Lab")
        sample_scores = pd.DataFrame(
            {
                "Name": ["Alex", "Ben", "Chloe", "Daniel", "Emma", "Felix"],
                "Math": np.random.randint(60, 100, 6),
                "Science": np.random.randint(60, 100, 6),
                "English": np.random.randint(60, 100, 6),
            }
        )
        st.dataframe(sample_scores)
        render_chart_lab(sample_scores.set_index("Name"), "free_chart")

    with worksheet_tab:
        worksheet_generator()

    with upload_tab:
        upload_lab()

    if mode == "Teacher":
        teacher_dashboard()

    st.markdown("---")
    st.caption(f"Excel Learning Studio v{APP_VERSION}")


if __name__ == "__main__":
    main()
