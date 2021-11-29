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

from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.auth import PlainTextAuthProvider

colors = {
    'background': '#222222',
    'text': '#FF4500'
}

app = DjangoDash("DashAppCassandra")

def cassandra_connection():
    cluster = Cluster(['0.0.0.0'], port=3042)
    session = cluster.connect('cs511',wait_for_all_pools=False)
    session.execute('USE cs511')
    rows = session.execute('SELECT * FROM google_store limit 10')
    for row in rows:
        print(row)

cassandra_connection()
#session, cluster_con = cassandra_connection()
#ans = session.execute("select * from google_store limit 10")
#print(ans)

# data = list(AppInfo_Mongo.objects.all().values().using('cassandra'))

# # Average value stored as dictionary, tested in other files
# # e.g for count {{"Education":2.3}, {"Sport":1.03}, {"Game":0.88}, .....}
# rating_avg = list(AppInfo_Mongo.objects.values('category').using('cassandra').annotate(average = Avg('rating')))
# rating_count_avg = list(AppInfo_Mongo.objects.values('category').using('cassandra').annotate(average = Avg('rating_count')))
# install_avg = list(AppInfo_Mongo.objects.values('category').using('cassandra').annotate(average = Avg('install_number')))
# price_avg = list(AppInfo_Mongo.objects.values('category').using('cassandra').annotate(average = Avg('price')))
# app_name = []
# rating = []
# category = []
# install_number = []
# rating_count = []
# price = []
# age_required = []
# ad_support = []

# # global variables
# base = 0

# for i in range(0,len(data)):
#     app_name.append(data[i]['app_name']) 
#     rating.append(data[i]['rating'])
#     category.append(data[i]['category'])
#     install_number.append(data[i]['install_number'])
#     rating_count.append(data[i]['rating_count'])
#     price.append(data[i]['price'])
#     age_required.append(data[i]['age_required'])
#     ad_support.append(data[i]['ad_support'])

# df = pd.DataFrame({
#     "App": app_name,
#     "Category": category,
#     "Rating": rating
# })
# fig = px.bar(df, x="App", y="Rating", color="Category", barmode="group")
# fig.update_xaxes(visible=False)

# scatterPlot = px.scatter(x=install_number, y=rating, hover_name=app_name)
# scatterPlot.update_layout(plot_bgcolor=colors['background'], paper_bgcolor='#191970',font_color=colors['text'])
# scatterPlot.update_xaxes(title='Install Number')
# scatterPlot.update_yaxes(title='Rating')

# #Table generating

# dt = pd.DataFrame(data)

# def generate_table(max_rows=50):
#     return html.Table([
#         html.Thead(
#             html.Tr([html.Th('Category'),html.Th('Avg Rating'),html.Th('Avg Rating Count'),html.Th('Avg Install'),html.Th('Avg Price')])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(rating_avg[i]['category']),
#                 html.Td(rating_avg[i]['average']),
#                 html.Td(rating_count_avg[i]['average']),
#                 html.Td(install_avg[i]['average']),
#                 html.Td(price_avg[i]['average']),
#             ], style={ 'border': 'solid', 'border-width': '1px 0'}) for i in range(min(len(rating_avg), max_rows))
#         ])
#     ],id = 'summary', style={'width': '100%', 'border-collapse': 'collapse'})

# #SpreadSheet columns
# params = [
#     'category', 'rating', 'rating_count', 'install_number',
#     'price', 'age_required', 'ad_support'
# ]

# #App layout

