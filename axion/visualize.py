import base64
import html
import random
import numpy as np
import pandas as pd
from typing import Any, Optional, Tuple, Callable, List

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from IPython.display import HTML, display
from IPython import get_ipython


pio.templates.default = "plotly_dark"

class PlotHTML(HTML):
    """An IPython HTML object that also stores the file path of the rendered plot."""
    def __init__(self, data=None, filename=None, filepath=None):
        if filename:
            super().__init__(filename=filename)
        else:
            super().__init__(data=data)
        self.filepath = filepath

def visualize(fig: go.Figure) -> Any:
    """Display a plotly figure in a notebook (inline HTML) or in the browser otherwise."""
    if get_ipython() is not None:
        vizFileName = '.viz-' + str(random.randint(1, 100)) + '.html'
        fig.write_html(vizFileName, auto_open=False, config={"responsive": True})
        return PlotHTML(filename=vizFileName, filepath=vizFileName)
    pio.show(fig)


BG_COLOR = 'rgba(0,0,0,0)'
GRID_COLOR = 'rgba(255,255,255,0.15)'
TEXT_COLOR = 'rgba(255,255,255,1)'
MUTED_TEXT_COLOR = 'rgba(180,180,180,1)'
ACCENT_COLOR = 'rgba(52, 152, 219,1.0)'

shades_of_white = [
    'rgb(31, 119, 180)',  # blue
    'rgb(255, 127, 14)',  # orange
    'rgb(44, 160, 44)',   # green
    'rgb(214, 39, 40)',   # red
    'rgb(148, 103, 189)', # purple
    'rgb(140, 86, 75)',   # brown
    'rgb(255, 255, 255)',
    'rgb(245, 245, 245)',
    'rgb(235, 235, 235)',
    'rgb(235, 225, 225)',
    'rgb(235, 215, 215)',
    'rgb(235, 205, 205)',
]

def generate_color_map(column_values: pd.Series) -> dict:
    """Map each unique value in a column to a color from the D3 qualitative palette."""
    unique_values = column_values.unique()
    colors = px.colors.qualitative.D3
    color_map = {value: colors[i % len(colors)] for i, value in enumerate(unique_values)}
    return color_map


def _apply_theme(fig: go.Figure, title: str = '', show_legend: bool = True, margin: Optional[dict] = None) -> go.Figure:
    """Shared chrome for every chart."""
    fig.update_layout(
        font=dict(color=TEXT_COLOR),
        autosize=True,
        margin=margin or dict(t=15, l=10, r=20, b=40),
        plot_bgcolor=BG_COLOR,
        paper_bgcolor=BG_COLOR,
        showlegend=show_legend,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='left',
            x=0,
            title_text='',
            font=dict(color=TEXT_COLOR),
        ),
    )
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='')
    if title:
        fig.update_layout(title=title)
    return fig


def _nice_ticks(values: pd.Series, n: int = 5, include_zero: bool = False) -> np.ndarray:
    """Compute nicely rounded tick positions."""
    values = values.dropna() if hasattr(values, 'dropna') else values
    y_min, y_max = values.min(), values.max()
    if include_zero:
        y_min, y_max = min(y_min, 0), max(y_max, 0)
    if y_min == y_max:
        return np.array([y_min])
    raw_step = (y_max - y_min) / n
    magnitude = 10 ** np.floor(np.log10(raw_step))
    nice = min([1, 2, 2.5, 5, 10], key=lambda s: abs(s * magnitude - raw_step))
    step = nice * magnitude
    if include_zero:
        tick_start = 0 if y_min >= 0 else -np.ceil(-y_min / step) * step
    else:
        tick_start = np.ceil(y_min / step) * step
    return np.arange(tick_start, y_max + step * 0.5, step)


def _decimals_for_step(step: float) -> int:
    """Determine decimal places needed for a tick step."""
    step = abs(step)
    if step == 0:
        return 0
    for d in range(7):
        if abs(round(step, d) - step) < 1e-9:
            return d
    return 6


