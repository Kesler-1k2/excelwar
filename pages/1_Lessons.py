import streamlit as st

# initialize
if "lesson_page" not in st.session_state:
    st.session_state.lesson_page = "main"

def go_to_basics():
    st.session_state.lesson_page = "basics"

# layout
cols = st.columns(4, gap="large")

if st.session_state.lesson_page == "main":
    with cols[0].container(border=True):
        st.markdown("""
        ### Lesson 1: Basics
        Learn Excel basics, key terms, and functions
        """)
        st.button("Let's Go! ➡", on_click=go_to_basics)
    with cols[1].container(border=True):
        st.markdown("""
        ### Lesson 1: Cell Formatting
        Learn how to format cells for better data presentation
        """)
        st.button("Let's Go! ➡", on_click=go_to_basics)

elif st.session_state.lesson_page == "basics":
    st.title("Lesson 1: Basics of Excel")
    st.write("Welcome to Lesson 1!")
    if st.button("Back to Lessons"):
        st.session_state.lesson_page = "main"
