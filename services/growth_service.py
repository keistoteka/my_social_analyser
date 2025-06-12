from datetime import datetime
from models import GrowthAnalysis, db

class GrowthAnalysisService:
    @staticmethod
    def analyze_growth(
        user_id: int, 
        platform: str, 
        start_followers: int,
        end_followers: int,
        start_engagement: float,
        end_engagement: float
    ) -> GrowthAnalysis:
        """
        Analyze follower growth and engagement changes
        
        Args:
            user_id (int): The ID of the user
            platform (str): The social media platform
            start_followers (int): Number of followers at start
            end_followers (int): Number of followers at end
            start_engagement (float): Engagement rate at start
            end_engagement (float): Engagement rate at end
            
        Returns:
            GrowthAnalysis: The created analysis record
        """
        # Calculate growth rate
        if start_followers == 0:
            growth_rate = 0
        else:
            growth_rate = ((end_followers - start_followers) / start_followers) * 100
            
        # Calculate engagement change
        engagement_change = end_engagement - start_engagement
        
        analysis = GrowthAnalysis(
            user_id=user_id,
            platform=platform,
            analyzed_at=datetime.utcnow(),
            start_followers=start_followers,
            end_followers=end_followers,
            growth_rate=growth_rate,
            engagement_change=engagement_change
        )
        
        db.session.add(analysis)
        db.session.commit()
        
        return analysis
    
    @staticmethod
    def get_latest_analysis(user_id: int, platform: str) -> GrowthAnalysis:
        """
        Get the most recent growth analysis for a user
        
        Args:
            user_id (int): The ID of the user
            platform (str): The social media platform
            
        Returns:
            GrowthAnalysis: The most recent analysis record
        """
        return GrowthAnalysis.query.filter_by(
            user_id=user_id,
            platform=platform
        ).order_by(GrowthAnalysis.analyzed_at.desc()).first()
    
    @staticmethod
    def get_growth_trend(user_id: int, platform: str, days: int = 30) -> list:
        """
        Get growth trend over a specified period
        
        Args:
            user_id (int): The ID of the user
            platform (str): The social media platform
            days (int): Number of days to analyze
            
        Returns:
            list: List of growth analysis records
        """
        return GrowthAnalysis.query.filter_by(
            user_id=user_id,
            platform=platform
        ).order_by(GrowthAnalysis.analyzed_at.desc()).limit(days).all() 