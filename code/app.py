import streamlit as st
from utils.stock_analysis import (
    get_stock_price, get_financial_ratios, get_beta, plot_stock_price,
    calculate_SMA, calculate_RSI, calculate_MACD
)

ALPHA_VANTAGE_API_KEY = '4AUJI66WLADGVGCM'
FMP_API_KEY = 'WxuP3is7UVQLtDg7s9YgnRes9g2Upf4e'

st.title("STOCK-WIZARD")

ticker = st.text_input("Enter the Ticker")

if ticker:
    ticker = ticker.upper()
    try:
        
        price = get_stock_price(ticker)
        st.write(f"### Latest price for {ticker}: ${price:.2f}")

      
        financial_ratios = get_financial_ratios(ticker)
        st.write(f"### Financial Ratios for {ticker}:")
        st.write(f"P/E Ratio: {financial_ratios['P/E Ratio']}")
        st.write(f"P/B Ratio: {financial_ratios['P/B Ratio']}")

       
        beta = get_beta(ticker)
        st.write(f"### Beta for {ticker}: {beta}")

        
        st.write("### Stock Price Over the Last Year")
        stock_chart = plot_stock_price(ticker)
        st.plotly_chart(stock_chart)

        
        sma_window = st.number_input('Enter SMA window:', min_value=1, max_value=365, value=50)
        sma = calculate_SMA(ticker, sma_window)
        st.write(f"{sma_window}-Day SMA for {ticker}: {sma}")

       
        rsi = calculate_RSI(ticker)
        st.write(f"RSI for {ticker}: {rsi}")

        
        macd = calculate_MACD(ticker)
        st.write(f"MACD for {ticker}: {macd}")

    except Exception as e:
        st.error(f"Error: {str(e)}")
