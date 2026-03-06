"""Breach API routes."""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...application.use_cases.data_collection.collect_hibp_data import CollectHIBPDataUseCase
from ...config.dependencies import get_breach_repository, get_credential_repository, get_hibp_client
from ...infrastructure.database.database import get_db
from ..schemas.breach_schemas import BreachListResponse, BreachResponse

router = APIRouter(prefix="/breaches", tags=["breaches"])


@router.get("", response_model=BreachListResponse)
async def get_breaches(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    """Get all breaches with pagination."""
    breach_repo = await get_breach_repository(db)
    breaches = await breach_repo.get_all(skip=skip, limit=limit)
    total = await breach_repo.count_all()
    
    return BreachListResponse(
        breaches=[BreachResponse.model_validate(b) for b in breaches],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/{breach_id}", response_model=BreachResponse)
async def get_breach(
    breach_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get breach by ID."""
    breach_repo = await get_breach_repository(db)
    breach = await breach_repo.get_by_id(breach_id)
    
    if not breach:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Breach with ID {breach_id} not found",
        )
    
    return BreachResponse.model_validate(breach)


@router.get("/search", response_model=List[BreachResponse])
async def search_breaches(
    query: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
):
    """Search breaches by query."""
    breach_repo = await get_breach_repository(db)
    breaches = await breach_repo.search(query)
    
    return [BreachResponse.model_validate(b) for b in breaches]


@router.post("/sync")
async def sync_breaches(
    db: AsyncSession = Depends(get_db),
):
    """Synchronize breaches from HIBP API (admin only)."""
    hibp_client = get_hibp_client()
    breach_repo = await get_breach_repository(db)
    credential_repo = await get_credential_repository(db)
    
    use_case = CollectHIBPDataUseCase(hibp_client, breach_repo, credential_repo)
    count = await use_case.sync_all_breaches()
    
    return {
        "success": True,
        "message": f"Synchronized {count} breaches",
        "count": count,
    }
