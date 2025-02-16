# Stock Analyzer and Predictor

This project is a Streamlit web application that allows users to analyze and predict stock prices. The app fetches stock data, visualizes it, and predicts future trends using the Exponential Smoothing method. Additionally, users can send the analysis report via email.

## Features

- Fetch stock data for the last 6 months
- Display stock data in a table
- Visualize daily closing prices with a bar chart
- Visualize stock price distribution with a box plot
- Predict future stock prices using Exponential Smoothing
- Send stock analysis report via email

## Requirements

The project requires the following Python packages:

- streamlit
- yfinance
- plotly
- pandas
- statsmodels
- smtplib
- email

You can install the required packages using the `requirements.txt` file:

```sh
pip install -r requirements.txt

Usage

Run the Streamlit app:
streamlit run main.py

