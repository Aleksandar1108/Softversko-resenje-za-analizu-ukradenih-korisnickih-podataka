"""Training script for ML models."""
import asyncio
import logging
from pathlib import Path
from typing import List, Tuple

import pandas as pd

from src.config.settings import settings
from ..models.credential_risk_analyzer import CredentialRiskAnalyzer
from ..features.advanced_feature_extractor import AdvancedFeatureExtractor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_synthetic_training_data(n_samples: int = 10000) -> Tuple[List[str], List[float], List[bool]]:
    """
    Generate synthetic training data for model training.
    
    In production, use real breach data.
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        Tuple of (passwords, risk_scores, is_weak_labels)
    """
    passwords = []
    risk_scores = []
    is_weak_labels = []
    
    feature_extractor = AdvancedFeatureExtractor()
    
    # Generate weak passwords
    weak_passwords = [
        "password", "123456", "qwerty", "abc123", "welcome",
        "admin", "letmein", "monkey", "12345", "password1",
        "123", "abc", "test", "guest", "root",
    ]
    
    for pwd in weak_passwords * (n_samples // 30):
        passwords.append(pwd)
        features = feature_extractor.extract_all_features(pwd)
        risk = 80.0 + (hash(pwd) % 20)  # High risk
        risk_scores.append(risk)
        is_weak_labels.append(True)
    
    # Generate medium passwords
    medium_passwords = [
        "Password123", "MyPass2020", "Secure1", "User1234",
        "Welcome1", "Admin2020", "Test1234", "Guest123",
    ]
    
    for pwd in medium_passwords * (n_samples // 20):
        passwords.append(pwd)
        features = feature_extractor.extract_all_features(pwd)
        risk = 40.0 + (hash(pwd) % 30)  # Medium risk
        risk_scores.append(risk)
        is_weak_labels.append(False)
    
    # Generate strong passwords
    import random
    import string
    
    for _ in range(n_samples // 2):
        # Generate random strong password
        length = random.randint(12, 20)
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        pwd = ''.join(random.choice(chars) for _ in range(length))
        
        passwords.append(pwd)
        features = feature_extractor.extract_all_features(pwd)
        risk = 10.0 + (hash(pwd) % 30)  # Low risk
        risk_scores.append(risk)
        is_weak_labels.append(False)
    
    return passwords, risk_scores, is_weak_labels


async def train_models_from_data(
    passwords: List[str],
    risk_scores: List[float],
    is_weak_labels: List[bool],
    model_path: Path = None,
):
    """
    Train ML models from provided data.
    
    Args:
        passwords: List of passwords
        risk_scores: List of risk scores (0-100)
        is_weak_labels: List of weak password labels
        model_path: Optional path to save models
    """
    logger.info(f"Training models on {len(passwords)} samples...")
    
    analyzer = CredentialRiskAnalyzer(model_path=model_path)
    
    # Train models
    analyzer.train_models(passwords, risk_scores, is_weak_labels)
    
    logger.info("Models trained and saved successfully")


async def train_models_from_csv(csv_path: str, model_path: Path = None):
    """
    Train models from CSV file.
    
    CSV should have columns: password, risk_score, is_weak
    
    Args:
        csv_path: Path to CSV file
        model_path: Optional path to save models
    """
    logger.info(f"Loading training data from {csv_path}...")
    
    df = pd.read_csv(csv_path)
    
    passwords = df["password"].tolist()
    risk_scores = df["risk_score"].tolist()
    is_weak_labels = df["is_weak"].astype(bool).tolist()
    
    await train_models_from_data(passwords, risk_scores, is_weak_labels, model_path)


async def main():
    """Main training function."""
    logger.info("Starting model training...")
    
    # Generate synthetic data (in production, use real breach data)
    passwords, risk_scores, is_weak_labels = generate_synthetic_training_data(n_samples=5000)
    
    # Train models
    await train_models_from_data(
        passwords=passwords,
        risk_scores=risk_scores,
        is_weak_labels=is_weak_labels,
        model_path=settings.ML_MODELS_PATH,
    )
    
    logger.info("Training completed!")


if __name__ == "__main__":
    asyncio.run(main())
