
import plotly.express as px
import plotly.graph_objects as go
from IPython.display import HTML
import plotly.io as pio
import random
import pandas as pd


pio.templates.default = "plotly_dark"

def visualize(fig):
    # vizFileName = '.viz-' + str(random.randint(1, 100)) + '.html'
    # fig.write_html(vizFileName, auto_open=False, config={"responsive":True })
    # return HTML(filename=vizFileName)
    pio.show(fig)

def cov(df):
    corr_matrix = df.corr()
    trace = go.Heatmap(z=corr_matrix.values,
                       x=corr_matrix.columns,
                       y=corr_matrix.columns,
                       colorscale='Viridis')

    layout = go.Layout(autosize=True, margin=dict(t=5, l=5, r=5, b=5))

    fig = go.Figure(data=[trace], layout=layout)
    return visualize(fig)

def candles(df):
    fig = go.Figure(
        data=[go.Candlestick(x=df['time'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'])])
    fig.update_layout(autosize=True, margin=dict(t=5, l=5, r=5, b=5))

    return visualize(fig)

def line(df, x, y, log=False):
    fig = go.Figure()
    fig = px.line(df, x=x, y=y,log_x=log)

    fig.update_layout(
        autosize=True,
        margin=dict(t=5, l=5, r=5, b=5),
        xaxis=dict(title=x),
        yaxis=dict(title=y),
    )
    return visualize(fig)

def pie(df, values, labels):
    fig = px.pie(df, values=values, names=labels)
    fig.update_layout(autosize=True, margin=dict(t=5, l=5, r=5, b=5))
    return visualize(fig)

def fit(df, x, y, log=False, hover=[], group=None):
    if group is None:
        fig = px.scatter(df, x=x, y=y, log_x=log, hover_data=hover,trendline="ols", trendline_options=dict(log_x=log))
    else:
        fig = px.scatter(df, x=x, y=y, log_x=log, hover_data=hover, color=group,trendline="ols", trendline_options=dict(log_x=log))

    fig.update_layout(autosize=True, margin=dict(t=5, l=5, r=5, b=5))
    return visualize(fig)

def scatter(df, x, y, log=False, hover=[], group=None):
    if group is None:
        fig = px.scatter(df, x=x, y=y, log_x=log, hover_data=hover)
    else:
        fig = px.scatter(df, x=x, y=y, log_x=log, hover_data=hover, color=group)

    fig.update_layout(autosize=True, margin=dict(t=5, l=5, r=5, b=5))
    return visualize(fig)

def bar(df, x, y):
    fig = px.bar(df, x=x, y=y)
    fig.update_layout(autosize=True, margin=dict(t=5, l=5, r=5, b=5))
    return visualize(fig)

def area(df, x, y, group, sub=""):
    fig = px.area(df, x=x, y=y,
                  color=group, line_group=group)

    fig.update_layout(autosize=True, margin=dict(t=5, l=5, r=5, b=5))
    return visualize(fig)

def heatmap(df, x, y, hover=[]):
    fig = px.density_heatmap(df, x=x, y=y)
    fig.update_layout(autosize=True, margin=dict(t=5, l=5, r=5, b=5))
    return visualize(fig)

def radar(df, values, labels):
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
          r=df[values],
          theta=df[labels],
          fill='toself',
          name=''
    ))

    # fig.add_trace(go.Scatterpolar(
    #       r=[4, 3, 2.5, 1, 2],
    #       theta=categories,
    #       fill='toself',
    #       name='Product B'
    # ))

    fig.update_layout(
      autosize=True, margin=dict(t=5, l=5, r=5, b=5),
      showlegend=False
    )

    return visualize(fig)

def barh(df, x, y):
    fig = px.bar(df, x=x, y=y, orientation='h')
    fig.update_layout(autosize=True, margin=dict(t=5, l=5, r=5, b=5))
    return visualize(fig)

def spread(dfs, x, y):
    merged_df = pd.merge(dfs[0], dfs[1], on=x, suffixes=('_df1', '_df2'))
    merged_df['spread'] = merged_df[y+'_df1'] - merged_df[y+'_df2']

    trace_price = go.Scatter(x=merged_df[x], y=merged_df[y+'_df1'], mode='lines', name='Asset 1')
    trace_price_2 = go.Scatter(x=merged_df[x], y=merged_df[y+'_df2'], mode='lines', name='Asset 2')
    trace_spread = go.Bar(x=merged_df[x], y=merged_df['spread'], name='Spread')

    layout = go.Layout(
        autosize=True,
        margin=dict(t=5, l=5, r=5, b=5),
    )

    fig = go.Figure(data=[trace_price, trace_price_2, trace_spread], layout=layout)
    return visualize(fig)

def polls(df):
    fig = go.Figure()
    for column in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=column))

    fig.update_layout(autosize=True, margin=dict(t=5, l=5, r=5, b=5))
    return visualize(fig)

def tree(df):
    fig = px.treemap(df, path=[ 'sector', 'industry', 'symbol' ], values='marketCap', hover_data=['pctchange', 'lastsale'], color_continuous_scale='RdGn')
    fig.update_layout(autosize=True, margin=dict(t=5, l=5, r=5, b=5))
    return visualize(fig)

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

def generate_color_map(column_values):
    unique_values = column_values.unique()
    colors = px.colors.qualitative.D3
    color_map = {value: colors[i % len(colors)] for i, value in enumerate(unique_values)}
    return color_map

def graph(df, x, bars=[], lines=[], areas=[], title='', color=None):
    fig = go.Figure()
    if color is not None:
        color_map = generate_color_map(df[color])

    for y in areas:
        fig.add_trace(go.Scatter(
            x=df[x],
            y=df[y],
            name=y,
            fill='tozeroy',
            mode='lines',
        ))

    for i, y in enumerate(lines):
        fig.add_trace(go.Scatter(
            x=df[x],
            y=df[y],
            name=y,
            mode='lines',
            line=dict(color=shades_of_white[i % len(shades_of_white)]),
        ))

    for y in bars:
        if color is None:
            fig.add_trace(go.Bar(
                x=df[x],
                y=df[y],
                name=y,
            ))
        else:
            fig.add_trace(go.Bar(
                marker_color=[color_map[val] for val in df[color]],
                x=df[x],
                y=df[y],
                name=y,
            ))


    fig.update_layout(
        title=title,
        barmode='stack',
        autosize=True,
        margin=dict(t=5, l=5, r=5, b=5),
        xaxis=dict(
            gridcolor='#333',
            showline=True,  # Remove x-axis line
            zeroline=True   # Remove zero line
        ),
        yaxis=dict(
            title=' - '.join(bars + lines + areas),
            side='left',
            anchor='x',
            gridcolor='#333',
            showline=True,  # Remove y-axis line for bars
            zeroline=True   # Remove zero line for bars
        ),

        legend=dict(
            title='',
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),

    )

    return visualize(fig)
