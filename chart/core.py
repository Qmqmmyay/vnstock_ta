import pandas as pd
import numpy as np
import panel as pn
from typing import List, Dict, Any, Union, Tuple
from pyecharts import options as opts
from pyecharts.charts import Kline, Line, Bar, Scatter, Boxplot, HeatMap, Grid, Page
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from vnstock_ta.get_data import DataSource
from vnstock_ta.utils.env import SystemInfo
from vnstock_ta.utils.const import _EMERALD_GREEN, _CRIMSON_RED, _SLATE_BLUE, _GRADIENT_EMERALD

try:
    from IPython.display import display, HTML
    IS_NOTEBOOK = True
except ImportError:
    IS_NOTEBOOK = False

class BaseChart:
    def __init__(self, candle_data: pd.DataFrame, theme: str = "dark", color_category: str = 'neutral', width: str = "1500px", height: str = "900px"):
        """
        Initialize the chart with candle data, theme, and color category.

        Args:
            candle_data (pd.DataFrame): Candlestick data containing open, high, low, close, and volume.
            theme (str): Theme of the chart. Options are 'dark' or 'light'.
            color_category (str): Color category for the chart. Options are 'positive', 'negative', 'neutral', 'colorful'.
        """
        self.theme = theme.upper()
        self.color_category = color_category
        self.width = width
        self.height = height
        self.is_notebook = IS_NOTEBOOK
        self.data = candle_data
        self._validate_inputs()
        self._ui_config()
        self._config(theme=self.theme, color_category=color_category)

    def _validate_inputs(self):
        valid_themes = ['DARK', 'LIGHT']
        valid_categories = ['positive', 'negative', 'neutral', 'colorful']

        if self.theme not in valid_themes:
            raise ValueError(f"Unknown theme: {self.theme}. Valid themes are {valid_themes}")

        if self.color_category not in valid_categories:
            raise ValueError(f"Unknown category: {self.color_category}. Valid categories are {valid_categories}")

    def _ui_config(self):
        """
        Detect the UI configuration for the current machine.
        """
        system_info = SystemInfo()
        self.interface = system_info.interface()
        self.hosting = system_info.hosting()
        self.os = system_info.os()

        # Additional imports for Google Colab
        if self.hosting == "Google Colab":
            pn.extension('echarts')

    def _render(self, chart: Any, display: bool = True) -> Union[pn.pane.ECharts]:
        """
        Configure the preference for chart rendering.

        Args:
            chart: The chart object.
            display (bool): Render the chart directly or just return the raw chart object for further manipulation.

        Returns:
            Rendered chart or raw chart object.
        """
        if display:
            if self.hosting == "Google Colab":
                # try:
                #     return pn.pane.ECharts(chart)
                # except:
                return self._show_html(chart.render('chart.html'))
            elif self.hosting == "Jupyterlab":
                return self._show_html(chart.render('chart.html'))
            if self.interface == "Jupyter":
                return chart.render_notebook()
            else:
                return chart.render()
        else:
            return chart

    def _show_html(self, filename: str):
        """
        Display the saved HTML file in Google Colab.

        Args:
            filename (str): The path to the HTML file.
        """
        if self.is_notebook == True:
            with open(filename, 'r') as f:
                html_content = f.read()
            display(HTML(html_content))

    def _apply_color_palette(self, theme: str, color_category: str = 'neutral'):
        """
        Apply the color palette based on the theme and color category.
        """
        color_palettes = {
            'DARK': {
                'neutral': {
                    'bull_color': _EMERALD_GREEN,
                    'bear_color': _CRIMSON_RED,
                    'bg_color': '#0E1114',
                    'mono_color': _EMERALD_GREEN,
                    'text_color': "#fff",
                    'indicator_color': "#30A2DA",
                    'indicator_1_color': "#37745B",
                    'indicator_2_color': "#FC4F30",
                    'indicator_3_color': "#E5AE38",
                    'indicator_4_color': "#DA6A00",
                    'indicator_5_color': "#6A7793"
                },
                'positive': {
                    'bull_color': "#2BAE66FF",
                    'bear_color': "#EEA47FFF",
                    'bg_color': '#0E1114',
                    'mono_color': '#2BAE66FF',  # ISLAND GREEN
                    'text_color': "#fff",
                    'indicator_color': "#89ABE3FF",
                    'indicator_1_color': "#00539CFF",
                    'indicator_2_color': "#0063B2FF",
                    'indicator_3_color': "#FEE715FF",
                    'indicator_4_color': "#ADEFD1FF",
                    'indicator_5_color': "#D7A9E3FF"
                },
                'negative': {
                    'bull_color': "#2C5F2D",
                    'bear_color': "#F65058FF",
                    'bg_color': '#101820FF',
                    'mono_color': '#2C5F2D',  # FOREST GREEN
                    'text_color': "#fff",
                    'indicator_color': "#00539CFF",
                    'indicator_1_color': "#949398FF",
                    'indicator_2_color': "#A2A2A1FF",
                    'indicator_3_color': "#606060FF",
                    'indicator_4_color': "#28334AFF",
                    'indicator_5_color': "#006B38FF"
                },
                'colorful': {
                    'bull_color': "#6D904F",
                    'bear_color': "#FC4F30",
                    'bg_color': '#0E1114',
                    'mono_color': '#6D904F',  # VITAL GREEN
                    'text_color': "#fff",
                    'indicator_color': "#30A2DA",
                    'indicator_1_color': "#37745B",
                    'indicator_2_color': "#FC4F30",
                    'indicator_3_color': "#E5AE38",
                    'indicator_4_color': "#DA6A00",
                    'indicator_5_color': "#6A7793"
                }
            },
            'LIGHT': {
                'neutral': {
                    'bull_color': _EMERALD_GREEN,
                    'bear_color': _CRIMSON_RED,
                    'bg_color': "#F9F7FA",
                    'mono_color': _EMERALD_GREEN,
                    'text_color': "#000000",
                    'indicator_color': "#30A2DA",
                    'indicator_1_color': "#37745B",
                    'indicator_2_color': "#FC4F30",
                    'indicator_3_color': "#E5AE38",
                    'indicator_4_color': "#DA6A00",
                    'indicator_5_color': "#6A7793"
                },
                'positive': {
                    'bull_color': "#2BAE66FF",
                    'bear_color': "#EEA47FFF",
                    'bg_color': "#F9F7FA",
                    'mono_color': '#2BAE66FF',  # ISLAND GREEN
                    'text_color': "#000000",
                    'indicator_color': "#89ABE3FF",
                    'indicator_1_color': "#00539CFF",
                    'indicator_2_color': "#0063B2FF",
                    'indicator_3_color': "#FEE715FF",
                    'indicator_4_color': "#ADEFD1FF",
                    'indicator_5_color': "#D7A9E3FF"
                },
                'negative': {
                    'bull_color': "#2C5F2D",
                    'bear_color': "#F65058FF",
                    'bg_color': "#FCF6F5FF",
                    'mono_color': '#2C5F2D',  # FOREST GREEN
                    'text_color': "#000000",
                    'indicator_color': "#00539CFF",
                    'indicator_1_color': "#949398FF",
                    'indicator_2_color': "#A2A2A1FF",
                    'indicator_3_color': "#606060FF",
                    'indicator_4_color': "#28334AFF",
                    'indicator_5_color': "#006B38FF"
                },
                'colorful': {
                    'bull_color': "#6D904F",
                    'bear_color': "#FC4F30",
                    'bg_color': "#F9F7FA",
                    'mono_color': '#6D904F',  # VITAL GREEN
                    'text_color': "#000000",
                    'indicator_color': "#30A2DA",
                    'indicator_1_color': "#37745B",
                    'indicator_2_color': "#FC4F30",
                    'indicator_3_color': "#E5AE38",
                    'indicator_4_color': "#DA6A00",
                    'indicator_5_color': "#6A7793"
                }
            }
        }

        palette = color_palettes[theme][color_category]
        self.bull_color = palette['bull_color']
        self.bear_color = palette['bear_color']
        self.bg_color = palette['bg_color']
        self.mono_color = palette['mono_color']
        self.text_color = palette['text_color']
        self.indicator_color = palette['indicator_color']
        self.indicator_1_color = palette['indicator_1_color']
        self.indicator_2_color = palette['indicator_2_color']
        self.indicator_3_color = palette['indicator_3_color']
        self.indicator_4_color = palette['indicator_4_color']
        self.indicator_5_color = palette['indicator_5_color']

    def _common_global_opts(self, title: str, zoomable: bool, zoom_slider: bool, subplot: bool, legend: bool, tools: bool, watermark=False) -> Dict[str, Any]:
        """
        Get common global options for charts.
        
        Args:
            title (str): Title of the chart.
            zoomable (bool): Enable zoom functionality.
            zoom_slider (bool): Display zoom slider.
            subplot (bool): Create subplot.
            legend (bool): Show legend.
            tools (bool): Show toolbox and brush tools.
            
        Returns:
            Dict[str, Any]: Common global options.
        """

        global_opts = {
            "tooltip_opts": opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="cross",
                background_color=self.bg_color,
                border_width=1,
                border_color="#ccc",
                textstyle_opts=opts.TextStyleOpts(color=self.text_color),
            ),
            "axispointer_opts": opts.AxisPointerOpts(
                is_show=True,
                link=[{"xAxisIndex": "all"}],
                label=opts.LabelOpts(background_color="#777"),
            ),
            "graphic_opts": self._watermark(show=watermark)
        }

        if tools:
            global_opts["toolbox_opts"] = opts.ToolboxOpts(
                is_show=True,
                orient="vertical",
                pos_left="right",
                feature=opts.ToolBoxFeatureOpts(
                    save_as_image={"show": True, "title": "Save as Image", "type_": "png", "pixel_ratio": 1},
                    restore={"show": True, "title": "Restore"},
                    data_view={"show": True, "title": "Data View"},
                    data_zoom={"show": True, "title": "Data Zoom"},
                    magic_type={"show": True, "title": "Magic Type", "type": ["line", "bar", "stack", "tiled"], "option": {"seriesIndex": "all"}, "line_title": "Line Chart", "bar_title": "Bar Chart", "stack_title": "Stack Chart", "tiled_title": "Tiled Chart"},
                ),
            )
            global_opts["brush_opts"] = opts.BrushOpts(
                tool_box=["rect", "polygon", "lineX", "lineY", "keep", "clear"],
                x_axis_index="all",
                brush_link="all",
                out_of_brush={"colorAlpha": 0.1},
                brush_type="lineX",
            )

        if zoomable:
            global_opts["datazoom_opts"] = [
                opts.DataZoomOpts(
                    is_show=zoom_slider,
                    type_="slider",
                    xaxis_index=[0, 1, 2],
                    range_start=0,
                    range_end=100,
                ),
                opts.DataZoomOpts(
                    is_show=True,
                    type_="inside",
                    xaxis_index=[0, 1, 2],
                    range_start=0,
                    range_end=100,
                ),
            ]

        if subplot:
            global_opts["title_opts"] = opts.TitleOpts(
                title=title,
                pos_left='center',
                pos_top=20,
                title_textstyle_opts=opts.TextStyleOpts(font_family=self.font_family, font_size=self.font_size, color=self.text_color)
            )
        else:
            global_opts["title_opts"] = opts.TitleOpts(
                title=title,
                pos_left='center',
                pos_top=20,
                title_textstyle_opts=opts.TextStyleOpts(font_family=self.font_family, font_size=self.font_size * 1.5, color=self.text_color)
            )

        if legend:
            global_opts["legend_opts"] = opts.LegendOpts(is_show=True)
        else:
            global_opts["legend_opts"] = opts.LegendOpts(is_show=False)

        return global_opts

    def _config(self, theme: str = 'dark', color_category: str = 'neutral', width: str = "1500px", height: str = "900px"):
        """
        Set the chart configuration based on the theme and category.
        """
        self._apply_color_palette(theme, color_category)
        
        if width:
            self.chart_width = width
        else:
            self.chart_width = "1500px"

        if height:
            self.chart_height = height
        else:
            self.chart_height = "900px"

        self.font_family = "Nunito"
        self.font_size = 18
        self.logo_width = 300
        self.logo_height = 112
        self.logo_right_pos = int(self.chart_width.replace('px', '')) / 2 - self.logo_width / 2
        self.logo_top_pos = int(self.chart_height.replace('px', '')) / 4
        self.logo_opacity = 0.3
        self.buy_marker = "diamond"
        self.sell_marker = 'triangle'
        self.legend_top_pos = self.legend_bottom_pos = 10
        self.pos_left = "center"
        self.data_zoom_pos = "inside"
        self.data_zoom_range_start = 40


        self.data_zoom_range_end = 100
        self.gridline_width = 0.3
        self.gridline_opacity = 0.1
        self.gridline_splitx = 20
        self.gridline_splity = 2

        if theme == 'DARK':
            self.logo_path = "https://vnstocks.com/img/vnstock_logo_trans_rec_hoz_bw.png"
        elif theme == 'LIGHT':
            self.logo_path = "https://vnstocks.com/img/vnstock_logo_trans_rec_hoz.png"

    def _watermark(self, show: bool = True) -> List[opts.GraphicImage]:
        """
        Create watermark configuration for the chart.

        Args:
            show (bool): Show or hide the watermark.

        Returns:
            List[opts.GraphicImage]: Watermark configuration.
        """
        if show:
            watermark = [
                opts.GraphicImage(
                    graphic_item=opts.GraphicItem(
                        id_="logo", left=50, top=self.logo_top_pos, z=-10, bounding="raw", origin=[75, 75]
                    ),
                    graphic_imagestyle_opts=opts.GraphicImageStyleOpts(
                        image=self.logo_path,
                        width=self.logo_width,
                        height=self.logo_height,
                        opacity=self.logo_opacity,
                    ),
                )
            ]
        else:
            watermark = []
        return watermark

    def _volume(self, time_series: List[str], data_series: List[Union[Dict[str, Any], float]], title: str = "Volume", yaxis_name: str = 'Volume', subplot=True,
                compatibility: bool = False, color: str = _SLATE_BLUE, label: bool = False,
                zoomable: bool = True, zoom_slider: bool = False, legend=False, theme: str = 'dark', watermark: bool =False) -> Bar:
        """
        Create a volume chart layer for the chart which will be used in conjunction with the candlestick chart to create the final candlestick chart.

        Args:
            time_series (List[str]): List of time series data.
            data_series (List[Union[Dict[str, Any], float]]): List of volume data or a DataFrame.
            title (str): Title of the volume chart.
            subplot (bool): Create subplot or display as a main chart.
            compatibility (bool): Use compatibility mode for the volume chart.
            color (str): Color of the bars.
            label (bool): Show labels on the bars.
            zoomable (bool): Enable zoom functionality.
            zoom_slider (bool): Display zoom slider if zoomable is True.
            theme (str): Theme of the chart.

        Returns:
            Bar: The configured Bar chart.
        """
        theme_opts = ThemeType.DARK if theme.upper() == 'DARK' else ThemeType.LIGHT

        _opts_volume_label = opts.LabelOpts(is_show=True) if compatibility else opts.LabelOpts(
            formatter=JsCode("""
                function(value) {
                    if (value >= 1000000) {
                        return (value / 1000000).toFixed(1) + 'M';
                    } else if (value >= 1000) {
                        return (value / 1000).toFixed(1) + 'K';
                    }
                    return value;
                }
            """),
        )

        if not all(isinstance(d, dict) and "itemStyle" in d for d in data_series):
            data_series = [{"value": d, "itemStyle": {"color": color}} for d in data_series]

        volume_bar = (
            Bar(init_opts=opts.InitOpts(theme=theme_opts, bg_color=self.bg_color))
            .add_xaxis(xaxis_data=time_series)
            .add_yaxis(
                series_name=yaxis_name,
                y_axis=data_series,
                itemstyle_opts=opts.ItemStyleOpts(color=color),
                label_opts=opts.LabelOpts(is_show=label),  # Use the defined label options
            )
        )

        specific_opts = {
            "xaxis_opts": opts.AxisOpts(
                type_="category",
                is_scale=True,
                boundary_gap=False,
                axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=True, 
                        linestyle_opts=opts.LineStyleOpts(opacity=self.gridline_opacity)),
                axislabel_opts=opts.LabelOpts(is_show=True), 
                split_number=self.gridline_splitx,
                min_="dataMin",
                max_="dataMax",
            ),
            "yaxis_opts": opts.AxisOpts(
                name=yaxis_name,
                is_scale=True,
                split_number=self.gridline_splity,
                axislabel_opts=_opts_volume_label,
                axisline_opts=opts.AxisLineOpts(is_show=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=True, 
                        linestyle_opts=opts.LineStyleOpts(opacity=self.gridline_opacity)),
                position='right'
            ),
        }

        common_opts = self._common_global_opts(title=title, zoomable=zoomable, zoom_slider=zoom_slider, subplot=subplot, legend=legend, tools=False, watermark=watermark)
        # remove title_opts from common_opts
        common_opts.pop("title_opts", None)
        volume_bar.set_global_opts(**{**specific_opts, **common_opts})
        return volume_bar

    def _kline(self, time_series: List[str], ohlc_data: List[List[float]], title: str = 'Candlestick Chart', yaxis_name: str = 'Price', right_y:bool=True, show_xaxis: bool = False,
               tools: bool = True, watermark: bool = False) -> Kline:
        """
        Create the candlestick layer for the chart which will be used in conjunction with the volume bar chart to create the final candlestick chart.

        Args:
            time_series (List[str]): List of time series data.
            ohlc_data (List[List[float]]): OHLC data.
            title (str): Title of the candlestick chart.
            yaxis_name (str): Name of the y-axis.
            right_y (bool): Position of the y-axis.
            show_xaxis (bool): Show x-axis.
            tools (bool): Show or hide toolbox and brush tools.
            watermark (bool): Show or hide watermark.

        Returns:
            Kline: The configured Kline chart.
        """
        if show_xaxis:
            _xaxis_label_opt= opts.LabelOpts(is_show=True)
            _show_xaxis = True
        else:
            _xaxis_label_opt = opts.LabelOpts(is_show=False)
            _show_xaxis = False

        yaxis_pos = "right" if right_y else "left"
        kline = (
            Kline(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color=self.bg_color))
            .add_xaxis(xaxis_data=time_series)
            .add_yaxis(
                series_name=title,
                y_axis=ohlc_data,
                itemstyle_opts=opts.ItemStyleOpts(
                    color=self.bull_color,
                    color0=self.bear_color,
                    border_color=self.bull_color,
                    border_color0=self.bear_color,
                ),
            )
        )

        specific_opts = {
            "yaxis_opts": opts.AxisOpts(
                name=yaxis_name,
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=False, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, 
                    linestyle_opts=opts.LineStyleOpts(opacity=self.gridline_opacity)
                ),
                position=yaxis_pos
            ),
            "xaxis_opts": opts.AxisOpts(
                is_show=_show_xaxis,
                is_inverse=_show_xaxis,
                axislabel_opts=_xaxis_label_opt,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=False, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, 
                    linestyle_opts=opts.LineStyleOpts(opacity=self.gridline_opacity)
                ),
            ),
            "visualmap_opts": opts.VisualMapOpts(
                is_show=False,
                dimension=2

,
                series_index=5,
                is_piecewise=True,
                pieces=[
                    {"value": 1, "color": self.bull_color},
                    {"value": -1, "color": self.bear_color},
                ],
            ),
        }

        common_opts = self._common_global_opts(title=title, zoomable=True, zoom_slider=True, subplot=False, legend=False, tools=tools, watermark=watermark)
        
        kline.set_global_opts(**{**specific_opts, **common_opts})
        return kline

    def _line(self, time_series: List[str], data_series: List[float], mark_points_data: List[opts.MarkPointItem] = None,
              title: str = "Line Chart", yaxis_name:str='Price', right_y: bool = True, 
              color: str = _EMERALD_GREEN, is_step: bool = False, is_smooth:bool=True, area_style: bool = False, gradient_color: Dict = None, 
              label: bool = False, zoomable: bool = True, subplot: bool = False, legend: bool = False, tools: bool = True, show_xaxis: bool = True,
              line_width: int = 1, zoom_slider: bool = False, theme: str = 'dark', watermark: bool = False, **kwargs) -> Line:
        """
        Create a line/step line chart based on series data and configuration.

        Args:
            time_series (List[str]): List of time series data.
            data_series (List[float]): List of series data.
            mark_points_data (List[opts.MarkPointItem]): List of mark points data.
            title (str): Title of the chart.
            yaxis_name (str): Name of the y-axis.
            right_y (bool): Position of the y-axis.
            color (str): Color of the line.
            is_step (bool): Use step line chart.
            is_smooth (bool): Use smooth line chart.
            area_style (bool): Use area style for the line chart.
            gradient_color (Dict): Gradient color for the area style.
            label (bool): Show symbol on the line.
            zoomable (bool): Enable zoom functionality.
            subplot (bool): Create subplot.
            legend (bool): Show legend.
            tools (bool): Show toolbox and brush tools.
            line_width (int): Width of the line.
            zoom_slider (bool): Display zoom slider.
            watermark (bool): Show watermark.
            theme (str): Theme of the chart.

        Keyword Args:
            **kwargs: Additional keyword arguments.
                - markline_opts (opts.MarkLineOpts): Mark line options.

        Returns:
            Line: The configured Line chart.
        """
        yaxis_pos = "right" if right_y else "left"
        theme_opts = ThemeType.DARK if theme.upper() == 'DARK' else ThemeType.LIGHT

        if gradient_color:
            area_color = gradient_color
        else:
            area_color = {
                        "type": "linear",
                        "x": 0,
                        "y": 0,
                        "x2": 0,
                        "y2": 1,
                        "colorStops": [{
                        "offset": 0, "color": _GRADIENT_EMERALD[0]
                        }, {
                        "offset": 1, "color": _GRADIENT_EMERALD[1]
                        }],
                        "global": False
                        }

        if area_style:
            areastyle_opts = opts.AreaStyleOpts(opacity=0.2, 
                                                color=area_color,
                                                )
        else:
            areastyle_opts = None

        if show_xaxis:
            _xaxis_label_opt= opts.LabelOpts(is_show=True)
        else:
            _xaxis_label_opt = opts.LabelOpts(is_show=False)

        # check if markline_opts is provided
        markline_opts = kwargs.get("markline_opts", None)

        if markline_opts:
            markline_opts = markline_opts
        else:
            markline_opts = None

        line_chart = (
            Line(init_opts=opts.InitOpts(theme=theme_opts, bg_color=self.bg_color))
            .add_xaxis(time_series)
            .add_yaxis(series_name=yaxis_name, y_axis=data_series, 
                       is_step=is_step,
                       is_smooth=is_smooth, 
                       is_symbol_show=label,
                       areastyle_opts=areastyle_opts,
                       linestyle_opts=opts.LineStyleOpts(
                           width=line_width, 
                           color=color
                           ),
                        itemstyle_opts=opts.ItemStyleOpts(color=color),
                        markpoint_opts=opts.MarkPointOpts(
                            data=mark_points_data,
                            label_opts=opts.LabelOpts(position="bottom", color="#fff"),
                        ),
                        markline_opts=markline_opts,
                        label_opts=opts.LabelOpts(is_show=label),
                )
        )

        specific_opts = {
            "xaxis_opts": opts.AxisOpts(
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(width=self.gridline_width, opacity=self.gridline_opacity),
                ),
                axislabel_opts=_xaxis_label_opt,
            ),
            "yaxis_opts": opts.AxisOpts(
                name=yaxis_name,
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(width=self.gridline_width, opacity=self.gridline_opacity)
                ),
                position=yaxis_pos,
            ),
        }

        common_opts = self._common_global_opts(title=title, zoomable=zoomable, zoom_slider=zoom_slider, subplot=subplot, legend=legend, tools=tools, watermark=watermark)

        line_chart.set_global_opts(**{**specific_opts, **common_opts})
        return line_chart

    def _base_line(self, time_series: List[str], data_series: List[float], title: str = 'Base Line', 
                   yaxis_name: str = 'Price', right_y: bool = True,
                   up_color: str = _EMERALD_GREEN, down_color: str = _CRIMSON_RED, 
                   base_value: int = 1, values_range: List[int] = None, dimension: int = 1, show_visualmap: bool = True, tools: bool = True,
                   is_step: bool = False, area_style: bool = False, 
                   label: bool = False, zoomable: bool = True, subplot: bool = False, 
                   legend: bool = False, show_xaxis:bool=True, zoom_slider: bool = False, theme: str = 'dark', watermark: bool = False, **kwargs) -> Line:
        """
        Create a base line chart using for plotting

 value greater than 0 in green and less than 0 in red.

        Args:
            time_series (List[str]): List of time series data.
            data_series (List[float]): List of series data.
            title (str): Title of the line chart.
            yaxis_name (str): Name of the y-axis.
            right_y (bool): Position of the y-axis.
            up_color (str): Color of the line when the value is positive.
            down_color (str): Color of the line when the value is negative.
            base_value (int): The base value to separate the positive and negative values.
            values_range (List[int]): List of values to define different ranges.
            dimension (int): Dimension of the line chart. 0 for x-axis and 1 for y-axis.
            show_visualmap (bool): Show visual map.
            tools (bool): Show toolbox and brush tools.
            is_step (bool): Use step line chart.
            area_style (bool): Use area style for the line chart.
            label (bool): Show symbol on the line.
            zoomable (bool): Enable zoom functionality.
            subplot (bool): Create subplot.
            legend (bool): Show legend.
            zoom_slider (bool): Display zoom slider.
            watermark (bool): Show watermark.
            theme (str): Theme of the chart.
            watermark (bool): Show watermark.

        Keyword Args:
            **kwargs: Additional keyword arguments.
                - markline_opts (opts.MarkLineOpts): Mark line options.
        Returns:
            Line: The configured Line chart.
        """
        
        theme_opts = ThemeType.DARK if theme.upper() == 'DARK' else ThemeType.LIGHT
        yaxis_pos = "right" if right_y else "left"

        if dimension not in [0, 1]:
            raise ValueError("Dimension must be 0 or 1")
        
        if show_xaxis:
            _xaxis_label_opt= opts.LabelOpts(is_show=True)
        else:
            _xaxis_label_opt = opts.LabelOpts(is_show=False)

        # check if markline_opts is provided
        markline_opts = kwargs.get("markline_opts", None)

        if markline_opts:
            markline_opts = markline_opts
        else:
            markline_opts = None

        baseline_chart = Line(init_opts=opts.InitOpts(theme=theme_opts, bg_color=self.bg_color)).add_xaxis(xaxis_data=time_series)
        baseline_chart.add_yaxis(
            series_name=title, 
            y_axis=data_series, 
            is_step=is_step,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.2, color=up_color) if area_style else None,
            is_smooth=True, 
            is_symbol_show=label,
            linestyle_opts=opts.LineStyleOpts(width=1),
            markline_opts=markline_opts,
        )
        
        pieces = []
        if values_range is not None:
            values_range = sorted(values_range)
            if base_value < values_range[0]:
                pieces.append({"lte": base_value, "color": down_color})
                pieces.append({"gt": base_value, "lte": values_range[0], "color": up_color})
            else:
                pieces.append({"lte": values_range[0], "color": down_color})
                pieces.append({"gt": values_range[0], "lte": base_value, "color": down_color})

            for i in range(1, len(values_range)):
                pieces.append({"gt": values_range[i-1], "lte": values_range[i], "color": up_color if values_range[i] > base_value else down_color})

            if values_range[-1] < base_value:
                pieces.append({"gt": values_range[-1], "lte": base_value, "color": down_color})
                pieces.append({"gt": base_value, "color": up_color})
            else:
                pieces.append({"gt": values_range[-1], "color": up_color})
        else:
            pieces = [
                {"lte": base_value, "color": down_color},  # Values less than or equal to base_value
                {"gt": base_value, "color": up_color},    # Values greater than base_value
            ]

        specific_opts = {
            "xaxis_opts": opts.AxisOpts(
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(width=self.gridline_width, opacity=self.gridline_opacity)
                ),
                axislabel_opts=_xaxis_label_opt,
            ),
            "yaxis_opts": opts.AxisOpts(
                name=yaxis_name,
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(width=self.gridline_width, opacity=self.gridline_opacity)
                ),
                position=yaxis_pos
            ),
            "visualmap_opts": opts.VisualMapOpts(
                is_show=show_visualmap,
                is_piecewise=True,
                dimension=1,  # 1 indicates y-axis dimension
                pieces=pieces,
            ),
        }

        common_opts = self._common_global_opts(title=title, zoomable=zoomable, zoom_slider=zoom_slider, subplot=subplot, legend=legend, tools=tools, watermark=watermark)

        baseline_chart.set_global_opts(**{**specific_opts, **common_opts})
        return baseline_chart

    def _add_line(self, line_chart: Line, data_series: List[float], title: str = 'Additional Line', yaxis_name='Line',
                  color: str = _EMERALD_GREEN, is_step: bool = False, is_smooth:bool=True, area_style: bool = False, gradient_color: Dict = None, 
                  label: bool = False) -> Line:
        """
        Add a line to an existing line chart.

        Args:
            line_chart (Line): The existing Line chart.
            data_series (List[float]): List of series data for the additional line.
            title (str): Title of the additional line.
            color (str): Color of the additional line.
            is_step (bool): Use step line chart for the additional line.
            is_smooth (bool): Use smooth line chart for the additional line.
            area_style (bool): Use area style for the additional line.
            gradient_color (Dict): Gradient color for the additional line.
            label (bool): Show symbol on the additional line.

        Returns:
            Line: The updated Line chart.
        """

        if gradient_color:
            area_color = gradient_color
        else:
            area_color = {
                        "type": "linear",
                        "x": 0,
                        "y": 0,
                        "x2": 0,
                        "y2": 1,
                        "colorStops": [{
                        "offset": 0, "color": _GRADIENT_EMERALD[0]
                        }, {
                        "offset": 1, "color": _GRADIENT_EMERALD[1]
                        }],
                        "global": False
                        }

        if area_style:
            areastyle_opts = opts.AreaStyleOpts(opacity=0.2, 
                                                color=area_color
                                                )
        else:
            areastyle_opts = None
        
        line_chart.add_yaxis(
            series_name=yaxis_name, 
            y_axis=data_series, 
            is_step=is_step,
            areastyle_opts=areastyle_opts,
            is_smooth=is_smooth, 
            is_symbol_show=label,
            linestyle_opts=opts.LineStyleOpts(color=color),
            itemstyle_opts=opts.ItemStyleOpts(color=color),
        )
        return line_chart

    def _multi_lines(self, time_series: List[str], series_list: List[List[float]], color_list: List[str], 
                     title_list: List[str] = ["Indicator"], yaxis_name:str='Price', right_y:bool=False, mark_points_data: List[opts.MarkPointItem] = None, 
                     zoomable: bool = True, subplot: bool = False, legend: bool = False, watermark: bool = False) -> Line:
        """
        Create multiple lines (or single line) chart for the technical indicators based on list of series data and configuration.

        Args:
            time_series (List[str]): List of time series data.
            series_list (List[List[float]]): List of series data.
            color_list (List[str]): List of colors for the series.
            title_list (List[str]): List of titles for the series.
            yaxis_name (str): Name of the y-axis.
            right_y (bool): Position of the y-axis.
            mark_points_data (List[opts.MarkPointItem]): List of mark points data for the series.
            zoomable (bool): Enable zoom functionality.
            subplot (bool): Create subplot.
            legend (bool): Show legend.
            watermark (bool): Show watermark.

        Returns:
            Line: The configured Line chart.
        """
        if len(series_list) != len(color_list):
            raise ValueError("series_list and color_list must have the same length")

        yaxis_pos = "right" if right_y else "left"

        line_chart = Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT)).add_xaxis(xaxis_data=time_series)
        
        for name, color, series in zip(title_list, color_list, series_list):
            line_chart.add_yaxis(
                series_name=name,
                y_axis=series,
                is_smooth=True,
                linestyle_opts=opts.LineStyleOpts(width=1, color=color),
                is_symbol_show=False,
                markpoint_opts=opts.MarkPointOpts(
                    data=mark_points_data,
                    label_opts=opts.LabelOpts(position="bottom", color="#fff"),
                )
            )
        
        specific_opts = {
            "xaxis_opts": opts.AxisOpts(
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(width=self.gridline_width, opacity=self.gridline_opacity)
                )
            ),
            "yaxis_opts": opts.AxisOpts(
                name=yaxis_name,
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(width=self.gridline_width, opacity=self.gridline_opacity)
                ),
                position=yaxis_pos
            ),
        }

        common_opts = self._common_global_opts(title=title_list[0], zoomable=zoomable, zoom_slider=True, subplot=subplot, legend=legend, tools=False, watermark=watermark)

        line_chart.set_global_opts(**{**specific_opts, **common_opts})
        return line_chart

    def _bar(self, time_series: List[str], data_series: List[Union[Dict[str, Any], float]], title: str = 'Bar Chart', 
             yaxis_name: str = 'Price', right_y: bool = True, show_xaxis: bool = False,
             color: str = _EMERALD_GREEN, label: bool = False, zoomable: bool = True, 
             zoom_slider: bool = False, subplot: bool = False, legend: bool = False, 
             tools: bool = True, theme: str = 'dark', watermark: bool = False) -> Bar:
        """
        Create bar chart based on series data and configuration.

        Args:
            time_series (List[str]): List of time series data.
            data_series (List[Union[Dict[str, Any], float]]): List of series data.
            title (str): Title of the bar chart.
            yaxis_name (str): Name of the y-axis.
            right_y (bool): Position of the y-axis.
            color (str): Color of the bar.
            label (bool): Show labels on the bar.
            zoomable (bool): Enable zoom functionality.
            zoom_slider (bool): Display zoom slider.
            subplot (bool): Create subplot.
            legend (bool): Show legend.
            tools (bool): Show toolbox and brush tools.
            watermark (bool): Show watermark.
            theme (str): Theme of the chart.
            watermark (bool): Show watermark.

        Returns:
            Bar: The configured Bar chart.
        """

        theme_opts = ThemeType.DARK if theme.upper() == 'DARK' else ThemeType.LIGHT

        yaxis_pos = "right" if right_y else "left"

        if not all(isinstance(d, dict) and "itemStyle" in d for d in data_series):
            data_series = [{"value": d, "itemStyle": {"color": color}} for d in data_series]

        if show_xaxis:
            _xaxis_label_opt= opts.LabelOpts(is_show=True)
        else:
            _xaxis_label_opt = opts.LabelOpts(is_show=False)

        bar_chart = (
            Bar(init_opts=opts.InitOpts(theme=theme_opts, bg_color=self.bg_color))
            .add_xaxis(xaxis_data=time_series)
            .add_yaxis(
                series_name=title,
                y_axis=data_series,
                itemstyle_opts=opts.ItemStyleOpts(color=color),
                label_opts=opts.LabelOpts(is_show=label),
            )
        )

        global_opts = {
            "xaxis_opts": opts.AxisOpts(
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(width=self.gridline_width, opacity=self.gridline_opacity)
                )
            ),
            "yaxis_opts": opts.AxisOpts(
                name=yaxis_name,
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(width=self.gridline_width, opacity=self.gridline_opacity)
                ),
                position=yaxis_pos,
                axislabel_opts=_xaxis_label_opt
            ),
            "visualmap_opts": opts.VisualMapOpts(
                is_show=False,
                dimension=2,
                series_index=5,
                is_piecewise=True,
                pieces=[
                    {"value": 1, "color": self.bull_color},
                    {"value": -1, "color": self.bear_color},
                ],
            ),
        }

        common_opts = self._common_global_opts(title=title, zoomable=zoomable, zoom_slider=zoom_slider, subplot=False, legend=legend, tools=tools, watermark=watermark)

        bar_chart.set_global_opts(**{**global_opts, **common_opts})
        return bar_chart

    def _hist(self, time_series: List[str], data_series: pd.Series, title: str = 'Bar Chart', 
             yaxis_name: str = 'Price', right_y: bool = True, show_xaxis: bool = False,
             color: str = _EMERALD_GREEN, label: bool = False, zoomable: bool = True, 
             zoom_slider: bool = False, subplot: bool = False, legend: bool = False, 
             tools: bool = True, theme: str = 'dark', watermark: bool = False) -> Bar:
        """
        Create bar chart based on series data and configuration.

        Args:
            time_series (List[str]): List of time series data.
            data_series (pd.Series): Series data.
            title (str): Title of the bar chart.
            yaxis_name (str): Name of the y-axis.
            right_y (bool): Position of the y-axis.
            color (str): Color of the bar.
            label (bool): Show labels on the bar.
            zoomable (bool): Enable zoom functionality.
            zoom_slider (bool): Display zoom slider.
            subplot (bool): Create subplot.
            legend (bool): Show legend.
            tools (bool): Show toolbox and brush tools.
            watermark (bool): Show watermark.
            theme (str): Theme of the chart.
            watermark (bool): Show watermark.

        Returns:
            Bar: The configured Bar chart.
        """

        theme_opts = ThemeType.DARK if theme.upper() == 'DARK' else ThemeType.LIGHT

        yaxis_pos = "right" if right_y else "left"

        if show_xaxis:
            _xaxis_label_opt= opts.LabelOpts(is_show=True)
        else:
            _xaxis_label_opt = opts.LabelOpts(is_show=False)

        bar_chart = (
            Bar(init_opts=opts.InitOpts(theme=theme_opts, bg_color=self.bg_color))
            .add_xaxis(xaxis_data=time_series)
            .add_yaxis(
                series_name=title,
                y_axis=data_series.to_list(),
                itemstyle_opts=opts.ItemStyleOpts(color=color),
                label_opts=opts.LabelOpts(is_show=label),
            )
        )

        global_opts = {
            "xaxis_opts": opts.AxisOpts(
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(width=self.gridline_width, opacity=self.gridline_opacity)
                )
            ),
            "yaxis_opts": opts.AxisOpts(
                name=yaxis_name,
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(width=self.gridline_width, opacity=self.gridline_opacity)
                ),
                position=yaxis_pos,
                axislabel_opts=_xaxis_label_opt
            ),
            "visualmap_opts": opts.VisualMapOpts(
                is_show=False,
                dimension=2,
                series_index=5,
                is_piecewise=True,
                pieces=[
                    {"value": 1, "color": self.bull_color},
                    {"value": -1, "color": self.bear_color},
                ],
            ),
        }

        common_opts = self._common_global_opts(title=title, zoomable=zoomable, zoom_slider=zoom_slider, subplot=False, legend=legend, tools=tools, watermark=watermark)

        bar_chart.set_global_opts(**{**global_opts, **common_opts})
        return bar_chart

    def _scatter(self, time_series: List[str], data_series: List[List[float]], title: str = 'Scatter Chart', 
                 yaxis_name: str = 'Price', right_y: bool = True,
                color: str = _EMERALD_GREEN, symbol_size: int = 5, label: bool = False, zoomable: bool = True, 
                zoom_slider: bool = False, subplot: bool = False, legend: bool = False, tools: bool = True, 
                theme: str = 'dark', watermark: bool = False) -> Scatter:
        """
        Create scatter chart based on series data and configuration.

        Args:
            time_series (List[str]): List of time series data.
            data_series (List[List[float]]): List of series data.
            title (str): Title of the scatter chart.
            yaxis_name (str): Name of the y-axis.
            right_y (bool): Position of the y-axis.
            color (str): Color of the scatter points.
            label (bool): Show labels on the scatter points.
            zoomable (bool): Enable zoom functionality.
            zoom_slider (bool): Display zoom slider.
            subplot (bool): Create subplot.
            legend (bool): Show legend.
            tools (bool): Show toolbox and brush tools.
            watermark (bool): Show watermark.
            theme (str): Theme of the chart.

        Returns:
            Scatter: The configured Scatter chart.
        """
        theme_opts = ThemeType.DARK if theme.upper() == 'DARK' else ThemeType.LIGHT

        yaxis_pos = "right" if right_y else "left"

        scatter_chart = (
            Scatter(init_opts=opts.InitOpts(theme=theme_opts, bg_color=self.bg_color))
            .add_xaxis(xaxis_data=time_series)
        )
        
        scatter_chart.add_yaxis(
            series_name=title,
            y_axis=data_series,
            symbol_size=symbol_size,
            label_opts=opts.LabelOpts(is_show=label),
            itemstyle_opts=opts.ItemStyleOpts(color=color),
        )

        specific_opts = {
            "xaxis_opts": opts.AxisOpts(
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(width=self.gridline_width, opacity=self.gridline_opacity)
                )
            ),
            "yaxis_opts": opts.AxisOpts(
                name=yaxis_name,
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(width=self.gridline_width, opacity=self.gridline_opacity)
                ),
                position=yaxis_pos
            ),
        }

        common_opts = self._common_global_opts(title, zoomable, zoom_slider, subplot, legend, tools)
        scatter_chart.set_global_opts(**{**specific_opts, **common_opts})
        return scatter_chart

    def _candlestick(self, title: str = "Candlestick Chart", yaxis_name:bool='Price', tools: bool =True, watermark: bool = True, display: bool = False) -> Grid:
        """
        Create a candlestick chart with OHLC data.

        Args:
            title (str): Title of the candlestick chart.
            yaxis_name (str): Name of the y-axis.
            tools (bool): Show toolbox and brush tools.
            display (bool): Display the chart as display or return the chart object.
            watermark (bool): Show watermark.

        Returns:
            Grid: A Grid object containing the candlestick and volume charts.
        """
        time_index = self.data.index.strftime('%Y-%m-%d').to_list()
        candle_data = self.data[['open', 'close', 'low', 'high']].values.tolist()
        
        self.data['itemStyleColor'] = np.where(self.data['open'] > self.data['close'], self.bear_color, self.bull_color)
        
        volume_data = [{
            "value": row["volume"],
            "itemStyle": {"color": row["itemStyleColor"]}
        } for index, row in self.data.iterrows()]

        kline = self._kline(time_series=time_index, ohlc_data=candle_data, title=title, yaxis_name=yaxis_name, right_y=True, tools=tools, watermark=watermark, show_xaxis=False)
        bar = self._volume(time_series=time_index, data_series=volume_data, title=title, yaxis_name='Volume')
        if display:
            self._grid_layout(chart_series={'MainChart': kline, 'Volume': bar}, layout='minimal')
        else:
            return kline, bar

    def _price_volume(self, title: str = "Area Price and Volume Chart", yaxis_name:bool='Price', area_style:bool=True, tools:bool=True, watermark:bool=True, display=False) -> Grid:
        """
        Create Price and Volume chart with Price shown as Area.

        Args:
            title (str): Title of the chart.
            yaxis_name (str): Name of the y-axis.
            area_style (bool): Use area style for the price chart or just line style.
            tools (bool): Show toolbox and brush tools.
            watermark (bool): Show watermark.
            display (bool): Display the chart as display or return the chart object.

        Returns:
            Grid: A Grid object containing the price area chart and volume chart.
        """
        time_index = self.data.index.strftime('%Y-%m-%d').to_list()
        close_data = self.data['close'].values.tolist()
        
        self.data['itemStyleColor'] = np.where(self.data['open'] > self.data['close'], self.bear_color, self.bull_color)
        
        volume_data = [{
            "value": row["volume"],
            "itemStyle": {"color": row["itemStyleColor"]}
        } for index, row in self.data.iterrows()]

        line = self._line(time_series=time_index, data_series=close_data, title=title, yaxis_name=yaxis_name, right_y=True, color=self.bull_color, area_style=area_style, zoomable=True, tools=tools, watermark=watermark, show_xaxis=False)
        bar = self._volume(time_series=time_index, data_series=volume_data, title=title, yaxis_name='Volume')
        if display:
            return self._grid_layout(chart_series={'MainChart': line, 'Volume': bar}, layout='minimal')
        else:
            return line, bar

    def _grid_layout(self, chart_series: Dict[str, Any], layout: str = 'overlap', 
                     chart_height: str = '900px', chart_width: str = '1500px', 
                     theme: str = "dark", bg_color: str = None) -> Grid:
        """
        Create a grid layout for the charts.

        Args:
            chart_series (Dict[str, Any]): Dictionary containing the charts.
            layout (str): Layout type ('minimal', 'overlap', 'subplot').
            chart_height (str): Height of the chart.
            chart_width (str): Width of the chart.
            theme (str): Theme of the chart.
            bg_color (str): Background color of the chart.

        Returns:
            Grid: A Grid object containing the charts.
        """
        theme = theme.upper()
        set_theme = ThemeType.DARK if theme == "DARK" else ThemeType.LIGHT
        if bg_color is None:
            bg_color = '#0E1117' if theme == "DARK" else '#FFFFFF'

        grid_chart = Grid(
            init_opts=opts.InitOpts(
                width=chart_width,
                height=chart_height,
                animation_opts=opts.AnimationOpts(animation=True),
                theme=set_theme,
                bg_color=bg_color
            )
        )

        if layout == 'minimal':
            grid_chart.add(
                chart_series['MainChart'],
                grid_opts=opts.GridOpts(pos_left="3%", pos_right="7%", height="65%"),
            )
            grid_chart.add(
                chart_series['Volume'],
                grid_opts=opts.GridOpts(
                    pos_left="3%", pos_right="7%", pos_top="77%", height="13%"
                ),
            )
        elif layout == 'overlap':
            grid_chart.add(
                chart_series['MainChart'].overlap(chart_series['Indicator']),
                grid_opts=opts.GridOpts(pos_left="3%", pos_right="7%", height="65%"),
            )
            grid_chart.add(
                chart_series['Volume'],
                grid_opts=opts.GridOpts(
                    pos_left="3%", pos_right="7%", pos_top="77%", height="13%"
                ),
            )
        elif layout == 'subplot':
            grid_chart.add(
                chart_series['MainChart'],
                grid_opts=opts.GridOpts(pos_left="3%", pos_right="7%", height="50%"),
            )
            grid_chart.add(
                chart_series['Volume'],
                grid_opts=opts.GridOpts(
                    pos_left="3%", pos_right="7%", pos_top="62%", height="11%"
                ),
            )
            grid_chart.add(
                chart_series['Indicator'],
                grid_opts=opts.GridOpts(
                    pos_left="3%", pos_right="7%", pos_top="80%", height="13%"
                ),
            )
        return grid_chart

    def base_trading_chart(self, title: str = 'Candlestick Chart', display: bool = True, tools:bool=True, watermark: bool = True, chart_width='1500px', chart_height='900px') -> Union[pn.pane.ECharts, str]:
        """
        Create a basic trading chart with candlestick and volume.

        Args:
            title (str): Title of the chart.
            display (bool): Render the chart directly or just return the raw chart object.
            watermark (bool): Show watermark.

        Returns:
            Union[pn.pane.ECharts, str]: The rendered chart or raw chart object.
        """
        if chart_width:
            grid_width = chart_width
        else:
            grid_width = self.chart_width

        if chart_height:
            grid_height = chart_height
        else:
            grid_height = self.chart_height

        kline, bar = self._candlestick(title=title, yaxis_name='Price', watermark=watermark, tools=tools, display=False)
        grid_chart = self._grid_layout(chart_series={'MainChart': kline, 'Volume': bar}, layout='minimal', chart_height=grid_height, chart_width=grid_width, theme=self.theme, bg_color=self.bg_color)
        return self._render(chart=grid_chart, display=display)

    def minimal_trading_chart(self, title: str = 'Candlestick Chart', area_style:bool=False, tools:bool=True, watermark:bool=True, display:bool = True, chart_width='1500px', chart_height='900px') -> Union[pn.pane.ECharts, str]:
        """
        Create a minimal trading chart with price area and volume.

        Args:
            title (str): Title of the chart.
            display (bool): Render the chart directly or just return the raw chart object.

        Returns:
            Union[pn.pane.ECharts, str]: The rendered chart or raw chart object.
        """
        if chart_width:
            grid_width = chart_width
        else:
            grid_width = self.chart_width
            
        if chart_height:
            grid_height = chart_height
        else:
            grid_height = self.chart_height

        line, bar = self._price_volume(title=title, display=False, area_style=area_style, tools=tools, watermark=watermark)
        grid_chart = self._grid_layout(chart_series={'MainChart': line, 'Volume': bar}, layout='minimal', chart_height=self.chart_height, chart_width=self.chart_width, theme=self.theme, bg_color=self.bg_color)
        return self._render(chart=grid_chart, display=display)

