from __future__ import annotations

import re
from datetime import datetime
from app.config import settings
from app.memory.store import MemoryStore
from app.models.schemas import ActivityRecord, RiskLevel, ToolResult
from app.security.permissions import PermissionManager
from app.tools.registry import ToolRegistry
from app.agent.providers import get_provider


class Agent:
    def __init__(self, registry: ToolRegistry, memory: MemoryStore, permissions: PermissionManager) -> None:
        self.registry, self.memory, self.permissions = registry, memory, permissions
        self.automation_enabled = settings.veronica_automation_enabled

    def _plan(self, text: str) -> tuple[str | None, dict[str, str], str]:
        normalized = text.lower().strip()
        if normalized in {"stop veronica", "stop automation", "stop"}: return "stop", {}, "stop"
        if normalized in {"start veronica", "start automation"}: return "start", {}, "start"
        if "cpu" in normalized or "ram" in normalized or "check my pc" in normalized or "system status" in normalized:
            return "system_info", {}, "system_health"
        if "docker" in normalized and ("container" in normalized or "show" in normalized or "list" in normalized): return "docker_containers", {}, "docker_list"
        match = re.search(r"restart (?:the )?(?:docker )?(?:container )?([\w.-]+)", normalized)
        if match: return "docker_restart", {"container": match.group(1)}, "docker_restart"
        if "git status" in normalized: return "git_status", {"cwd": str(self.memory.preferences().get("project_directory", ""))}, "git_status"
        if "git pull" in normalized: return "git_pull", {"cwd": str(self.memory.preferences().get("project_directory", ""))}, "git_pull"
        match = re.search(r"open (?:the )?(.+)", text, re.I)
        if match: return "open_application", {"application": match.group(1).strip()}, "open_application"
        match = re.search(r"remember (?:that )?(?:my )?(.+?) (?:is|=) (.+)", text, re.I)
        if match: return "remember", {"key": match.group(1).strip().lower().replace(" ", "_"), "value": match.group(2).strip()}, "remember"
        if normalized.startswith("forget") or normalized == "clear memory": return "forget", {}, "forget"
        return None, {}, "conversation"

    async def handle(self, text: str, confirmed: bool = False) -> ToolResult:
        tool_name, arguments, intent = self._plan(text)
        if tool_name == "stop":
            self.automation_enabled = False
            return self._record(text, intent, None, {}, RiskLevel.LOW, confirmed, ToolResult(success=True, tool="core", action="stop", message="Automation stopped. Veronica will not run tools until started."))
        if tool_name == "start":
            self.automation_enabled = True
            return self._record(text, intent, None, {}, RiskLevel.LOW, confirmed, ToolResult(success=True, tool="core", action="start", message="Automation started."))
        if tool_name == "remember":
            self.memory.set_preference(arguments["key"], arguments["value"])
            return self._record(text, intent, None, arguments, RiskLevel.LOW, confirmed, ToolResult(success=True, tool="memory", action="remember", message="I saved that preference."))
        if tool_name == "forget":
            allowed, reason = self.permissions.authorize(RiskLevel.HIGH, confirmed, self.automation_enabled)
            if not allowed:
                return self._record(text, intent, "memory", {}, RiskLevel.HIGH, confirmed,
                    ToolResult(success=False, tool="memory", action="forget", message=reason or "Permission denied.",
                               data={"confirmation_required": True}, error="confirmation_required"))
            count = self.memory.forget()
            return self._record(text, intent, None, {}, RiskLevel.HIGH, confirmed, ToolResult(success=True, tool="memory", action="forget", message=f"Removed {count} stored preferences."))
        if tool_name is None:
            answer = await get_provider().respond(text)
            return self._record(text, intent, None, {}, RiskLevel.LOW, confirmed, ToolResult(success=True, tool="ai", action="respond", message=answer))
        tool = self.registry.get(tool_name)
        assert tool is not None
        validation_error = await tool.validate(**arguments)
        if validation_error:
            result = ToolResult(success=False, tool=tool.name, action="validate", message="I couldn't run that request.", error=validation_error)
            return self._record(text, intent, tool.name, arguments, tool.risk_level, confirmed, result)
        allowed, reason = self.permissions.authorize(tool.risk_level, confirmed, self.automation_enabled)
        if not allowed:
            result = ToolResult(success=False, tool=tool.name, action="permission", message=reason or "Permission denied.", data={"confirmation_required": self.permissions.needs_confirmation(tool.risk_level)}, error="confirmation_required")
            return self._record(text, intent, tool.name, arguments, tool.risk_level, confirmed, result)
        result = await tool.execute(**arguments)
        return self._record(text, intent, tool.name, arguments, tool.risk_level, confirmed, result)

    def _record(self, request: str, intent: str, tool: str | None, arguments: dict, risk: RiskLevel, confirmed: bool, result: ToolResult) -> ToolResult:
        self.memory.log(ActivityRecord(timestamp=datetime.now(), user_request=request, intent=intent, tool=tool,
            arguments=arguments, risk=risk, confirmation=confirmed, success=result.success, result=result.message, error=result.error))
        return result
