"""ML model for analyzing credential risk."""
import pickle
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from src.config.settings import settings
from ..features.advanced_feature_extractor import AdvancedFeatureExtractor


class RiskLevel(Enum):
    """Risk level enumeration."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class CredentialRiskAnalyzer:
    """ML model for analyzing credential risk and generating recommendations."""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize credential risk analyzer.
        
        Args:
            model_path: Optional path to saved model directory
        """
        self.model_path = Path(model_path) if model_path else settings.ML_MODELS_PATH
        self.model_path.mkdir(parents=True, exist_ok=True)
        
        self.feature_extractor = AdvancedFeatureExtractor()
        
        # Risk score predictor (0-100)
        self.risk_predictor: Optional[GradientBoostingRegressor] = None
        
        # Weak password classifier
        self.weak_password_classifier: Optional[RandomForestClassifier] = None
        
        # Feature scaler
        self.scaler: Optional[StandardScaler] = None
        
        self._load_models()
    
    def _load_models(self):
        """Load trained models from files."""
        try:
            # Load risk predictor
            risk_model_path = self.model_path / "risk_predictor.pkl"
            if risk_model_path.exists():
                with open(risk_model_path, "rb") as f:
                    self.risk_predictor = pickle.load(f)
            
            # Load weak password classifier
            weak_model_path = self.model_path / "weak_password_classifier.pkl"
            if weak_model_path.exists():
                with open(weak_model_path, "rb") as f:
                    self.weak_password_classifier = pickle.load(f)
            
            # Load scaler
            scaler_path = self.model_path / "feature_scaler.pkl"
            if scaler_path.exists():
                with open(scaler_path, "rb") as f:
                    self.scaler = pickle.load(f)
            
            # If models don't exist, create default untrained models
            if self.risk_predictor is None:
                self.risk_predictor = GradientBoostingRegressor(
                    n_estimators=100,
                    learning_rate=0.1,
                    max_depth=5,
                    random_state=42,
                )
            
            if self.weak_password_classifier is None:
                self.weak_password_classifier = RandomForestClassifier(
                    n_estimators=100,
                    max_depth=10,
                    random_state=42,
                )
            
            if self.scaler is None:
                self.scaler = StandardScaler()
        
        except Exception as e:
            print(f"Error loading models: {e}")
            # Create default models
            self.risk_predictor = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42,
            )
            self.weak_password_classifier = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
            )
            self.scaler = StandardScaler()
    
    def analyze_credential(
        self,
        password: str,
        email: Optional[str] = None,
        breach_count: int = 0,
    ) -> Dict:
        """
        Analyze credential and return risk assessment.
        
        Args:
            password: Plain text password
            email: Optional email address
            breach_count: Number of breaches this credential appears in
            
        Returns:
            Dictionary with risk_score, risk_level, and recommendations
        """
        # Extract features
        features = self.feature_extractor.extract_all_features(password)
        feature_vector = self.feature_extractor.extract_feature_vector(password)
        
        # Add breach-related features
        features["breach_count"] = float(breach_count)
        
        # Scale features if scaler is fitted
        if self.scaler is not None and hasattr(self.scaler, "mean_"):
            feature_vector_scaled = self.scaler.transform([feature_vector])[0]
        else:
            feature_vector_scaled = feature_vector
        
        # Predict risk score (0-100)
        if self.risk_predictor is not None and hasattr(self.risk_predictor, "feature_importances_"):
            risk_score = self.risk_predictor.predict([feature_vector_scaled])[0]
            risk_score = max(0.0, min(100.0, float(risk_score)))
        else:
            # Use rule-based fallback
            risk_score = self._calculate_rule_based_risk(features)
        
        # Classify as weak password
        is_weak = False
        if self.weak_password_classifier is not None and hasattr(self.weak_password_classifier, "classes_"):
            is_weak = self.weak_password_classifier.predict([feature_vector_scaled])[0] == 1
        else:
            # Use rule-based fallback
            is_weak = self._is_weak_password_rule_based(features)
        
        # Determine risk level
        risk_level = self._determine_risk_level(risk_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(features, risk_score, is_weak)
        
        return {
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level.value,
            "is_weak": is_weak,
            "features": features,
            "recommendations": recommendations,
        }
    
    def _calculate_rule_based_risk(self, features: Dict[str, float]) -> float:
        """Calculate risk score using rule-based approach."""
        risk = 0.0
        
        # Length penalty
        length = features.get("length", 0)
        if length < 8:
            risk += 30.0
        elif length < 12:
            risk += 15.0
        
        # Character variety penalty
        char_types = features.get("char_types", 0)
        if char_types < 2:
            risk += 25.0
        elif char_types < 3:
            risk += 15.0
        
        # Common password penalty
        if features.get("is_common", 0) > 0:
            risk += 40.0
        
        # Dictionary word penalty
        if features.get("contains_dictionary_word", 0) > 0:
            risk += 20.0
        
        # Sequential pattern penalty
        if features.get("has_sequential", 0) > 0:
            risk += 15.0
        
        # Repetition penalty
        if features.get("repeated_chars", 0) > 0:
            risk += 10.0
        
        # Low entropy penalty
        entropy = features.get("entropy", 0)
        if entropy < 2.0:
            risk += 20.0
        elif entropy < 3.0:
            risk += 10.0
        
        # Normalize to 0-100
        return min(100.0, max(0.0, risk))
    
    def _is_weak_password_rule_based(self, features: Dict[str, float]) -> bool:
        """Determine if password is weak using rules."""
        length = features.get("length", 0)
        char_types = features.get("char_types", 0)
        is_common = features.get("is_common", 0)
        entropy = features.get("entropy", 0)
        
        # Weak if: short, few character types, common, or low entropy
        return (
            length < 8
            or char_types < 2
            or is_common > 0
            or entropy < 2.0
        )
    
    def _determine_risk_level(self, risk_score: float) -> RiskLevel:
        """Determine risk level from risk score."""
        if risk_score < 33.0:
            return RiskLevel.LOW
        elif risk_score < 66.0:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.HIGH
    
    def _generate_recommendations(
        self,
        features: Dict[str, float],
        risk_score: float,
        is_weak: bool,
    ) -> List[str]:
        """Generate security recommendations based on analysis."""
        recommendations = []
        
        length = features.get("length", 0)
        char_types = features.get("char_types", 0)
        entropy = features.get("entropy", 0)
        
        if is_weak or risk_score >= 66.0:
            recommendations.append("⚠️ CRITICAL: Change this password immediately!")
        
        if length < 12:
            recommendations.append(f"Use at least 12 characters (currently {int(length)})")
        
        if char_types < 4:
            missing = []
            if features.get("has_uppercase", 0) == 0:
                missing.append("uppercase letters")
            if features.get("has_lowercase", 0) == 0:
                missing.append("lowercase letters")
            if features.get("has_digits", 0) == 0:
                missing.append("numbers")
            if features.get("has_special", 0) == 0:
                missing.append("special characters")
            
            if missing:
                recommendations.append(f"Add {', '.join(missing)}")
        
        if features.get("is_common", 0) > 0:
            recommendations.append("Avoid using common passwords")
        
        if features.get("contains_dictionary_word", 0) > 0:
            recommendations.append("Avoid dictionary words - use random combinations")
        
        if features.get("has_sequential", 0) > 0:
            recommendations.append("Avoid sequential patterns (e.g., 12345, abcde)")
        
        if features.get("repeated_chars", 0) > 0:
            recommendations.append("Avoid repeated characters")
        
        if entropy < 3.0:
            recommendations.append("Increase password complexity to improve entropy")
        
        if not recommendations:
            recommendations.append("✓ Password meets basic security requirements")
        
        return recommendations
    
    def train_models(
        self,
        passwords: List[str],
        risk_scores: List[float],
        is_weak_labels: List[bool],
    ):
        """
        Train ML models on provided data.
        
        Args:
            passwords: List of passwords
            risk_scores: List of risk scores (0-100)
            is_weak_labels: List of weak password labels (True/False)
        """
        # Extract features
        feature_vectors = []
        for password in passwords:
            features = self.feature_extractor.extract_feature_vector(password)
            feature_vectors.append(features)
        
        X = np.array(feature_vectors)
        y_risk = np.array(risk_scores)
        y_weak = np.array([1 if w else 0 for w in is_weak_labels])
        
        # Fit scaler
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)
        
        # Train risk predictor
        self.risk_predictor.fit(X_scaled, y_risk)
        
        # Train weak password classifier
        self.weak_password_classifier.fit(X_scaled, y_weak)
        
        # Save models
        self._save_models()
    
    def _save_models(self):
        """Save trained models to disk."""
        try:
            # Save risk predictor
            risk_model_path = self.model_path / "risk_predictor.pkl"
            with open(risk_model_path, "wb") as f:
                pickle.dump(self.risk_predictor, f)
            
            # Save weak password classifier
            weak_model_path = self.model_path / "weak_password_classifier.pkl"
            with open(weak_model_path, "wb") as f:
                pickle.dump(self.weak_password_classifier, f)
            
            # Save scaler
            scaler_path = self.model_path / "feature_scaler.pkl"
            with open(scaler_path, "wb") as f:
                pickle.dump(self.scaler, f)
        
        except Exception as e:
            print(f"Error saving models: {e}")
