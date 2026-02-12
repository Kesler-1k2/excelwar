import streamlit as st

st.title("Progress")
st.write("Track your lesson completion and quiz performance here.")

xp = st.session_state.get("xp", 0)
level = st.session_state.get("level", 1)
completed = st.session_state.get("completed", {})

metric_col_1, metric_col_2 = st.columns(2)
metric_col_1.metric("XP", xp)
metric_col_2.metric("Level", level)

if completed:
    st.subheader("Lesson Completion")
    st.json(completed)
else:
    st.info("No progress has been recorded yet.")
