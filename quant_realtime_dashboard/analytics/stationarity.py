from statsmodels.tsa.stattools import adfuller

def adf_test(series):
    result = adfuller(series)
    return {
        "ADF Statistic": result[0],
        "p-value": result[1]
    }
