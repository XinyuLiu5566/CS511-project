# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from re import match
import re
import dash_core_components as dcc
import dash_html_components as html
import plotly as py
import plotly.graph_objs as go 
import plotly.express as px
import pandas as pd
import random
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from .models import *
import numpy as np
from django.db.models import Avg

colors = {
    'background': '#222222',
    'text': '#FF4500'
}

order = []
for i in range(-3, 4):
    for j in range(-3, 4):
        order.append([i*i+j*j, i, j])
order.sort()


app = DjangoDash("DashApp")

data = list(AppInfo.objects.all().values())

#wordcloud
def generate_wordcloud(column):
    if column == 'Install Number':
        avg = list(AppInfo.objects.values('category').annotate(average = Avg('install_number')))
    elif column == 'Rating Count':
        avg = list(AppInfo.objects.values('category').annotate(average = Avg('rating_count')))
    elif column ==  'Price':
        avg = list(AppInfo.objects.values('category').annotate(average = Avg('price')))
    else: 
        avg = list(AppInfo.objects.values('category').annotate(average = Avg('rating')))
    max_val = np.max([avg[i]['average'] for i in range(len(avg))])
    min_val = np.min([avg[i]['average'] for i in range(len(avg))])
    normalized_val = [(int)((avg[i]['average']-min_val)/(max_val-min_val)*25)+15 for i in range(len(avg))]
    normalized_val.sort(reverse=True)
    sorted_val = sorted(avg, key = lambda i: i['average'], reverse=True)
    fcolor = [py.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(len(avg))]

    wordcloud_d = go.Scatter(
                       #x=list(range(len(rating_avg))),
                       #y=random.choices(range(len(rating_avg)), k=len(rating_avg)),
                       x=[order[i][1] for i in range(len(avg))],
                       y=[order[i][2] for i in range(len(avg))],
                       mode='text',
                       text= [sorted_val[i]['category'] for i in range(len(avg))],
                       marker={'opacity': 0.3},
                       #textfont = {'size': [random.randint(15, 35) for i in range(len(rating_avg))]})
                       textfont={'size': normalized_val, 'color': fcolor})
    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                    'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}})
    wordcloud = go.Figure(data=[wordcloud_d], layout=layout)
    wordcloud.update_layout(plot_bgcolor=colors['background'], paper_bgcolor='#191970',font_color=colors['text'])
    return wordcloud

#Table generating

dt = pd.DataFrame(data)

def generate_table(max_rows=50):
    rating_avg = list(AppInfo.objects.values('category').annotate(average = Avg('rating')))
    rating_count_avg = list(AppInfo.objects.values('category').annotate(average = Avg('rating_count')))
    install_avg = list(AppInfo.objects.values('category').annotate(average = Avg('install_number')))
    price_avg = list(AppInfo.objects.values('category').annotate(average = Avg('price')))
    return html.Table([
        html.Thead(
            html.Tr([html.Th('Category'),html.Th('Avg Rating'),html.Th('Avg Rating Count'),html.Th('Avg Install'),html.Th('Avg Price')])
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
    ],id = 'summary', style={'width': '100%', 'border-collapse': 'collapse'})

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
    html.H2(children='Summary'),
    generate_table(),
    html.H2(children='Word Cloud for Summary:', style={
        'textAlign': 'left',
    }),
    html.Div([
        html.H3(children='Value:', style={
            'textAlign': 'left',
        }),
        dcc.Dropdown(
            id='Val',
            options=[{'label': i, 'value': i} for i in ['Rating','Install Number', 'Rating Count', 'Price']],
            value='Rating',
            style={ 'color': '#000000','background-color': '#A0A0A0'} 
        ),
    ], style={'width': '25%', 'display': 'inline-block'}),
    dcc.Graph(
        id='word-cloud',
        figure=generate_wordcloud('Rating'),
        style={'width': '100%', 'display': 'inline-block'}
    ),
], style={'background-color': '#191970', 'color': '#FF4500', 'font-family': '"Trebuchet MS", sans-serif'})

#Callbacks:

@app.callback(
    Output('word-cloud', 'figure'),
    Input('Val', 'value'))
def update_wordcloud(val):
    return generate_wordcloud(val)