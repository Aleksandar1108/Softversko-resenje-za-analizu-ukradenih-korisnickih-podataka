"""Use case for analyzing breach trends."""
from datetime import datetime, timedelta
from typing import Dict, List

from src.domain.repositories import BreachRepository, CredentialRepository


class AnalyzeBreachTrendsUseCase:
    """Use case for analyzing trends in breach incidents."""
    
    def __init__(
        self,
        breach_repository: BreachRepository,
        credential_repository: CredentialRepository,
    ):
        """Initialize use case with dependencies."""
        self.breach_repository = breach_repository
        self.credential_repository = credential_repository
    
    async def execute(self, days: int = 30) -> Dict:
        """
        Analyze breach trends over specified period.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with trend analysis
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get recent breaches
        recent_breaches = await self.breach_repository.get_recent(days=days)
        
        # Calculate statistics
        total_breaches = len(recent_breaches)
        verified_breaches = sum(1 for b in recent_breaches if b.is_verified)
        total_credentials = await self.credential_repository.count_by_date_range(
            start_date, end_date
        )
        
        # Group by month
        monthly_stats = {}
        for breach in recent_breaches:
            if breach.breach_date:
                month_key = breach.breach_date.strftime("%Y-%m")
                if month_key not in monthly_stats:
                    monthly_stats[month_key] = {"breaches": 0, "credentials": 0}
                monthly_stats[month_key]["breaches"] += 1
        
        # Most common data classes
        all_data_classes = []
        for breach in recent_breaches:
            all_data_classes.extend(breach.data_classes)
        
        data_class_counts = {}
        for data_class in all_data_classes:
            data_class_counts[data_class] = data_class_counts.get(data_class, 0) + 1
        
        top_data_classes = sorted(
            data_class_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return {
            "period_days": days,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_breaches": total_breaches,
            "verified_breaches": verified_breaches,
            "total_credentials": total_credentials,
            "monthly_trends": monthly_stats,
            "top_data_classes": [{"class": k, "count": v} for k, v in top_data_classes],
            "average_breaches_per_month": total_breaches / max(days / 30, 1),
        }
