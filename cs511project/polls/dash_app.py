# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash

app = DjangoDash("DashApp")

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
named = ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"]
amountd = [4, 1, 2, 2, 4, 5]
cityd = ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
df = pd.DataFrame({
    "Fruit": named,
    "Amount": amountd,
    "City": cityd
})

dt = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")


fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor='#4B0082',
    font_color=colors['text']
)

app.layout = html.Div(children=[
    html.H1(
        children='Dashboard',
        style={
            'textAlign': 'center',
            'color': 'black'
        }
    ),

    html.Div(children='Dash: A web application framework for your data.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    html.H4(children='US Agriculture Exports (2011)'),
    generate_table(dt)
])