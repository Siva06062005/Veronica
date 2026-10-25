<<<<<<< HEAD
# VERONICA

VERONICA is a local Windows desktop AI operating assistant. It provides a FastAPI control plane, a responsive React HUD, persistent local memory and audit history, guarded Windows/developer tools, and provider abstractions for AI and voice.

## Current capabilities

- Real local system monitoring: CPU, RAM, disks, battery, uptime, hostname and network interface availability.
- Launch installed applications by executable name/path when Windows can resolve them.
- Docker container listing and confirmed container restart through the Docker CLI.
- Git status and confirmed fast-forward pull through Git CLI.
- Controlled developer command execution with an executable allowlist, destructive-token blocklist, 60-second timeout, captured output, and exit-code validation.
- SQLite-backed preferences and audit history. It does not store passwords, API keys, or tokens.
- Global `Stop Veronica` command that turns automation off until explicitly restarted.

## Quick start

Run PowerShell from the project root:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\setup.ps1
.\start_veronica.ps1
```

Open `http://127.0.0.1:5173`. Stop both processes with:

```powershell
.\stop_veronica.ps1
```

`setup.ps1` does not change machine-wide policy or system configuration. It creates `.venv`, installs declared project dependencies, and copies `backend/.env.example` to `backend/.env` only if absent.

## Configuration

Edit `backend/.env` after setup. The default `AI_PROVIDER=mock` provides deterministic offline fallback messages. Veronica supports these LLM modes:

| Provider value | Typical use | Required configuration |
| --- | --- | --- |
| `mock` | Offline deterministic fallback | None |
| `openai` | OpenAI Responses API | `OPENAI_API_KEY`, `AI_MODEL` |
| `ollama` | Local Ollama models | `AI_MODEL`, optional `OLLAMA_BASE_URL` |
| `openai_compatible` | LM Studio, vLLM, LocalAI, or compatible hosted API | `LLM_BASE_URL`, `AI_MODEL`, optional `LLM_API_KEY` |

For example, an Ollama setup can use `AI_PROVIDER=ollama` and `AI_MODEL=llama3.2`. A local LM Studio server normally uses `AI_PROVIDER=openai_compatible`, `LLM_BASE_URL=http://127.0.0.1:1234/v1`, and its loaded model identifier. Do not commit API-key fields. Voice has an explicit provider seam but ships disabled (`VOICE_PROVIDER=none`) because microphone/STT/TTS packages and credentials must be selected and installed deliberately.

Set `VERONICA_ALLOWED_ROOTS` to semicolon-separated approved file roots before enabling future file-management tools. Current release deliberately omits deletion, registry, firewall, credential, and other system-configuration tools.

## Security model

| Risk | Policy |
| --- | --- |
| Low | Read-only system data and application launch run immediately while automation is enabled. |
| Medium | Developer commands, Docker restart, and Git pull require a UI confirmation. |
| High / Critical | Reserved for future tools and must always require explicit confirmation. No critical tool is included. |

Commands use argument lists rather than a shell. The terminal tool accepts only `git`, `docker`, `npm`, `node`, `python`, `pytest`, and `uvicorn`, blocks destructive/system-changing tokens, captures output, and times out. The audit log records arguments excluding secrets.

## API

- `GET /health`
- `GET /system/status`
- `GET /tools`
- `GET /activity`
- `GET /memory`
- `POST /command` with `{ "text": "Check my PC", "confirmed": false }`
- `WS /ws/veronica` for frontend heartbeat/state

## Tests

After setup:

```powershell
Set-Location backend
..\.venv\Scripts\python.exe -m pytest -q
```

Tests mock no destructive actions and never remove user files or change system settings.

## Troubleshooting

- Backend offline: run `backend` with `..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload` to view errors.
- Docker unavailable: install/start Docker Desktop, then verify `docker version` in a terminal. Veronica reports CLI failures instead of claiming success.
- Application not found: use its `.exe` path or ensure it is on `PATH`.
- Frontend missing: rerun `setup.ps1` to install `frontend/node_modules`.

## Extension roadmap

Add the voice provider adapters (Windows Speech, Whisper, or cloud providers), a Tauri desktop shell, explicit file operations constrained by approved roots, window focus controls, richer installed-app discovery, project capability detection, and signed packaging. Each addition should retain structured results, permission enforcement, and audit logging.
=======
# VERONICA — Personal AI & Voice Assistant for Windows

**VERONICA** is a personal AI and voice assistant for Windows, combining the conversational intelligence of ChatGPT, the vocal ease of Siri, and the local system automation power of JARVIS.

