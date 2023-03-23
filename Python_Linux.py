# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 21:48:00 2023

@author: Utilisateur
"""
import dash
from dash import dcc
from dash import html
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from dash.dependencies import Input, Output
df = pd.read_csv('/home/ec2-user/Projet/bitcoin_price.csv', sep=',', names=['Date', 'Price'])

# Créer l'application Dash
app = dash.Dash(__name__)

# Compute mean
mean_price = df['Price'].mean()
min_price = df['Price'].min()
max_price = df['Price'].max()

table = html.Table([
    html.Thead(
        html.Tr([html.Th("Header 1"), html.Th("Header 2"), html.Th("Header 3")])
    ),
    html.Tbody([
        html.Tr([html.Td("Row 1, Col 1"), html.Td("Row 1, Col 2"), html.Td("Row 1, Col 3")]),
        html.Tr([html.Td("Row 2, Col 1"), html.Td("Row 2, Col 2"), html.Td("Row 2, Col 3")]),
        html.Tr([html.Td("Row 3, Col 1"), html.Td("Row 3, Col 2"), html.Td("Row 3, Col 3")]),
    ])
])

# Créer la mise en page de l'application
app.layout = html.Div([
    html.Div(
        children=[html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/800px-Bitcoin.svg.png', 
                         style={'height': '5%', 'width': '5%'}),
                html.H2("Bitcoin", style={"margin-left": "1rem"})],
             style={"display": "flex", "align-items": "center",'font-size': '2rem'}),
    html.Div('${:,.2f}'.format(df['Price'][len(df)-1]),style={'font-size': '3rem'}),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [{'x': df['Date'], 'y': df['Price'], 'type': 'line'}],
            'layout': {'title': 'Value over Time'}
        }
    ),
    html.Table(
        [html.Tr([html.Th('Stat'), html.Th('Price')])] +
        [html.Tr([html.Td('Min'), html.Td('${:,.2f}'.format(min_price))]),
        html.Tr([html.Td('Max'), html.Td('${:,.2f}'.format(max_price))]),
        html.Tr([html.Td('Mean'), html.Td('${:,.2f}'.format(round(mean_price,2)))])
        ],
        style={'textAlign': 'center'},
        className='stats-table'
    ),
])

if __name__ == '__main__':
    app.run_server(debug=False)
