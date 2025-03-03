import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Streamlit app title
st.title("Stock Analyzer and Predictor")

# Sidebar input for stock selection
stock_ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", "AAPL")

# Fetch stock data
if stock_ticker:
    stock_data = yf.download(stock_ticker, period="6mo", interval="1d")
    stock_data.columns = stock_data.columns.get_level_values(0)
    
    if not stock_data.empty:
        st.subheader(f"Stock Data for {stock_ticker}")
        st.dataframe(stock_data.tail(10))
        
        # Bar Chart for Daily Close Prices
        st.subheader("Bar Chart of Closing Prices")
        fig_bar = px.bar(stock_data, x=stock_data.index, y="Close", title="Daily Closing Prices")
        st.plotly_chart(fig_bar)
        
        # Box Plot for Open, High, Low, and Close Prices
        st.subheader("Box Plot of Stock Prices")
        stock_data_melted = stock_data.melt(value_vars=["Open", "High", "Low", "Close"], var_name="Price Type", value_name="Value")
        fig_box = px.box(stock_data_melted, x="Price Type", y="Value", title="Stock Price Distribution")
        st.plotly_chart(fig_box)
        
        # Prediction Methods Selection
        st.subheader("Stock Price Prediction")
        periods = st.slider("Select number of days to predict", min_value=5, max_value=30, value=15)
        method = st.selectbox("Select Prediction Method", ["Moving Average", "ARIMA", "Exponential Smoothing"])
        
        if method == "Moving Average":
            stock_data['Moving_Avg'] = stock_data['Close'].rolling(window=5).mean()
            pred_df = pd.DataFrame({"Date": stock_data.index, "Predicted Close": stock_data['Moving_Avg']}).dropna()
        
        elif method == "ARIMA":
            model = ARIMA(stock_data['Close'], order=(5,1,0))
            model_fit = model.fit()
            future_dates = pd.date_range(start=stock_data.index[-1], periods=periods+1, freq='B')[1:]
            predictions = model_fit.forecast(steps=periods)
            pred_df = pd.DataFrame({"Date": future_dates, "Predicted Close": predictions})
            pred_df.set_index("Date", inplace=True)
        
        elif method == "Exponential Smoothing":
            model = ExponentialSmoothing(stock_data['Close'], trend='add', seasonal=None, damped_trend=True)
            model_fit = model.fit()
            future_dates = pd.date_range(start=stock_data.index[-1], periods=periods+1, freq='B')[1:]
            predictions = model_fit.forecast(periods)
            pred_df = pd.DataFrame({"Date": future_dates, "Predicted Close": predictions})
            pred_df.set_index("Date", inplace=True)
        
        # Plot predictions
        fig_pred = px.line(pred_df, x=pred_df.index, y="Predicted Close", title=f"Stock Price Prediction ({method})")
        st.plotly_chart(fig_pred)
        
        # Email functionality
        st.sidebar.subheader("Send Report via Email")
        email = st.sidebar.text_input("Enter recipient email")
        if st.sidebar.button("Send Email"):
            try:
                sender_email = "your_email@gmail.com"
                sender_password = "your_password"
                
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = email
                msg['Subject'] = f"Stock Analysis Report for {stock_ticker}"
                
                body = f"""
                Stock Analysis for {stock_ticker}
                
                - Last 10 Days Data:
                {stock_data.tail(10).to_string()}
                
                - Predicted Closing Prices for Next {periods} Days:
                {pred_df.to_string()}
                
                """
                msg.attach(MIMEText(body, 'plain'))
                
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
                server.quit()
                
                st.toast("Email sent successfully!")
            except Exception as e:
                st.error(f"Failed to send email: {e}")
        
    else:
        st.error("Failed to fetch data. Please check the stock ticker and try again.")
