from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any
from app.models.schemas import RiskLevel, ToolResult
from app.tools.base import Tool


class TerminalTool(Tool):
    name = "run_terminal_command"
    description = "Run a constrained developer command with output capture and timeout."
    risk_level = RiskLevel.MEDIUM
    parameters = {"command": {"type": "array", "items": {"type": "string"}}, "cwd": {"type": "string"}}
    allowed_commands = {"git", "docker", "npm", "node", "python", "pytest", "uvicorn"}
    blocked_tokens = {"format", "diskpart", "reg", "shutdown", "restart-computer", "remove-item", "del", "rd", "rmdir", "rm"}

    async def validate(self, **kwargs: Any) -> str | None:
        command = kwargs.get("command")
        if not isinstance(command, list) or not command or not all(isinstance(x, str) for x in command):
            return "Command must be a non-empty argument list."
        if command[0].lower() not in self.allowed_commands:
            return f"{command[0]} is not in the developer command allowlist."
        joined = " ".join(command).lower()
        if any(token in joined for token in self.blocked_tokens):
            return "Command contains a blocked destructive or system-changing operation."
        return None

    async def execute(self, **kwargs: Any) -> ToolResult:
        command: list[str] = kwargs["command"]
        cwd = Path(kwargs.get("cwd") or Path.cwd())
        try:
            process = await asyncio.create_subprocess_exec(*command, cwd=cwd, stdout=asyncio.subprocess.PIPE,
                                                           stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=60)
            ok = process.returncode == 0
            return ToolResult(success=ok, tool=self.name, action="execute", message="Command completed." if ok else "Command failed.",
                              data={"command": command, "cwd": str(cwd), "stdout": stdout.decode(errors="replace")[-12000:],
                                    "stderr": stderr.decode(errors="replace")[-12000:], "exit_code": process.returncode},
                              error=None if ok else f"Exit code {process.returncode}")
        except TimeoutError:
            return ToolResult(success=False, tool=self.name, action="execute", message="Command timed out after 60 seconds.", error="timeout")
        except OSError as exc:
            return ToolResult(success=False, tool=self.name, action="execute", message="Command could not start.", error=str(exc))
