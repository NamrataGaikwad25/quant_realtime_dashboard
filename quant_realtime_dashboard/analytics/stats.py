import pandas as pd

def resample_data(df, timeframe):
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    rule = {"1s": "1S", "1m": "1T", "5m": "5T"}[timeframe]

    resampled = df.resample(rule).last().dropna()
    return resampled