def _style_value_axis(fig: go.Figure, values: pd.Series, axis: str = 'y',
                      prefix: str = '', suffix: str = '',
                      top_prefix: str = '', top_suffix: str = '',
                      zero_baseline: bool = False) -> go.Figure:
    """Add formatted tick labels, gridlines, and axis range for a numeric axis."""
    ticks = _nice_ticks(values, include_zero=zero_baseline)

    clean_values = values.dropna() if hasattr(values, 'dropna') else pd.Series(values).dropna()
    raw_min, raw_max = float(clean_values.min()), float(clean_values.max())

    tick_min, tick_max = float(ticks[0]), float(ticks[-1])
    span = tick_max - tick_min
    if span <= 0:
        span = abs(tick_max) if tick_max != 0 else 1
    pad_top = span * 0.15

    if len(ticks) > 1:
        step = ticks[1] - ticks[0]
    else:
        step = 0 if float(ticks[0]).is_integer() else ticks[0]
    decimals = _decimals_for_step(step)

    shapes = list(fig.layout.shapes) if fig.layout.shapes else []
    annotations = list(fig.layout.annotations) if fig.layout.annotations else []

    labels = []
    for i, val in enumerate(ticks):
        is_top = i == len(ticks) - 1
        p = top_prefix if is_top else prefix
        s = top_suffix if is_top else suffix
        labels.append(f"{p}{val:,.{decimals}f}{s}")

    max_label_len = max(len(l) for l in labels)
    reserved_frac = min(0.16, 0.045 + 0.004 * max_label_len)
    extra_px = 10 + int(max_label_len * 4)

    domain_right = round(1 - reserved_frac, 3)

    for i, val in enumerate(ticks):
        label = labels[i]
        if axis == 'y':
            annotations.append(dict(
                x=1.0, xref="paper",
                y=val, yref="y",
                text=label, showarrow=False,
                xanchor="right", yanchor="bottom",
                font=dict(size=13, color=TEXT_COLOR),
            ))
            shapes.append(dict(
                type='line', xref='paper', yref='y',
                x0=0, x1=1.0, y0=val, y1=val,
                line=dict(color=GRID_COLOR, width=1),
            ))
        else:
            annotations.append(dict(
                y=-0.12, yref="paper",
                x=val, xref="x",
                text=label, showarrow=False,
                xanchor="center", yanchor="top",
                font=dict(size=13, color=TEXT_COLOR),
            ))
            shapes.append(dict(
                type='line', yref='paper', xref='x',
                y0=0, y1=1, x0=val, x1=val,
                line=dict(color=GRID_COLOR, width=1),
            ))

    range_min = tick_min if zero_baseline else min(tick_min, raw_min - span * 0.05)
    range_max = max(tick_max + pad_top, raw_max + span * 0.05)

    m = fig.layout.margin
    if axis == 'y':
        fig.update_yaxes(tickvals=ticks, showticklabels=False, side='right',
                          showgrid=False, showline=False, zeroline=False,
                          range=[range_min, range_max])
        fig.update_xaxes(domain=[0, domain_right])
        fig.update_layout(margin=dict(
            l=m.l, t=m.t, b=m.b,
            r=max(m.r or 0, extra_px),
        ))
    else:
        fig.update_xaxes(tickvals=ticks, showticklabels=False,
                          showgrid=False, showline=False, zeroline=False,
                          range=[range_min, range_max])
        fig.update_layout(margin=dict(
            r=m.r, t=m.t, l=m.l,
            b=max(m.b or 0, 55),
        ))

    fig.update_layout(shapes=shapes, annotations=annotations)
    return fig


def _pick_date_ticks(x_min: pd.Timestamp, x_max: pd.Timestamp) -> Tuple[str, str, str]:
    """Choose dtick/minor_dtick/tickformat based on date span."""
    span_days = (x_max - x_min).days
    if span_days <= 21:
        return "D3", "D1", "%b %d"
    if span_days <= 60:
        return "D7", "D1", "%b %d"
    if span_days <= 180:
        return "M1", "D7", "%b"
    if span_days <= 730:
        return "M3", "M1", "%b"
    if span_days <= 365 * 5:
        return "M6", "M1", "%b"
    return "M12", "M3", "%b '%y"


