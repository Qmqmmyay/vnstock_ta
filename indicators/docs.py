# Define docstrings as constants
SMA_DOC = """
    Calculate Simple Moving Average Indicator (SMA).

    Args:
        length (int): The rolling window for lookback data. Default is 14.

    Returns:
        pd.Series: Series containing the SMA values.

    Reference:
        - TradingView: https://www.tradingview.com/support/solutions/43000502338-moving-average-ma/
        - Investopedia: https://www.investopedia.com/terms/s/sma.asp
"""

EMA_DOC = """
    Calculate Exponential Moving Average Indicator (EMA).

    Args:
        length (int): The rolling window for lookback data. Default is 14.

    Returns:
        pd.Series: Series containing the EMA values.

    Reference:
        - TradingView: https://vn.tradingview.com/support/solutions/43000589132/
        - Investopedia: https://www.investopedia.com/terms/e/ema.asp
"""

VWAP_DOC = """
    Calculate the Volume Weighted Average Price (VWAP).

    Args:
        anchor (str): How to anchor VWAP. Depending on the index values, it will
        implement various Timeseries Offset Aliases as listed here:
        https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases
        Default: "D".
    Returns:
        pd.Series: Series containing the VWAP values.

    Reference:
        - TradingView: https://vn.tradingview.com/support/solutions/43000502018/
        - Investopedia: https://www.investopedia.com/terms/v/vwap.asp
"""

VWMA_DOC = """
    Calculate the Volume Weighted Moving Average (VWMA).

    Args:
        length (int): The period for calculating VWMA. Default is 14.

    Returns:
        pd.Series: Series containing the VWMA values.

    Reference:
        - TradingView: https://vn.tradingview.com/support/solutions/43000592293/
        - Investopedia: https://www.investopedia.com/terms/v/vwma.asp
"""

OBV_DOC = """
    Calculate On Balance Volume (OBV) Indicator.
    """

ADX_DOC = """
    Calculate the Average Directional Movement Index (ADX).

    Args:
        length (int): The period for calculating ADX. Default is 14.

    Returns:
        pd.Series: Series containing the ADX values.

    Reference:
        - TradingView: https://vn.tradingview.com/support/solutions/43000589099/
        - Investopedia: https://www.investopedia.com/terms/a/adx.asp
"""

AROON_DOC = """
    Calculate the Aroon & Aroon Oscillator.

    Args:
        length (int): The period for calculating Aroon. Default is 14.

    Returns:
        pd.DataFrame: DataFrame containing Aroon Up, Aroon Down, and Aroon Oscillator values.

    Reference:
        - TradingView: https://vn.tradingview.com/support/solutions/43000501801/
        - Investopedia: https://www.investopedia.com/terms/a/aroon.asp
"""

PSAR_DOC = """
    Calculate the Parabolic Stop and Reverse (PSAR).

    Args:
        af0 (float): Initial Acceleration Factor. Default: 0.02
        af (float): Acceleration Factor. Default: 0.02
        max_af (float): Maximum Acceleration Factor. Default: 0.2

    Returns:
        pd.Series: Series containing the PSAR values.

    Reference:
        - TradingView: https://vn.tradingview.com/support/solutions/43000502597/
        - Investopedia: https://www.investopedia.com/terms/p/parabolicindicator.asp
"""

SUPERTREND_DOC = """
    Calculate the Supertrend.

    Args:
        length (int) : length for ATR calculation. Default: 7
        multiplier (float): Coefficient for upper and lower band distance to
            midrange. Default: 3.0

    Returns:
        pd.DataFrame: DataFrame containing the Supertrend and Supertrend Direction values.

    Reference:
        - TradingView: https://www.tradingview.com/support/solutions/43000543540-supertrend/
        - Investopedia: https://www.investopedia.com/terms/s/supertrend.asp
"""

# MOMENTUM INDICATORS

RSI_DOC = """
    Calculate Relative Strength Index (RSI) Indicator.

    Args:
        length (int): The rolling window for lookback data. Default is 14.

    Returns:
        pd.Series: Series containing the RSI values.

    Reference:
        - TradingView: https://www.tradingview.com/support/solutions/43000502339-relative-strength-index-rsi/
        - Investopedia: https://www.investopedia.com/terms/r/rsi.asp
"""

