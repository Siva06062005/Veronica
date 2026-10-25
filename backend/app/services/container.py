from app.agent.agent import Agent
from app.memory.store import MemoryStore
from app.security.permissions import PermissionManager
from app.tools.applications import OpenApplicationTool
from app.tools.docker import DockerRestartTool, DockerTool
from app.tools.git import GitPullTool, GitStatusTool
from app.tools.registry import ToolRegistry
from app.tools.system import SystemInfoTool
from app.tools.terminal import TerminalTool


memory = MemoryStore()
permissions = PermissionManager()
registry = ToolRegistry()
for tool in (SystemInfoTool(), OpenApplicationTool(), TerminalTool(), DockerTool(), DockerRestartTool(), GitStatusTool(), GitPullTool()):
    registry.register(tool)
agent = Agent(registry, memory, permissions)
