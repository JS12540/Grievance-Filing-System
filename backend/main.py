import asyncio
import tempfile

import streamlit as st
from gtts import gTTS
from pipeline.pipeline import InferencePipeline
from streamlit_mic_recorder import speech_to_text

# Language options
LANGUAGE_OPTIONS = {
    "English": "en",
    "Hindi": "hi",
    "Gujarati": "gu",
    "Marathi": "mr",
}

# Sidebar selection for language
st.sidebar.title("Settings")
selected_language = st.sidebar.selectbox(
    "Select Language:", list(LANGUAGE_OPTIONS.keys())
)
selected_language_code = LANGUAGE_OPTIONS[selected_language]

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_data_object" not in st.session_state:
    st.session_state.last_data_object = None


def text_to_speech_gtts(text, language="en"):
    """Convert text to speech using gTTS."""
    try:
        # Create TTS object
        tts = gTTS(text=text, lang=language)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tts.save(f.name)
            audio_path = f.name

        st.audio(audio_path, format="audio/mp3")
    except Exception as e:
        st.error(f"Error with TTS: {e}")


st.write("### Greviance Filing System:")
recorded_text = speech_to_text(
    language=selected_language_code,
    start_prompt="Start recording",
    stop_prompt="Stop recording",
    use_container_width=True,
    just_once=True,
    key=f"STT_{selected_language}",
)

# Step 2-4: Generate question, convert to speech, and play
if recorded_text:
    st.write("**User:**", recorded_text)
    st.session_state.chat_history.append(
        {"role": "user", "content": recorded_text}
    )

    data = {
        "text": recorded_text,
        "chat_history": st.session_state.chat_history,
        "selected_language": selected_language,
    }

    pipeline = InferencePipeline()

    # Run the pipeline asynchronously using asyncio
    async def process_pipeline():
        """Run the pipeline asynchronously."""
        return await pipeline.run(data)

    data = asyncio.run(process_pipeline())
    st.session_state.last_data_object = (
        data  # Store the data object in session state
    )

    if "bot_response" in data:
        st.write("**Bot:**", data["bot_response"])
        st.session_state.chat_history.append(
            {"role": "assistant", "content": data["bot_response"]}
        )

        text_to_speech_gtts(
            data["bot_response"], language=selected_language_code
        )

# Show Data Object Button
if st.sidebar.button("Show Data Object"):
    st.sidebar.write("### Data Object")
    if st.session_state.last_data_object:
        st.sidebar.json(st.session_state.last_data_object)
    else:
        st.sidebar.write("No data object available yet.")

# Show Chat History Button
if st.sidebar.button("Show Chat History"):
    st.sidebar.write("### Chat History")
    for entry in st.session_state.chat_history:
        role = "User" if entry["role"] == "user" else "Assistant"
        st.sidebar.write(f"**{role}:** {entry['content']}")
