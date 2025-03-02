# Cryptocurrency Sentiment Analysis Project

## Overview

This project analyzes the correlation between global news sentiment and cryptocurrency price fluctuations. It combines real-time news aggregation, sentiment analysis, machine learning, and data visualization.

## Tech Stack

*   Python
*   PostgreSQL
*   MongoDB
*   Flask
*   Power BI
*   TensorFlow/Keras (LSTM)
*   NLTK

## File Structure

(See detailed file structure in the previous responses)

## Setup

1.  Install dependencies: `pip install -r requirements.txt`
2.  Set up PostgreSQL and MongoDB.
3.  Obtain API keys (NewsAPI, CoinGecko) and Power BI credentials.
4.  Configure the `.env` file.
5.  Run `python src/database/db_setup.py` and `python src/database/mongo_setup.py`.

## Usage

1.  Run the main script: `python src/main.py`

## Power BI Integration

*   Create a Power BI dataset connected to your data source.
*   Configure the Power BI refresh script (`src/powerbi/pbi_refresh.py`).
*   Schedule the script execution for automated updates.

## Notes

*   Remember to fill in the `.env` file with your API keys and database credentials.
*   Tune the LSTM model parameters for better performance.
*   Handle API rate limits and errors gracefully.

## Author

[Your Name]
