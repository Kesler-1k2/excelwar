
import streamlit as st
import json
import os
from PIL import Image

# -------- Paths for saving data --------
PROFILE_DATA_FILE = "profile_data.json"
PROFILE_PIC_FILE = "profile_pic.png"

# -------- Load existing data --------
if os.path.exists(PROFILE_DATA_FILE):
    with open(PROFILE_DATA_FILE, "r") as f:
        profile_data = json.load(f)
else:
    profile_data = {"name": "", "profile_pic": None}

# -------- Streamlit UI --------
st.title("Account")

# Name input
name = st.text_input("Your Name:", value=profile_data.get("name", ""))

# Profile picture upload
uploaded_file = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])

# Show current profile pic if exists
if os.path.exists(PROFILE_PIC_FILE):
    st.image(PROFILE_PIC_FILE, width=150, caption="Current Profile Picture")

# Save button
if st.button("Save Changes"):
    # Save name
    profile_data["name"] = name

    # Save profile pic
    if uploaded_file:
        image = Image.open(uploaded_file)
        image.save(PROFILE_PIC_FILE)
        profile_data["profile_pic"] = PROFILE_PIC_FILE

    # Save JSON data
    with open(PROFILE_DATA_FILE, "w") as f:
        json.dump(profile_data, f)

    st.success("Profile updated successfully!")

# Optional: show current saved profile pic and name
st.write("Current Name:", profile_data.get("name", ""))
if profile_data.get("profile_pic") and os.path.exists(profile_data["profile_pic"]):
    st.image(profile_data["profile_pic"], width=150)
