import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

def prepare_data(df, sequence_length):
    """
    Prepares data for LSTM model.  Scales features using MinMaxScaler and creates
    sequences of specified length.
    """
    df = df.dropna()  # Remove any rows with missing values after feature engineering
    data = df.values
    scaler = MinMaxScaler(feature_range=(0, 1))  # Scale features to 0-1
    scaled_data = scaler.fit_transform(data)

    X, y = [], []
    for i in range(sequence_length, len(scaled_data)):
        X.append(scaled_data[i-sequence_length:i])
        y.append(scaled_data[i, 0])  # Predict the 'price' (first column)

    X, y = np.array(X), np.array(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False) # Time series - NO SHUFFLE
    return X_train, X_test, y_train, y_test, scaler # Return the scaler to inverse transform later


def create_lstm_model(input_shape):
    """
    Defines the LSTM model architecture.
    """
    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(units=50, return_sequences=True, input_shape=input_shape),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.LSTM(units=50, return_sequences=False),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(units=25),
        tf.keras.layers.Dense(units=1)  # Output: Predicted price
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


def train_model(model, X_train, y_train, epochs=10, batch_size=32):
    """
    Trains the LSTM model.
    """
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)
    return model


def predict_prices(model, X_test, scaler):
    """
    Predicts prices using the trained model and inverse transforms the scaled predictions.
    """
    predicted_prices = model.predict(X_test)
    # Create a dummy array with the same number of columns as the original scaled data
    # and fill it with the predicted prices in the first column.
    dummy_array = np.zeros((len(predicted_prices), scaler.data_max_.shape[0]))
    dummy_array[:, 0] = predicted_prices[:, 0]  # Place predicted prices in the first column

    # Inverse transform the dummy array to get the original scale
    predicted_prices = scaler.inverse_transform(dummy_array)[:, 0]
    return predicted_prices

# Example Usage (Illustrative):
if __name__ == '__main__':
    # Create dummy data
    data = {'price': [10, 12, 15, 14, 16, 18, 20, 19, 22, 25, 27, 29, 31, 30, 32, 34, 36, 35, 38, 40],
            'sentiment_score': [0.1, 0.2, -0.1, 0.0, 0.3, 0.2, -0.2, 0.1, 0.4, 0.3, 0.2, 0.1, 0.0, -0.1, 0.2, 0.3, 0.4, 0.1, 0.0, -0.2]}
    dates = pd.date_range('2023-01-01', periods=20, freq='D')
    df = pd.DataFrame(data, index=dates)

    sequence_length = 5  # Tune this parameter

    X_train, X_test, y_train, y_test, scaler = prepare_data(df, sequence_length)

    # Reshape X_train to 3D array [number of samples, timesteps, number of features]
    num_features = X_train.shape[2] # Determine the number of features from X_train
    input_shape = (sequence_length, num_features)
    model = create_lstm_model(input_shape)

    model = train_model(model, X_train, y_train, epochs=10, batch_size=32)

    predicted_prices = predict_prices(model, X_test, scaler)

    print("Predicted Prices:", predicted_prices)
