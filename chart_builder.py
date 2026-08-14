"""
Insight Flow — Chart Builder Module v3
Theme-aware Plotly charts — colors sync with active dashboard theme.
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from theme_engine import get_plotly_config

_current_theme = 'Default'

def set_chart_theme(theme_name):
    """Set the active chart theme globally for this module."""
    global _current_theme
    _current_theme = theme_name

def _get_config():
    return get_plotly_config(_current_theme)

def _layout_defaults():
    cfg = _get_config()
    return dict(
        font=dict(family="'IBM Plex Mono', Courier, monospace", size=11, color=cfg['font_color']),
        paper_bgcolor=cfg['paper_bgcolor'],
        plot_bgcolor=cfg['plot_bgcolor'],
        margin=dict(l=45, r=15, t=45, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(size=10, color=cfg['font_color'])),
        hoverlabel=dict(bgcolor=cfg['hover_bg'], font_size=11,
                        font_family="'IBM Plex Mono', monospace",
                        bordercolor=cfg['hover_border']),
    )

def _colors():
    return _get_config()['colors']

def _apply_layout(fig, title=""):
    cfg = _get_config()
    fig.update_layout(**_layout_defaults(),
        title=dict(text=title, font=dict(size=13, color=cfg['font_color'],
                                          family="'VT323', monospace")))
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=cfg['grid_color'],
                     linecolor=cfg['axis_color'], linewidth=1,
                     tickfont=dict(size=10, color=cfg['tick_color']))
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=cfg['grid_color'],
                     linecolor=cfg['axis_color'], linewidth=1,
                     tickfont=dict(size=10, color=cfg['tick_color']))
    return fig

def _pie_layout(fig, title=""):
    cfg = _get_config()
    fig.update_layout(**_layout_defaults(),
        title=dict(text=title, font=dict(size=13, color=cfg['font_color'],
                                          family="'VT323', monospace")))
    return fig

def bar_chart(df, x, y, title="", color=None):
    fig = px.bar(df, x=x, y=y, color=color, color_discrete_sequence=_colors(),
                 title=title, barmode='group')
    return _apply_layout(fig, title)

def line_chart(df, x, y, title="", color=None):
    fig = px.line(df, x=x, y=y, color=color, color_discrete_sequence=_colors(),
                  title=title, markers=True)
    fig.update_traces(line=dict(width=2.5))
    return _apply_layout(fig, title)

def area_chart(df, x, y, title="", color=None):
    fig = px.area(df, x=x, y=y, color=color, color_discrete_sequence=_colors(), title=title)
    fig.update_traces(line=dict(width=2))
    return _apply_layout(fig, title)

def pie_chart(df, names, values, title=""):
    cfg = _get_config()
    fig = px.pie(df, names=names, values=values, color_discrete_sequence=_colors(), title=title)
    fig.update_traces(textposition='inside', textinfo='percent+label',
                      textfont=dict(size=11, color=cfg['font_color']),
                      hoverinfo='label+percent+value')
    return _pie_layout(fig, title)

def donut_chart(df, names, values, title=""):
    cfg = _get_config()
    fig = px.pie(df, names=names, values=values, hole=0.45,
                 color_discrete_sequence=_colors(), title=title)
    fig.update_traces(textposition='inside', textinfo='percent+label',
                      textfont=dict(size=11, color=cfg['font_color']))
    return _pie_layout(fig, title)

def scatter_plot(df, x, y, title="", color=None):
    fig = px.scatter(df, x=x, y=y, color=color, color_discrete_sequence=_colors(),
                     title=title, opacity=0.7)
    return _apply_layout(fig, title)

def stacked_bar(df, x, y, color, title=""):
    fig = px.bar(df, x=x, y=y, color=color, color_discrete_sequence=_colors(),
                 title=title, barmode='stack')
    return _apply_layout(fig, title)

def histogram(df, x, title="", nbins=30):
    fig = px.histogram(df, x=x, nbins=nbins, color_discrete_sequence=[_colors()[0]], title=title)
    cfg = _get_config()
    fig.update_traces(marker_line_color=cfg['axis_color'], marker_line_width=0.5)
    return _apply_layout(fig, title)

def heatmap(corr_matrix, title="Correlation Heatmap"):
    cfg = _get_config()
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values, x=corr_matrix.columns, y=corr_matrix.index,
        colorscale='RdBu_r', zmin=-1, zmax=1,
        text=np.round(corr_matrix.values, 2), texttemplate='%{text}',
        textfont=dict(size=10, color=cfg['font_color'])))
    return _apply_layout(fig, title)

CHART_REGISTRY = {
    'Bar Chart': bar_chart, 'Line Chart': line_chart, 'Area Chart': area_chart,
    'Pie Chart': pie_chart, 'Donut Chart': donut_chart, 'Scatter Plot': scatter_plot,
    'Stacked Bar Chart': stacked_bar, 'Histogram': histogram, 'Heatmap': heatmap,
}
