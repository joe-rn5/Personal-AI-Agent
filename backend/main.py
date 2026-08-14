import json
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama

# --- Config ---------------------------------------------------------------
MODEL = "local-coder"
MAX_TOOL_ITERATIONS = 5
PROFILE_PATH = Path(__file__).parent / "profile.json"

PROFILE: Dict[str, Any] = json.loads(PROFILE_PATH.read_text())

app = FastAPI(title="Personal Agent API (Local Ollama)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = """
You are the personal AI assistant for Youssef Ramadan. 
- Youssef is a second-year computer engineering student at Alexandria University in Egypt.
- He is skilled in software development (Java, C++, MATLAB, and Python) and computer engineering concepts.
- Answer questions about him, his projects, and his background professionally and accurately.
- CRITICAL RULE: When you use tools to retrieve profile data or project lists, ALWAYS summarize the information in natural, friendly, conversational English sentences. NEVER output raw JSON, code blocks, or raw dictionaries to the user.
"""

# --- Tools -------------------------------------------------------------
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_profile",
            "description": "Get the person's name, tagline, bio, skills, and contact info.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_projects",
            "description": "List the person's projects. Optionally filter by a keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Optional filter keyword, e.g. 'python' or 'java'.",
                    }
                },
            },
        },
    },
]

def run_tool(name: str, tool_input: Dict[str, Any]) -> Any:
    if name == "get_profile":
        return {k: v for k, v in PROFILE.items() if k != "projects"}
    if name == "list_projects":
        keyword = (tool_input.get("keyword") or "").lower().strip()
        projects = PROFILE["projects"]
        if not keyword:
            return projects
        return [
            p for p in projects
            if keyword in p["name"].lower()
            or keyword in p["description"].lower()
            or any(keyword in t.lower() for t in p.get("tech", []))
        ]
    return {"error": f"unknown tool '{name}'"}

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]

@app.post("/chat")
def chat(request: ChatRequest) -> Dict[str, str]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [dict(m) for m in request.messages]

    for _ in range(MAX_TOOL_ITERATIONS):
        response = ollama.chat(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
        )

        message = response.get("message", {})
        content = message.get("content", "").strip()
        tool_calls = message.get("tool_calls", [])

        # Handle local models outputting tool calls as text JSON
        if not tool_calls and content.startswith("{") and "name" in content:
            try:
                parsed = json.loads(content)
                if "name" in parsed:
                    tool_calls = [{
                        "function": {
                            "name": parsed["name"],
                            "arguments": parsed.get("arguments", {})
                        }
                    }]
            except Exception:
                pass

        if tool_calls:
            messages.append(message)
            for tool in tool_calls:
                func_name = tool["function"]["name"]
                func_args = tool["function"]["arguments"]
                result = run_tool(func_name, func_args)
                messages.append({
                    "role": "tool",
                    "content": json.dumps(result),
                })
            continue

        # Forcefully strip out any markdown bold asterisks if the model insists on using them
        content = content.replace("**", "")
        return {"reply": content}

    return {"reply": "I'm having trouble finishing that thought — try rephrasing?"}

@app.get("/")
def read_root() -> Dict[str, str]:
    return {"status": "online", "message": "Youssef's Personal Agent API is running!"}