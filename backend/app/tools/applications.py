from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any
from app.models.schemas import ToolResult
from app.tools.base import Tool


class OpenApplicationTool(Tool):
    name = "open_application"
    description = "Open an installed application by executable name or absolute executable path."
    parameters = {"application": {"type": "string"}}

    async def validate(self, **kwargs: Any) -> str | None:
        app = str(kwargs.get("application", "")).strip()
        if not app:
            return "An application name is required."
        if any(token in app for token in ["&", "|", ";", "\n"]):
            return "Application name contains unsafe shell characters."
        return None

    async def execute(self, **kwargs: Any) -> ToolResult:
        app = str(kwargs["application"]).strip()
        candidate = Path(app)
        executable = str(candidate) if candidate.is_file() else shutil.which(app)
        if not executable and os.name == "nt":
            aliases = {"chrome": "chrome.exe", "edge": "msedge.exe", "vscode": "Code.exe", "code": "Code.exe", "docker": "Docker Desktop.exe"}
            executable = shutil.which(aliases.get(app.lower(), app))
        if not executable:
            return ToolResult(success=False, tool=self.name, action="open", message=f"I couldn't find {app}.", error="not_found")
        try:
            subprocess.Popen([executable], shell=False, close_fds=True)
            return ToolResult(success=True, tool=self.name, action="open", message=f"Opening {app}.", data={"executable": executable})
        except OSError as exc:
            return ToolResult(success=False, tool=self.name, action="open", message=f"I couldn't open {app}.", error=str(exc))
