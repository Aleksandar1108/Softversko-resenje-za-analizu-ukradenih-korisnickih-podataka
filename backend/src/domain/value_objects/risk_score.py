"""Risk score value object."""
from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    """Risk levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class RiskScore:
    """Risk score value object."""
    
    value: float  # 0.0-10.0
    level: RiskLevel
    factors: list[str]
    
    def __post_init__(self):
        """Validate risk score."""
        if not 0.0 <= self.value <= 10.0:
            raise ValueError("Risk score must be between 0.0 and 10.0")
        
        # Determine level based on value
        if self.value < 3.0:
            object.__setattr__(self, 'level', RiskLevel.LOW)
        elif self.value < 6.0:
            object.__setattr__(self, 'level', RiskLevel.MEDIUM)
        elif self.value < 8.0:
            object.__setattr__(self, 'level', RiskLevel.HIGH)
        else:
            object.__setattr__(self, 'level', RiskLevel.CRITICAL)
