# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from re import match
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
from .models import *

colors = {
    'background': '#222222',
    'text': '#FF4500'
}

app = DjangoDash("barchart")

def generate_graph(color_value, yaxis_value):
    data = list(AppInfo.objects.all().values())
    if color_value == 'Age Required':
        cval = [d['age_required'] for d in data]
    elif color_value == 'Ad Support':
        cval = [d['ad_support'] for d in data]
    else:
        cval = [d['category'] for d in data]
    if yaxis_value == 'Install Number':
        yval = [d['install_number'] for d in data]
    elif yaxis_value == 'Rating Count':
        yval = [d['rating_count'] for d in data]
    elif yaxis_value == 'Price':
        yval = [d['price'] for d in data]
    else:
        yval = [d['rating'] for d in data]
    df = pd.DataFrame({
    "App": [d['app_name'] for d in data],
    color_value: cval,
    yaxis_value: yval
    })
    fig = px.bar(df, x="App", y=yaxis_value, color=color_value, barmode="group")
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor='#191970',
        font_color=colors['text']
    )
    fig.update_xaxes(visible=False)
    print("update barchart")
    return fig

#App layout

app.layout = html.Div(children=[
     html.H1(
        children='Google Appstore Info Dashboard',
        style={
            'textAlign': 'center',
        }
    ),
    html.A([
        html.Div(children='Home', style={
        'left':'50px',
        'textAlign': 'center',
        'color': '#FF4500',
        'background-color': '#222222',
        'height': '25px',
        'font-size': '20px',
        'width': '120px',
        'border': '1px solid #FF4500'
    })], target="_parent", href='http://localhost:8000/'),
    html.A([
        html.Div(children='Bar Chart', style={
        'left':'50px',
        'textAlign': 'center',
        'color': '#FF4500',
        'background-color': '#222222',
        'height': '25px',
        'font-size': '20px',
        'width': '120px',
        'border': '1px solid #FF4500', 
        'left': '30%', 
        'position': 'absolute'
    })], target="_parent", href='http://localhost:8000/barchart'),
    html.A([
        html.Div(children='Scatter Plot', style={
        'left':'50px',
        'textAlign': 'center',
        'color': '#FF4500',
        'background-color': '#222222',
        'height': '25px',
        'font-size': '20px',
        'width': '120px',
        'border': '1px solid #FF4500', 
        'left': '40%', 
        'position': 'absolute'
    })], target="_parent", href='http://localhost:8000/scatterplot'),
    html.A([
        html.Div(children='Spreadsheet', style={
        'left':'50px',
        'textAlign': 'center',
        'color': '#FF4500',
        'background-color': '#222222',
        'height': '25px',
        'font-size': '20px',
        'width': '120px',
        'border': '1px solid #FF4500', 
        'left': '50%', 
        'position': 'absolute'
    })], target="_parent", href='http://localhost:8000/spreadsheet'),
    html.A([
        html.Div(children='SQL', style={
        'left':'50px',
        'textAlign': 'center',
        'color': '#FF4500',
        'background-color': '#222222',
        'height': '25px',
        'font-size': '20px',
        'width': '120px',
        'border': '1px solid #FF4500', 
        'left': '60%', 
        'position': 'absolute'
    })], target="_parent", href='http://localhost:8000/customizeSQL'),
    html.H2(children='Bar Chart:', style={
        'textAlign': 'left',
    }),
    html.Div(children='Y Axis Value', style={
        'textAlign': 'left',
        'color': '#222222',
    }),
    html.Div([
        html.H3(children='Y-axis:', style={
            'textAlign': 'left',
        }),
        dcc.Dropdown(
            id='yaxis_value',
            options=[{'label': i, 'value': i} for i in ['Rating','Install Number', 'Rating Count', 'Price']],
            value='Rating',
            style={ 'color': '#000000','background-color': '#A0A0A0'} 
        ),
    ], style={'width': '25%', 'display': 'inline-block'}),
    html.Div([
        html.H3(children='Group by (Colors):', style={
            'textAlign': 'left',
        }),
        dcc.Dropdown(
            id='color_value',
            options=[{'label': i, 'value': i} for i in ['Category', 'Age Required', 'Ad Support']],
            value='Category',
            style={ 'color': '#000000','background-color': '#A0A0A0'} 
        ),
    ], style={'width': '25%', 'display': 'inline-block', 'left': '65%', 'position': 'absolute'}),
    dcc.Graph(
        id='example-graph',
        figure=generate_graph('Category', 'Rating'),
        style={'width': '100%', 'display': 'inline-block'}
    ),
], style={'background-color': '#191970', 'color': '#FF4500', 'font-family': '"Trebuchet MS", sans-serif'})

#Callbacks:

@app.callback(
    Output('example-graph', 'figure'),
    Input('color_value', 'value'),
    Input('yaxis_value', 'value'))
def update_graph(color_value, yaxis_value):
    return generate_graph(color_value, yaxis_value)