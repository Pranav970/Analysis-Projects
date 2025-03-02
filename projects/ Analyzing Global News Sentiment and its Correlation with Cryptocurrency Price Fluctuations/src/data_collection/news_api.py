import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv('NEWS_API_KEY')

def get_crypto_news(query, from_date, to_date, api_key=NEWS_API_KEY, page_size=100):
    """
    Fetches news articles related to cryptocurrency from NewsAPI.
    """
    url = f"https://newsapi.org/v2/everything?q={query}&from={from_date}&to={to_date}&pageSize={page_size}&sortBy=relevancy&apiKey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['articles']
    else:
        print(f"Error fetching news: {response.status_code}")
        return None

if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    news = get_crypto_news("Bitcoin", yesterday, today)
    if news:
        print(f"Found {len(news)} articles.")
        for article in news[:3]:  # Print titles of first 3 articles
            print(article['title'])
