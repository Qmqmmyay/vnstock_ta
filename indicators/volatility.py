import pandas as pd
from pta_reload import ta
from typing import Union
from .docs import *

class VolatilityIndicator:
    def __init__(self, data: pd.DataFrame):
        """
        Calculate Volatility Indicators.

        Args:
            data (pd.DataFrame): DataFrame containing price data with columns like 'close'.
        """
        self.data = data

    def bbands(self, length: int = 14, std: float = 2) -> pd.DataFrame:
        bbands_series = ta.bbands(self.data['close'], length=length, std=std, talib=False)
        return bbands_series
    bbands.__doc__ = BBANDS_DOC

    def kc(self, length: int = 20, scalar: float = 2.0, mamode: str = 'ema') -> pd.DataFrame:
        kc_series = ta.kc(high=self.data['high'], low=self.data['low'], close=self.data['close'], length=length, scalar=scalar, mamode=mamode)
        return kc_series
    kc.__doc__ = KC_DOC

    def atr(self, length: int = 14) -> pd.Series:
        atr_series = ta.atr(self.data['high'], self.data['low'], self.data['close'], length=length, talib=False)
        return atr_series
    atr.__doc__ = ATR_DOC
    
    def stdev(self, length: int = 14, ddof: int = 1) -> pd.Series:
        stdev_series = ta.stdev(self.data['close'], length=length, ddof=ddof, talib=False)
        return stdev_series
    stdev.__doc__ = STDEV_DOC
    
    def linreg(self, length: int = 14) -> pd.Series:
        linreg_series = ta.linreg(self.data['close'], length=length)
        return linreg_series
    linreg.__doc__ = LINREG_DOC