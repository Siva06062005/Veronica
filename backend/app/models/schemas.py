from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any
from pydantic import BaseModel, Field


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ToolResult(BaseModel):
    success: bool
    tool: str
    action: str
    message: str
    data: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class ToolDescriptor(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any]
    risk_level: RiskLevel
    requires_confirmation: bool


class CommandRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4000)
    confirmed: bool = False


class AssistantEvent(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    state: str
    message: str
    tool_result: ToolResult | None = None


class ActivityRecord(BaseModel):
    id: int | None = None
    timestamp: datetime
    user_request: str
    intent: str
    tool: str | None = None
    arguments: dict[str, Any] = Field(default_factory=dict)
    risk: RiskLevel = RiskLevel.LOW
    confirmation: bool = False
    success: bool
    result: str
    error: str | None = None
