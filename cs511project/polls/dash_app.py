# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from re import match
import dash_core_components as dcc
import dash_html_components as html
# from pandas.core.arrays import string_
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
from .models import *
from django.core import serializers
from django.http import JsonResponse
import numpy as np
from django.db.models import Avg


colors = {
    'background': '#222222',
    'text': '#FF4500'
}

app = DjangoDash("DashApp")

data = list(AppInfo.objects.all().values())

# Average value stored as dictionary, tested in other files
# e.g for count {{"Education":2.3}, {"Sport":1.03}, {"Game":0.88}, .....}
rating_avg = list(AppInfo.objects.values('category').annotate(average = Avg('rating')))
rating_count_avg = list(AppInfo.objects.values('category').annotate(average = Avg('rating_count')))
install_avg = list(AppInfo.objects.values('category').annotate(average = Avg('install_number')))
price_avg = list(AppInfo.objects.values('category').annotate(average = Avg('price')))
name_origin = []
named = []
rating = []
category = []
maximum_install = []
rating_count = []
price = []
age_required = []
ad_support = []
for i in range(0,len(data)):
    name_origin.append(data[i]['app_name'])
    named.append((str)(data[i]['idx'])+':'+(data[i]['app_name'][:8] if len(data) > 8 else data[i]['app_name'])) 
    rating.append(data[i]['rating'])
    category.append(data[i]['category'])
    maximum_install.append(data[i]['install_number'])
    rating_count.append(data[i]['rating_count'])
    price.append(data[i]['price'])
    age_required.append(data[i]['age_required'])
    ad_support.append(data[i]['ad_support'])

df = pd.DataFrame({
    "App": named,
    "Category": category,
    "Rating": rating
})
fig = px.bar(df, x="App", y="Rating", color="Category", barmode="group")
fig.update_xaxes(visible=False)

scatterPlot = px.scatter(x=maximum_install, y=rating, hover_name=name_origin)
scatterPlot.update_layout(plot_bgcolor=colors['background'], paper_bgcolor='#191970',font_color=colors['text'])
scatterPlot.update_xaxes(title='Maximum Install')
scatterPlot.update_yaxes(title='Rating')

#Table generating

dt = pd.DataFrame(data)

def generate_table(max_rows=50):
    return html.Table([
        html.Thead(
            html.Tr([html.Th('Category'),html.Th('Avg Rating'),html.Th('Avg Rating Count'),html.Th('Avg Maximum Install'),html.Th('Avg Price')])
        ),
        html.Tbody([
            html.Tr([
                html.Td(rating_avg[i]['category']),
                html.Td(rating_avg[i]['average']),
                html.Td(rating_count_avg[i]['average']),
                html.Td(install_avg[i]['average']),
                html.Td(price_avg[i]['average']),
            ], style={ 'border': 'solid', 'border-width': '1px 0'}) for i in range(min(len(rating_avg), max_rows))
        ])
    ],style={'width': '100%', 'border-collapse': 'collapse'})


#App layout

app.layout = html.Div(children=[
    html.H1(
        children='Google Appstore Info Dashboard',
        style={
            'textAlign': 'center',
        }
    ),
    html.H2(children='Summary'),
    generate_table(),
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
            options=[{'label': i, 'value': i} for i in ['Rating','Maximum Install', 'Rating Count', 'Price']],
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
        figure=fig,
        style={'width': '100%', 'display': 'inline-block'}
    ),
    html.H2(children='Scatter Plot:'),
    html.Div([
        html.H3(children='X-axis:', style={
            'textAlign': 'left',
        }),
        dcc.Dropdown(
            id='scatterx',
            options=[{'label': i, 'value': i} for i in ['Maximum Install','Rating', 'Rating Count', 'Price']],
            value='Maximum Install',
            style={ 'color': '#000000','background-color': '#A0A0A0'} 
        ),
    ], style={'width': '25%', 'display': 'inline-block'}),
    html.Div([
        html.H3(children='Y-axis', style={
            'textAlign': 'left',
        }),
        dcc.Dropdown(
            id='scattery',
            options=[{'label': i, 'value': i} for i in ['Rating','Maximum Install', 'Rating Count', 'Price']],
            value='Rating',
            style={ 'color': '#000000','background-color': '#A0A0A0'} 
        ),
    ], style={'width': '25%', 'display': 'inline-block', 'left': '65%', 'position': 'absolute'}),
    dcc.Graph(
        id='scatter-plot',
        figure=scatterPlot,
        style={'width': '100%', 'display': 'inline-block'}
    ),
], style={'background-color': '#191970', 'color': '#FF4500', 'font-family': '"Trebuchet MS", sans-serif'})

#Callbacks:

@app.callback(
    Output('example-graph', 'figure'),
    Input('color_value', 'value'),
    Input('yaxis_value', 'value'))
def update_graph(color_value, yaxis_value):
    cval = category
    if color_value == 'Age Required':
        cval = age_required
    elif color_value == 'Ad Support':
        cval = ad_support
    yval = rating
    if yaxis_value == 'Maximum Install':
        yval = maximum_install
    elif yaxis_value == 'Rating Count':
        yval = rating_count
    elif yaxis_value == 'Price':
        yval = price
    df = pd.DataFrame({
    "App": named,
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
    return fig

@app.callback(
    Output('scatter-plot', 'figure'),
    Input('scatterx', 'value'),
    Input('scattery', 'value'))
def update_scatter(scatterx, scattery):
    xval = maximum_install
    if scatterx == 'Maximum Install':
        xval = maximum_install
    elif scatterx == 'Rating Count':
        xval = rating_count
    elif scatterx == 'Price':
        xval = price
    yval = rating
    if scattery == 'Maximum Install':
        yval = maximum_install
    elif scattery == 'Rating Count':
        yval = rating_count
    elif scattery == 'Price':
        yval = price

    scatterPlot = px.scatter(x=xval, y=yval, hover_name=name_origin)
    scatterPlot.update_layout(plot_bgcolor=colors['background'], paper_bgcolor='#191970',font_color=colors['text'])
    scatterPlot.update_xaxes(title=scatterx)
    scatterPlot.update_yaxes(title=scattery)
    return scatterPlot