def _style_time_axis(fig: go.Figure, df: pd.DataFrame, x: str) -> go.Figure:
    """Configure the x-axis for datetime data."""
    df = df.copy()
    df[x] = pd.to_datetime(df[x])

    x_min, x_max = df[x].min(), df[x].max()
    if x_min.tzinfo is not None:
        x_min = x_min.tz_localize(None)
        x_max = x_max.tz_localize(None)

    dtick, minor_dtick, tickformat = _pick_date_ticks(x_min, x_max)

    fig.update_xaxes(
        tickformat=tickformat,
        dtick=dtick,
        tick0="2000-01-01",
        showgrid=True,
        gridcolor=GRID_COLOR,
        gridwidth=2,
        showline=True,
        linecolor=GRID_COLOR,
        linewidth=2,
        zeroline=False,
        ticks='outside',
        ticklen=10,
        tickwidth=2,
        tickcolor=TEXT_COLOR,
        tickfont=dict(size=13, color=TEXT_COLOR),
        minor=dict(
            dtick=minor_dtick,
            tick0="2000-01-01",
            ticks='outside',
            ticklen=5,
            tickwidth=1,
            tickcolor=GRID_COLOR,
        ),
    )

    years = sorted(df[x].dt.year.unique())
    annotations = list(fig.layout.annotations) if fig.layout.annotations else []

    for yr in years:
        yr_df = df[df[x].dt.year == yr]
        mid_point = yr_df[x].iloc[len(yr_df) // 2]
        annotations.append(dict(
            x=mid_point, y=-0.22,
            xref="x", yref="paper",
            text=str(yr), showarrow=False,
            font=dict(size=13, color=MUTED_TEXT_COLOR),
        ))
        jan_first = pd.Timestamp(year=yr, month=1, day=1)
        if x_min <= jan_first <= x_max:
            annotations.append(dict(
                x=jan_first, y=-0.17,
                xref="x", yref="paper",
                text="|", showarrow=False,
                font=dict(size=12, color=TEXT_COLOR),
            ))

    fig.update_layout(annotations=annotations)
    return fig


def _style_categorical_axis(fig: go.Figure) -> go.Figure:
    """Apply gridlines and angled labels to a categorical x-axis."""
    fig.update_xaxes(
        showgrid=True,
        gridcolor=GRID_COLOR,
        gridwidth=1,
        showline=True,
        linecolor=GRID_COLOR,
        linewidth=2,
        zeroline=False,
        tickangle=-30,
        tickfont=dict(size=13, color=TEXT_COLOR),
        automargin=True,
    )
    return fig


def _is_datetime(series: pd.Series) -> bool:
    """Check whether a pandas Series has a datetime64 dtype."""
    return pd.api.types.is_datetime64_any_dtype(series)


def cov(df: pd.DataFrame) -> Any:
    """Plot a correlation heatmap."""
    corr_matrix = df.corr()
    trace = go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='Viridis',
    )
    fig = go.Figure(data=[trace])
    _apply_theme(fig, show_legend=False, margin=dict(t=10, l=90, r=70, b=90))
    fig.update_xaxes(showgrid=False, tickangle=-45, tickfont=dict(size=13, color=TEXT_COLOR), automargin=True)
    fig.update_yaxes(showgrid=False, tickfont=dict(size=13, color=TEXT_COLOR), automargin=True)
    return visualize(fig)


