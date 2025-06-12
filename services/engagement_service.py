from datetime import datetime
from models import EngagementAnalysis, db

class EngagementAnalysisService:
    @staticmethod
    def analyze_engagement(user_id: int, platform: str, data: dict) -> EngagementAnalysis:
        """
        Analyze engagement metrics for a user's social media content
        
        Args:
            user_id (int): The ID of the user
            platform (str): The social media platform (e.g., 'facebook', 'instagram')
            data (dict): Raw engagement data from the platform
            
        Returns:
            EngagementAnalysis: The created analysis record
        """
        analysis = EngagementAnalysis(
            user_id=user_id,
            platform=platform,
            analyzed_at=datetime.utcnow(),
            total_likes=data.get('likes', 0),
            total_comments=data.get('comments', 0),
            total_shares=data.get('shares', 0),
            post_count=data.get('post_count', 0)
        )
        
        db.session.add(analysis)
        db.session.commit()
        
        return analysis
    
    @staticmethod
    def get_latest_analysis(user_id: int, platform: str) -> EngagementAnalysis:
        """
        Get the most recent engagement analysis for a user
        
        Args:
            user_id (int): The ID of the user
            platform (str): The social media platform
            
        Returns:
            EngagementAnalysis: The most recent analysis record
        """
        return EngagementAnalysis.query.filter_by(
            user_id=user_id,
            platform=platform
        ).order_by(EngagementAnalysis.analyzed_at.desc()).first()
    
    @staticmethod
    def calculate_engagement_rate(analysis: EngagementAnalysis) -> float:
        """
        Calculate the engagement rate based on total interactions and followers
        
        Args:
            analysis (EngagementAnalysis): The analysis record
            
        Returns:
            float: The calculated engagement rate
        """
        total_interactions = (
            analysis.total_likes + 
            analysis.total_comments + 
            analysis.total_shares
        )
        
        if analysis.post_count == 0:
            return 0.0
            
        return (total_interactions / analysis.post_count) * 100 