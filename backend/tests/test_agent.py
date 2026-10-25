import pytest
from app.agent.agent import Agent
from app.memory.store import MemoryStore
from app.security.permissions import PermissionManager
from app.tools.registry import ToolRegistry
from app.tools.system import SystemInfoTool

@pytest.mark.asyncio
async def test_agent_resolves_cpu_request(tmp_path, monkeypatch):
    registry = ToolRegistry(); registry.register(SystemInfoTool())
    agent = Agent(registry, MemoryStore(), PermissionManager())
    result = await agent.handle("What's my CPU usage?")
    assert result.success and result.tool == "system_info"

@pytest.mark.asyncio
async def test_stop_veronica_blocks_actions():
    registry = ToolRegistry(); registry.register(SystemInfoTool())
    agent = Agent(registry, MemoryStore(), PermissionManager())
    await agent.handle("Stop Veronica")
    result = await agent.handle("Check my PC")
    assert not result.success and result.error == "confirmation_required"

@pytest.mark.asyncio
async def test_clear_memory_requires_confirmation():
    registry = ToolRegistry(); registry.register(SystemInfoTool())
    agent = Agent(registry, MemoryStore(), PermissionManager())
    result = await agent.handle("Clear memory")
    assert not result.success and result.error == "confirmation_required"
