import streamlit as st
import speech_recognition as sr
import os
os.system("pip install pyaudio")
from datetime import datetime

def transcribe_speech(recognizer, microphone, api_choice, language):
    """Recognizes speech using the selected API."""
    with microphone as source:
        st.info("Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        if api_choice == "Google Speech Recognition":
            text = recognizer.recognize_google(audio, language=language)
        elif api_choice == "Sphinx (Offline)":
            text = recognizer.recognize_sphinx(audio)
        else:
            return "Error: API not supported!"
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio. Please try again."
    except sr.RequestError:
        return "API request failed. Check your internet connection."

# Streamlit UI
st.title("🎙️ Speech Recognition App")
st.markdown("<h6 style = 'top_margin: 0rem; color: #F2921D'>Built by LOLA</h6>", unsafe_allow_html = True)
st.write("Speak into the microphone and convert speech to text!")

# Select API
api_choice = st.selectbox("Select Speech Recognition API", ["Google Speech Recognition", "Sphinx (Offline)"])

# Select Language
language = st.selectbox("Select Language", ["en-US", "fr-FR", "es-ES", "de-DE", "zh-CN"])  # Add more as needed

# Speech Recognizer Setup
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Pause and Resume
if 'paused' not in st.session_state:
    st.session_state.paused = False

if st.button("Start Recording"):
    st.session_state.paused = False
    transcribed_text = transcribe_speech(recognizer, microphone, api_choice, language)
    st.session_state.transcribed_text = transcribed_text

if st.button("Pause Recording"):
    st.session_state.paused = True

# Display Transcribed Text
if 'transcribed_text' in st.session_state:
    st.text_area("Transcribed Text", st.session_state.transcribed_text, height=150)

    # Save Transcription
    if st.button("Save Transcription"):
        filename = f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(st.session_state.transcribed_text)
        st.success(f"Transcription saved as {filename}")
        st.download_button("Download File", data=st.session_state.transcribed_text, file_name=filename)
