import os
from dotenv import load_dotenv
import datetime
import pandas as pd

# Import your modules
from src.data_collection import crypto_api, news_api
from src.preprocessing import cleaner, sentiment, feature_engineering
from src.modeling import lstm_model, model_evaluation
from src.powerbi import pbi_refresh
from src.database import db_setup, mongo_setup

load_dotenv()

# --- Configuration ---
CRYPTO_COIN = "bitcoin"
NEWS_QUERY = "Bitcoin"
DAYS_BACK = 30 #How far back in time to get the data from Crypto_api

POWER_BI_ENABLED = True #Enable/Disable Power BI integration
# --- End Configuration ---

def main():
    """
    Main function to orchestrate the entire process.
    """
    print("Starting Crypto Sentiment Analysis...")

    # 1. Data Collection
    print("Collecting data...")
    #a. Crypto Data:
    crypto_data = crypto_api.get_crypto_price_data(CRYPTO_COIN, days = DAYS_BACK)
    if crypto_data:
        print(f"Successfully fetched crypto data for {CRYPTO_COIN}")
    else:
        print(f"Failed to fetch crypto data for {CRYPTO_COIN}.")
        return  # Exit if data collection fails

    #b. News Data:
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    news_articles = news_api.get_crypto_news(NEWS_QUERY, yesterday, today) #Adjust date to fetch as needed
    if news_articles:
        print(f"Successfully fetched {len(news_articles)} news articles.")
    else:
        print("Failed to fetch news articles.")
        return

    # 2. Data Preprocessing
    print("Preprocessing data...")
    #a. Crypto Data
    price_data = [[row[0], row[1]] for row in crypto_data]
    price_df = pd.DataFrame(price_data, columns=['timestamp', 'price'])
    price_df['timestamp'] = pd.to_datetime(price_df['timestamp'], unit='ms')
    price_df = price_df.set_index('timestamp')

    #b. News Data & Sentiment Analysis:
    sentiment_scores = []
    for article in news_articles:
        cleaned_text = cleaner.clean_text(article['title'] + " " + article['description'])  # Combine title and description
        scores = sentiment.analyze_sentiment(cleaned_text)
        sentiment_scores.append(scores['compound'])  # Use compound score

    sentiment_df = pd.DataFrame(sentiment_scores, index = [article['publishedAt'] for article in news_articles], columns=['sentiment_score'])
    sentiment_df.index = pd.to_datetime(sentiment_df.index)

    # 3. Feature Engineering
    print("Engineering Features...")
    price_df = feature_engineering.create_technical_indicators(price_df.copy())
    price_df = feature_engineering.create_date_features(price_df.copy())

    # Aggregate sentiment scores to match price data frequency (e.g., daily):

    sentiment_df = sentiment_df.resample('D').mean() #Daily aggregation
    combined_df = feature_engineering.combine_features(price_df.copy(), sentiment_df.copy()) #combining of the data

    # 4. Machine Learning
    print("Training Machine Learning Model...")
    SEQUENCE_LENGTH = 10 #tune this parameter based on your data
    X_train, X_test, y_train, y_test, scaler = lstm_model.prepare_data(combined_df.copy(), SEQUENCE_LENGTH) #preparing the LSTM model

    #Ensure the data is not None
    if X_train is None or X_test is None or y_train is None or y_test is None or scaler is None:
        print("Error: Could not prepare the data correctly. Check the dataframe and sequence length.")
        return

    # Reshape X_train for LSTM: [samples, time steps, features]
    NUM_FEATURES = X_train.shape[2]
    INPUT_SHAPE = (SEQUENCE_LENGTH, NUM_FEATURES)
    model = lstm_model.create_lstm_model(INPUT_SHAPE) #Creating LSTM model
    model = lstm_model.train_model(model, X_train, y_train, epochs=10, batch_size=32) #Model training

    # 5. Model Evaluation:
    print("Evaluating Model...")
    predicted_prices = lstm_model.predict_prices(model, X_test, scaler) #predicting the prices
    rmse, mae = model_evaluation.evaluate_model(y_test[:len(predicted_prices)], predicted_prices) #Evaluating the results of the model

    # 6. Power BI Integration
    if POWER_BI_ENABLED:
        print("Refreshing Power BI Dataset...")
        dataset_id = os.getenv("POWER_BI_DATASET_ID")
        group_id = os.getenv("POWER_BI_GROUP_ID")

        access_token = pbi_refresh.get_power_bi_token()
        if access_token:
            pbi_refresh.refresh_power_bi_dataset(dataset_id, group_id, access_token)
        else:
            print("Failed to get Power BI access token. Skipping Power BI refresh.")
    else:
        print("Power BI integration is disabled.")

    print("Finished Crypto Sentiment Analysis.")

if __name__ == "__main__":
    main()
