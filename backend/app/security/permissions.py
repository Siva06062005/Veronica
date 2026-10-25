from __future__ import annotations

from app.models.schemas import RiskLevel


class PermissionManager:
    """Central confirmation policy. High-impact actions never run implicitly."""

    def needs_confirmation(self, risk: RiskLevel) -> bool:
        return risk in {RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL}

    def authorize(self, risk: RiskLevel, confirmed: bool, automation_enabled: bool) -> tuple[bool, str | None]:
        if not automation_enabled:
            return False, "Automation is stopped. Start Veronica before running tools."
        if self.needs_confirmation(risk) and not confirmed:
            return False, f"This {risk.value}-risk action needs explicit confirmation."
        return True, None
