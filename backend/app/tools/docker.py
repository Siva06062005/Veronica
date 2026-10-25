from __future__ import annotations

import re
from typing import Any
from app.models.schemas import RiskLevel, ToolResult
from app.tools.base import Tool
from app.tools.terminal import TerminalTool


class DockerTool(Tool):
    name = "docker_containers"
    description = "List Docker containers using the local Docker CLI."
    parameters = {}
    async def execute(self, **kwargs: Any) -> ToolResult:
        return await TerminalTool().execute(command=["docker", "ps", "-a", "--format", "{{json .}}"])


class DockerRestartTool(Tool):
    name = "docker_restart"
    description = "Restart one named Docker container."
    risk_level = RiskLevel.MEDIUM
    parameters = {"container": {"type": "string"}}
    async def validate(self, **kwargs: Any) -> str | None:
        container = str(kwargs.get("container", "")).strip()
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", container):
            return "Container name must contain only letters, numbers, dots, underscores, and hyphens."
        return None
    async def execute(self, **kwargs: Any) -> ToolResult:
        container = str(kwargs.get("container", "")).strip()
        if not container:
            return ToolResult(success=False, tool=self.name, action="restart", message="A container name is required.", error="validation")
        return await TerminalTool().execute(command=["docker", "restart", container])
