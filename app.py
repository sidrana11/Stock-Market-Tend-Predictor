
from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    forecast = []
    chart_path = None
    if request.method == 'POST':
        symbol = request.form['symbol'].upper()
        start = request.form['start']
        end = request.form['end']
        degree = int(request.form['degree'])
        forecast_days = int(request.form['forecast'])

        try:
            data = yf.download(symbol, start=start, end=end)
            if data.empty:
                return render_template('index.html', error="No data found. Check symbol or date range.")
            data.reset_index(inplace=True)
            data["Date_ordinal"] = data["Date"].apply(lambda x: x.toordinal())
            data["SMA_10"] = data["Close"].rolling(10).mean()
            data["SMA_20"] = data["Close"].rolling(20).mean()

            X = data["Date_ordinal"].values.reshape(-1, 1)
            y = data["Close"].values

            poly = PolynomialFeatures(degree=degree)
            X_poly = poly.fit_transform(X)
            model = LinearRegression().fit(X_poly, y)
            y_pred = model.predict(X_poly)

            last_date = data["Date"].max()
            future_dates = [last_date + timedelta(days=i) for i in range(1, forecast_days + 1)]
            future_ordinals = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)
            future_poly = poly.transform(future_ordinals)
            future_preds = model.predict(future_poly)

            forecast = [(d.strftime('%Y-%m-%d'), f'{p:.2f}') for d, p in zip(future_dates, future_preds)]

            plt.figure(figsize=(10, 4))
            plt.plot(data["Date"], data["Close"], label="Actual", color="black")
            plt.plot(data["Date"], y_pred, label="Polynomial Fit", color="red")
            plt.plot(data["Date"], data["SMA_10"], label="10-day SMA", linestyle="--", color="blue")
            plt.plot(data["Date"], data["SMA_20"], label="20-day SMA", linestyle="--", color="green")
            plt.plot(future_dates, future_preds, label="Forecast", marker="o", color="orange")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.title(f"{symbol} Stock Trend & Forecast")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()

            chart_path = os.path.join("static", "chart.png")
            plt.savefig(chart_path)
            plt.close()

        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html', forecast=forecast, chart=chart_path)

if __name__ == "__main__":
    app.run(debug=True)