class TAChart:
    def __init__ (self, data, theme:str="dark", watermark:bool=False, display:bool=True):
        """
        Initialize the TAChart class.

        Args:
            data (pd.DataFrame): The OHLCV data.
            theme (str): Theme of the chart.
            width (str): Width of the chart.
            height (str): Height of the chart.
        """
        self.data = data
        self.theme = theme
        self.watermark = watermark
        self.display = display
        self.ta = self._import_indicator()(data=self.data)
        self.chart = BaseChart(candle_data=self.data, theme=self.theme)

    def _import_indicator(self):
        from vnstock_ta.interface import Indicator
        return Indicator
    
    # def _show_html(self, html:str):

    def _base_chart (self, indicator_chart, title='Đồ thị kỹ thuật', width:str=None, height:str=None, layout:str='overlap', watermark:bool=None):
        """
        Create a basic trading chart with candlestick and volume style.

        Args:
            indicator_chart (Any): The indicator chart.
            title (str): Title of the chart.
            width (str): Width of the chart. Default is 1500px, inherited from the BaseChart class if not specify.
            height (str): Height of the chart. Default is 900px, inherited from the BaseChart class if not specify.
            layout (str): Layout of the chart.
            watermark (bool): Show watermark.
        """
        if watermark:
            show_watermark = watermark
        else:
            show_watermark = self.watermark
        
        if width:
            chart_width = width
        else:
            chart_width = self.chart.chart_width

        if height:
            chart_height = height
        else:
            chart_height = self.chart.chart_height

        main_chart, volume_chart = self.chart._candlestick(title=title, watermark=show_watermark)
        grid_chart = self.chart._grid_layout(chart_series={'MainChart': main_chart, 'Volume': volume_chart, 'Indicator': indicator_chart}, 
                                             layout=layout, 
                                             chart_height=chart_height, chart_width=chart_width, 
                                             theme=ThemeType.WHITE, bg_color=self.chart.bg_color)
        return self.chart._render(grid_chart, display=self.display)
    
    def _minimal_chart (self, indicator_chart, title='Đồ thị kỹ thuật', width:str=None, height:str=None, layout:str='overlap', watermark:bool=None):
        """
        Create a minimal trading chart with price area and volume style.

        Args:
            indicator_chart (Any): The indicator chart.
            title (str): Title of the chart.
            layout (str): Layout of the chart.
            watermark (bool): Show watermark.
        """
        if watermark:
            show_watermark = watermark
        else:
            show_watermark = self.watermark

        if width:
            chart_width = width
        else:
            chart_width = self.chart.chart_width

        if height:
            chart_height = height
        else:
            chart_height = self.chart.chart_height

        main_chart, volume_chart = self.chart._price_volume(title=title, area_style=False, watermark=show_watermark)

        grid_chart = self.chart._grid_layout(chart_series={'MainChart': main_chart, 'Volume': volume_chart, 'Indicator': indicator_chart}, 
                                            layout=layout, 
                                            chart_height=chart_height, chart_width=chart_width, 
                                            theme=ThemeType.WHITE, bg_color=self.chart.bg_color)
        return self.chart._render(grid_chart, display=self.display)