def candles(df: pd.DataFrame, prefix: str = '', suffix: str = '',
            top_prefix: str = '', top_suffix: str = '') -> Any:
    """Plot a candlestick chart."""
    fig = go.Figure(
        data=[go.Candlestick(x=df['time'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'])])

    _apply_theme(fig, show_legend=False, margin=dict(t=15, l=10, r=70, b=100))
    _style_time_axis(fig, df, 'time')
    all_vals = pd.concat([df['high'], df['low']])
    _style_value_axis(fig, all_vals, prefix=prefix, suffix=suffix, top_prefix=top_prefix, top_suffix=top_suffix)
    fig.update_xaxes(rangeslider_visible=False)
    return visualize(fig)


def pie(df: pd.DataFrame, values: str, labels: str) -> Any:
    """Plot a pie chart."""
    fig = px.pie(df, values=values, names=labels, color_discrete_sequence=shades_of_white)
    _apply_theme(fig, margin=dict(t=55, l=20, r=20, b=20))
    fig.update_traces(textfont=dict(color=TEXT_COLOR))
    return visualize(fig)


def fit(df: pd.DataFrame, x: str, y: str, log: bool = False, hover: list = [],
        group: Optional[str] = None, prefix: str = '', suffix: str = '',
        top_prefix: str = '', top_suffix: str = '') -> Any:
    """Scatter plot with OLS trendline."""
    if group is None:
        fig = px.scatter(df, x=x, y=y, log_x=log, hover_data=hover, trendline="ols",
                          trendline_options=dict(log_x=log), color_discrete_sequence=[ACCENT_COLOR])
    else:
        fig = px.scatter(df, x=x, y=y, log_x=log, hover_data=hover, color=group, trendline="ols",
                          trendline_options=dict(log_x=log), color_discrete_sequence=shades_of_white)

    date_axis = _is_datetime(df[x])
    show_legend = group is not None
    top = 55 if show_legend else 15
    bottom = 100 if date_axis else 70
    _apply_theme(fig, show_legend=show_legend, margin=dict(t=top, l=10, r=70, b=bottom))
    if date_axis:
        _style_time_axis(fig, df, x)
    else:
        _style_categorical_axis(fig)
    _style_value_axis(fig, df[y], prefix=prefix, suffix=suffix, top_prefix=top_prefix, top_suffix=top_suffix)
    return visualize(fig)


def scatter(df: pd.DataFrame, x: str, y: str, log: bool = False, hover: list = [],
            group: Optional[str] = None, prefix: str = '', suffix: str = '',
            top_prefix: str = '', top_suffix: str = '') -> Any:
    """Plot a scatter chart."""
    if group is None:
        fig = px.scatter(df, x=x, y=y, log_x=log, hover_data=hover, color_discrete_sequence=[ACCENT_COLOR])
    else:
        fig = px.scatter(df, x=x, y=y, log_x=log, hover_data=hover, color=group, color_discrete_sequence=shades_of_white)

    date_axis = _is_datetime(df[x])
    show_legend = group is not None
    top = 55 if show_legend else 15
    bottom = 100 if date_axis else 70
    _apply_theme(fig, show_legend=show_legend, margin=dict(t=top, l=10, r=70, b=bottom))
    if date_axis:
        _style_time_axis(fig, df, x)
    else:
        _style_categorical_axis(fig)
    _style_value_axis(fig, df[y], prefix=prefix, suffix=suffix, top_prefix=top_prefix, top_suffix=top_suffix)
    return visualize(fig)


def bar(df: pd.DataFrame, x: str, y: str, prefix: str = '', suffix: str = '',
        top_prefix: str = '', top_suffix: str = '', legend: Optional[str] = None) -> Any:
    """Plot a vertical bar chart. Pass a non-empty string to `legend` to show a legend."""
    fig = px.bar(df, x=x, y=y, color_discrete_sequence=[ACCENT_COLOR])

    if legend:                     # only if a non-empty legend name is given
        fig.data[0].name = legend
        fig.data[0].showlegend = True         
        show_legend = True
        top_margin = 55
    else:
        show_legend = False
        top_margin = 15

    date_axis = _is_datetime(df[x])
    bottom = 100 if date_axis else 70
    _apply_theme(fig, show_legend=show_legend, margin=dict(t=top_margin, l=10, r=70, b=bottom))
    if date_axis:
        _style_time_axis(fig, df, x)
    else:
        _style_categorical_axis(fig)
    _style_value_axis(fig, df[y], prefix=prefix, suffix=suffix, top_prefix=top_prefix, top_suffix=top_suffix, zero_baseline=True)
    return visualize(fig)


def area(df: pd.DataFrame, x: str, y: str, group: str, sub: str = "",
         prefix: str = '', suffix: str = '',
         top_prefix: str = '', top_suffix: str = '') -> Any:
    """Stacked area chart grouped by a column."""
    fig = px.area(df, x=x, y=y, color=group, line_group=group, color_discrete_sequence=shades_of_white)
    date_axis = _is_datetime(df[x])
    bottom = 100 if date_axis else 70
    _apply_theme(fig, margin=dict(t=55, l=10, r=70, b=bottom))
    if date_axis:
        _style_time_axis(fig, df, x)
    else:
        _style_categorical_axis(fig)
    stacked_totals = df.groupby(x)[y].sum()
    _style_value_axis(fig, stacked_totals, prefix=prefix, suffix=suffix, top_prefix=top_prefix, top_suffix=top_suffix, zero_baseline=True)
    return visualize(fig)


def heatmap(df: pd.DataFrame, x: str, y: str, hover: list = []) -> Any:
    """2D density heatmap."""
    fig = px.density_heatmap(df, x=x, y=y, color_continuous_scale='Viridis')
    _apply_theme(fig, show_legend=False, margin=dict(t=10, l=70, r=80, b=80))
    _style_categorical_axis(fig)
    fig.update_yaxes(showgrid=True, gridcolor=GRID_COLOR, tickfont=dict(size=13, color=TEXT_COLOR), automargin=True)
    return visualize(fig)


def radar(df: pd.DataFrame, values: str, labels: str) -> Any:
    """Polar radar chart."""
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
          r=df[values],
          theta=df[labels],
          fill='toself',
          name='',
          line=dict(color=ACCENT_COLOR, width=3),
    ))
    _apply_theme(fig, show_legend=False, margin=dict(t=40, l=60, r=60, b=40))
    fig.update_layout(
        polar=dict(
            bgcolor=BG_COLOR,
            radialaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color=TEXT_COLOR, size=12)),
            angularaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color=TEXT_COLOR, size=13)),
        )
    )
    return visualize(fig)


