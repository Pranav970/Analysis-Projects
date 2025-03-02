import pandas as pd

def create_technical_indicators(df):
    """
    Creates common technical indicators for price data.  Requires a DataFrame
    with a 'price' column.
    """
    df['SMA_5'] = df['price'].rolling(window=5).mean()
    df['SMA_20'] = df['price'].rolling(window=20).mean()
    df['EMA_12'] = df['price'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['price'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    return df

def create_date_features(df):
    """
    Creates date-based features (year, month, day, day of week).
    """
    df['year'] = df.index.year
    df['month'] = df.index.month
    df['day'] = df.index.day
    df['dayofweek'] = df.index.dayofweek
    return df

def combine_features(price_df, sentiment_df):
    """
    Combines price data with aggregated sentiment scores.
    Assumes both DataFrames have a common index (timestamp).
    """
    combined_df = pd.merge(price_df, sentiment_df, left_index=True, right_index=True, how='inner')
    return combined_df

# Example Usage (Illustrative):
if __name__ == '__main__':
    # Create dummy price data
    data = {'price': [10, 12, 15, 14, 16, 18, 20, 19, 22, 25]}
    dates = pd.date_range('2023-01-01', periods=10, freq='D')
    price_df = pd.DataFrame(data, index=dates)

    # Create dummy sentiment data
    sentiment_data = {'sentiment_score': [0.1, 0.2, -0.1, 0.0, 0.3, 0.2, -0.2, 0.1, 0.4, 0.3]}
    sentiment_df = pd.DataFrame(sentiment_data, index=dates)

    price_df = create_technical_indicators(price_df.copy())  # Create a copy to avoid modifying original
    price_df = create_date_features(price_df.copy())
    combined_df = combine_features(price_df.copy(), sentiment_df.copy())

    print(combined_df.head())
