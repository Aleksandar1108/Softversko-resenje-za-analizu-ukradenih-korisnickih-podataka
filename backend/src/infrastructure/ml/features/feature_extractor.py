"""Feature extraction for ML models."""
from typing import Dict


class FeatureExtractor:
    """Extract features from credentials for ML models."""
    
    @staticmethod
    def extract_password_features(password: str) -> Dict:
        """
        Extract features from password.
        
        Args:
            password: Plain text password
            
        Returns:
            Dictionary of features
        """
        return {
            "length": len(password),
            "has_upper": any(c.isupper() for c in password),
            "has_lower": any(c.islower() for c in password),
            "has_digit": any(c.isdigit() for c in password),
            "has_special": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password),
            "entropy": FeatureExtractor._calculate_entropy(password),
            "is_common": password.lower() in ["password", "123456", "qwerty"],
        }
    
    @staticmethod
    def extract_credential_features(credential) -> Dict:
        """
        Extract features from credential entity.
        
        Args:
            credential: Credential entity
            
        Returns:
            Dictionary of features
        """
        from datetime import datetime
        
        features = {
            "strength": credential.password_strength_score or 0,
            "is_weak": credential.is_weak,
        }
        
        if credential.discovered_date:
            days_old = (datetime.utcnow() - credential.discovered_date).days
            features["days_old"] = days_old
        else:
            features["days_old"] = 0
        
        if credential.pattern_type:
            features["pattern_type"] = credential.pattern_type
        
        return features
    
    @staticmethod
    def _calculate_entropy(text: str) -> float:
        """Calculate Shannon entropy of text."""
        import math
        from collections import Counter
        
        if not text:
            return 0.0
        
        length = len(text)
        counts = Counter(text)
        entropy = 0.0
        
        for count in counts.values():
            probability = count / length
            entropy -= probability * math.log2(probability)
        
        return entropy
