"""Data collection API routes."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.dependencies import (
    get_breach_repository,
    get_credential_repository,
    get_hibp_client,
)
from src.infrastructure.database.database import get_db
from src.infrastructure.external_apis.breach_scraper import BreachScraper
from src.infrastructure.external_apis.data_collector_service import DataCollectorService
from src.api.middleware.auth_middleware import get_current_user_id

router = APIRouter(prefix="/data-collection", tags=["data-collection"])


@router.post("/sync/hibp")
async def sync_hibp_breaches(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),  # Require authentication
):
    """
    Manually trigger HIBP breach synchronization.
    Requires authentication.
    """
    hibp_client = get_hibp_client()
    breach_repo = await get_breach_repository(db)
    credential_repo = await get_credential_repository(db)
    breach_scraper = BreachScraper()
    
    data_collector = DataCollectorService(
        hibp_client=hibp_client,
        breach_scraper=breach_scraper,
        breach_repository=breach_repo,
        credential_repository=credential_repo,
    )
    
    try:
        stats = await data_collector.collect_from_hibp()
        return {
            "success": True,
            "message": "HIBP synchronization completed",
            "statistics": stats,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during synchronization: {str(e)}",
        )


@router.post("/scrape")
async def scrape_web_sources(
    sources: List[str],
    parse_credentials: bool = True,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id),  # Require authentication
):
    """
    Manually trigger web scraping from specified sources.
    Requires authentication.
    
    Args:
        sources: List of URLs to scrape
        parse_credentials: Whether to parse email/password data
    """
    hibp_client = get_hibp_client()
    breach_repo = await get_breach_repository(db)
    credential_repo = await get_credential_repository(db)
    breach_scraper = BreachScraper()
    
    data_collector = DataCollectorService(
        hibp_client=hibp_client,
        breach_scraper=breach_scraper,
        breach_repository=breach_repo,
        credential_repository=credential_repo,
    )
    
    try:
        stats = await data_collector.collect_from_web_scraping(
            sources=sources,
            parse_credentials=parse_credentials,
        )
        return {
            "success": True,
            "message": "Web scraping completed",
            "statistics": stats,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during scraping: {str(e)}",
        )


@router.post("/collect/all")
async def collect_all_data(
    sources: List[str] = None,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id),  # Require authentication
):
    """
    Manually trigger collection from all sources.
    Requires authentication.
    
    Args:
        sources: Optional list of web sources to scrape
    """
    hibp_client = get_hibp_client()
    breach_repo = await get_breach_repository(db)
    credential_repo = await get_credential_repository(db)
    breach_scraper = BreachScraper()
    
    data_collector = DataCollectorService(
        hibp_client=hibp_client,
        breach_scraper=breach_scraper,
        breach_repository=breach_repo,
        credential_repository=credential_repo,
    )
    
    try:
        stats = await data_collector.collect_all(sources=sources)
        return {
            "success": True,
            "message": "Data collection completed",
            "statistics": stats,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during collection: {str(e)}",
        )
