from datetime import datetime
from models import SentimentAnalysis, db
from textblob import TextBlob

class SentimentAnalysisService:
    @staticmethod
    def analyze_sentiment(user_id: int, platform: str, comments: list) -> SentimentAnalysis:
        """
        Analyze sentiment of comments and interactions
        
        Args:
            user_id (int): The ID of the user
            platform (str): The social media platform
            comments (list): List of comment texts to analyze
            
        Returns:
            SentimentAnalysis: The created analysis record
        """
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        total_score = 0
        
        for comment in comments:
            # Analyze sentiment using TextBlob
            analysis = TextBlob(comment)
            score = analysis.sentiment.polarity
            
            # Categorize sentiment
            if score > 0.1:
                positive_count += 1
            elif score < -0.1:
                negative_count += 1
            else:
                neutral_count += 1
                
            total_score += score
        
        total_comments = len(comments)
        average_score = total_score / total_comments if total_comments > 0 else 0
        
        analysis = SentimentAnalysis(
            user_id=user_id,
            platform=platform,
            analyzed_at=datetime.utcnow(),
            positive_count=positive_count,
            negative_count=negative_count,
            neutral_count=neutral_count,
            average_score=average_score
        )
        
        db.session.add(analysis)
        db.session.commit()
        
        return analysis
    
    @staticmethod
    def get_latest_analysis(user_id: int, platform: str) -> SentimentAnalysis:
        """
        Get the most recent sentiment analysis for a user
        
        Args:
            user_id (int): The ID of the user
            platform (str): The social media platform
            
        Returns:
            SentimentAnalysis: The most recent analysis record
        """
        return SentimentAnalysis.query.filter_by(
            user_id=user_id,
            platform=platform
        ).order_by(SentimentAnalysis.analyzed_at.desc()).first()
    
    @staticmethod
    def get_sentiment_distribution(analysis: SentimentAnalysis) -> dict:
        """
        Calculate the distribution of sentiments
        
        Args:
            analysis (SentimentAnalysis): The analysis record
            
        Returns:
            dict: Distribution of sentiments as percentages
        """
        total = (
            analysis.positive_count + 
            analysis.negative_count + 
            analysis.neutral_count
        )
        
        if total == 0:
            return {
                'positive': 0,
                'negative': 0,
                'neutral': 0
            }
            
        return {
            'positive': (analysis.positive_count / total) * 100,
            'negative': (analysis.negative_count / total) * 100,
            'neutral': (analysis.neutral_count / total) * 100
        } 