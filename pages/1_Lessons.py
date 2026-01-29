import streamlit as st
st.title("Lessons")

# initialize
if "lesson_page" not in st.session_state:
    st.session_state.lesson_page = "main"

def go_to_basics():
    st.session_state.lesson_page = "basics"
def go_to_cell_formatting():
    st.session_state.lesson_page = "cell_formatting"
def go_to_formulas_functions():
    st.session_state.lesson_page = "formulas_functions"
# layout
cols = st.columns(4, gap="large")

if st.session_state.lesson_page == "main":
    with cols[0].container(border=True):
        st.markdown("""
        ### Lesson 1: Basics
        Learn Excel basics, key terms, and functions
        """)
        st.button("Let's Go! ➡", key="lesson1", on_click=go_to_basics)
    with cols[1].container(border=True):
        st.markdown("""
        ### Lesson 2: Cell Formatting
        Learn how to format cells for better data presentation
        """)
        st.button("Let's Go! ➡", key="lesson2", on_click=go_to_cell_formatting)
    with cols[2].container(border=True):
        st.markdown("""
        ### Lesson 3: Formulas & Functions
        Learn how to use formulas and functions effectively
        """)
        st.button("Let's Go! ➡", key="lesson3", on_click=go_to_formulas_functions)
   

elif st.session_state.lesson_page == "basics":
    st.title("Lesson 1: Basics of Excel")
    st.write("Welcome to Lesson 1!")
    if st.button("Back to Lessons"):
        st.session_state.lesson_page = "main"
