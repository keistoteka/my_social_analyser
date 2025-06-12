from datetime import datetime
from models import ContentAnalysis, db
from collections import Counter

class ContentAnalysisService:
    @staticmethod
    def analyze_content(
        user_id: int,
        platform: str,
        posts: list,
        content_types: list
    ) -> ContentAnalysis:
        """
        Analyze content performance and types
        
        Args:
            user_id (int): The ID of the user
            platform (str): The social media platform
            posts (list): List of post data including engagement metrics
            content_types (list): List of content types for each post
            
        Returns:
            ContentAnalysis: The created analysis record
        """
        # Find top performing content type
        type_counter = Counter(content_types)
        top_content_type = type_counter.most_common(1)[0][0] if type_counter else None
        
        # Find top performing post
        top_post = max(posts, key=lambda x: x.get('engagement', 0)) if posts else None
        top_post_id = top_post.get('id') if top_post else None
        top_post_engagement = top_post.get('engagement', 0) if top_post else 0
        
        # Calculate average engagement
        total_engagement = sum(post.get('engagement', 0) for post in posts)
        avg_engagement = total_engagement / len(posts) if posts else 0
        
        analysis = ContentAnalysis(
            user_id=user_id,
            platform=platform,
            analyzed_at=datetime.utcnow(),
            top_content_type=top_content_type,
            top_post_id=top_post_id,
            top_post_engagement=top_post_engagement,
            avg_engagement=avg_engagement
        )
        
        db.session.add(analysis)
        db.session.commit()
        
        return analysis
    
    @staticmethod
    def get_latest_analysis(user_id: int, platform: str) -> ContentAnalysis:
        """
        Get the most recent content analysis for a user
        
        Args:
            user_id (int): The ID of the user
            platform (str): The social media platform
            
        Returns:
            ContentAnalysis: The most recent analysis record
        """
        return ContentAnalysis.query.filter_by(
            user_id=user_id,
            platform=platform
        ).order_by(ContentAnalysis.analyzed_at.desc()).first()
    
    @staticmethod
    def get_content_type_distribution(analysis: ContentAnalysis) -> dict:
        """
        Get distribution of content types
        
        Args:
            analysis (ContentAnalysis): The analysis record
            
        Returns:
            dict: Distribution of content types
        """
        return {
            'top_type': analysis.top_content_type,
            'top_post_engagement': analysis.top_post_engagement,
            'average_engagement': analysis.avg_engagement
        } 