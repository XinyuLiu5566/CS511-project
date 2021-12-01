# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from re import match
import dash_core_components as dcc
import dash_html_components as html
import plotly as py
import plotly.graph_objs as go 
import plotly.express as px
import pandas as pd
import random
from django_plotly_dash import DjangoDash
from .models import *
import numpy as np
from django.db.models import Avg

colors = {
    'background': '#222222',
    'text': '#FF4500'
}

app = DjangoDash("DashApp")

data = list(AppInfo.objects.all().values())

#wordcloud
def generate_wordcloud():
    rating_avg = list(AppInfo.objects.values('category').annotate(average = Avg('rating')))
    rating_count_avg = list(AppInfo.objects.values('category').annotate(average = Avg('rating_count')))
    install_avg = list(AppInfo.objects.values('category').annotate(average = Avg('install_number')))
    price_avg = list(AppInfo.objects.values('category').annotate(average = Avg('price')))
    maxrating = np.max([rating_avg[i]['average'] for i in range(len(rating_avg))])
    minrating = np.min([rating_avg[i]['average'] for i in range(len(rating_avg))])
    normalized_rating = [(int)((rating_avg[i]['average']-minrating)/(maxrating-minrating)*20)+15 for i in range(len(rating_avg))]
    fcolor = [py.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(len(rating_avg))]

    wordcloud_d = go.Scatter(
                       x=list(range(len(rating_avg))),
                       y=random.choices(range(len(rating_avg)), k=len(rating_avg)),
                       mode='text',
                       text= [rating_avg[i]['category'] for i in range(len(rating_avg))],
                       marker={'opacity': 0.3},
                       #textfont = {'size': [random.randint(15, 35) for i in range(len(rating_avg))]})
                       textfont={'size': normalized_rating, 'color': fcolor})
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
    html.H2(children='Summary'),
    generate_table(),
    dcc.Graph(
        id='word-cloud',
        figure=generate_wordcloud(),
        style={'width': '100%', 'display': 'inline-block'}
    ),
], style={'background-color': '#191970', 'color': '#FF4500', 'font-family': '"Trebuchet MS", sans-serif'})