import json
from pathlib import Path

import streamlit as st
from PIL import Image

PROFILE_DATA_FILE = Path("profile_data.json")
PROFILE_PIC_FILE = Path("profile_pic.png")


def load_profile_data() -> dict:
    """Read saved profile data from disk."""
    if not PROFILE_DATA_FILE.exists():
        return {"name": "", "profile_pic": None}

    try:
        with PROFILE_DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {"name": "", "profile_pic": None}


def save_profile_data(profile_data: dict) -> None:
    with PROFILE_DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(profile_data, file, ensure_ascii=False, indent=2)


st.title("Account")
profile_data = load_profile_data()

name = st.text_input("Your Name", value=profile_data.get("name", ""))
uploaded_file = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])

if PROFILE_PIC_FILE.exists():
    st.image(str(PROFILE_PIC_FILE), width=150, caption="Current Profile Picture")

if st.button("Save Changes"):
    profile_data["name"] = name

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image.save(PROFILE_PIC_FILE)
        profile_data["profile_pic"] = str(PROFILE_PIC_FILE)

    save_profile_data(profile_data)
    st.success("Profile updated successfully.")

st.subheader("Current Profile")
st.write("Name:", profile_data.get("name", ""))

saved_picture = profile_data.get("profile_pic")
if saved_picture and Path(saved_picture).exists():
    st.image(saved_picture, width=150)
