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
