import pytest
from app.tools.registry import ToolRegistry
from app.tools.system import SystemInfoTool
from app.tools.terminal import TerminalTool

@pytest.mark.asyncio
async def test_system_tool_returns_structured_data():
    result = await SystemInfoTool().execute()
    assert result.success and "cpu_percent" in result.data

@pytest.mark.asyncio
async def test_terminal_rejects_destructive_command():
    tool = TerminalTool()
    assert await tool.validate(command=["powershell", "Remove-Item", "x"]) is not None

def test_registry_rejects_duplicate_tools():
    registry = ToolRegistry(); registry.register(SystemInfoTool())
    with pytest.raises(ValueError): registry.register(SystemInfoTool())
