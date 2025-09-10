import pandas as pd
from pyecharts import options as opts
from vnstock_ta.utils.const import _ISLAND_GREEN, _ORANGE, _TURKISH_SEA, _SLATE_BLUE, _GRADIENT_EMERALD, NEUTRAL_INFORMATION_COMPLETE, DARK_MODE_PRIMARY_COLORS, DARK_MODE_SECONDARY_COLORS, LIGHT_MODE_PRIMARY_COLORS, LIGHT_MODE_SECONDARY_COLORS
from vnstock_ta.chart.core import TAChart


# extend the TAChart class

class TATrend(TAChart):
    def __init__(self, data: pd.DataFrame, theme: str = 'light', watermark: bool = True, display: bool = True):
        super().__init__(data, theme, watermark, display)

    def sma (self, length:int=10, title:str='Simple Moving Average', color=_ORANGE,
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
        
        # check if length is a list
        if isinstance(length, list):
            indicator_data = self.ta.sma(length=length[0]).round(2)
            indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data, color=indicator_color, title=title, yaxis_name=f'SMA{length[0]}', legend=legend, watermark=watermark)

            for i in range(1, len(length)):
                new_indicator_data = self.ta.sma(length=length[i])
                indicator_line = self.chart._add_line(line_chart=indicator_line, data_series=new_indicator_data, color=color_list[i], title=f'SMA - {length[i]} kỳ', yaxis_name=f'SMA{length[i]}')
        else:
            indicator_data = self.ta.sma(length=length).round(2)
            indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data, color=indicator_color, title=title, yaxis_name='SMA', legend=legend, watermark=watermark)
        
        if minimal:
            return self._minimal_chart(indicator_chart=indicator_line, title=title)
        else:
            return self._base_chart(indicator_chart=indicator_line, title=title)

    def ema (self, length:int=10, title:str='Exponential Moving Average', color=_ORANGE,
            legend=True, watermark=True, minimal:bool=False):
        """
        Exponential Moving Average

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
        
        # check if length is a list
        if isinstance(length, list):
            indicator_data = self.ta.ema(length=length[0]).round(2)
            indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data, color=indicator_color, title=title, yaxis_name=f'EMA{length[0]}', legend=legend, watermark=watermark)

            for i in range(1, len(length)):
                new_indicator_data = self.ta.ema(length=length[i])
                indicator_line = self.chart._add_line(line_chart=indicator_line, data_series=new_indicator_data, color=color_list[i], title=f'EMA - {length[i]} kỳ', yaxis_name=f'EMA{length[i]}')
        else:
            indicator_data = self.ta.ema(length=length).round(2)
            indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data, color=indicator_color, title=title, yaxis_name='EMA', legend=legend, watermark=watermark)
        
        if minimal:
            return self._minimal_chart(indicator_chart=indicator_line, title=title)
        else:
            return self._base_chart(indicator_chart=indicator_line, title=title)
        
    def vwap (self, anchor:str='D', title:str='VWAP - Volume Weighted Average Price', color=_ORANGE,
            legend=True, watermark=True, minimal:bool=False):
        """
        Volume Weighted Average Price

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

        if isinstance(anchor, list):
            indicator_data = self.ta.vwap(anchor=anchor[0]).round(2)
            indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data, color=indicator_color, title=title, yaxis_name=f'VWAP - {anchor[0]}', legend=legend, watermark=watermark)

            for i in range(1, len(anchor)):
                new_indicator_data = self.ta.vwap(anchor=anchor[i])
                indicator_line = self.chart._add_line(line_chart=indicator_line, data_series=new_indicator_data, color=color_list[i], title=f'VWAP - {anchor[i]}', yaxis_name=f'VWAP - {anchor[i]}')
        else:
            indicator_data = self.ta.vwap(anchor=anchor)
            indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data, color=indicator_color, title=title, yaxis_name='VWAP', legend=legend, watermark=watermark)
        
        if minimal:
            return self._minimal_chart(indicator_chart=indicator_line, title=title)
        else:
            return self._base_chart(indicator_chart=indicator_line, title=title)
        
    def vwma (self, length:int=10, title:str='VWMA - Volume Weighted Moving Average', color=_ORANGE,
            legend=True, watermark=True, minimal:bool=False):
        """
        Volume Weighted Moving Average

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
        
        # check if length is a list
        if isinstance(length, list):
            indicator_data = self.ta.vwma(length=length[0]).round(2)
            indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data, color=indicator_color, title=title, yaxis_name=f'VWMA{length[0]}', legend=legend, watermark=watermark)

            for i in range(1, len(length)):
                new_indicator_data = self.ta.vwma(length=length[i])
                indicator_line = self.chart._add_line(line_chart=indicator_line, data_series=new_indicator_data, color=color_list[i], title=f'VWMA - {length[i]}', yaxis_name=f'VWMA{length[i]}')
        else:
            indicator_data = self.ta.vwma(length=length)
            indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data, color=indicator_color, title=title, yaxis_name='VWMA', legend=legend, watermark=watermark)
        
        if minimal:
            return self._minimal_chart(indicator_chart=indicator_line, title=title)
        else:
            return self._base_chart(indicator_chart=indicator_line, title=title)

    def psar (self, af0: float = 0.02, af: float = 0.02, max_af: float = 0.2, title='Parabollic Stop and Reverse', color=_ORANGE, symbol_size=5,
            legend=True, watermark=True, minimal:bool=False):
        """
        Parabolic Stop and Reverse

        Args:
            af0 (float): Initial Acceleration Factor. Default: 0.02
            af (float): Acceleration Factor. Default: 0.02
            max_af (float): Maximum Acceleration Factor. Default: 0.2
        """
        if color:
            indicator_color = color
        else:
            indicator_color = self.chart.mono_color

        indicator_data = self.ta.psar(af0=af0, af=af, max_af=max_af).round(2)
        # create psa_series by fillna the first column in indicator_data with the second column
        psar_series = indicator_data.iloc[:, 0].fillna(indicator_data.iloc[:, 1])
        time_index = self.data.index.strftime('%Y-%m-%d').tolist()
        indicator_scatter = self.chart._scatter(time_series=time_index, data_series=psar_series, color=indicator_color, symbol_size=symbol_size, title=title, yaxis_name='PSAR', legend=legend, watermark=watermark)
        
        if minimal:
            return self._minimal_chart(indicator_chart=indicator_scatter, title=title)
        else:
            return self._base_chart(indicator_chart=indicator_scatter, title=title)
        
    def supertrend (self, length: int = 10, multiplier: float = 3, title='Supertrend', color=[_ISLAND_GREEN, _ORANGE], 
                    legend=True, watermark=True, minimal:bool=False):
        """
        Supertrend

        Args:
            length (int) : length for ATR calculation. Default: 7
            multiplier (float): Coefficient for upper and lower band distance to
                midrange. Default: 3.0
            title (str): Title of the Chart.
            color (str): List of 2 colors to represent the Supertrend and Supertrend Direction values.
            legend (bool): Show legend on the chart.
            watermark (bool): Show watermark on the chart. Default is True
            minimal (bool): Display minimal chart. Default is True to display price chart as line chart, else display as candlestick chart.
        """
        if color:
            indicator_color = color
        else:
            indicator_color = self.chart.mono_color

        indicator_data = self.ta.supertrend(length=length, multiplier=multiplier).round(2)
        time_index = self.data.index.strftime('%Y-%m-%d').tolist()
        indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data.iloc[:, -2], color=indicator_color[0], title=title, yaxis_name='Up Trend', legend=legend, watermark=watermark)
        indicator_line = self.chart._add_line(line_chart=indicator_line, data_series=indicator_data.iloc[:, -1], color=indicator_color[1], title=title, yaxis_name='Down Trend')

        if minimal:
            return self._minimal_chart(indicator_chart=indicator_line, title=title)
        else:
            return self._base_chart(indicator_chart=indicator_line, title=title)
         
    def adx (self, length:int=14, title='Average Directional Index', color=_ORANGE, 
                    legend=False, watermark=True, minimal:bool=False):
        
        if color:
            indicator_color = color
        else:
            indicator_color = self.chart.mono_color

        indicator_data = self.ta.adx(length=length).round(2).iloc[:, 0]
        time_index = self.data.index.strftime('%Y-%m-%d').tolist()
        markline = opts.MarkLineOpts(data=[opts.MarkLineItem(y=25, name="Có xu hướng", 
                                                             linestyle_opts=opts.LineStyleOpts(width=1, color=_ISLAND_GREEN, opacity=0.5, type_='dashed'))],
                                                             label_opts=opts.LabelOpts(is_show=False)) # , opts.MarkLineItem(y=30, name="Quá bán")
        indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data, color=indicator_color, title=title, yaxis_name='ADX', 
                                          legend=legend, watermark=watermark, show_xaxis=False, markline_opts=markline)

        if minimal:
            return self._minimal_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        else:
            return self._base_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        
    def aroon (self, length:int=14, title='Aroon', color=[_ISLAND_GREEN, _ORANGE], 
                    legend=False, watermark=True, minimal:bool=False):
        if color:
            indicator_color = color
        else:
            indicator_color = [_ISLAND_GREEN, _ORANGE]

        indicator_data = self.ta.aroon(length=length).round(2)
        aroon_up = indicator_data.iloc[:, 1]
        aroon_down = indicator_data.iloc[:, 0]
        time_index = self.data.index.strftime('%Y-%m-%d').tolist()
        indicator_line = self.chart._line(time_series=time_index, data_series=aroon_up, color=indicator_color[0], title=title, yaxis_name='Aroon Up', is_smooth=False, legend=legend, watermark=watermark, show_xaxis=False)
        indicator_line = self.chart._add_line(line_chart=indicator_line, data_series=aroon_down, color=indicator_color[1], title=title, yaxis_name='Aroon Down', is_smooth=False)

        if minimal:
            return self._minimal_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        else:
            return self._base_chart(indicator_chart=indicator_line, title=title, layout='subplot')
