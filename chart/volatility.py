import pandas as pd
from pyecharts import options as opts
from vnstock_ta.utils.const import _ISLAND_GREEN, _ORANGE, _TURKISH_SEA, _SLATE_BLUE, _LIME_PUNCH, _GRADIENT_EMERALD, NEUTRAL_INFORMATION_COMPLETE, DARK_MODE_PRIMARY_COLORS, DARK_MODE_SECONDARY_COLORS, LIGHT_MODE_PRIMARY_COLORS, LIGHT_MODE_SECONDARY_COLORS
from vnstock_ta.chart.core import TAChart


# extend the TAChart class

class TAVolatility(TAChart):
    def __init__(self, data: pd.DataFrame, theme: str = 'light', watermark: bool = True, display: bool = True):
        super().__init__(data, theme, watermark, display)

    def bbands (self, length:int=10, std:int=2, title:str='Bollinger Bands', color=[_TURKISH_SEA, _ORANGE],
            legend=True, watermark=True, minimal:bool=False):
        """
        Bollinger Bands (BBANDS)
        """        

        if color:
            envelope_color = color[0]
            midband_color = color[1]
        else:
            envelope_color = "rgba(167, 202, 241, 0.1)"
            midband_color = _ORANGE

        indicator_data = self.ta.bbands(length=length, std=std).round(2)
        lower_band = indicator_data.iloc[:, 0]
        mid_band = indicator_data.iloc[:, 1]
        upper_band = indicator_data.iloc[:, 2]

        time_index = self.data.index.strftime('%Y-%m-%d').tolist()
        band_line = self.chart._line(time_series=time_index, data_series=upper_band, color=envelope_color, area_style=False, title=title, yaxis_name='Up Band', legend=legend, watermark=watermark)
        band_line = self.chart._add_line(line_chart=band_line, data_series=lower_band, color=envelope_color, title=title, yaxis_name='Low Band')
        mid_line = self.chart._add_line(line_chart=band_line, data_series=mid_band, color=midband_color, title=title, yaxis_name='Mid Band')

        if minimal:
            return self._minimal_chart(indicator_chart=mid_line, title=title)
        else:
            return self._base_chart(indicator_chart=mid_line, title=title)
        
    def kc (self, length:int=20, scalar:int=2, mamode:str='ema', title:str='Keltner Channels', color=[_TURKISH_SEA, _ORANGE],
            legend=True, watermark=True, minimal:bool=False):
        """
        Kelner Channels (KC)
        """        

        if color:
            envelope_color = color[0]
            midband_color = color[1]
        else:
            envelope_color = "rgba(167, 202, 241, 0.1)"
            midband_color = _ORANGE

        indicator_data = self.ta.kc(length=length, scalar=scalar, mamode=mamode).round(2)
        lower_band = indicator_data.iloc[:, 0]
        mid_band = indicator_data.iloc[:, 1]
        upper_band = indicator_data.iloc[:, 2]

        time_index = self.data.index.strftime('%Y-%m-%d').tolist()
        band_line = self.chart._line(time_series=time_index, data_series=upper_band, color=envelope_color, area_style=False, title=title, yaxis_name='Up', legend=legend, watermark=watermark)
        band_line = self.chart._add_line(line_chart=band_line, data_series=lower_band, color=envelope_color, title=title, yaxis_name='Low')
        mid_line = self.chart._add_line(line_chart=band_line, data_series=mid_band, color=midband_color, title=title, yaxis_name='Mid')

        if minimal:
            return self._minimal_chart(indicator_chart=mid_line, title=title)
        else:
            return self._base_chart(indicator_chart=mid_line, title=title)
        
    def atr (self, length:int=14, title='Average True Range', color=_ISLAND_GREEN, 
                    legend=False, watermark=True, minimal:bool=False):
        if color:
            indicator_color = color
        else:
            indicator_color = self.chart.mono_color

        indicator_data = self.ta.atr(length=length).round(2)
        time_index = self.data.index.strftime('%Y-%m-%d').tolist()     
        indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data, color=indicator_color, title=title, yaxis_name='ATR', is_smooth=False,
                                          legend=legend, watermark=watermark, show_xaxis=False)

        if minimal:
            return self._minimal_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        else:
            return self._base_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        
    def stdev (self, length:int=14, ddof=1, title='Standard Deviation', color=_ISLAND_GREEN, 
                    legend=False, watermark=True, minimal:bool=False): 
        if color:
            indicator_color = color
        else:
            indicator_color = self.chart.mono_color

        indicator_data = self.ta.stdev(length=length, ddof=ddof).round(2)
        time_index = self.data.index.strftime('%Y-%m-%d').tolist()     
        indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data, color=indicator_color, title=title, yaxis_name='STDEV', is_smooth=False,
                                          legend=legend, watermark=watermark, show_xaxis=False)

        if minimal:
            return self._minimal_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        else:
            return self._base_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        
    def linreg (self, length:int=10, title:str='Linear Regression Curve', color=_ORANGE,
            legend=True, watermark=True, minimal:bool=False):
        """
        Simple Moving Average

        Args:
            length (int): Number of periods to consider.
            title (str): Title of the Chart.
            color (str): Color of the indicator line.
            legend (bool): Show legend on the chart.
            watermark (bool): Show watermark on the chart. Default is True
            minimal (bool): Display minimal chart. Default is True to display price chart as line chart, else display as candlestick chart.
        """        
        if color:
            indicator_color = color
        else:
            indicator_color = self.chart.mono_color

        if self.theme == 'dark':
            color_list = list(DARK_MODE_PRIMARY_COLORS.values()) + list(DARK_MODE_SECONDARY_COLORS.values())
        else:
            color_list = list(LIGHT_MODE_PRIMARY_COLORS.values()) + list(LIGHT_MODE_SECONDARY_COLORS.values())

        time_index = self.data.index.strftime('%Y-%m-%d').tolist()
        
        indicator_data = self.ta.sma(length=length).round(2)
        indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data, color=_ORANGE, title=title, yaxis_name='LR', legend=legend, watermark=watermark)
        
        if minimal:
            return self._minimal_chart(indicator_chart=indicator_line, title=title)
        else:
            return self._base_chart(indicator_chart=indicator_line, title=title)