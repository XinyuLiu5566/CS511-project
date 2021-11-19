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
from neomodel import db
import numpy as np
from django.db.models import Avg


colors = {
    'background': '#222222',
    'text': '#FF4500'
}


users = User.nodes.all()
apps = App.nodes.all()
companies = Company.nodes.all()
q1 = db.cypher_query("MATCH (u:User)-[r:download]->(a:App) return a.name, count(u)")[0]
q2 = db.cypher_query("MATCH (u:User)-[r:download]->(a:App) return a.category, count(u)")[0]
q3 = db.cypher_query("MATCH (c:Company)-[r:develop]->(a:App) return c.name, count(a)")[0]
q1_name = []
app_download_count = []
q2_name = []
company_develop_count = []
q3_name = []
app_category_count = []
# get the info about users from neo4j database
user_name = []
user_gender = []
for user in users:
    user_name.append(user.name)
    user_gender.append(user.gender)
for i in range(len(q1)):
    app_download_count.append(q1[i][1])
    q1_name.append(q1[i][0])
for i in range(len(q2)):
    app_category_count.append(q2[i][1])
    q2_name.append(q2[i][0])
for i in range(len(q3)):
    company_develop_count.append(q3[i][1])
    q3_name.append(q3[i][0])

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
    "App": q1_name,
    "App Download Count": app_download_count
})
fig = px.bar(df, x="App", y="App Download Count")

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
            options=[{'label': i, 'value': i} for i in ['App Download Count', 'App Category Count', 'Company Develop Count']],
            value='App Download Count',
            style={ 'color': '#000000','background-color': '#A0A0A0'} 
        ),
    ], style={'width': '25%', 'display': 'inline-block'}),
    dcc.Graph(
        id='bar_chart',
        figure=fig,
        style={'width': '100%', 'display': 'inline-block'}
    ),
], style={'background-color': '#191970', 'color': '#FF4500', 'font-family': '"Trebuchet MS", sans-serif'})


@app.callback(
    Output('bar_chart', 'figure'),
    Input('yaxis_value', 'value'))
def update_graph(yaxis_value):
    yval = app_download_count
    xval = q1_name
    title = "App"
    if yaxis_value == 'App Category Count':
        yval = app_category_count
        xval = q2_name
        title = "Category"
    elif yaxis_value == 'Company Develop Count':
        yval = company_develop_count
        xval = q3_name
        title = "Company"
    df = pd.DataFrame({
    title: xval,
    yaxis_value: yval
    })
    fig = px.bar(df, x=title, y=yaxis_value)
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor='#191970',
        font_color=colors['text']
    )
    print("update barchart")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
#Callbacks:
