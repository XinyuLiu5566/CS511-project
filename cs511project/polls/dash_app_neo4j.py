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

app = DjangoDash("DashAppNeo4j")

users = list(User.nodes.all().values())
apps = list(App.nodes.all().values())
companies = list(Company.nodes.all().values())


# Average value stored as dictionary, tested in other files
# e.g for count {{"Education":2.3}, {"Sport":1.03}, {"Game":0.88}, .....}
rating_avg = list(AppInfo_Mongo.objects.values('category').using('cluster0').annotate(average = Avg('rating')))
rating_count_avg = list(AppInfo_Mongo.objects.values('category').using('cluster0').annotate(average = Avg('rating_count')))
install_avg = list(AppInfo_Mongo.objects.values('category').using('cluster0').annotate(average = Avg('install_number')))
price_avg = list(AppInfo_Mongo.objects.values('category').using('cluster0').annotate(average = Avg('price')))
named = []
rating = []
category = []
install_number = []
rating_count = []
price = []
age_required = []
ad_support = []
for i in range(0,len(data)):
    named.append(data[i]['app_name']) 
    rating.append(data[i]['rating'])
    category.append(data[i]['category'])
    install_number.append(data[i]['install_number'])
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

scatterPlot = px.scatter(x=install_number, y=rating, hover_name=named)
scatterPlot.update_layout(plot_bgcolor=colors['background'], paper_bgcolor='#191970',font_color=colors['text'])
scatterPlot.update_xaxes(title='Install Number')
scatterPlot.update_yaxes(title='Rating')

#Table generating

dt = pd.DataFrame(data)

def generate_table(max_rows=50):
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
    ],style={'width': '100%', 'border-collapse': 'collapse'})

#SpreadSheet columns
params = [
    'Category', 'Rating', 'Rating Count', 'Install Number',
    'Price', 'Age Required', 'Add Support'
]

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
        figure=scatterPlot,
        style={'width': '100%', 'display': 'inline-block'}
    ),
    html.H2(children='Spreadsheet View:'),
    html.Div([
        html.Div(children='Page:', style={
            'textAlign': 'left',
            'width': '40%'
        }),
        html.Div([
            dcc.Dropdown(
                id='pagedrop',
                options=[{'label': i/100+1, 'value': i/100+1} for i in range(0, len(named), 100)],
                value=1,
                style={ 'color': '#000000','background-color': '#A0A0A0'} 
            )],style={'width': '10%'}
        ),
    ]),
    dash_table.DataTable(
        id='spreadsheet',
        columns=(
            [{'id': 'App Name', 'name': 'App Name'}] +
            [{'id': p, 'name': p} for p in params]
        ),
        data=[
            dict({'App Name':named[i], 'Category': category[i], 'Rating': rating[i], 'Rating Count': rating_count[i], 'Install Number': install_number[i],
    'Price': price[i], 'Age Required': age_required[i], 'Add Support':ad_support[i]})
            for i in range(100)
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
    if yaxis_value == 'Install Number':
        yval = install_number
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
    xval = install_number
    if scatterx == 'Install Number':
        xval = install_number
    elif scatterx == 'Rating Count':
        xval = rating_count
    elif scatterx == 'Price':
        xval = price
    elif scatterx == 'Rating':
        xval = rating
    yval = rating
    if scattery == 'Install Number':
        yval = install_number
    elif scattery == 'Rating Count':
        yval = rating_count
    elif scattery == 'Price':
        yval = price
    elif scatterx == 'Rating':
        yval = rating

    scatterPlot = px.scatter(x=xval, y=yval, hover_name=named)
    scatterPlot.update_layout(plot_bgcolor=colors['background'], paper_bgcolor='#191970',font_color=colors['text'])
    scatterPlot.update_xaxes(title=scatterx)
    scatterPlot.update_yaxes(title=scattery)
    return scatterPlot

@app.callback(
    Output('spreadsheet', 'data'),
    Input('pagedrop', 'value'))
def update_spreadsheet(p):
    base = ((int)(p)-1)*100
    boundary = min(100, len(named)-base)
    return [
            dict({'App Name':named[base+i], 'Category': category[base+i], 'Rating': rating[base+i], 'Rating Count': rating_count[base+i], 'Install Number': install_number[i],
    'Price': price[base+i], 'Age Required': age_required[base+i], 'Add Support':ad_support[base+i]})
            for i in range(boundary)
    ]