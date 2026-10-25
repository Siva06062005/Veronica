from app.models.schemas import RiskLevel
from app.security.permissions import PermissionManager

def test_low_risk_is_allowed_without_confirmation():
    assert PermissionManager().authorize(RiskLevel.LOW, False, True)[0]

def test_medium_requires_confirmation():
    assert not PermissionManager().authorize(RiskLevel.MEDIUM, False, True)[0]
    assert PermissionManager().authorize(RiskLevel.MEDIUM, True, True)[0]

def test_stop_disables_all_tools():
    assert not PermissionManager().authorize(RiskLevel.LOW, True, False)[0]
