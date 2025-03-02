from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

def evaluate_model(y_true, y_predicted):
    """
    Evaluates the model using RMSE and MAE.
    """
    rmse = np.sqrt(mean_squared_error(y_true, y_predicted))
    mae = mean_absolute_error(y_true, y_predicted)
    print(f"Root Mean Squared Error (RMSE): {rmse}")
    print(f"Mean Absolute Error (MAE): {mae}")
    return rmse, mae

# Example Usage:
if __name__ == '__main__':
    y_true = [10, 12, 15, 14, 16]
    y_predicted = [10.5, 11.8, 14.7, 14.2, 15.5]
    evaluate_model(y_true, y_predicted)
