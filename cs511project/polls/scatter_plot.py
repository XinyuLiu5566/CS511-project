# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from re import match
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
from .models import *
colors = {
    'background': '#222222',
    'text': '#FF4500'
}

app = DjangoDash("scatterplot")

def generate_scatter(scatterx, scattery):
    data = list(AppInfo.objects.all().values())
    if scatterx == 'Rating':
        xval = [d['rating'] for d in data]
    elif scatterx == 'Rating Count':
        xval = [d['rating_count'] for d in data]
    elif scatterx == 'Price':
        xval = [d['price'] for d in data]
    else:
        xval = [d['install_number'] for d in data]
    if scattery == 'Install Number':
        yval = [d['install_number'] for d in data]
    elif scattery == 'Rating Count':
        yval = [d['rating_count'] for d in data]
    elif scattery == 'Price':
        yval = [d['price'] for d in data]
    else:
        yval = [d['rating'] for d in data]

    scatterPlot = px.scatter(x=xval, y=yval, hover_name=[d['app_name'] for d in data])
    scatterPlot.update_layout(plot_bgcolor=colors['background'], paper_bgcolor='#191970',font_color=colors['text'])
    scatterPlot.update_xaxes(title=scatterx)
    scatterPlot.update_yaxes(title=scattery)
    print("update scatterplot")
    return scatterPlot
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
        'left': '36%', 
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
        'left': '46%', 
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
        'left': '56%', 
        'position': 'absolute'
    })], target="_parent", href='http://localhost:8000/spreadsheet'),
    html.H2(children='Scatter Plot:'),
    html.Div([
        html.H3(children='X-axis:', style={
            'textAlign': 'left',
        }),
        dcc.Dropdown(
            id='scatterx',
            options=[{'label': i, 'value': i} for i in ['Install Number','Rating', 'Rating Count', 'Price']],
            value='Install Number',
            style={ 'color': '#000000','background-color': '#A0A0A0'} 
        ),
    ], style={'width': '25%', 'display': 'inline-block'}),
    html.Div([
        html.H3(children='Y-axis', style={
            'textAlign': 'left',
        }),
        dcc.Dropdown(
            id='scattery',
            options=[{'label': i, 'value': i} for i in ['Rating','Install Number', 'Rating Count', 'Price']],
            value='Rating',
            style={ 'color': '#000000','background-color': '#A0A0A0'} 
        ),
    ], style={'width': '25%', 'display': 'inline-block', 'left': '65%', 'position': 'absolute'}),
    dcc.Graph(
        id='scatter-plot',
        figure=generate_scatter('Install Number', 'Rating'),
        style={'width': '100%', 'display': 'inline-block'}
    ),
], style={'background-color': '#191970', 'color': '#FF4500', 'font-family': '"Trebuchet MS", sans-serif'})

#Callbacks:
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('scatterx', 'value'),
    Input('scattery', 'value'))
def update_scatter(scatterx, scattery):
    return generate_scatter(scatterx, scattery)