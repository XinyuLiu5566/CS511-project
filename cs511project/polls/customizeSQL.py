# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from itertools import count
from re import match
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from django.db.models.aggregates import Count
import pandas as pd
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output, State
from .models import *
import time

from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.auth import PlainTextAuthProvider

colors = {
    'background': '#222222',
    'text': '#FF4500'
}

cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('cs511',wait_for_all_pools=False)
session.execute('USE cs511')

app = DjangoDash("customizeSQL")

# Average value stored as dictionary, tested in other files
# e.g for count {{"Education":2.3}, {"Sport":1.03}, {"Game":0.88}, .....}
# global variables
base = 0
data_length = len(list(AppInfo.objects.all().values()))

#SpreadSheet columns
params = [
    'category', 'rating', 'rating_count', 'install_number',
    'price', 'age_required', 'ad_support'
]

#generate recommendation
def generate_table(max_rows=3):
    queries = list(AppInfo_query.objects.values('query').using('cluster0').annotate(count=Count('query')))
    queries.sort(key = lambda x: x['count'], reverse=True)
    return html.Table([
        html.Thead(
            html.Tr([html.Th('Recommend Queries')])
        ),
        html.Tbody([
            html.Tr([
                html.Td(queries[i]['query']),
            ], style={ 'border': 'solid', 'border-width': '1px 0'}) for i in range(min(len(queries), max_rows))
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
    html.H2(children='Cusomized SQL:'),
    html.Div(children='SQL query:', style={
            'textAlign': 'left',
            'width': '40%'
    }),
    html.Div([
        dcc.Input(id='sqlInput', value='', type='text', style={
            'width': '70%',
            }
        ),
    ]),
    html.Button('Submit', id='button', n_clicks=0),
    #html.Button('Time Testing', id='testing', n_clicks=0),
    generate_table(),
    dash_table.DataTable(
        id='spreadsheet',
        columns=(
            [{'id': 'idx', 'name': 'idx'},{'id': 'app_name', 'name': 'app_name'}] +
            [{'id': p, 'name': p} for p in params]
        ),
        data = [],
        editable=True,
        hidden_columns=['idx'],
        sort_action="native",
        sort_mode="multi",
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
    html.Div(id = 'my_output', style={'display':'None'}),
    #html.Div(id = 'my_test', style={'display':'None'})
], style={'background-color': '#191970', 'color': '#FF4500', 'font-family': '"Trebuchet MS", sans-serif'})

#Callbacks:
@app.callback(
    Output('spreadsheet', 'data'),
    Input('button', 'n_clicks'),
    State('sqlInput', 'value')
)
def update_output(n_clicks, value):
    data = AppInfo.objects.raw(value)
    app_name = []
    rating = []
    category = []
    install_number = []
    rating_count = []
    price = []
    age_required = []
    ad_support = []
    idx = []
    for i in data:
        idx.append(i.idx)
        app_name.append(i.app_name) 
        rating.append(i.rating)
        category.append(i.category)
        install_number.append(i.install_number)
        rating_count.append(i.rating_count)
        price.append(i.price)
        age_required.append(i.age_required)
        ad_support.append(i.ad_support)
    if len(idx) > 0: 
        target = AppInfo_query(query=value)
        target.save(using='cluster0')
    return [
        dict({'idx':idx[i], 'app_name':app_name[i], 'category': category[i], 'rating': rating[i], 'rating_count': rating_count[i], 'install_number': install_number[i], 'price': price[i], 'age_required': age_required[i], 'ad_support':ad_support[i]}) for i in range(len(app_name))
    ]

    
@app.callback(
    Output('my_output', 'children'),
    Input('spreadsheet', 'data_timestamp'),
    State('spreadsheet', 'active_cell'),
    State('spreadsheet', 'data'))
def display_output(timestamp, cell, data):
    column_name = cell['column_id']
    row = cell['row']-1
    id = data[row]['idx']
    value = data[row][column_name]
    print('value = ', value)
    print('idx = ', id)
    print('column = ', column_name)

    target = AppInfo.objects.get(idx=id)
    exec("target." + column_name + " = " + '"' + (str)(value) + '"')
    target.save()
    if column_name == 'rating' or column_name == 'rating_count' or column_name == 'install_number' or column_name == 'price':
        #print('UPDATE google_store SET '+column_name+' = "'+(str)(value)+'" WHERE idx = '+(str)(id))
        session.execute('UPDATE google_store SET '+column_name+' = '+(str)(value)+' WHERE idx = '+(str)(id))
    else:
        #print('UPDATE google_store SET '+column_name+' = \''+(str)(value)+'\' WHERE idx = '+(str)(id))
        session.execute('UPDATE google_store SET '+column_name+' = \''+(str)(value)+'\' WHERE idx = '+(str)(id))

    return 'Output: {}'.format(data[cell['row']-1]['app_name'])
@app.callback(
    Output('summary', 'children'),
    Input('spreadsheet', 'data'))
def update_query(timestamp):
    return generate_table()
'''
@app.callback(
    Output('my_test', 'children'),
    Input('testing', 'n_clicks'),
)
def time_testing(n_clicks):
    start = time.time()
    print("MySQL query")
    data = AppInfo.objects.raw('Select * from google_store')
    app_name = []
    rating = []
    category = []
    install_number = []
    rating_count = []
    price = []
    age_required = []
    ad_support = []
    idx = []
    for i in data:
        idx.append(i.idx)
        app_name.append(i.app_name) 
        rating.append(i.rating)
        category.append(i.category)
        install_number.append(i.install_number)
        rating_count.append(i.rating_count)
        price.append(i.price)
        age_required.append(i.age_required)
        ad_support.append(i.ad_support)
    end = time.time()
    print(end - start)  

    start = time.time()
    print("Cassandra query")
    data = data = session.execute('SELECT * FROM google_store')
    app_name = []
    rating = []
    category = []
    install_number = []
    rating_count = []
    price = []
    age_required = []
    ad_support = []
    idx = []
    for i in data:
        idx.append(i.idx)
        app_name.append(i.app_name) 
        rating.append(i.rating)
        category.append(i.category)
        install_number.append(i.install_number)
        rating_count.append(i.rating_count)
        price.append(i.price)
        age_required.append(i.age_required)
        ad_support.append(i.ad_support)
    end = time.time()
    print(end - start)  

    
    start = time.time()
    data = list(AppInfo_Mongo.objects.all().values().using('cluster0'))
    print("MongoDB query")
    app_name = []
    rating = []
    category = []
    install_number = []
    rating_count = []
    price = []
    age_required = []
    ad_support = []

    for i in range(0,len(data)):
        app_name.append(data[i]['app_name']) 
        rating.append(data[i]['rating'])
        category.append(data[i]['category'])
        install_number.append(data[i]['install_number'])
        rating_count.append(data[i]['rating_count'])
        price.append(data[i]['price'])
        age_required.append(data[i]['age_required'])
        ad_support.append(data[i]['ad_support'])
    end = time.time()
    print(end - start)
    return "test"
'''