def barh(df: pd.DataFrame, x: str, y: str, prefix: str = '', suffix: str = '',
         top_prefix: str = '', top_suffix: str = '') -> Any:
    """Horizontal bar chart."""
    fig = px.bar(df, x=x, y=y, orientation='h', color_discrete_sequence=[ACCENT_COLOR])
    _apply_theme(fig, show_legend=False, margin=dict(t=10, l=120, r=20, b=80))
    fig.update_yaxes(showgrid=False, showline=True, linecolor=GRID_COLOR,
                      tickfont=dict(size=13, color=TEXT_COLOR), automargin=True)
    _style_value_axis(fig, df[x], axis='x', prefix=prefix, suffix=suffix, top_prefix=top_prefix, top_suffix=top_suffix, zero_baseline=True)
    return visualize(fig)


def spread(dfs: List[pd.DataFrame], x: str, y: str, prefix: str = '', suffix: str = '',
           top_prefix: str = '', top_suffix: str = '') -> Any:
    """Spread between two DataFrames (line + bar)."""
    merged_df = pd.merge(dfs[0], dfs[1], on=x, suffixes=('_df1', '_df2'))
    merged_df['spread'] = merged_df[y+'_df1'] - merged_df[y+'_df2']
    merged_df[x] = pd.to_datetime(merged_df[x])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=merged_df[x], y=merged_df[y+'_df1'], mode='lines', name='Asset 1',
        line=dict(color=shades_of_white[0], shape='spline', smoothing=0.1),
    ))
    fig.add_trace(go.Scatter(
        x=merged_df[x], y=merged_df[y+'_df2'], mode='lines', name='Asset 2',
        line=dict(color=shades_of_white[1], shape='spline', smoothing=0.1),
    ))
    fig.add_trace(go.Bar(x=merged_df[x], y=merged_df['spread'], name='Spread', marker_color=ACCENT_COLOR))

    _apply_theme(fig, margin=dict(t=55, l=10, r=70, b=100))
    _style_time_axis(fig, merged_df, x)
    all_vals = pd.concat([merged_df[y+'_df1'], merged_df[y+'_df2'], merged_df['spread']])
    _style_value_axis(fig, all_vals, prefix=prefix, suffix=suffix, top_prefix=top_prefix, top_suffix=top_suffix)
    return visualize(fig)


def polls(df: pd.DataFrame, x: str='time', prefix: str = '', suffix: str = '',
          top_prefix: str = '', top_suffix: str = '') -> Any:
    """Each column as a line series."""
    fig = go.Figure()
    df = df.set_index(x)

    for i, column in enumerate(df.columns):
        fig.add_trace(go.Scatter(
            x=df.index, y=df[column], mode='lines', name=column,
            line=dict(color=shades_of_white[i % len(shades_of_white)], shape='spline', smoothing=0.1),
        ))

    idx_df = df.reset_index()
    idx_col = idx_df.columns[0]

    date_axis = True
    try:
        idx_df[idx_col] = pd.to_datetime(idx_df[idx_col])
    except Exception:
        date_axis = False

    bottom = 100 if date_axis else 70
    _apply_theme(fig, margin=dict(t=55, l=10, r=70, b=bottom))
    if date_axis:
        _style_time_axis(fig, idx_df, idx_col)
    else:
        _style_categorical_axis(fig)
    all_vals = pd.concat([df[c] for c in df.columns])
    _style_value_axis(fig, all_vals, prefix=prefix, suffix=suffix, top_prefix=top_prefix, top_suffix=top_suffix)
    return visualize(fig)


def tree(df: pd.DataFrame) -> Any:
    """Treemap chart."""
    fig = px.treemap(df, path=['sector', 'industry', 'symbol'], values='marketCap',
                     hover_data=['pctchange', 'lastsale'], color_continuous_scale='RdGn')
    _apply_theme(fig, show_legend=False, margin=dict(t=10, l=10, r=10, b=10))
    fig.update_traces(textfont=dict(color=TEXT_COLOR))
    return visualize(fig)


