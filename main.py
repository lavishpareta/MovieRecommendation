import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables securely
load_dotenv()

# Frontpage settings for a visually appealing layout
st.set_page_config(
    page_title=" Movie Recommendation ",
    page_icon=":clapper:",
    layout="centered",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Google GenerativeAI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-pro")


def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "Movie Recommender"
    else:
        return user_role

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Main app layout with clear headings and explanations
st.title(" Movie Recommendation ")
st.write("**Welcome!** Let's find you the perfect movie to watch.")
st.write("Tell me your preferences, genres you enjoy, or ask for specific recommendations.")

# Improved chat history display with speaker labels
chat_history = st.session_state.chat_session.history
for message in chat_history:
    speaker = translate_role_for_streamlit(message.role)
    st.write(f"**{speaker}**: {message.parts[0].text}")  # Use f-string for clean formatting

# User input area with more descriptive text
user_prompt = st.text_area(
    "  Tell me what kind of movie you're looking for:",
    height=100,  # Increase height for better usability
)

# Send user input to model and display response
if user_prompt:
    st.write(f"**You**: {user_prompt}")
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    st.write(f"**Movie Recommender **: {gemini_response.text}")