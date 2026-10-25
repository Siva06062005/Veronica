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
