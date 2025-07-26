## 2. `ARCHITECTURE.md`

```markdown
# Architecture Overview

Below, sketch (ASCII, hand-drawn JPEG/PNG pasted in, or ASCII art) the high-level components of your agent.
                ┌────────────────────────────┐
                │      👤 User Input          │
                │   (Thought via Streamlit)  │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │      Streamlit Frontend     │
                │ - User selects mood         │
                │ - Types messy thought       │
                │ - Sees plan with typing FX  │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │     ClarityBot Agent       │
                │   (Google ADK + Gemini)     │
                │ - Instruction tuned         │
                │ - Uses breakdown_thought()  
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │   Thought Breakdown Logic   │
                │ - Validates input length    │
                │ - Generates step-by-step    │
                │ - Cleans robotic language   │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │     Firebase Firestore      │
                │ - Stores thought + plan     │
                │ - Timestamped logs          │
                └────────────────────────────┘


## Components

1. **User Interface**  
   - Built using Streamlit as the primary interaction layer.
   - Allows users to input thoughts, select moods, and receive structured plans from ClarityMate.

2. **Agent Core**  
      The LLM interprets unstructured input and reformulates it into a step-by-step action plan
      The prompt ensures clarity, task breakdown, and motivational tone
      root_agent (LlmAgent): Configured using ADK’s AgentBuilder and Gemini 2.0 Flash.
      Instruction Layer: Uses a warm, human-style persona to deliver responses in a friendly, supportive tone.
      Tool Integration: Uses breakdown_thought as a custom tool to transform thoughts into action plans.
      Handles response formatting via a clean_response() function => due issues faced after the first interaction on a thought.

   - **Memory**: 
   - Firestore (Firebase)
     Used to store past interactions, user inputs, and clarified responses
     Enables continuity across sessions or devices
     Can later support: User-specific patterns, Trending topics, Task recurrence detection, Analytics for productivity

   - Future Expansion Ideas:
      Embedding-based memory using Pinecone or Weaviate
      Caching + prioritization with Redis or Firebase's in-memory layer
      Offline mode with local browser storage or on-device cache

3. **Tools / APIs**  
   - Google Gemini API (via google.generativeai): Handles all natural language understanding and output generation, Acts as both planner and executor in current architecture


4. **Observability**  
   Logging:
   Print/debug logs available in terminal via FastAPI
   Traces input received, raw output, and final cleaned message

   Error Handling:
   Handles no-input cases
   Try/catch blocks return user-friendly error messages
   Fallback messages shown in frontend if backend fails

   Thoughtfully cleaned Gemini responses via the clean_response function to remove robotic or dev-speak tone.