Designed exclusively as a personal companion for **Papa**, VERONICA runs fully locally using [Ollama](https://ollama.ai) and provides safe, allowlisted Windows automation, persistent personal memory, document knowledge (RAG), and a modern web interface with a glowing cybernetic voice orb.

---

## Key Features

1. **Cybernetic Holographic Voice Orb**
   - Interactive glowing voice sphere responding to your voice with 4 animated states: *Idle (breathing)*, *Listening (pulsing cyan)*, *Thinking (orbital spin)*, and *Speaking (sound wave harmonics)*.
   - Speech-to-Text (STT) via Web Speech API with interim speech display.
   - Continuous Wake-word mode: activates upon hearing *"Veronica"*.
   - Speech Synthesis (TTS): natural voice replies with mute/replay controls.

2. **Unified Intent Router**
   - Deterministic pattern matching for instant answers (time, date, math calculation, system specifications, web search).
   - Conversational fallback to local Ollama LLM (`llama3.2:3b` by default, with live model switcher).
   - Strips `<think>` tags automatically for clean responses.

3. **Safe Windows Automation & Allowlisted Control**
   - Launch allowed apps: Chrome, Notepad, Calculator, File Explorer, Task Manager, Command Prompt, PowerShell.
   - Safe system operations: System specs, lock workstation, volume control.
   - Dangerous operations (shutdown, restart) require explicit confirmation before execution.

4. **Persistent Personal Memory Vault**
   - Dedicated JSON-backed long-term memory that survives restarts.
   - Natural language commands: `"Remember that..."`, `"What do you remember?"`, `"Forget memory..."`.
   - Full UI panel to view, search, add, and delete memories.
   - Automatically injects user context into Ollama prompts.

5. **Document Knowledge (RAG)**
   - Upload `.txt`, `.md`, or `.pdf` files to expand Veronica's knowledge base.
   - Embeddings and vector retrieval to answer questions grounded in your local documents.

---

## Project Structure

```
C:\Veronica\
├── app/
│   ├── agent/             # Assistant controller & intent router
│   │   ├── assistant.py   # Main router (deterministic + LLM fallback)
│   │   └── api.py         # Assistant router endpoints
│   ├── core/              # Core configs & LLM brain
│   │   ├── config.py      # Environment variables & system prompts
│   │   └── brain.py       # Ollama integration, error classification, history
│   ├── memory/            # Long-term memory storage
│   │   └── veronica_memory.py
│   ├── rag/               # Document ingestion & vector retrieval
│   ├── tools/             # Tool registry & allowed operations
│   │   ├── registry.py    # ToolRegistry implementation
│   │   └── windows_registry.py
│   ├── windows/           # Windows-specific system integrations
│   │   └── windows_control.py
│   └── webui/             # FastAPI web server & REST endpoints
│       └── server.py
├── web/                   # Modern React + Vite frontend
│   ├── src/
│   │   ├── App.jsx        # Assistant UI, Voice Orb, Chat, Memory Vault, Tools
│   │   ├── styles.css     # Cyber-assistant dark aesthetic & animations
│   │   └── main.jsx
│   └── package.json
├── VERONICA_WEB.bat       # One-click Windows launcher (Ollama + Backend + UI)
└── README.md
```

---

## Getting Started

### Prerequisites
- **Windows 10 / 11**
- **Python 3.10+** (virtual environment located in `C:\Veronica\.venv`)
- **Node.js 18+** & npm
- **Ollama** installed with `llama3.2:3b` (or another model) pulled:
  ```powershell
  ollama pull llama3.2:3b
  ```

### Quick Launch
Simply double-click:
```bat
VERONICA_WEB.bat
```
This batch file will:
1. Ensure Ollama is running (starting `ollama serve` if needed).
2. Start the FastAPI backend server on `http://127.0.0.1:8000`.
3. Start the Vite React development server on `http://127.0.0.1:5173`.
4. Automatically open your browser to the VERONICA interface.

---

## API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Backend and Ollama status check |
| `GET` | `/api/models` | List installed Ollama models |
| `POST` | `/api/models/select` | Switch the active LLM model |
| `POST` | `/api/chat` | Send a message/command to VERONICA |
| `POST` | `/api/confirm` | Confirm a pending dangerous action |
| `POST` | `/api/cancel` | Cancel a pending dangerous action |
| `GET` | `/api/memory` | Retrieve all persistent memories |
| `POST` | `/api/memory` | Store a new memory item |
| `DELETE`| `/api/memory/{id}` | Delete a specific memory item |
| `POST` | `/api/rag/ingest` | Ingest a document for RAG search |

---

## Voice & Chat Commands Examples

- **Time & Date:** *"What time is it?"*, *"What is today's date?"*
- **Calculations:** *"Calculate 144 * 25"*, *"What is 20 percent of 850?"*
- **System Specs:** *"Show system info"*, *"What computer is this?"*
- **Apps:** *"Open Google Chrome"*, *"Open Notepad"*, *"Open Calculator"*
- **Memory:** *"Remember that Papa prefers working in Python"*, *"Show what you remember"*
- **Conversations:** *"Tell me a story about an autonomous AI assistant"*, *"Explain quantum computing simply"*
"# Veronica" 
>>>>>>> 54689d97cef9805a3bf126efa0aa964139b725fb
