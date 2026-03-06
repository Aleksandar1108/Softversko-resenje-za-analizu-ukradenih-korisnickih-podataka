"""Risk predictor ML model."""
import pickle
from pathlib import Path
from typing import Dict, Optional

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

from ...config.settings import settings


class RiskPredictor:
    """ML model for predicting risk scores."""
    
    def __init__(self, model_path: Optional[str] = None):
        """Initialize risk predictor."""
        self.model_path = model_path or settings.ML_MODELS_PATH / "risk_predictor.pkl"
        self.model: Optional[GradientBoostingRegressor] = None
        self._load_model()
    
    def _load_model(self):
        """Load trained model from file."""
        try:
            if Path(self.model_path).exists():
                with open(self.model_path, "rb") as f:
                    self.model = pickle.load(f)
            else:
                # Create a default untrained model
                self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    
    async def predict(self, features: Dict) -> float:
        """
        Predict risk score from features.
        
        Args:
            features: Feature dictionary
            
        Returns:
            Predicted risk score (0.0-10.0)
        """
        # Extract feature vector
        feature_vector = self._extract_features(features)
        
        if self.model is None:
            # Return default risk score
            return 5.0
        
        # Predict
        prediction = self.model.predict([feature_vector])[0]
        
        # Normalize to 0.0-10.0
        prediction = max(0.0, min(10.0, float(prediction)))
        
        return prediction
    
    def _extract_features(self, features: Dict) -> np.ndarray:
        """
        Extract feature vector from features dictionary.
        
        Args:
            features: Feature dictionary
            
        Returns:
            Feature vector
        """
        # Extract features
        feature_list = [
            features.get("strength", 50),
            features.get("length", 0),
            features.get("has_upper", 0),
            features.get("has_lower", 0),
            features.get("has_digit", 0),
            features.get("has_special", 0),
            features.get("is_common", 0),
            features.get("days_old", 0),
        ]
        
        return np.array(feature_list)
    
    def train(self, X, y):
        """
        Train the predictor model.
        
        Args:
            X: Feature matrix
            y: Target risk scores
        """
        if self.model is None:
            self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        
        self.model.fit(X, y)
        
        # Save model
        Path(self.model_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.model_path, "wb") as f:
            pickle.dump(self.model, f)
