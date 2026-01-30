import streamlit as st
import json
import os
from PIL import Image
PROFILE_DATA_FILE = "profile_data.json"
if os.path.exists(PROFILE_DATA_FILE):
    with open(PROFILE_DATA_FILE, "r") as f:
        profile_data = json.load(f)
else:
    profile_data = {"name": "", "profile_pic": None}

st.set_page_config(page_title="ExcelWars", layout="wide")

st.title("ExcelWars")
st.title(f"Welcome back, {profile_data.get('name', 'User')}!")

st.subheader("The perfect place to excel, in Excel!")


st.title("🏠 ExcelWars")

cols = st.columns(4, gap="large")

with cols[0].container(border=True,height=350):
    st.markdown(
        """
        ### 📚 Lessons
        Find your lessons and
        quizzes here.
        
        """
    )
    st.page_link("pages/1_Lessons.py", label="Open")

with cols[1].container(border=True,height=350):
    st.markdown(
        """
        ### 📈 Progress  
        Track your learning progress  
        and performance over time.
        """
    )
    st.page_link("pages/2_Progress.py", label="Open", use_container_width=True)

with cols[2].container(border=True,height=350):
    st.markdown(
        """
        ### 👤 Account  
        Manage your profile,  
        settings, and preferences.
        """
    )
    st.page_link("pages/3_Account.py", label="Open", use_container_width=True)

st.caption("2026 ExcelWars Ltd®")