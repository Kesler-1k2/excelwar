import json
from pathlib import Path

import streamlit as st

PROFILE_DATA_FILE = Path("profile_data.json")


def load_profile_data() -> dict:
    """Load saved profile information, falling back to defaults."""
    if not PROFILE_DATA_FILE.exists():
        return {"name": "", "profile_pic": None}

    try:
        with PROFILE_DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {"name": "", "profile_pic": None}


st.set_page_config(page_title="ExcelWars", layout="wide")

profile_data = load_profile_data()
display_name = profile_data.get("name") or "User"

st.title("🏠 ExcelWars")
st.subheader(f"Welcome back, {display_name}!")
st.caption("The perfect place to excel, in Excel.")

lesson_col, progress_col, account_col = st.columns(3, gap="large")

with lesson_col.container(border=True, height=260):
    st.markdown("### 📚 Lessons")
    st.write("Find your lessons and quizzes.")
    st.page_link("pages/1_Lessons.py", label="Open", use_container_width=True)

with progress_col.container(border=True, height=260):
    st.markdown("### 📈 Progress")
    st.write("Track your learning progress and performance.")
    st.page_link("pages/2_Progress.py", label="Open", use_container_width=True)

with account_col.container(border=True, height=260):
    st.markdown("### 👤 Account")
    st.write("Manage your profile, settings, and preferences.")
    st.page_link("pages/3_Account.py", label="Open", use_container_width=True)

st.caption("2026 ExcelWars Ltd®")
