"""Password classifier ML model."""
import pickle
from pathlib import Path
from typing import Dict, Optional

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from src.config.settings import settings


class PasswordClassifier:
    """ML model for classifying password strength."""
    
    def __init__(self, model_path: Optional[str] = None):
        """Initialize password classifier."""
        self.model_path = model_path or settings.ML_MODELS_PATH / "password_classifier.pkl"
        self.model: Optional[RandomForestClassifier] = None
        self._load_model()
    
    def _load_model(self):
        """Load trained model from file."""
        try:
            if Path(self.model_path).exists():
                with open(self.model_path, "rb") as f:
                    self.model = pickle.load(f)
            else:
                # Create a default untrained model
                self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    async def classify(self, password_hash: str) -> Dict:
        """
        Classify password based on hash.
        
        Args:
            password_hash: SHA-1 hash of password
            
        Returns:
            Classification result
        """
        # Extract features from hash
        features = self._extract_features(password_hash)
        
        if self.model is None:
            # Return default classification
            return {
                "class": "unknown",
                "confidence": 0.0,
                "features": features,
            }
        
        # Predict
        prediction = self.model.predict([features])[0]
        probabilities = self.model.predict_proba([features])[0]
        confidence = float(max(probabilities))
        
        return {
            "class": prediction,
            "confidence": confidence,
            "features": features,
        }
    
    def _extract_features(self, password_hash: str) -> np.ndarray:
        """
        Extract features from password hash.
        
        Args:
            password_hash: SHA-1 hash string
            
        Returns:
            Feature vector
        """
        # Basic features from hash
        features = [
            len(password_hash),  # Hash length
            password_hash.count("0"),  # Number of zeros
            password_hash.count("A"),  # Number of uppercase hex
            password_hash.count("a"),  # Number of lowercase hex
            sum(1 for c in password_hash if c.isdigit()),  # Digits
            sum(1 for c in password_hash if c.isalpha()),  # Letters
        ]
        
        return np.array(features)
    
    def train(self, X, y):
        """
        Train the classifier model.
        
        Args:
            X: Feature matrix
            y: Target labels
        """
        if self.model is None:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        self.model.fit(X, y)
        
        # Save model
        Path(self.model_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.model_path, "wb") as f:
            pickle.dump(self.model, f)
