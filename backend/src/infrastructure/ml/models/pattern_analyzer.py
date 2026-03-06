"""Pattern analyzer for passwords."""
import re
from typing import Dict


class PatternAnalyzer:
    """Analyzer for detecting password patterns."""
    
    def __init__(self):
        """Initialize pattern analyzer."""
        # Common password patterns
        self.common_patterns = {
            "common": ["password", "123456", "qwerty", "admin", "welcome"],
            "sequential": ["12345", "abcde", "qwerty", "asdf"],
            "repeated": ["aaaa", "1111", "aaaaa"],
        }
    
    async def analyze(self, password_hash: str) -> Dict:
        """
        Analyze password hash for patterns.
        
        Args:
            password_hash: SHA-1 hash of password
            
        Returns:
            Dictionary with pattern analysis
        """
        # Since we only have hash, pattern detection is limited
        # In production, you'd analyze the actual password
        
        patterns_detected = []
        primary_pattern = None
        
        # Check for sequential patterns in hash
        if self._has_sequential_in_hash(password_hash):
            patterns_detected.append("sequential")
            primary_pattern = "sequential"
        
        # Check for repeated characters
        if self._has_repeated_chars(password_hash):
            patterns_detected.append("repeated")
            if not primary_pattern:
                primary_pattern = "repeated"
        
        return {
            "patterns": patterns_detected,
            "primary_pattern": primary_pattern,
            "complexity": self._calculate_complexity(password_hash),
        }
    
    def analyze_password(self, password: str) -> Dict:
        """
        Analyze actual password for patterns.
        
        Args:
            password: Plain text password
            
        Returns:
            Dictionary with pattern analysis
        """
        patterns_detected = []
        primary_pattern = None
        
        password_lower = password.lower()
        
        # Check for common passwords
        if password_lower in self.common_patterns["common"]:
            patterns_detected.append("common")
            primary_pattern = "common"
        
        # Check for dictionary words
        if self._is_dictionary_word(password_lower):
            patterns_detected.append("dictionary")
            if not primary_pattern:
                primary_pattern = "dictionary"
        
        # Check for sequential patterns
        for seq in self.common_patterns["sequential"]:
            if seq in password_lower:
                patterns_detected.append("sequential")
                if not primary_pattern:
                    primary_pattern = "sequential"
                break
        
        # Check for repeated characters
        if self._has_repeated_chars(password):
            patterns_detected.append("repeated")
            if not primary_pattern:
                primary_pattern = "repeated"
        
        # Check for keyboard patterns
        if self._has_keyboard_pattern(password_lower):
            patterns_detected.append("keyboard")
            if not primary_pattern:
                primary_pattern = "keyboard"
        
        return {
            "patterns": patterns_detected,
            "primary_pattern": primary_pattern,
            "complexity": self._calculate_complexity(password),
        }
    
    def _has_sequential_in_hash(self, hash_str: str) -> bool:
        """Check for sequential patterns in hash."""
        # Simplified check
        sequences = ["0123", "abcd", "ABCD"]
        return any(seq in hash_str for seq in sequences)
    
    def _has_repeated_chars(self, text: str) -> bool:
        """Check for repeated characters."""
        if len(text) < 3:
            return False
        for i in range(len(text) - 2):
            if text[i] == text[i+1] == text[i+2]:
                return True
        return False
    
    def _is_dictionary_word(self, word: str) -> bool:
        """Check if word is a dictionary word (simplified)."""
        # In production, use a proper dictionary
        common_words = {
            "password", "admin", "welcome", "hello", "world",
            "computer", "internet", "email", "user", "login",
        }
        return word in common_words
    
    def _has_keyboard_pattern(self, text: str) -> bool:
        """Check for keyboard patterns."""
        keyboard_rows = [
            "qwertyuiop",
            "asdfghjkl",
            "zxcvbnm",
            "1234567890",
        ]
        
        for row in keyboard_rows:
            for i in range(len(row) - 3):
                pattern = row[i:i+4]
                if pattern in text or pattern[::-1] in text:
                    return True
        
        return False
    
    def _calculate_complexity(self, text: str) -> str:
        """Calculate complexity level."""
        has_upper = any(c.isupper() for c in text)
        has_lower = any(c.islower() for c in text)
        has_digit = any(c.isdigit() for c in text)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in text)
        
        variety = sum([has_upper, has_lower, has_digit, has_special])
        
        if variety >= 4 and len(text) >= 12:
            return "high"
        elif variety >= 3 and len(text) >= 8:
            return "medium"
        else:
            return "low"
