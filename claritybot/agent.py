import os
import re
from google.adk.agents import Agent
from google.cloud import aiplatform
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime


# Initialize Firebase only once
if not firebase_admin._apps:
    key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test-clarity-466818-1d556de1e24d.json"))
    print("📍 Firebase key path:", key_path)  # ← Debug line
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"❌ File not found: {key_path}")
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)


db = firestore.client()

# Breakdown thought
def breakdown_thought(thought: str, mood: str = "🤔 Just exploring") -> dict:
    """Breaks down a messy thought into an action plan, adjusted for mood."""
    if not thought or len(thought.strip()) < 10:
        return {
            "status": "error",
            "error_message": "Please provide a longer or more detailed thought.",
        }
    
# Adjust empathy intro based on mood
    mood_intro = {
        "😵 Overwhelmed": "You're carrying a lot right now. Let’s gently untangle it.",
        "😐 Unfocused": "Let’s sharpen things and bring your next step into focus.",
        "😔 Anxious": "You’re not alone — let’s find something calming and actionable.",
        "🤔 Just exploring": "Let’s play with some options to get clarity."
    }

    intro = mood_intro.get(mood, "Let’s make this easier.")

    steps = [
        "Write down everything that’s on your mind or stressing you out.",
        "Circle the top 1–2 things that feel most urgent or important.",
        "Break each one down into smaller tasks or steps.",
        "Block 30–60 minutes on your calendar to start the first step.",
        "Set a timer and work with no pressure to finish everything.",
        "Take a short break, then reassess how you feel.",
    ]

    
    raw_report = (
        f"{intro}\n\nHere's a structure that might help:\n\n" +
        "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)]) +
        "\n\n*Remember: one clear step is better than ten chaotic ones.*"
    )

# Clean the response in case Gemini language slips in later
    final_report = clean_response(raw_report)

    response = {
        "status": "success",
        "report": final_report
    }
# Save to Firestore
    try:
        doc = {
            "thought": thought,
            "response": response["report"],
            "mood": mood,
            "timestamp": datetime.utcnow()
        }
        print("📝 Writing to Firestore:")
        print(doc)
        db.collection("thought_plans").add(doc)
        print("✅ Thought-plan pair saved to Firestore.")
    except Exception as e:
        print(f"❌ Firestore write failed: {e}")

    return response
# This function softens or rewrites robotic phrases commonly returned by Gemini,
# replacing them with more natural, human-sounding alternatives.
# Useful for ensuring ClarityBot sounds warm and relatable.
def clean_response(text: str) -> str:
    """Cleans Gemini's response of robotic or developer-like phrasing."""

    substitutions = {
        r"\bthe tool gave us\b": "we came up with",
        r"\bthe AI suggests\b": "here’s what I suggest",
        r"\bthe model generated\b": "here’s a possible plan",
        r"\bI am an AI\b": "I’m here to help",
        r"`?breakdown_thought`?": "a step-by-step method I use",
        r"\bthe breakdown_thought function\b": "this simple breakdown method",
        r"\bfunction\b": "approach",  # generic catch-all
    }

    for pattern, replacement in substitutions.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text.strip()






root_agent = Agent(
    name="claritybot",
    #model=vertex_model,
    model="gemini-2.0-flash",
    description=(
        "An empathetic assistant that transforms messy or anxious thoughts into structured, step-by-step plans. "
        "Especially useful for neurodivergent users like those with ADHD or anxiety."
    ),
    instruction=(
        "You are ClarityBot, a supportive, executive-function-friendly AI assistant. "
        "You sound like a thoughtful, emotionally intelligent human—never robotic. "
        "Never refer to tools, functions, or code names like breakdown_thought. Respond as if you are doing the work yourself."
        "Speak with warmth, calm, and clarity, like a supportive friend who helps people get unstuck. "
        "Your mission: help users turn overwhelming thoughts into calm, doable plans. "
        "Acknowledge input with empathy. Break it into 3–7 simple steps. Always include a 'Tiny First Step.' "
        "Avoid hype. Use plain language. Emojis only if helpful (🌱✅📌)."
    ),
    tools=[breakdown_thought],
)
