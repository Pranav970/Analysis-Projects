from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the text using VADER.
    """
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    return scores  # Returns a dictionary of {'neg': ..., 'neu': ..., 'pos': ..., 'compound': ...}

# Example usage:
if __name__ == '__main__':
    text = "Bitcoin is showing strong bullish momentum.  Analysts predict further gains."
    sentiment_scores = analyze_sentiment(text)
    print(sentiment_scores)
