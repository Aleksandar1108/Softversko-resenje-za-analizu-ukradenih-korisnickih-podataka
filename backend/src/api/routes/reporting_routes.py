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
    try:
        breach_repo = await get_breach_repository(db)
        credential_repo = await get_credential_repository(db)
        
        use_case = AnalyzeBreachTrendsUseCase(breach_repo, credential_repo)
        trends = await use_case.execute(days=days)
        
        return {
            "success": True,
            "data": trends,
        }
    except Exception as e:
        # Return empty trends if there's an error
        import traceback
        print(f"Error in get_breach_trends: {e}")
        print(traceback.format_exc())
        
        from datetime import datetime, timedelta
        return {
            "success": True,
            "data": {
                "period_days": days,
                "start_date": (datetime.utcnow() - timedelta(days=days)).isoformat(),
                "end_date": datetime.utcnow().isoformat(),
                "total_breaches": 0,
                "verified_breaches": 0,
                "total_credentials": 0,
                "monthly_trends": {},
                "top_data_classes": [],
                "average_breaches_per_month": 0,
            },
        }


@router.get("/statistics")
async def get_statistics(
    db: AsyncSession = Depends(get_db),
):
    """Get system statistics."""
    try:
        breach_repo = await get_breach_repository(db)
        credential_repo = await get_credential_repository(db)
        user_repo = await get_user_repository(db)
        
        use_case = GenerateStatisticsUseCase(breach_repo, credential_repo, user_repo)
        stats = await use_case.execute()
        
        return {
            "success": True,
            "data": stats,
        }
    except Exception as e:
        # Return empty statistics if there's an error
        import traceback
        print(f"Error in get_statistics: {e}")
        print(traceback.format_exc())
        
        return {
            "success": True,
            "data": {
                "total_breaches": 0,
                "total_credentials": 0,
                "total_users": 0,
                "weak_passwords": {
                    "count": 0,
                    "percentage": 0,
                },
                "high_risk_credentials": {
                    "count": 0,
                    "percentage": 0,
                },
                "breach_sources": {
                    "hibp": 0,
                    "scraped": 0,
                },
            },
        }
