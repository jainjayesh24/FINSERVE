from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])

def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except ValueError as e:
        st.error("Error fetching response from Gemini: " + str(e))
        return None

st.set_page_config(page_title="FinBot - Microfinance Management", page_icon="💰")

st.markdown("""
    <style>
        .stApp {
            font-family: 'Helvetica', sans-serif;
            color: #2E3A59;
        }
        h1 {
            font-size: 2.5em;
            text-align: center;
            color: #4A90E2;
            margin-bottom: 20px;
        }
        h2 {
            font-size: 1.5em;
            text-align: center;
            color: #2E3A59;
            margin-top: -10px;
        }
        .stTextInput > div > div > input {
            font-size: 1.1em;
            padding: 12px 20px;
            border-radius: 10px;
            border: 1px solid #4A90E2;
            width: 100%;
        }
        .stButton > button {
            font-size: 1.1em;
            padding: 12px 24px;
            border-radius: 10px;
            background-color: #4A90E2;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: #357ABD;
        }
        .stMarkdown {
            font-size: 1.2em;
            line-height: 1.6;
        }
        .stSubheader {
            font-size: 1.5em;
            color: #4A90E2;
        }
        .chat-bubble {
            max-width: 75%;
            margin-bottom: 15px;
            padding: 12px;
            border-radius: 15px;
            display: inline-block;
        }
        .user-bubble {
            background-color: #4A90E2;
            color: white;
            text-align: right;
        }
        .bot-bubble {
            background-color: #E1F5FE;
            color: #2E3A59;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>FinBot 💰</h1>", unsafe_allow_html=True)
st.markdown("<h2>Microfinance Management System</h2>", unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Type your question here:", key="input")
submit = st.button("Ask", help="Click to get a response from the bot")

if submit and input:
    response = get_gemini_response(input)
    if response:
        st.session_state['chat_history'].append(("You", input))
        
        for chunk in response:
            if hasattr(chunk, 'text'):
                st.session_state['chat_history'].append(("Bot", chunk.text))
            else:
                st.warning("Received an empty or invalid response chunk.")

st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    if role == "You":
        st.markdown(f"<div class='chat-bubble user-bubble'><strong>{role}:</strong> {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble bot-bubble'><strong>{role}:</strong> {text}</div>", unsafe_allow_html=True)