MACD_DOC = """
    Calculate the Moving Average Convergence Divergence (MACD).

    Args:
        fast (int): The short period for calculating MACD. Default is 12.
        slow (int): The long period for calculating MACD. Default is 26.
        signal (int): The signal period for calculating MACD. Default is 9.

    Returns:
        pd.DataFrame: DataFrame containing the MACD line, Signal line, and Histogram.

    Reference:
        - TradingView: https://vn.tradingview.com/support/solutions/43000502344/
        - Investopedia: https://www.investopedia.com/terms/m/macd.asp
"""

WILLR_DOC = """
    Calculate the Williams %R.

    Args:
        length (int): The period for calculating Williams %R. Default is 14.

    Returns:
        pd.Series: Series containing the Williams %R values.

    Reference:
        - Investopedia: https://www.investopedia.com/terms/w/williamsr.asp
"""

CMO_DOC = """
    Calculate the Chande Momentum Oscillator (CMO).

    Args:
        length (int): The period for calculating CMO. Default is 14.

    Returns:
        pd.Series: Series containing the CMO values.

    Reference:
        - TradingView: https://www.tradingview.com/support/solutions/43000501970-chande-momentum-oscillator-cmo/
"""

STOCH_DOC = """
    Calculate the Stochastic Oscillator.

    Args:
        k (int): The period for the %K line. Default is 14.
        d (int): The period for the %D line. Default is 1.
        smooth_k (int): The smoothing period for the %K line. Default is 3.

    Returns:
        pd.DataFrame: DataFrame containing the %K and %D values.

    Reference:
        - TradingView: https://vn.tradingview.com/support/solutions/43000502332/
        - Investopedia: https://www.investopedia.com/terms/s/stochasticoscillator.asp
"""

ROC_DOC = """
    Calculate the Rate of Change (ROC).

    Args:
        length (int): The period for calculating ROC. Default is 14.

    Returns:
        pd.Series: Series containing the ROC values.

    Reference:
        - TradingView: https://vn.tradingview.com/support/solutions/43000502343/
        - Investopedia: https://www.investopedia.com/terms/r/rateofchange.asp
"""

MOM_DOC = """
    Calculate the Momentum (MOM).

    Args:
        length (int): The period for calculating MOM. Default is 14.

    Returns:
        pd.Series: Series containing the MOM values.

    Reference:
        - TradingView: https://www.tradingview.com/support/solutions/43000589187-momentum/
        - Investopedia: https://www.investopedia.com/terms/m/momentum.asp
"""

# VOLATILITY INDICATORS

BBANDS_DOC = """
    Calculate Bollinger Bands Indicator.

    Args:
        length (int): The rolling window for lookback data. Default is 14.
        std (float): The number of standard deviations to use. Default is 2.

    Returns:
        pd.DataFrame: DataFrame containing the Bollinger Bands values (lower, middle, upper).

    Reference:
        - TradingView: https://www.tradingview.com/support/solutions/43000501963-bollinger-bands-bb/
        - Investopedia: https://www.investopedia.com/terms/b/bollingerbands.asp
"""

KC_DOC = """
    Calculate the Keltner Channels (KC).

    Args:
        length (int): The period for calculating KC. Default is 20.
        scalar (float): ATR scalar. Default is 2.0.
        mamode (str): The Moving Average mode. Default is 'ema'.

    Returns:
        pd.DataFrame: DataFrame containing the Keltner Channels values (lower, middle, upper).
"""

ATR_DOC = """
    Calculate the Average True Range (ATR).

    Args:
        length (int): The period for calculating ATR. Default is 14.

    Returns:
        pd.Series: Series containing the ATR values.

    Reference:
        - Investopedia: https://www.investopedia.com/terms/a/atr.asp
"""

STDEV_DOC = """
    Calculate the Standard Deviation (STDEV).

    Args:
        length (int): The period for calculating Standard Deviation. Default is 14.
        ddof (int): Delta degrees of freedom for the calculation. Default is 1.

    Returns:
        pd.Series: Series containing the Standard Deviation values.

    Reference:
        - Investopedia: https://www.investopedia.com/terms/s/standarddeviation.asp
"""

LINREG_DOC = """
    Calculate the Linear Regression (LINREG).

    Args:
        length (int): The period for calculating Linear Regression. Default is 14.

    Returns:
        pd.Series: Series containing the Linear Regression values.

    Reference:
        - Investopedia: https://www.investopedia.com/terms/l/linear-regression.asp
"""
