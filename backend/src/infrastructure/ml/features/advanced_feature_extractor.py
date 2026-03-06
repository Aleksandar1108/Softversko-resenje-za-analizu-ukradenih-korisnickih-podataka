"""Advanced feature extraction for credential analysis."""
import math
import re
from collections import Counter
from typing import Dict, List, Set

import numpy as np


class AdvancedFeatureExtractor:
    """Advanced feature extraction for password and credential analysis."""
    
    # Common passwords list (extended)
    COMMON_PASSWORDS: Set[str] = {
        "password", "123456", "123456789", "12345678", "12345",
        "1234567", "1234567890", "qwerty", "abc123", "password1",
        "welcome", "admin", "letmein", "monkey", "1234567890",
        "dragon", "master", "sunshine", "shadow", "princess",
        "football", "michael", "jesus", "superman", "harley",
    }
    
    # Dictionary words (common English words)
    DICTIONARY_WORDS: Set[str] = {
        "password", "admin", "welcome", "hello", "world",
        "computer", "internet", "email", "user", "login",
        "secret", "private", "secure", "access", "account",
    }
    
    # Sequential patterns
    SEQUENTIAL_PATTERNS: List[str] = [
        "0123456789", "abcdefghijklmnopqrstuvwxyz",
        "qwertyuiop", "asdfghjkl", "zxcvbnm",
        "9876543210", "zyxwvutsrqponmlkjihgfedcba",
    ]
    
    def __init__(self):
        """Initialize feature extractor."""
        pass
    
    def extract_all_features(self, password: str) -> Dict[str, float]:
        """
        Extract all features from password.
        
        Args:
            password: Plain text password
            
        Returns:
            Dictionary of extracted features
        """
        features = {}
        
        # Basic features
        features.update(self._extract_basic_features(password))
        
        # Complexity features
        features.update(self._extract_complexity_features(password))
        
        # Pattern features
        features.update(self._extract_pattern_features(password))
        
        # Dictionary features
        features.update(self._extract_dictionary_features(password))
        
        # Entropy features
        features.update(self._extract_entropy_features(password))
        
        return features
    
    def _extract_basic_features(self, password: str) -> Dict[str, float]:
        """Extract basic password features."""
        length = len(password)
        
        return {
            "length": float(length),
            "has_uppercase": float(any(c.isupper() for c in password)),
            "has_lowercase": float(any(c.islower() for c in password)),
            "has_digits": float(any(c.isdigit() for c in password)),
            "has_special": float(any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)),
            "digit_count": float(sum(1 for c in password if c.isdigit())),
            "special_count": float(sum(1 for c in password if c in "!@#$%^&*()_+-=[]{}|;:,.<>?")),
            "upper_count": float(sum(1 for c in password if c.isupper())),
            "lower_count": float(sum(1 for c in password if c.islower())),
        }
    
    def _extract_complexity_features(self, password: str) -> Dict[str, float]:
        """Extract complexity-related features."""
        length = len(password)
        
        # Character variety
        unique_chars = len(set(password))
        char_variety_ratio = unique_chars / length if length > 0 else 0.0
        
        # Character type variety (0-4)
        char_types = sum([
            any(c.isupper() for c in password),
            any(c.islower() for c in password),
            any(c.isdigit() for c in password),
            any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password),
        ])
        
        return {
            "unique_chars": float(unique_chars),
            "char_variety_ratio": char_variety_ratio,
            "char_types": float(char_types),
            "repetition_ratio": 1.0 - char_variety_ratio,
        }
    
    def _extract_pattern_features(self, password: str) -> Dict[str, float]:
        """Extract pattern-related features."""
        password_lower = password.lower()
        
        # Sequential patterns
        has_sequential = 0.0
        sequential_count = 0
        
        for pattern in self.SEQUENTIAL_PATTERNS:
            for i in range(len(pattern) - 3):
                seq = pattern[i:i+4]
                if seq in password_lower or seq[::-1] in password_lower:
                    has_sequential = 1.0
                    sequential_count += 1
        
        # Repeated characters
        repeated_chars = 0
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                repeated_chars += 1
        
        # Keyboard patterns
        keyboard_rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm", "1234567890"]
        keyboard_patterns = 0
        
        for row in keyboard_rows:
            for i in range(len(row) - 3):
                pattern = row[i:i+4]
                if pattern in password_lower or pattern[::-1] in password_lower:
                    keyboard_patterns += 1
        
        # Consecutive same character
        max_consecutive = 0
        current_consecutive = 1
        
        for i in range(1, len(password)):
            if password[i] == password[i-1]:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 1
        
        return {
            "has_sequential": has_sequential,
            "sequential_count": float(sequential_count),
            "repeated_chars": float(repeated_chars),
            "keyboard_patterns": float(keyboard_patterns),
            "max_consecutive": float(max_consecutive),
        }
    
    def _extract_dictionary_features(self, password: str) -> Dict[str, float]:
        """Extract dictionary-related features."""
        password_lower = password.lower()
        
        # Check if password is common
        is_common = 1.0 if password_lower in self.COMMON_PASSWORDS else 0.0
        
        # Check for dictionary words
        contains_dictionary_word = 0.0
        dictionary_word_count = 0
        
        for word in self.DICTIONARY_WORDS:
            if word in password_lower:
                contains_dictionary_word = 1.0
                dictionary_word_count += 1
        
        # Check for common substitutions (l33t speak)
        leet_substitutions = {
            "a": "4", "e": "3", "i": "1", "o": "0", "s": "5", "t": "7",
        }
        has_leet = 0.0
        for char, sub in leet_substitutions.items():
            if sub in password:
                has_leet = 1.0
                break
        
        return {
            "is_common": is_common,
            "contains_dictionary_word": contains_dictionary_word,
            "dictionary_word_count": float(dictionary_word_count),
            "has_leet": has_leet,
        }
    
    def _extract_entropy_features(self, password: str) -> Dict[str, float]:
        """Extract entropy-related features."""
        if not password:
            return {
                "entropy": 0.0,
                "entropy_per_char": 0.0,
                "effective_length": 0.0,
            }
        
        # Shannon entropy
        length = len(password)
        counts = Counter(password)
        entropy = 0.0
        
        for count in counts.values():
            probability = count / length
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        # Effective password length (based on character set)
        char_set_size = 0
        if any(c.isupper() for c in password):
            char_set_size += 26
        if any(c.islower() for c in password):
            char_set_size += 26
        if any(c.isdigit() for c in password):
            char_set_size += 10
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            char_set_size += len("!@#$%^&*()_+-=[]{}|;:,.<>?")
        
        effective_length = length * math.log2(char_set_size) if char_set_size > 0 else 0.0
        
        return {
            "entropy": entropy,
            "entropy_per_char": entropy / length if length > 0 else 0.0,
            "effective_length": effective_length,
        }
    
    def extract_feature_vector(self, password: str) -> np.ndarray:
        """
        Extract feature vector as numpy array for ML models.
        
        Args:
            password: Plain text password
            
        Returns:
            Feature vector as numpy array
        """
        features = self.extract_all_features(password)
        
        # Order features consistently
        feature_order = [
            "length",
            "has_uppercase",
            "has_lowercase",
            "has_digits",
            "has_special",
            "digit_count",
            "special_count",
            "upper_count",
            "lower_count",
            "unique_chars",
            "char_variety_ratio",
            "char_types",
            "repetition_ratio",
            "has_sequential",
            "sequential_count",
            "repeated_chars",
            "keyboard_patterns",
            "max_consecutive",
            "is_common",
            "contains_dictionary_word",
            "dictionary_word_count",
            "has_leet",
            "entropy",
            "entropy_per_char",
            "effective_length",
        ]
        
        return np.array([features.get(key, 0.0) for key in feature_order])
