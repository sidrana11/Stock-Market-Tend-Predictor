# 📈 Stock Trend Forecaster

A Flask-based web application that allows users to visualize historical stock prices and forecast future trends using Polynomial Regression. It integrates financial data fetching via Yahoo Finance and provides a customizable forecasting experience.

---

## 🚀 Features

- 🔎 Input stock symbol (e.g., `AAPL`, `RELIANCE.NS`)
- 📅 Select custom start and end dates
- ⚙️ Choose curve complexity (polynomial degree)
- 📆 Specify number of days to forecast
- 📊 Visual representation of actual and predicted trends
- 🌄 Background image for a visually appealing UI
- ✅ Forecast displayed in tabular format

---

## 🧠 Machine Learning Approach

This project uses **Polynomial Regression** (a form of supervised learning) to fit a curve over historical closing prices and extrapolate future prices.

- **Curve Complexity**: Controlled by the polynomial degree (1 = linear, 4 = complex curve)
- **Library Used**: `scikit-learn` for training the regression model
- **Forecasting**: Future prices are predicted based on the regression curve using extrapolated days

---

## 📦 Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS
- **Data Source**: Yahoo Finance (`yfinance`)
- **Visualization**: Matplotlib

## 📁 Project Structure

