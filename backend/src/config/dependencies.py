"""Dependency injection."""
from sqlalchemy.ext.asyncio import AsyncSession

from ..infrastructure.database.database import get_db
from ..infrastructure.database.repositories import (
    BreachRepositoryImpl,
    CredentialRepositoryImpl,
    UserRepositoryImpl,
)
from ..infrastructure.database.password_hasher import PasswordHasher
from ..infrastructure.external_apis.hibp_client import HIBPClient
from ..infrastructure.ml.models.pattern_analyzer import PatternAnalyzer
from ..infrastructure.ml.models.password_classifier import PasswordClassifier
from ..infrastructure.ml.models.risk_predictor import RiskPredictor
from ..application.services.password_analyzer_service import PasswordAnalyzerService
from ..application.services.risk_calculator_service import RiskCalculatorService
from ..infrastructure.notifications.email_service import EmailService
from ..infrastructure.notifications.notification_queue import NotificationQueue
from ..config.settings import settings


# Singleton instances
_hibp_client = None
_password_hasher = None
_password_analyzer = None
_risk_calculator = None
_password_classifier = None
_pattern_analyzer = None
_risk_predictor = None
_email_service = None


def get_hibp_client() -> HIBPClient:
    """Get HIBP client instance."""
    import sys
    global _hibp_client
    # Always create a new client to ensure API key is refreshed from settings
    # (in case .env file was updated)
    api_key = settings.HIBP_API_KEY
    print(f"DEBUG: Creating HIBPClient. API Key from settings: {api_key[:8] if api_key else 'None'}... (length: {len(api_key) if api_key else 0})", file=sys.stderr, flush=True)
    print(f"DEBUG: Creating HIBPClient. API Key from settings: {api_key[:8] if api_key else 'None'}... (length: {len(api_key) if api_key else 0})")
    _hibp_client = HIBPClient(api_key=api_key)
    print(f"DEBUG: HIBPClient created successfully", file=sys.stderr, flush=True)
    return _hibp_client


def get_password_hasher() -> PasswordHasher:
    """Get password hasher instance."""
    global _password_hasher
    if _password_hasher is None:
        _password_hasher = PasswordHasher()
    return _password_hasher


def get_password_analyzer() -> PasswordAnalyzerService:
    """Get password analyzer service instance."""
    global _password_analyzer
    if _password_analyzer is None:
        _password_analyzer = PasswordAnalyzerService()
    return _password_analyzer


def get_risk_calculator() -> RiskCalculatorService:
    """Get risk calculator service instance."""
    global _risk_calculator
    if _risk_calculator is None:
        _risk_calculator = RiskCalculatorService()
    return _risk_calculator


def get_password_classifier() -> PasswordClassifier:
    """Get password classifier instance."""
    global _password_classifier
    if _password_classifier is None:
        _password_classifier = PasswordClassifier()
    return _password_classifier


def get_pattern_analyzer() -> PatternAnalyzer:
    """Get pattern analyzer instance."""
    global _pattern_analyzer
    if _pattern_analyzer is None:
        _pattern_analyzer = PatternAnalyzer()
    return _pattern_analyzer


def get_risk_predictor() -> RiskPredictor:
    """Get risk predictor instance."""
    global _risk_predictor
    if _risk_predictor is None:
        _risk_predictor = RiskPredictor()
    return _risk_predictor


def get_email_service() -> EmailService:
    """Get email service instance."""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service


async def get_breach_repository(session: AsyncSession) -> BreachRepositoryImpl:
    """Get breach repository instance."""
    return BreachRepositoryImpl(session)


async def get_credential_repository(session: AsyncSession) -> CredentialRepositoryImpl:
    """Get credential repository instance."""
    return CredentialRepositoryImpl(session)


async def get_user_repository(session: AsyncSession) -> UserRepositoryImpl:
    """Get user repository instance."""
    return UserRepositoryImpl(session)


async def get_notification_queue(session: AsyncSession) -> NotificationQueue:
    """Get notification queue instance."""
    user_repo = await get_user_repository(session)
    return NotificationQueue(user_repo, session=session)
