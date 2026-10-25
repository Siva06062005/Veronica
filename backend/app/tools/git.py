from __future__ import annotations

from typing import Any
from app.models.schemas import RiskLevel, ToolResult
from app.tools.base import Tool
from app.tools.terminal import TerminalTool


class GitStatusTool(Tool):
    name = "git_status"
    description = "Show Git repository status."
    parameters = {"cwd": {"type": "string"}}
    async def execute(self, **kwargs: Any) -> ToolResult:
        return await TerminalTool().execute(command=["git", "status", "--short", "--branch"], cwd=kwargs.get("cwd"))


class GitPullTool(Tool):
    name = "git_pull"
    description = "Pull repository changes from configured remote."
    risk_level = RiskLevel.MEDIUM
    parameters = {"cwd": {"type": "string"}}
    async def execute(self, **kwargs: Any) -> ToolResult:
        return await TerminalTool().execute(command=["git", "pull", "--ff-only"], cwd=kwargs.get("cwd"))
