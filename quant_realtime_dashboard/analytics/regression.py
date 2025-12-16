# import numpy as np
# import statsmodels.api as sm

# def hedge_ratio(y, x):
#     x = sm.add_constant(x)
#     model = sm.OLS(y, x).fit()
#     return model.params[1]
import numpy as np
import statsmodels.api as sm

def hedge_ratio(y, x):
    """
    Computes OLS hedge ratio.
    Returns NaN if insufficient data.
    """
    if len(y) < 5 or len(x) < 5:
        return np.nan

    x = sm.add_constant(x)

    model = sm.OLS(y, x).fit()

    # Safety check
    if len(model.params) < 2:
        return np.nan

    return model.params.iloc[1]
