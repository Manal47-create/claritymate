# streamlit_app.py

import streamlit as st
import asyncio
import time
from agent import root_agent            # ADK-powered agent
from agent import clean_response
from agent import breakdown_thought

# -----------------------------
# Streamlit page setup
# -----------------------------
st.set_page_config(page_title="Clarity Mate", page_icon="🧠", layout="centered")
st.title("🧠 Clarity Mate")
st.markdown("Let’s turn your overwhelm into a clear, doable plan.")

# -----------------------------
# Optional: Mood selector for future personalization
# -----------------------------
mood = st.selectbox(
    "How are you feeling right now?",
    ["😵 Overwhelmed", "😐 Unfocused", "😔 Anxious", "🤔 Just exploring"],
)

# -----------------------------
# User input text area
# -----------------------------
user_input = st.text_area(
    "What's on your mind?",
    height=150,
    placeholder="e.g. I have too much to do and don’t know where to start..."
)

# -----------------------------
# Typing effect helper function
# -----------------------------
def typewriter_effect(text, delay=0.01):
    output = ""
    placeholder = st.empty()
    for char in text:
        output += char
        placeholder.markdown(f"```\n{output}_\n```")
        time.sleep(delay)
    placeholder.markdown(f"```\n{output}\n```")

# -----------------------------
# Async wrapper to call ADK Agent
# -----------------------------
def get_agent_response(thought, mood):
    result = breakdown_thought(thought, mood)
    return result["report"] if result["status"] == "success" else result["error_message"]

# -----------------------------
# Main button logic
# -----------------------------
if user_input:
    if st.button("Get Clarity"):
        with st.spinner("🧠 ClarityMate is thinking..."):
            #result = root_agent.run(user_input)
            #final_response = clean_response(str(result))
            final_response = get_agent_response(user_input, mood)

        st.markdown("---")
        st.markdown("### ✅ Here's your clarity plan:")
        typewriter_effect(final_response)
else:
    st.info("💬 Enter your thought above to get started.")
