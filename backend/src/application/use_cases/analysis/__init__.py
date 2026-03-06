"""Analysis use cases."""
from .analyze_credentials import AnalyzeCredentialsUseCase
from .detect_weak_passwords import DetectWeakPasswordsUseCase
from .generate_recommendations import GenerateRecommendationsUseCase

__all__ = [
    "AnalyzeCredentialsUseCase",
    "DetectWeakPasswordsUseCase",
    "GenerateRecommendationsUseCase",
]
