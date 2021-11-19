# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from re import match
import dash_core_components as dcc
import dash_html_components as html
import dash_table
# from pandas.core.arrays import string_
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output, State
from .models import *
from django.core import serializers
from django.http import JsonResponse
import numpy as np
from django.db.models import Avg


colors = {
    'background': '#222222',
    'text': '#FF4500'
}

app = DjangoDash("Spreadsheet")

data = list(AppInfo.objects.all().values())

# Average value stored as dictionary, tested in other files
# e.g for count {{"Education":2.3}, {"Sport":1.03}, {"Game":0.88}, .....}
rating_avg = list(AppInfo.objects.values('category').annotate(average = Avg('rating')))
rating_count_avg = list(AppInfo.objects.values('category').annotate(average = Avg('rating_count')))
install_avg = list(AppInfo.objects.values('category').annotate(average = Avg('install_number')))
price_avg = list(AppInfo.objects.values('category').annotate(average = Avg('price')))
app_name = []
rating = []
category = []
install_number = []
rating_count = []
price = []
age_required = []
ad_support = []

# global variables
base = 0

for i in range(0,len(data)):
    app_name.append(data[i]['app_name']) 
    rating.append(data[i]['rating'])
    category.append(data[i]['category'])
    install_number.append(data[i]['install_number'])
    rating_count.append(data[i]['rating_count'])
    price.append(data[i]['price'])
    age_required.append(data[i]['age_required'])
    ad_support.append(data[i]['ad_support'])

df = pd.DataFrame({
    "App": app_name,
    "Category": category,
    "Rating": rating
})
#SpreadSheet columns
params = [
    'category', 'rating', 'rating_count', 'install_number',
    'price', 'age_required', 'ad_support'
]

#App layout

app.layout = html.Div(children=[
    html.H1(
        children='Google Appstore Info Dashboard',
        style={
            'textAlign': 'center',
        }
    ),
    html.A([
        html.Div(children='Dashboard', style={
        'left':'50px',
        'textAlign': 'left',
        'color': '#FF4500',
        'background-color': '#222222',
        'height': '25px',
        'font-size': '20px',
        'width': '120px',
        'border': '1px solid #FF4500'
    })], target="_parent", href='http://localhost:8000/'),
    html.H2(children='Spreadsheet View:'),
    html.Div([
        html.Div(children='Page:', style={
            'textAlign': 'left',
            'width': '40%'
        }),
        html.Div([
            dcc.Dropdown(
                id='pagedrop',
                options=[{'label': i/100+1, 'value': i/100+1} for i in range(0, len(app_name), 100)],
                value=1,
                style={ 'color': '#000000','background-color': '#A0A0A0'} 
            )],style={'width': '10%'}
        ),
    ]),
    dash_table.DataTable(
        id='spreadsheet',
        columns=(
            [{'id': 'app_name', 'name': 'app_name'}] +
            [{'id': p, 'name': p} for p in params]
        ),
        data=[
            dict({'app_name':app_name[i], 'category': category[i], 'rating': rating[i], 'rating_count': rating_count[i], 'install_number': install_number[i], 'price': price[i], 'age_required': age_required[i], 'ad_support':ad_support[i]}) for i in range(100)
        ],
        editable=True,
        export_format='csv',
        style_header={
            'backgroundColor': 'rgb(50, 50, 50)',
            'fontWeight': 'bold'
        },
         style_data={
            'backgroundColor': 'rgb(100, 100, 100)',
            'color': 'black'
        },
    ),
    html.Div(id = 'my_output', style={'display':'None'})
], style={'background-color': '#191970', 'color': '#FF4500', 'font-family': '"Trebuchet MS", sans-serif'})

#Callbacks:

@app.callback(
    Output('spreadsheet', 'data'),
    Input('pagedrop', 'value'))
def update_spreadsheet(p):
    global base 
    base = ((int)(p)-1)*100
    boundary = min(100, len(app_name)-base)
    return [
        dict({'app_name':app_name[base+i], 'category': category[base+i], 'rating': rating[base+i], 'rating_count': rating_count[base+i], 'install_number': install_number[i], 'price': price[base+i], 'age_required': age_required[base+i], 'ad_support':ad_support[base+i]}) for i in range(boundary)
    ]

@app.callback(
    Output('my_output', 'children'),
    Input('spreadsheet', 'data_timestamp'),
    State('spreadsheet', 'active_cell'),
    State('spreadsheet', 'data'))
def display_output(timestamp, cell, data):
    column_name = cell['column_id']
    row = cell['row']-1
    id = base+row
    value = data[row][column_name]
    print('value = ', value)
    print('idx = ', id)
    print('column = ', column_name)

    target = AppInfo.objects.get(idx=id)
    exec("target." + column_name + " = " + '"' + (str)(value) + '"')
    target.save()

    exec(column_name + "["+ (str)(id) +"] = " + '"' + (str)(value) + '"')

    return 'Output: {}'.format(data[cell['row']-1]['app_name'])