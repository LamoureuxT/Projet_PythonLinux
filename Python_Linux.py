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
from datetime import datetime, time, timedelta
df = pd.read_csv('/home/ec2-user/Projet/bitcoin_price.csv', sep=',', names=['Date', 'Price'])
df['Date'] = pd.to_datetime(df['Date'])
# Créer l'application Dash
app = dash.Dash(__name__)

now = datetime.now().date()            
start_day = datetime.combine(now, time.min)  
end_day = datetime.combine(now, time.max)     
df_day = df.loc[(df['Date'] >= start_day) & (df['Date'] <= end_day)] 

var = round((df_day['Price'].iloc[-1] - df_day['Price'].iloc[0]) / df_day['Price'].iloc[0] * 100,2)
col = 'red' if var < 0 else 'green'
min_price = df_day['Price'].min()
max_price = df_day['Price'].max()
daily_vol = round(df_day['Price'].std(),2)
price_return = round((df_day['Price'].iloc[-1] - df_day['Price'].iloc[0]) / df_day['Price'].iloc[0] * 100,2)

def generate_table():
    table = html.Div([
        html.H3("Daily Report {}".format(now.strftime('%d-%m-%Y')), style={'text-align': 'center'}),
        html.Table([
            html.Tbody([
                html.Tr([html.Td('Min.'), html.Td('${:,.0f}'.format(min_price))]),
                html.Tr([html.Td('Max.'), html.Td('${:,.0f}'.format(max_price))]),
                html.Tr([html.Td('Vol.'), html.Td(daily_vol)]),
                html.Tr([html.Td('Return'), html.Td('{}%'.format(price_return))]),
                html.Tr([html.Td('Open price'), html.Td('${:,.0f}'.format(df_day['Price'].iloc[0]))]),
                html.Tr([html.Td('Close price'), html.Td('${:,.0f}'.format(df_day['Price'].iloc[-1]))])
        ])
    ], className='table', style={'margin': 'auto'})
    ])

    return table


# Créer la mise en page de l'application
app.layout = html.Div([
    html.Div(
        children=[html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/800px-Bitcoin.svg.png', 
                         style={'height': '5%', 'width': '5%'}),
                html.H2("Bitcoin", style={"margin-left": "1rem"})],
             style={"display": "flex", "align-items": "center",'font-size': '2rem'}),
    html.Div('${:,.0f}'.format(df['Price'][len(df)-1]),style={'font-size': '3rem'}),
    html.Div('{:.2f}%'.format(var), style={'font-size': '3rem', 'color':col}),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [{'x': df['Date'], 'y': df['Price'], 'type': 'line','fill': 'tozeroy', 'fillcolor': 'lavender'}],
            'layout':{'yaxis': {'range': [min_price, max_price]}}
        }
    ),
    html.Div(className='table-container', children=generate_table(), style={'border': '1px solid #ddd', 'border-radius': '10px', 'margin-top': '20px'})
])

if __name__ == '__main__':
     app.run_server(host = "0.0.0.0", port = 8080, debug=True) 