# app.layout = html.Div(children=[
#     html.H1(
#         children='Google Appstore Info Dashboard',
#         style={
#             'textAlign': 'center',
#         }
#     ),
#     html.H2(children='Summary'),
#     generate_table(),
#     html.H2(children='Bar Chart:', style={
#         'textAlign': 'left',
#     }),
#     html.Div(children='Y Axis Value', style={
#         'textAlign': 'left',
#         'color': '#222222',
#     }),
#     html.Div([
#         html.H3(children='Y-axis:', style={
#             'textAlign': 'left',
#         }),
#         dcc.Dropdown(
#             id='yaxis_value',
#             options=[{'label': i, 'value': i} for i in ['Rating','Install Number', 'Rating Count', 'Price']],
#             value='Rating',
#             style={ 'color': '#000000','background-color': '#A0A0A0'} 
#         ),
#     ], style={'width': '25%', 'display': 'inline-block'}),
#     html.Div([
#         html.H3(children='Group by (Colors):', style={
#             'textAlign': 'left',
#         }),
#         dcc.Dropdown(
#             id='color_value',
#             options=[{'label': i, 'value': i} for i in ['Category', 'Age Required', 'Ad Support']],
#             value='Category',
#             style={ 'color': '#000000','background-color': '#A0A0A0'} 
#         ),
#     ], style={'width': '25%', 'display': 'inline-block', 'left': '65%', 'position': 'absolute'}),
#     dcc.Graph(
#         id='example-graph',
#         figure=fig,
#         style={'width': '100%', 'display': 'inline-block'}
#     ),
#     html.H2(children='Scatter Plot:'),
#     html.Div([
#         html.H3(children='X-axis:', style={
#             'textAlign': 'left',
#         }),
#         dcc.Dropdown(
#             id='scatterx',
#             options=[{'label': i, 'value': i} for i in ['Install Number','Rating', 'Rating Count', 'Price']],
#             value='Install Number',
#             style={ 'color': '#000000','background-color': '#A0A0A0'} 
#         ),
#     ], style={'width': '25%', 'display': 'inline-block'}),
#     html.Div([
#         html.H3(children='Y-axis', style={
#             'textAlign': 'left',
#         }),
#         dcc.Dropdown(
#             id='scattery',
#             options=[{'label': i, 'value': i} for i in ['Rating','Install Number', 'Rating Count', 'Price']],
#             value='Rating',
#             style={ 'color': '#000000','background-color': '#A0A0A0'} 
#         ),
#     ], style={'width': '25%', 'display': 'inline-block', 'left': '65%', 'position': 'absolute'}),
#     dcc.Graph(
#         id='scatter-plot',
#         figure=scatterPlot,
#         style={'width': '100%', 'display': 'inline-block'}
#     ),
#     html.H2(children='Spreadsheet View:'),
#     html.Div([
#         html.Div(children='Page:', style={
#             'textAlign': 'left',
#             'width': '40%'
#         }),
#         html.Div([
#             dcc.Dropdown(
#                 id='pagedrop',
#                 options=[{'label': i/100+1, 'value': i/100+1} for i in range(0, len(app_name), 100)],
#                 value=1,
#                 style={ 'color': '#000000','background-color': '#A0A0A0'} 
#             )],style={'width': '10%'}
#         ),
#     ]),
#     dash_table.DataTable(
#         id='spreadsheet',
#         columns=(
#             [{'id': 'app_name', 'name': 'app_name'}] +
#             [{'id': p, 'name': p} for p in params]
#         ),
#         data=[
#             dict({'app_name':app_name[i], 'category': category[i], 'rating': rating[i], 'rating_count': rating_count[i], 'install_number': install_number[i], 'price': price[i], 'age_required': age_required[i], 'ad_support':ad_support[i]}) for i in range(100)
#         ],
#         editable=True,
#         export_format='csv',
#         style_header={
#             'backgroundColor': 'rgb(50, 50, 50)',
#             'fontWeight': 'bold'
#         },
#          style_data={
#             'backgroundColor': 'rgb(100, 100, 100)',
#             'color': 'black'
#         },
#     ),
#     html.Div(id = 'my_output', style={'display':'None'})
# ], style={'background-color': '#191970', 'color': '#FF4500', 'font-family': '"Trebuchet MS", sans-serif'})

