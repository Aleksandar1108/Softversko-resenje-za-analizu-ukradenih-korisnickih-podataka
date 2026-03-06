"""Service for analyzing password strength."""
from src.domain.value_objects.password_strength import (
    PasswordStrength,
    PasswordStrengthLevel,
)


class PasswordAnalyzerService:
    """Service for analyzing password strength."""
    
    def __init__(self):
        """Initialize password analyzer service."""
        # Common passwords list (simplified - in production, use larger dataset)
        self.common_passwords = {
            "password", "123456", "123456789", "12345678", "12345",
            "1234567", "1234567890", "qwerty", "abc123", "password1",
        }
    
    async def analyze_password_strength(self, password_hash: str) -> PasswordStrength:
        """
        Analyze password strength from hash.
        
        Note: In production, you might need the actual password.
        This is a simplified version that works with hash patterns.
        
        Args:
            password_hash: SHA-1 hash of the password
            
        Returns:
            PasswordStrength value object
        """
        # Since we only have hash, we'll use basic heuristics
        # In real scenario, you'd analyze the actual password
        
        # Basic scoring (simplified)
        score = 50  # Base score
        
        # Check hash length (longer hashes might indicate longer passwords)
        if len(password_hash) > 40:
            score += 10
        
        # Check for common patterns in hash
        # This is a simplified approach - real analysis needs the password
        
        # Determine level
        if score < 30:
            level = PasswordStrengthLevel.WEAK
        elif score < 60:
            level = PasswordStrengthLevel.MEDIUM
        elif score < 80:
            level = PasswordStrengthLevel.STRONG
        else:
            level = PasswordStrengthLevel.VERY_STRONG
        
        feedback = []
        if score < 30:
            feedback.append("Password is too weak")
            feedback.append("Use at least 12 characters")
            feedback.append("Include uppercase, lowercase, numbers, and symbols")
        
        return PasswordStrength(
            score=score,
            level=level,
            feedback=feedback,
        )
    
    def analyze_password(self, password: str) -> PasswordStrength:
        """
        Analyze actual password (when available).
        
        Args:
            password: Plain text password
            
        Returns:
            PasswordStrength value object
        """
        score = 0
        feedback = []
        
        # Length check
        length = len(password)
        if length < 8:
            feedback.append("Password is too short (minimum 8 characters)")
        elif length < 12:
            score += 10
            feedback.append("Consider using at least 12 characters")
        else:
            score += 20
        
        # Character variety
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        char_variety = sum([has_upper, has_lower, has_digit, has_special])
        score += char_variety * 15
        
        if not has_upper:
            feedback.append("Add uppercase letters")
        if not has_lower:
            feedback.append("Add lowercase letters")
        if not has_digit:
            feedback.append("Add numbers")
        if not has_special:
            feedback.append("Add special characters")
        
        # Check for common passwords
        if password.lower() in self.common_passwords:
            score = max(0, score - 50)
            feedback.append("This is a very common password - avoid it!")
        
        # Check for patterns
        if self._has_sequential_pattern(password):
            score = max(0, score - 20)
            feedback.append("Avoid sequential patterns (e.g., 12345, abcde)")
        
        if self._has_repeated_pattern(password):
            score = max(0, score - 15)
            feedback.append("Avoid repeated characters")
        
        # Normalize score to 0-100
        score = min(100, max(0, score))
        
        # Determine level
        if score < 30:
            level = PasswordStrengthLevel.WEAK
        elif score < 60:
            level = PasswordStrengthLevel.MEDIUM
        elif score < 80:
            level = PasswordStrengthLevel.STRONG
        else:
            level = PasswordStrengthLevel.VERY_STRONG
        
        return PasswordStrength(
            score=score,
            level=level,
            feedback=feedback,
        )
    
    def _has_sequential_pattern(self, password: str) -> bool:
        """Check if password contains sequential patterns."""
        sequences = ["12345", "abcde", "qwerty", "asdf"]
        password_lower = password.lower()
        return any(seq in password_lower for seq in sequences)
    
    def _has_repeated_pattern(self, password: str) -> bool:
        """Check if password contains repeated characters."""
        if len(password) < 3:
            return False
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                return True
        return False
