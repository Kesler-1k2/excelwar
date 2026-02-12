import os

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = "gemini-2.5-flash"

if API_KEY:
    genai.configure(api_key=API_KEY)

st.title("Gemini Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "cache" not in st.session_state:
    st.session_state.cache = {}

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    if user_input in st.session_state.cache:
        bot_reply = st.session_state.cache[user_input]
    elif not API_KEY:
        bot_reply = "GOOGLE_API_KEY is missing. Add it to your .env file to enable chat responses."
    else:
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(user_input)
            bot_reply = response.text
            st.session_state.cache[user_input] = bot_reply
        except Exception as error:  # noqa: BLE001
            bot_reply = f"API error: {error}"

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
