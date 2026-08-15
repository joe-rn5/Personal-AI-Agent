# Personal AI Agent

![Python](https://img.shields.io/badge/python-3.12-blue) ![FastAPI](https://img.shields.io/badge/backend-FastAPI-teal) ![Ollama](https://img.shields.io/badge/LLM-Ollama-orange) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

An AI agent embedded on my portfolio site that answers questions about my background, skills, and projects—using real tool calls against my own data, powered locally via Ollama.

## What it does

- Answers visitor questions by calling tools (`get_profile`, `list_projects`) instead of hallucinating from a prompt.
- Runs an agent loop against a local LLM via Ollama: model requests a tool → backend executes it → result goes back to the model → model responds.
- Ships as a self-contained widget — can be dropped into any static site.

## Stack

| Layer | Tech |
|---|---|
| LLM | Local LLM via Ollama |
| Backend | Python, FastAPI |
| Frontend | Vanilla HTML/CSS/JS — no framework |
| Deploy | Cloudflare Tunnel (backend) + Netlify (frontend) |

## How it works

~~~
visitor → chat widget (JS) → POST /chat → FastAPI Backend
                                              │
                                   tool_use? ─┤
                                              ▼
                                   run_tool() reads profile.json
                                              │
                                              ▼
                          result sent back → Ollama → reply → widget
~~~

## Project structure

~~~
backend/
  main.py          FastAPI app + tool-use loop
  profile.json     Agent's knowledge base — my data, edited by hand
  requirements.txt
frontend/
  index.html
  style.css
  chat.js
~~~

## Run it locally

1. Ensure Ollama is running locally on your machine.
2. Start the backend server:
   ```bash
   cd backend
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn backend.main:app --reload --port 8081
   
3. Open frontend/index.html in a browser.

## Deploy

Backend → Exposed publicly via Cloudflare Tunnel:

cloudflared tunnel --url http://localhost:8081

Frontend → Hosted statically via Netlify Drop, with API_URL updated in chat.js to point to the Cloudflare tunnel URL.

## Known limitations
Requires your local Mac and terminal processes to stay active for the public link to work.

No persistent memory across page refreshes (history lives in the browser tab only).

No response streaming.

## Author
Youssef Ramadan — Computer Engineering Student at Alexandria University