import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

class AnalysisService:
    def __init__(self):
        self.sentiment = SentimentIntensityAnalyzer()

    def sentiment_analysis(self, texts):
        # texts: list of strings
        results = []
        for text in texts:
            score = self.sentiment.polarity_scores(text)
            results.append(score)
        return pd.DataFrame(results)

    def plot_sentiment(self, sentiment_df):
        fig, ax = plt.subplots()
        sentiment_df[['pos', 'neu', 'neg']].plot(kind='bar', stacked=True, ax=ax)
        plt.title('Sentiment Distribution')
        plt.xlabel('Post')
        plt.ylabel('Score')
        plt.tight_layout()
        return fig

    def plot_interactive(self, df, x, y, color=None):
        fig = px.scatter(df, x=x, y=y, color=color)
        return fig

    # Galima pridėti daugiau analizės ir vizualizacijos funkcijų 