def graph(df: pd.DataFrame, x: str, bars: List[str] = [], lines: List[str] = [],
          areas: List[str] = [], title: str = '', color: Optional[str] = None,
          value_suffix: str = '', prefix: str = '', suffix: str = '',
          top_prefix: str = '', top_suffix: str = '') -> Any:
    """Combo chart: bars, lines, areas."""
    fig = go.Figure()
    df = df.copy()
    df[x] = pd.to_datetime(df[x])

    if color is not None:
        color_map = generate_color_map(df[color])

    for y in areas:
        fig.add_trace(go.Scatter(
            x=df[x], y=df[y], name=y, fill='tozeroy', mode='lines',
            line=dict(shape='spline', smoothing=0.1),
        ))

    for i, y in enumerate(lines):
        fig.add_trace(go.Scatter(
            x=df[x], y=df[y], name=y, mode='lines',
            line=dict(color=shades_of_white[i % len(shades_of_white)], shape='spline', smoothing=0.1),
        ))

    for y in bars:
        if color is None:
            fig.add_trace(go.Bar(x=df[x], y=df[y], name=y))
        else:
            fig.add_trace(go.Bar(
                marker_color=[color_map[val] for val in df[color]],
                x=df[x], y=df[y], name=y,
            ))

    _apply_theme(fig, title=title, show_legend=True, margin=dict(t=45 if title else 15, l=10, r=70, b=100))
    fig.update_layout(barmode='stack')
    _style_time_axis(fig, df, x)

    value_series = []
    if bars:
        value_series.append(df[bars].sum(axis=1) if color is None else df[bars[0]])
    value_series += [df[y] for y in lines] + [df[y] for y in areas]
    all_vals = pd.concat(value_series)

    final_suffix = suffix if suffix else value_suffix
    final_top_suffix = top_suffix if top_suffix else value_suffix

    _style_value_axis(fig, all_vals,
                      prefix=prefix, suffix=final_suffix,
                      top_prefix=top_prefix, top_suffix=final_top_suffix,
                      zero_baseline=bool(bars) or bool(areas))
    return visualize(fig)


def line(df: pd.DataFrame, x: str, y: str, log: bool = False,
         prefix: str = '', suffix: str = '', top_prefix: str = '', top_suffix: str = '',
         legend: Optional[str] = None) -> Any:
    """Spline-smoothed line chart. Optionally show a legend by giving a string name."""
    fig = px.line(df, x=x, y=y, log_x=log, render_mode='svg')
    df = df.copy()
    df[x] = pd.to_datetime(df[x])

    fig.update_traces(
        line=dict(color=ACCENT_COLOR, shape='spline', smoothing=0.1),
        selector=dict(mode='lines'),
    )

    if legend:                     # only if non-empty
        fig.data[0].name = legend
        fig.data[0].showlegend = True         
        show_legend = True
        top_margin = 55
    else:
        show_legend = False
        top_margin = 15

    _apply_theme(fig, show_legend=show_legend, margin=dict(t=top_margin, l=10, r=70, b=100))
    _style_time_axis(fig, df, x)
    _style_value_axis(fig, df[y], prefix=prefix, suffix=suffix, top_prefix=top_prefix, top_suffix=top_suffix)
    return visualize(fig)


def layout(figs: List[Any], cols: int, height: int = 450) -> HTML:
    """
    Arrange figures in a responsive grid. Rows are computed automatically.

    Parameters
    ----------
    figs : list of HTML objects (from visualize())
    cols : int   - number of columns
    height : int - cell height in pixels (default 450)
    """
    total = len(figs)
    rows = (total + cols - 1) // cols

    css = f"""
    .grid-layout {{
        display: grid;
        grid-template-columns: repeat({cols}, 1fr);
        grid-auto-rows: {height}px;
        width: 100%;
        height: auto;
        gap: 6px 2px;
        padding: 0;
        margin: 0;
    }}
    .grid-layout iframe {{
        width: 100%;
        height: 100%;
        border: none;
        display: block;
        overflow: hidden;
    }}
    """
    cells = []
    for fig in figs:
        content = fig.data if hasattr(fig, 'data') else str(fig)
        content = content.replace(
            '<body', '<body style="background-color:#111111; margin:0;"', 1
        )
        escaped = html.escape(content, quote=True)
        cells.append(
            f'<iframe srcdoc="{escaped}" '
            f'allowfullscreen sandbox="allow-scripts allow-same-origin"></iframe>'
        )

    combined = f"""<style>{css}</style><div class="grid-layout">{''.join(cells)}</div>"""
    return HTML(combined)