# #Callbacks:
# @app.callback(
#     Output('summary', 'children'),
#     Input('my_output', 'children')
#     )
# def update_table(my_output):
#     global rating_avg, rating_count_avg, install_avg, price_avg
#     rating_avg = list(AppInfo_Mongo.objects.values('category').using('cluster0').annotate(average = Avg('rating')))
#     rating_count_avg = list(AppInfo_Mongo.objects.values('category').using('cluster0').annotate(average = Avg('rating_count')))
#     install_avg = list(AppInfo_Mongo.objects.values('category').using('cluster0').annotate(average = Avg('install_number')))
#     price_avg = list(AppInfo_Mongo.objects.values('category').using('cluster0').annotate(average = Avg('price')))

#     print('update summary table')
#     return generate_table()


# @app.callback(
#     Output('example-graph', 'figure'),
#     Input('color_value', 'value'),
#     Input('yaxis_value', 'value'),
#     Input('my_output', 'children'))
# def update_graph(color_value, yaxis_value, my_output):
#     cval = category
#     if color_value == 'Age Required':
#         cval = age_required
#     elif color_value == 'Ad Support':
#         cval = ad_support
#     yval = rating
#     if yaxis_value == 'Install Number':
#         yval = install_number
#     elif yaxis_value == 'Rating Count':
#         yval = rating_count
#     elif yaxis_value == 'Price':
#         yval = price
#     df = pd.DataFrame({
#     "App": app_name,
#     color_value: cval,
#     yaxis_value: yval
#     })
#     fig = px.bar(df, x="App", y=yaxis_value, color=color_value, barmode="group")
#     fig.update_layout(
#         plot_bgcolor=colors['background'],
#         paper_bgcolor='#191970',
#         font_color=colors['text']
#     )
#     fig.update_xaxes(visible=False)
#     print("update barchart")
#     return fig

# @app.callback(
#     Output('scatter-plot', 'figure'),
#     Input('scatterx', 'value'),
#     Input('scattery', 'value'),
#     Input('my_output', 'children'))
# def update_scatter(scatterx, scattery, my_output):
#     xval = install_number
#     if scatterx == 'Install Number':
#         xval = install_number
#     elif scatterx == 'Rating Count':
#         xval = rating_count
#     elif scatterx == 'Price':
#         xval = price
#     elif scatterx == 'Rating':
#         xval = rating
#     yval = rating
#     if scattery == 'Install Number':
#         yval = install_number
#     elif scattery == 'Rating Count':
#         yval = rating_count
#     elif scattery == 'Price':
#         yval = price
#     elif scatterx == 'Rating':
#         yval = rating

#     scatterPlot = px.scatter(x=xval, y=yval, hover_name=app_name)
#     scatterPlot.update_layout(plot_bgcolor=colors['background'], paper_bgcolor='#191970',font_color=colors['text'])
#     scatterPlot.update_xaxes(title=scatterx)
#     scatterPlot.update_yaxes(title=scattery)
#     print("update scatterplot")
#     return scatterPlot

# @app.callback(
#     Output('spreadsheet', 'data'),
#     Input('pagedrop', 'value'))
# def update_spreadsheet(p):
#     global base 
#     base = ((int)(p)-1)*100
#     boundary = min(100, len(app_name)-base)
#     return [
#         dict({'app_name':app_name[base+i], 'category': category[base+i], 'rating': rating[base+i], 'rating_count': rating_count[base+i], 'install_number': install_number[i], 'price': price[base+i], 'age_required': age_required[base+i], 'ad_support':ad_support[base+i]}) for i in range(boundary)
#     ]

# @app.callback(
#     Output('my_output', 'children'),
#     Input('spreadsheet', 'data_timestamp'),
#     State('spreadsheet', 'active_cell'),
#     State('spreadsheet', 'data'))
# def display_output(timestamp, cell, data):
#     column_name = cell['column_id']
#     row = cell['row']-1
#     id = base+row
#     value = data[row][column_name]
#     print('value = ', value)
#     print('idx = ', id)
#     print('column = ', column_name)

#     target = AppInfo_Mongo.objects.using('cluster0').get(idx=id)
#     exec("target." + column_name + " = " + '"' + (str)(value) + '"')
#     target.save()

#     exec(column_name + "["+ (str)(id) +"] = " + '"' + (str)(value) + '"')

#     return 'Output: {}'.format(data[cell['row']-1]['app_name'])