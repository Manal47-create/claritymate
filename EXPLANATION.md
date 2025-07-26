# Technical Explanation

## 1. Agent Workflow
Here’s how ClarityBot processes each user input step-by-step:
1. Receive user input via the frontend (Streamlit).
2. Call root_agent() which uses Google ADK's AgentBuilder with a Gemini model
3. Run the breakdown_thought() tool to generate a humanized step-by-step plan
4. Clean the response using clean_response() to remove robotic phrases
5. Store thought, mood + response in Firestore
6. Return structured response to the frontend for display.

## 2. Key Modules

- Agent Builder (agent.py): Defines root_agent using Google ADK with a Gemini 2.0 Flash model, custom instructions, and breakdown_thought() as a tool

- Tool: Thought Breakdown (agent.py): Custom function that transforms messy thoughts into a 6-step plan, optionally adjusted for user mood

- Response Cleaner (agent.py): clean_response() softens Gemini's robotic tone and replaces dev-language with friendly phrasing

- Memory Store (Firestore): All thought/response pairs are saved to Firebase's Firestore with a timestamp and optional mood


## 3. Tool Integration

LLM API:
- Currently uses Gemini API
- Handles fuzzy thinking → clarity via structured planning prompt.

Firebase Firestore (Planned):
- Stores user input/output history.
- Used to persist user thoughts and plans

## 4. Observability & Testing

- Logs printed to terminal for each Firestore write and tool invocation
- Firebase errors are caught and printed in the backend
- Debug logs include key path confirmation and Firestore write results
- Typewriter animation in Streamlit provides clear output feedback

## 5. Known Limitations

Does not support concurrent users with identity/session isolation
Long or vague thoughts may result in generic advice ( life sucks for example)
No frontend validation of input length or duplication
Gemini response control limited to prompt engineering; doesn't yet use memory to improve continuity
No authentication yet – public use not production-secure 

