import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini with your free API key from Google AI Studio
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

PROFILE_PATH = os.path.join(os.path.dirname(__file__), "profile.json")


def load_profile():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    return {}


def get_profile() -> dict:
    """Retrieve the user's profile, bio, skills, and contact info."""
    return load_profile()


def list_projects() -> list:
    """List all projects built by the user along with their descriptions and tech stacks."""
    profile = load_profile()
    return profile.get("projects", [])


# Pass Python functions directly as tools; Gemini handles execution flow automatically
tools = [get_profile, list_projects]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=tools,
    system_instruction=(
        "You are Youssef Ramadan's personal AI assistant embedded on his portfolio website. "
        "You answer questions about his background as a second-year computer engineering student at Alexandria University, "
        "his skills, and his projects. Always use the available tools to fetch accurate data. "
        "Be concise, professional, and friendly."
    )
)


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        # Map frontend roles ('assistant' -> 'model') for Gemini chat history
        history = []
        for m in request.messages[:-1]:
            gemini_role = "user" if m.role == "user" else "model"
            history.append({"role": gemini_role, "parts": [m.content]})

        chat_session = model.start_chat(history=history, enable_automatic_function_calling=True)

        last_message = request.messages[-1].content
        response = chat_session.send_message(last_message)

        return {"reply": response.text.strip()}
    except Exception as e:
        return {"reply": "I encountered an error connecting to the AI service.", "error": str(e)}