import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Sidebar Settings
st.sidebar.title("⚙️ Settings")
model_name = st.sidebar.selectbox(
    "Select Gemini Model",
    ["gemini-2.5-flash", "gemini-2.5-pro"]
)

temperature = st.sidebar.slider("Temperature (Creativity)", 0.0, 1.0, 0.7, 0.1)

# API Key Check
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY .env file mein nahi mila!")
    st.stop()

genai.configure(api_key=api_key)

# Initialize Model & Chat
model = genai.GenerativeModel(model_name=model_name)
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Message (sirf pehli baar)
if len(st.session_state.messages) == 0:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Assalamualaikum! 👋\n\nMain tumhara AI Chatbot hoon, powered by Google Gemini.\n\nKya baat karni hai aaj? University, studies, programming, career advice, ya kuch bhi pooch sakte ho!"
    })

st.title("🤖 My AI Chatbot")
st.caption("**Powered by Ibrar Ali Qureshi** | Final Year Project ")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                reply = response.text
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Clear Chat Button
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])
    st.rerun()

st.sidebar.success("✅ Connected to Google Gemini API")