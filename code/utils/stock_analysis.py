import yfinance as yf
import requests
import plotly.express as px

FMP_API_KEY = 'WxuP3is7UVQLtDg7s9YgnRes9g2Upf4e'

def get_stock_price(ticker):
    try:
        data = yf.Ticker(ticker).history(period='1d')
        if data.empty:
            raise ValueError("No data found for the ticker.")
        return float(data['Close'].iloc[-1])
    except Exception as e:
        raise ValueError(f"Error fetching stock price: {e}")

def get_financial_ratios(ticker):
    url = f"https://financialmodelingprep.com/api/v3/ratios/{ticker}?apikey={FMP_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Error fetching financial ratios: {response.text}")
    ratios = response.json()
    if not ratios:
        raise ValueError("No financial ratios found.")
    return {
        'P/E Ratio': ratios[0]['priceEarningsRatio'],
        'P/B Ratio': ratios[0]['priceToBookRatio']
    }

def get_beta(ticker):
    url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={FMP_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Error fetching Beta: {response.text}")
    profile = response.json()
    if not profile:
        raise ValueError("No profile data found.")
    return profile[0]['beta']

def plot_stock_price(ticker):
    try:
        data = yf.Ticker(ticker).history(period='1y')
        if data.empty:
            raise ValueError("No data found for the ticker.")
        fig = px.line(data, x=data.index, y='Close', title=f'{ticker} stock price over the last year')
        return fig
    except Exception as e:
        raise ValueError(f"Error plotting stock price: {e}")

def calculate_SMA(ticker, window):
    try:
        data = yf.Ticker(ticker).history(period='1y')
        if data.empty:
            raise ValueError("No data found for the ticker.")
        sma = data['Close'].rolling(window=window).mean().iloc[-1]
        return round(sma, 2)
    except Exception as e:
        raise ValueError(f"Error calculating SMA: {e}")

def calculate_RSI(ticker, period=14):
    try:
        data = yf.Ticker(ticker).history(period='1y')
        if data.empty:
            raise ValueError("No data found for the ticker.")
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi.iloc[-1], 2)
    except Exception as e:
        raise ValueError(f"Error calculating RSI: {e}")

def calculate_MACD(ticker, short_window=12, long_window=26, signal_window=9):
    try:
        data = yf.Ticker(ticker).history(period='1y')
        if data.empty:
            raise ValueError("No data found for the ticker.")
        short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
        long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
        macd_line = short_ema - long_ema
        signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
        macd_value = macd_line.iloc[-1] - signal_line.iloc[-1]
        return round(macd_value, 2)
    except Exception as e:
        raise ValueError(f"Error calculating MACD: {e}")
