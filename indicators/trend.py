import pandas as pd
from pta_reload import ta
from typing import Union
from .docs import *

class TrendIndicator:
    def __init__(self, data: pd.DataFrame):
        """
        Calculate Trend Indicators.

        Args:
            data (pd.DataFrame): DataFrame containing price data with columns like 'close'.
        """
        self.data = data

    def sma(self, length: int = 14) -> pd.Series:
        sma_data = ta.sma(self.data['close'], length=length, talib=False)
        return sma_data
    sma.__doc__ = SMA_DOC

    def ema(self, length: int = 14) -> pd.Series:
        ema_data = ta.ema(self.data['close'], length=length, talib=False)
        return ema_data
    ema.__doc__ = EMA_DOC

    def vwap(self, anchor:str = 'D') -> pd.Series:
        vwap_data = ta.vwap(high=self.data['high'], low=self.data['low'], close=self.data['close'], volume=self.data['volume'], anchor=anchor)
        return vwap_data
    vwap.__doc__ = VWAP_DOC

    def vwma(self, length: int = 20) -> pd.Series:
        vwma_data = ta.vwma(self.data['close'], self.data['volume'], length=length, talib=False)
        return vwma_data
    vwma.__doc__ = VWMA_DOC
    
    def adx(self, length: int = 14) -> pd.Series:
        adx_data = ta.adx(high=self.data['high'], low=self.data['low'], close=self.data['close'], length=length)
        return adx_data
    adx.__doc__ = ADX_DOC

    def aroon(self, length: int = 14) -> pd.DataFrame:
        aroon_data = ta.aroon(high=self.data['high'], low=self.data['low'], length=length, talib=False)
        return aroon_data
    aroon.__doc__ = AROON_DOC

    def psar(self, af0: float = 0.02, af: float = 0.02, max_af: float = 0.2) -> pd.Series:
        psar_data = ta.psar(high=self.data['high'], low=self.data['low'], close=None, af=af, max_af=max_af)
        return psar_data
    psar.__doc__ = PSAR_DOC

    def supertrend(self, length: int = 10, multiplier: float = 3) -> pd.DataFrame:
        supertrend_df = ta.supertrend(high=self.data['high'], low=self.data['low'], close=self.data['close'], length=length, multiplier=multiplier)
        return supertrend_df
    supertrend.__doc__ = SUPERTREND_DOC
