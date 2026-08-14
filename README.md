# Personal AI Agent

![Python](https://img.shields.io/badge/python-3.12-blue) ![FastAPI](https://img.shields.io/badge/backend-FastAPI-teal) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

An AI agent embedded on my portfolio site that answers questions about my background, skills, and projects — using real tool calls against my own data, not a static FAQ or a scripted bot.

**Live demo:** [https://sage-klepon-4537d3.netlify.app](https://your-site.com) 

## What it does

- Answers visitor questions by calling tools (`get_profile`, `list_projects`) instead of hallucinating from a prompt
- Runs an agent loop against the Claude API: model requests a tool → backend executes it → result goes back to the model → model responds
- Ships as a self-contained widget — drop it into any static site

## Stack

| Layer | Tech |
|---|---|
| LLM | Claude API (`claude-sonnet-5`), tool use / function calling |
| Backend | Python, FastAPI |
| Frontend | Vanilla HTML/CSS/JS — no framework |
| Deploy | Render (backend) + Vercel (frontend) |

## How it works

```
visitor → chat widget (JS) → POST /chat → Claude API
                                              │
                                   tool_use? ─┤
                                              ▼
                                   run_tool() reads profile.json
                                              │
                                              ▼
                          result sent back → Claude API → reply → widget
```

## Project structure

```
backend/
  main.py          FastAPI app + tool-use loop
  profile.json     Agent's knowledge base — my data, edited by hand
  requirements.txt
frontend/
  index.html
  style.css
  chat.js
```

## Run it locally

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
uvicorn main:app --reload --port 8000
```

Open `frontend/index.html` in a browser.

## Deploy

- **Backend** → Render / Fly.io. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`. Set `ANTHROPIC_API_KEY` as an env var.
- **Frontend** → Vercel / Netlify, static files. Update `API_URL` in `chat.js` to the deployed backend URL.

## Known limitations

- No persistent memory across page refreshes (history lives in the browser tab only)
- No response streaming
- No rate limiting — add before making the URL public

## Roadmap

- [ ] GitHub-activity tool
- [ ] Resume-download tool
- [ ] Server-side session memory
- [ ] Streaming responses

## Author

**Youssef Ramadan** — Computer Engineering student


Built as the technical centerpiece of my AI fluency capstone.

## License

MIT
