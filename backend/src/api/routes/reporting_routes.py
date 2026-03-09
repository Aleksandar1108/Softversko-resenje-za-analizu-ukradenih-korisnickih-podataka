"""Reporting API routes."""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.config.dependencies import (
    get_breach_repository,
    get_credential_repository,
    get_user_repository,
    get_hibp_client,
)
from src.infrastructure.database.database import get_db
from src.application.use_cases.reporting.analyze_breach_trends import AnalyzeBreachTrendsUseCase
from src.application.use_cases.reporting.generate_statistics import GenerateStatisticsUseCase
from src.api.middleware.auth_middleware import get_optional_user_id
from src.infrastructure.database.models.user_breach_model import UserBreachModel
from src.infrastructure.database.models.breach_model import BreachModel

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
    user_id: Optional[UUID] = Depends(get_optional_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get statistics - user-specific if logged in, system-wide otherwise."""
    try:
        # If user is logged in, return user-specific statistics
        if user_id:
            user_repo = await get_user_repository(db)
            user = await user_repo.get_by_id(user_id)
            
            if not user:
                return {
                    "success": True,
                    "data": {
                        "total_breaches": 0,
                        "breaches": [],
                        "risk_level": "low",
                        "data_types_count": {},
                        "total_credentials": 0,
                        "weak_passwords": {"count": 0, "percentage": 0},
                        "high_risk_credentials": {"count": 0, "percentage": 0},
                        "breach_sources": {"hibp": 0, "scraped": 0},
                    },
                }
            
            # Get user breaches from database
            result = await db.execute(
                select(UserBreachModel, BreachModel)
                .join(BreachModel, UserBreachModel.breach_id == BreachModel.id)
                .where(UserBreachModel.user_id == user_id)
                .order_by(BreachModel.breach_date.desc() if BreachModel.breach_date else BreachModel.added_date.desc())
            )
            user_breaches_data = result.all()
            
            breaches_list = []
            data_types_count = {}
            hibp_count = 0
            scraped_count = 0
            
            for user_breach, breach in user_breaches_data:
                breach_dict = {
                    "id": str(breach.id),
                    "name": breach.name,
                    "domain": breach.domain,
                    "breach_date": breach.breach_date.isoformat() if breach.breach_date else None,
                    "data_classes": breach.data_classes or [],
                }
                breaches_list.append(breach_dict)
                
                # Count data types
                for data_class in breach.data_classes or []:
                    data_types_count[data_class] = data_types_count.get(data_class, 0) + 1
                
                # Count sources
                if breach.source == 'hibp':
                    hibp_count += 1
                elif breach.source == 'scraped':
                    scraped_count += 1
            
            total_breaches = len(breaches_list)
            
            # Calculate risk level
            if total_breaches == 0:
                risk_level = "low"
            elif total_breaches <= 3:
                risk_level = "medium"
            else:
                risk_level = "high"
            
            # Get credentials for user (if any)
            credential_repo = await get_credential_repository(db)
            user_credentials = await credential_repo.get_by_email(user.email)
            total_credentials = len(user_credentials)
            
            weak_passwords_count = sum(1 for c in user_credentials if getattr(c, 'is_weak', False))
            high_risk_count = sum(1 for c in user_credentials if getattr(c, 'risk_score', 0) > 70)
            
            weak_passwords_percentage = (weak_passwords_count / total_credentials * 100) if total_credentials > 0 else 0
            high_risk_percentage = (high_risk_count / total_credentials * 100) if total_credentials > 0 else 0
            
            return {
                "success": True,
                "data": {
                    "total_breaches": total_breaches,
                    "breaches": breaches_list,
                    "risk_level": risk_level,
                    "data_types_count": data_types_count,
                    "total_credentials": total_credentials,
                    "weak_passwords": {
                        "count": weak_passwords_count,
                        "percentage": round(weak_passwords_percentage, 2),
                    },
                    "high_risk_credentials": {
                        "count": high_risk_count,
                        "percentage": round(high_risk_percentage, 2),
                    },
                    "breach_sources": {
                        "hibp": hibp_count,
                        "scraped": scraped_count,
                    },
                },
            }
        else:
            # System-wide statistics for non-authenticated users
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
                "breaches": [],
                "risk_level": "low",
                "data_types_count": {},
                "total_credentials": 0,
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
