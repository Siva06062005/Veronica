from __future__ import annotations

import platform
import socket
import time
from typing import Any
import psutil
from app.models.schemas import ToolResult
from app.tools.base import Tool


class SystemInfoTool(Tool):
    name = "system_info"
    description = "Read current Windows system health and resource usage."
    parameters = {}

    async def execute(self, **kwargs: Any) -> ToolResult:
        memory = psutil.virtual_memory()
        disks = [{"device": d.device, "percent": psutil.disk_usage(d.mountpoint).percent}
                 for d in psutil.disk_partitions() if d.fstype]
        battery = psutil.sensors_battery()
        data = {"cpu_percent": psutil.cpu_percent(interval=0.15), "memory_percent": memory.percent,
                "memory_available_gb": round(memory.available / 1024**3, 2), "disks": disks,
                "hostname": socket.gethostname(), "platform": platform.platform(),
                "uptime_seconds": round(time.time() - psutil.boot_time()),
                "battery_percent": battery.percent if battery else None,
                "network_up": bool(psutil.net_if_stats())}
        return ToolResult(success=True, tool=self.name, action="inspect", message="System status retrieved.", data=data)
