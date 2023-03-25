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
day_1= datetime.now().date() - timedelta(days=1)
day_1_start = datetime.combine(day_1, time.min)
day_1_end = datetime.combine(day_1, time.max)
df_day_1 = df.loc[(df['Date'] >= day_1_start) & (df['Date'] <= day_1_end)]
var = round((df_day['Price'].iloc[-1] - df_day['Price'].iloc[0]) / df_day['Price'].iloc[0] * 100,2)
col = 'red' if var < 0 else 'green'


def new_report():
    min_price = df_day['Price'].min()
    max_price = df_day['Price'].max()
    price_return = round((df_day['Price'].iloc[-1] - df_day['Price'].iloc[0]) / df_day['Price'].iloc[0] * 100,2)
    daily_vol = round(price_return.std(),2)
    
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

def previous_report():
    min_price = df_day_1['Price'].min()
    max_price = df_day_1['Price'].max()
    price_return = round((df_day_1['Price'].iloc[-1] - df_day_1['Price'].iloc[0]) / df_day_1['Price'].iloc[0] * 100,2)
    daily_vol = round(price_return.std(),2)
    

    table = html.Div([
        html.H3("Daily Report {}".format(yesterday.strftime('%d-%m-%Y')), style={'text-align': 'center'}),
        html.Table([
            html.Tbody([
                html.Tr([html.Td('Min.'), html.Td(min_price)]),
                html.Tr([html.Td('Max.'), html.Td(max_price)]),
                html.Tr([html.Td('Volatility'), html.Td(daily_vol)]),
                html.Tr([html.Td('Return'), html.Td('{}%'.format(price_return))]),
                html.Tr([html.Td('Open price'), html.Td(df_day_1['Price'].iloc[0])]),
                html.Tr([html.Td('Close price'), html.Td(df_day_1['Price'].iloc[-1])])
        ])
    ], className='table', style={'margin': 'auto'})
    ])
    return table

def report():
    now = datetime.now() 
    today_8pm = datetime.combine(now.date(), time(hour=20))  
    if now.hour >= today_8pm.hour:  
        return new_report()      
    else:
        return previous_report()
    
# Créer la mise en page de l'application
app.layout = html.Div([    
   html.Div([html.Div([        
       html.Div([html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/800px-Bitcoin.svg.png',                 
                 style={'height': '5%', 'width': '5%'}),            
                 html.H2("Bitcoin", style={"margin-left": "1rem"})], 
                style={"display": "flex", "align-items": "center", 'font-size': '2rem'}),
       html.Div('${:,.0f}'.format(df['Price'][len(df)-1]),style={'font-size': '3rem'}),
       html.Div('{:.2f}%'.format(var), style={'font-size': '3rem', 'color':col}),
   ]), 
   html.Div([
       html.Div(className='table-container', children=report(),            
                style={'border': '1px solid #ddd', 'border-radius': '10px', 'margin': '20px 20px 20px 20px','flex': '1'})       
   ])], style={"display": "flex", "flex-direction": "row", "margin-top": "20px"}), 
    
    html.Div(dcc.Graph(id='example-graph',
              figure={'data': [{'x': df['Date'], 'y': df['Price'], 'type': 'line','fill': 'tozeroy', 'fillcolor': 'lavender'}],
                'layout':{'yaxis': {'range': [df['Price'].min(), df['Price'].max()]}}
            }
        )
    )
])



if __name__ == '__main__':
     app.run_server(host = "0.0.0.0", port = 8080, debug=True) 
