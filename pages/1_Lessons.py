import streamlit as st

LESSONS = {
    "basics": {
        "title": "Lesson 1: Basics of Excel",
        "summary": "Understand cells, rows, columns, and core spreadsheet workflows.",
        "topics": ["Workbook layout", "Entering data", "Basic navigation"],
    },
    "cell_formatting": {
        "title": "Lesson 2: Cell Formatting",
        "summary": "Format data clearly so it is easier to read and present.",
        "topics": ["Number formats", "Alignment", "Fonts and colors"],
    },
    "formulas_functions": {
        "title": "Lesson 3: Formulas and Functions",
        "summary": "Use formulas to calculate and analyze worksheet values.",
        "topics": ["SUM and AVERAGE", "Relative vs absolute references", "Common function patterns"],
    },
}


if "lesson_page" not in st.session_state:
    st.session_state.lesson_page = "main"


def open_lesson(lesson_key: str) -> None:
    st.session_state.lesson_page = lesson_key


def back_to_lessons() -> None:
    st.session_state.lesson_page = "main"


st.title("Lessons")

if st.session_state.lesson_page == "main":
    lesson_columns = st.columns(3, gap="large")

    with lesson_columns[0].container(border=True, height=260):
        st.markdown("### Lesson 1: Basics")
        st.write("Learn Excel basics, key terms, and core workflow.")
        st.button("Open Lesson", key="lesson_basics", on_click=open_lesson, args=("basics",))

    with lesson_columns[1].container(border=True, height=260):
        st.markdown("### Lesson 2: Cell Formatting")
        st.write("Format cells for clear, professional data presentation.")
        st.button(
            "Open Lesson",
            key="lesson_cell_formatting",
            on_click=open_lesson,
            args=("cell_formatting",),
        )

    with lesson_columns[2].container(border=True, height=260):
        st.markdown("### Lesson 3: Formulas and Functions")
        st.write("Write formulas and use common Excel functions.")
        st.button(
            "Open Lesson",
            key="lesson_formulas",
            on_click=open_lesson,
            args=("formulas_functions",),
        )
else:
    lesson_key = st.session_state.lesson_page
    lesson_data = LESSONS.get(lesson_key)

    if lesson_data is None:
        st.error("This lesson page could not be found.")
    else:
        st.header(lesson_data["title"])
        st.write(lesson_data["summary"])
        st.write("Key topics:")
        for topic in lesson_data["topics"]:
            st.write(f"- {topic}")

    st.button("Back to Lessons", on_click=back_to_lessons)
