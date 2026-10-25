from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from app.models.schemas import RiskLevel, ToolDescriptor, ToolResult


class Tool(ABC):
    name: str
    description: str
    risk_level: RiskLevel = RiskLevel.LOW
    parameters: dict[str, Any] = {}

    @property
    def descriptor(self) -> ToolDescriptor:
        return ToolDescriptor(name=self.name, description=self.description, parameters=self.parameters,
                              risk_level=self.risk_level, requires_confirmation=self.risk_level != RiskLevel.LOW)

    @abstractmethod
    async def execute(self, **kwargs: Any) -> ToolResult: ...

    async def validate(self, **kwargs: Any) -> str | None:
        return None
