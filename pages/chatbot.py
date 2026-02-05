import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv(dotenv_path=".env")  # Make sure .env is in the same folder as app.py

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ GOOGLE_API_KEY not found! Use a valid key or hardcode for testing.")
else:
    genai.configure(api_key=api_key)

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("Gemini Chatbot with Cache")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize cache to store responses
if "cache" not in st.session_state:
    st.session_state.cache = {}  # {user_input: bot_reply}

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Check cache first
    if user_input in st.session_state.cache:
        bot_reply = st.session_state.cache[user_input]
    else:
        # Call Gemini API (rate-limited)
        try:
            response = genai.GenerativeModel("gemini-2.5-flash").generate_content(user_input)
            bot_reply = response.text
            # Store in cache
            st.session_state.cache[user_input] = bot_reply
        except Exception as e:
            bot_reply = f"⚠️ API Error: {e}"

    # Show bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
