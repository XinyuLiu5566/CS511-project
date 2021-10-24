# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from re import match
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components.H1 import H1
import dash_table
import dash
# from pandas.core.arrays import string_
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
from .models import *
import numpy as np
from django.db.models import Avg


colors = {
    'background': '#222222',
    'text': '#FF4500'
}


users = User.nodes.all()
apps = App.nodes.all()
companies = Company.nodes.all()

# get the info about users from neo4j database
user_name = []
user_gender = []
for user in users:
    user_name.append(user.name)
    user_gender.append(user.gender)

# get the info about apps from neo4j database
app_name = []
app_category = []
app_year = []
for app in apps:
    app_name.append(app.name)
    app_category.append(app.category)
    app_year.append(app.year)

#get the info about companies from neo4j database
company_name = []
company_address = []
company_year = []
for company in companies:
    company_name.append(company.name)
    company_address.append(company.address)
    company_year.append(company.year)

df = pd.DataFrame({
    "App": app_name,
    "Category": category,
    "Rating": rating
})
fig = px.bar(df, x="App", y="Rating", color="Category", barmode="group")
fig.update_xaxes(visible=False)

#App layout
app = DjangoDash("DashAppNeo4j")

app.layout = html.Div(children=[
    html.H1(
        children='User Table',
        style={
            'textAlign': 'center',
        }
    ),
    html.Table([
        html.Thead(
            html.Tr([html.Th('User Name'),html.Th('User Gender')], style={'textAlign' : 'left'})
        ),
        html.Tbody([
            html.Tr([
                html.Td(user_name[i]),
                html.Td(user_gender[i]),
            ], style={ 'border': 'solid', 'border-width': '1px 0'}) for i in range(len(user_name))
        ])
    ],style={'width': '100%', 'border-collapse': 'collapse'}),
    html.H1(
        children='Company Table',
        style={
            'textAlign': 'center',
        }
    ),
    html.Table([
        html.Thead(
            html.Tr([html.Th('Company Name'),html.Th('Company Address'),html.Th('Company Estabilish Year')], style={'textAlign' : 'left'})
        ),
        html.Tbody([
            html.Tr([
                html.Td(company_name[i]),
                html.Td(company_address[i]),
                html.Td(company_year[i])
            ], style={ 'border': 'solid', 'border-width': '1px 0'}) for i in range(len(company_name))
        ])
    ],style={'width': '100%', 'border-collapse': 'collapse'}),
    html.H1(
        children='App Table',
        style={
            'textAlign': 'center',
        }
    ),
    html.Table([
        html.Thead(
            html.Tr([html.Th('App Name'),html.Th('App Category'),html.Th('App Release Year')], style={'textAlign' : 'left'})
        ),
        html.Tbody([
            html.Tr([
                html.Td(app_name[i]),
                html.Td(app_category[i]),
                html.Td(app_year[i])
            ], style={ 'border': 'solid', 'border-width': '1px 0'}) for i in range(len(app_name))
        ])
    ],style={'width': '100%', 'border-collapse': 'collapse'}),
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
], style={'background-color': '#191970', 'color': '#FF4500', 'font-family': '"Trebuchet MS", sans-serif'})


if __name__ == '__main__':
    app.run_server(debug=True)
#Callbacks:
