import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def build_forecast(df: pd.DataFrame, days: int = 7) -> pd.DataFrame:
    df = df[["date", "avg_temp_c"]].copy()
    df["lag_1"] = df["avg_temp_c"].shift(1)
    df["lag_2"] = df["avg_temp_c"].shift(2)
    df["lag_7"] = df["avg_temp_c"].shift(7)
    df = df.dropna()

    X = df[["lag_1", "lag_2", "lag_7"]]
    y = df["avg_temp_c"]
    
    model = LinearRegression()
    model.fit(X, y)

    y_pred = model.predict(X)
    mae = round(float(np.mean(np.abs(y - y_pred))), 2)
    df["model_pred_c"] = y_pred.round(2)
    last_row = df.iloc[-1]
    future_dates = pd.date_range(pd.Timestamp(df["date"].max()), periods=days + 1, freq="D")[1:]
    
    forecasts = []
    lag_1 = last_row["avg_temp_c"]
    lag_2 = last_row["lag_1"]
    lag_7 = last_row["lag_7"]
    
    for date in future_dates:
        pred = model.predict(pd.DataFrame([[lag_1, lag_2, lag_7]], columns=["lag_1", "lag_2", "lag_7"]))[0]
        forecasts.append({"date": date, "forecast_temp_c": round(pred, 2)})
        lag_2 = lag_1
        lag_1 = pred
    
    forecast_df = pd.DataFrame(forecasts)
    historical_preds = df[["date", "avg_temp_c", "model_pred_c"]].copy()
    return forecast_df, mae, historical_preds
