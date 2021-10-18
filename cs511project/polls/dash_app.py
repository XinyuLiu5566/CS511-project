# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output

app = DjangoDash("DashApp")

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
named = ["Gakondo","Ampere Battery Info","Vibook","Smart City Trichy Public Service Vehicles 17UCS548","GROW.me","IMOCCI","unlimited 4G data prank free app","The Everyday Calendar","WhatsOpen","Neon 3d Iron Tech Keyboard Theme"]
rating = [0.1,4.4,0.1,5,0.1,0.1,4.5,2,0.1,4.7]
category = ["Adventure","Tools","Productivity","Communication","Tools","Social","Libraries & Demo","Lifestyle","Communication","Personalization"]
maximum_install = [15,7662,58,19,478,89,2567,702,18,62433]
df = pd.DataFrame({
    "App": named,
    "Category": category,
    "Rating": rating
})
fig = px.bar(df, x="App", y="Rating", color="Category", barmode="group")
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
    'background': '#222222',
    'text': '#222222'
}


fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor='#5555AA',
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
    html.H4(children='US Agriculture Exports (2011)'),
    generate_table(dt),
    html.H3(children='Dash: A web application framework for your data.', style={
        'textAlign': 'center',
        'color': colors['text'],
    }),
    html.Div(children='Y Axis Value', style={
        'textAlign': 'left',
        'color': '#222222',
    }),
    html.Div([
        dcc.Dropdown(
            id='yaxis-value',
            options=[{'label': i, 'value': i} for i in ['Rating','Maximum_install']],
            value='Rating',
            style={ 'color': '#000000','background-color': '#545454'} 
        ),
    ], style={'width': '25%', 'display': 'inline-block'}),
    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
], style={'background-color': 'lightblue'})
@app.callback(
    Output('example-graph', 'figure'),
    Input('yaxis-value', 'value'))
def update_graph(yaxis_value):
    if yaxis_value == 'Rating':
        df = pd.DataFrame({
        "App": named,
        "Category": category,
        "Rating": rating
        })
        fig = px.bar(df, x="App", y="Rating", color="Category", barmode="group")
    else:
        df = pd.DataFrame({
        "App": named,
        "Category": category,
        "Maximum Install": maximum_install
        })
        fig = px.bar(df, x="App", y="Maximum Install", color="Category", barmode="group")
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor='#5555AA',
        font_color=colors['text']
    )
    return fig