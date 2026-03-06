"""Password strength value object."""
from dataclasses import dataclass
from enum import Enum


class PasswordStrengthLevel(Enum):
    """Password strength levels."""
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"
    VERY_STRONG = "very_strong"


@dataclass(frozen=True)
class PasswordStrength:
    """Password strength value object."""
    
    score: int  # 0-100
    level: PasswordStrengthLevel
    feedback: list[str]
    
    def __post_init__(self):
        """Validate password strength."""
        if not 0 <= self.score <= 100:
            raise ValueError("Password strength score must be between 0 and 100")
        
        # Determine level based on score
        if self.score < 30:
            object.__setattr__(self, 'level', PasswordStrengthLevel.WEAK)
        elif self.score < 60:
            object.__setattr__(self, 'level', PasswordStrengthLevel.MEDIUM)
        elif self.score < 80:
            object.__setattr__(self, 'level', PasswordStrengthLevel.STRONG)
        else:
            object.__setattr__(self, 'level', PasswordStrengthLevel.VERY_STRONG)
