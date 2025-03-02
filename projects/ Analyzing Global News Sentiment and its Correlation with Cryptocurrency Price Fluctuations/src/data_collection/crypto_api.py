import requests
import json

def get_crypto_price_data(coin_id, vs_currency='usd', days='max'):
    """
    Fetches historical price data from CoinGecko API.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency={vs_currency}&days={days}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['prices'] # Returns a list of [timestamp, price] pairs
    else:
        print(f"Error fetching data for {coin_id}: {response.status_code}")
        return None

if __name__ == '__main__':
    bitcoin_data = get_crypto_price_data('bitcoin', days=30)
    if bitcoin_data:
        print(bitcoin_data[:5]) # Print the first 5 entries for preview
