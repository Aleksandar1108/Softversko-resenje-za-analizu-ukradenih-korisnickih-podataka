"""Reporting API routes."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.dependencies import (
    get_breach_repository,
    get_credential_repository,
    get_user_repository,
)
from src.infrastructure.database.database import get_db
from src.application.use_cases.reporting.analyze_breach_trends import AnalyzeBreachTrendsUseCase
from src.application.use_cases.reporting.generate_statistics import GenerateStatisticsUseCase

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/trends")
async def get_breach_trends(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
):
    """Get breach trends analysis."""
    breach_repo = await get_breach_repository(db)
    credential_repo = await get_credential_repository(db)
    
    use_case = AnalyzeBreachTrendsUseCase(breach_repo, credential_repo)
    trends = await use_case.execute(days=days)
    
    return {
        "success": True,
        "data": trends,
    }


@router.get("/statistics")
async def get_statistics(
    db: AsyncSession = Depends(get_db),
):
    """Get system statistics."""
    breach_repo = await get_breach_repository(db)
    credential_repo = await get_credential_repository(db)
    user_repo = await get_user_repository(db)
    
    use_case = GenerateStatisticsUseCase(breach_repo, credential_repo, user_repo)
    stats = await use_case.execute()
    
    return {
        "success": True,
        "data": stats,
    }
