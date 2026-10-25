from __future__ import annotations

import asyncio
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.core.logging import configure_logging
from app.models.schemas import CommandRequest
from app.services.container import agent, memory, registry

configure_logging()
log = logging.getLogger(__name__)
app = FastAPI(title="VERONICA", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health(): return {"status": "online", "service": "veronica", "automation_enabled": agent.automation_enabled}

@app.get("/system/status")
async def system_status(): return (await registry.get("system_info").execute()).model_dump()

@app.get("/tools")
async def tools(): return [item.model_dump() for item in registry.descriptors()]

@app.get("/activity")
async def activity(): return [item.model_dump() for item in memory.activity()]

@app.get("/memory")
async def get_memory(): return memory.preferences()

@app.delete("/memory")
async def clear_memory(confirmed: bool = False):
    if not confirmed: return {"success": False, "message": "Explicit confirmation required.", "confirmation_required": True}
    return {"success": True, "removed": memory.forget()}

@app.post("/command")
async def command(request: CommandRequest): return (await agent.handle(request.text, request.confirmed)).model_dump()

@app.websocket("/ws/veronica")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            await ws.send_json({"state": "idle", "automation_enabled": agent.automation_enabled})
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        log.info("Frontend disconnected")
