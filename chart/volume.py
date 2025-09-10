import pandas as pd
from pyecharts import options as opts
from vnstock_ta.utils.const import _ISLAND_GREEN, _ORANGE, _TURKISH_SEA, _SLATE_BLUE, _LIME_PUNCH, _GRADIENT_EMERALD, NEUTRAL_INFORMATION_COMPLETE, DARK_MODE_PRIMARY_COLORS, DARK_MODE_SECONDARY_COLORS, LIGHT_MODE_PRIMARY_COLORS, LIGHT_MODE_SECONDARY_COLORS
from vnstock_ta.chart.core import TAChart

class TAVolume(TAChart):
    def __init__(self, data: pd.DataFrame, theme: str = 'light', watermark: bool = True, display: bool = True):
        super().__init__(data, theme, watermark, display)

    def obv (self, title='On-Balance Volume', color=_ISLAND_GREEN, 
                    legend=False, watermark=True, minimal:bool=False):
        
        if color:
            indicator_color = color
        else:
            indicator_color = self.chart.mono_color

        indicator_data = self.ta.obv().round(2)
        time_index = self.data.index.strftime('%Y-%m-%d').tolist()
        
        indicator_line = self.chart._line(time_series=time_index, data_series=indicator_data, color=indicator_color, title=title, yaxis_name='OBV', is_smooth=False,
                                          legend=legend, watermark=watermark, show_xaxis=False)

        if minimal:
            return self._minimal_chart(indicator_chart=indicator_line, title=title, layout='subplot')
        else:
            return self._base_chart(indicator_chart=indicator_line, title=title, layout='subplot')