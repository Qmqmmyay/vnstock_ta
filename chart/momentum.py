import pandas as pd
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from vnstock_ta.utils.const import _ISLAND_GREEN, _ORANGE, _TURKISH_SEA, _SLATE_BLUE, _LIME_PUNCH, _GRADIENT_EMERALD, NEUTRAL_INFORMATION_COMPLETE, DARK_MODE_PRIMARY_COLORS, DARK_MODE_SECONDARY_COLORS, LIGHT_MODE_PRIMARY_COLORS, LIGHT_MODE_SECONDARY_COLORS
from vnstock_ta.chart.core import TAChart


# extend the TAChart class

class TAMomentum(TAChart):
    def __init__(self, data: pd.DataFrame, theme: str = 'light', watermark: bool = True, display: bool = True):
        super().__init__(data, theme, watermark, display)

    def rsi (self, length:int=14, title='Relative Strength Index', color=_ISLAND_GREEN, 
                    legend=False, watermark=True, minimal:bool=False):
        
        if color:
            indicator_color = color
        else:
            indicator_color = self.chart.mono_color

        indicator_data = self.ta.rsi(length=length).round(2)
        time_index = self.data.index.strftime('%Y-%m-%d').tolist()
        markline = opts.MarkLineOpts(data=[opts.MarkLineItem(y=70, name="Quá mua", 
                                                             linestyle_opts=opts.LineStyleOpts(width=1, color=_SLATE_BLUE, opacity=0.5, type_='dashed')),
                                            opts.MarkLineItem(y=30, name="Quá bán", 
                                                             linestyle_opts=opts.LineStyleOpts(width=1, color=_SLATE_BLUE, opacity=0.5, type_='dashed'))
                                                             ],
                                                             label_opts=opts.LabelOpts(is_show=False)) 
        
        indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data, color=indicator_color, title=title, yaxis_name='RSI', is_smooth=False,
                                          legend=legend, watermark=watermark, show_xaxis=False, markline_opts=markline)

        if minimal:
            return self._minimal_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        else:
            return self._base_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        
    def macd (self, fast:int=12, slow:int=26, signal:int=9, title='Moving Average Convergence Divergence', color=_ORANGE, 
                    legend=False, watermark=True, minimal:bool=False):
        
        if color:
            indicator_color = color
        else:
            indicator_color = self.chart.mono_color

        indicator_data = self.ta.macd(fast=fast, slow=slow, signal=signal).round(2)
        macd_line = indicator_data.iloc[:, 0]
        macd_signal = indicator_data.iloc[:, 2]
        macd_histogram = indicator_data.iloc[:, 1] 

        def determine_color(histogram, prev_histogram):
            if histogram > 0 and histogram >= prev_histogram:
                return "#3CB371"  # Green
            elif histogram > 0 and histogram < prev_histogram:
                return "#90EE90"  # Light Green
            elif histogram < 0 and histogram <= prev_histogram:
                return "#FF6347"  # Red
            elif histogram < 0 and histogram > prev_histogram:
                return "#FFB6C1"  # Light Red
            else:
                return "#000000"  # Should not be reached

        hist_colors = [determine_color(macd_histogram.iloc[i], macd_histogram.iloc[i-1] if i > 0 else 0) for i in range(len(indicator_data))]
        indicator_color = JsCode(
                            """
                            function(params) {
                                var colors = %s;
                                return colors[params.dataIndex];
                            }
                            """ % hist_colors
                        )        

        time_index = self.data.index.strftime('%Y-%m-%d').tolist()
        indicator_line = self.chart._line(time_series=time_index, data_series=macd_line, color=indicator_color, title=title, yaxis_name='MACD', 
                                          legend=legend, watermark=watermark, show_xaxis=False)
        
        indicator_line = self.chart._add_line(line_chart=indicator_line, data_series=macd_signal, color=_ISLAND_GREEN, title='', yaxis_name='Signal')
        
        histogram_bar = self.chart._hist(time_series=time_index, data_series=macd_histogram, title='', color=indicator_color, yaxis_name='Histogram', show_xaxis=False)

        subplots = histogram_bar.overlap(indicator_line)

        if minimal:
            return self._minimal_chart(indicator_chart=subplots, title=title, layout='subplot')
        else:
            return self._base_chart(indicator_chart=subplots, title=title, layout='subplot')

    def willr (self, length:int=14, title='William %R', color=_ISLAND_GREEN, 
                    legend=False, watermark=True, minimal:bool=False):
        
        if color:
            indicator_color = color
        else:
            indicator_color = self.chart.mono_color

        indicator_data = self.ta.willr(length=length).round(2)
        time_index = self.data.index.strftime('%Y-%m-%d').tolist()
        markline = opts.MarkLineOpts(data=[opts.MarkLineItem(y=-20, name="Quá mua", 
                                                             linestyle_opts=opts.LineStyleOpts(width=1, color=_SLATE_BLUE, opacity=0.5, type_='dashed')),
                                            opts.MarkLineItem(y=-80, name="Quá bán", 
                                                             linestyle_opts=opts.LineStyleOpts(width=1, color=_SLATE_BLUE, opacity=0.5, type_='dashed'))
                                                             ],
                                                             label_opts=opts.LabelOpts(is_show=False)) # , opts.MarkLineItem(y=30, name="Quá bán")
        indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data, color=indicator_color, title=title, yaxis_name='William %R', is_smooth=False,
                                          legend=legend, watermark=watermark, show_xaxis=False, markline_opts=markline)

        if minimal:
            return self._minimal_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        else:
            return self._base_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        
    def cmo (self, length:int=14, title='Chande Momentum Oscilator', color=_ISLAND_GREEN, 
                    legend=False, watermark=True, minimal:bool=False):
        
        if color:
            indicator_color = color
        else:
            indicator_color = self.chart.mono_color

        indicator_data = self.ta.cmo(length=length).round(2)
        time_index = self.data.index.strftime('%Y-%m-%d').tolist()
        indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data, color=indicator_color, title=title, yaxis_name='CMO', is_smooth=False,
                                          legend=legend, watermark=watermark, show_xaxis=False)

        if minimal:
            return self._minimal_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        else:
            return self._base_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        
    def stoch (self, k=14, d=3, smooth_k=3, title='Stochastic Oscillator', color=_ORANGE, 
                    legend=False, watermark=True, minimal:bool=False):
        
        if color:
            indicator_color = color
        else:
            indicator_color = self.chart.mono_color

        indicator_data = self.ta.stoch(k=k, d=d, smooth_k=smooth_k)
        stoch_k = indicator_data.iloc[:, 0]
        stoch_d = indicator_data.iloc[:, 1]

        time_index = self.data.index.strftime('%Y-%m-%d').tolist()

        markline = opts.MarkLineOpts(data=[opts.MarkLineItem(y=80, name="Quá mua", 
                                                             linestyle_opts=opts.LineStyleOpts(width=1, color=_SLATE_BLUE, opacity=0.5, type_='dashed')),
                                            opts.MarkLineItem(y=20, name="Quá bán", 
                                                             linestyle_opts=opts.LineStyleOpts(width=1, color=_SLATE_BLUE, opacity=0.5, type_='dashed'))
                                                             ],
                                                             label_opts=opts.LabelOpts(is_show=False)) 
        
        indicator_line = self.chart._line(time_series=time_index, data_series=stoch_k, color=_ISLAND_GREEN, title='', yaxis_name='STOCH', is_smooth=False,
                                          legend=legend, watermark=watermark, show_xaxis=False, markline_opts=markline)
        indicator_line = self.chart._add_line(line_chart=indicator_line, data_series=stoch_d, color=_ORANGE, title='', yaxis_name='STOCH')

        if minimal:
            return self._minimal_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        else:
            return self._base_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        
    def roc (self, length:int=9, title='Rate of Change', color=_ISLAND_GREEN, 
                    legend=False, watermark=True, minimal:bool=False):
        
        if color:
            indicator_color = color
        else:
            indicator_color = self.chart.mono_color

        indicator_data = self.ta.roc(length=length).round(2)
        time_index = self.data.index.strftime('%Y-%m-%d').tolist()
        indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data, color=indicator_color, title=title, yaxis_name='ROC', is_smooth=False,
                                          legend=legend, watermark=watermark, show_xaxis=False)

        if minimal:
            return self._minimal_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        else:
            return self._base_chart(indicator_chart=indicator_line, title=title, layout='subplot')

    def mom (self, length:int=10, title='Momentum Indicator', color=_ISLAND_GREEN, 
                    legend=False, watermark=True, minimal:bool=False):
        
        if color:
            indicator_color = color
        else:
            indicator_color = self.chart.mono_color

        indicator_data = self.ta.mom(length=length).round(2)
        time_index = self.data.index.strftime('%Y-%m-%d').tolist()
        indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data, color=indicator_color, title=title, yaxis_name='MOM', is_smooth=False,
                                          legend=legend, watermark=watermark, show_xaxis=False)

        if minimal:
            return self._minimal_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        else:
            return self._base_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        
