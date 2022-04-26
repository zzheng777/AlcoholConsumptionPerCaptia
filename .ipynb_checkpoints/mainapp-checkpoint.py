# Good modules to have
import numpy as np, pandas as pd
import random, json, time, os

# Required Modules
import plotly
import plotly.graph_objects as go
import plotly.express as px
from dash import dash, dcc, html
from dash.dependencies import Input, Output


# Add basic CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# This is the main application
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Do not bother us with exceptions
app.config.suppress_callback_exceptions = True


###################
#  Make Basic Plot  #
#####################
df = pd.read_csv("alcohol-consumption-vs-gdp-per-capita.csv")

    
#################################################
################# Layout ########################
#################################################

app.layout = html.Div([
    html.H1(children='Changes in the World by Year', style={"text-align": "center", "font-weight": "bold"}),
    html.H2(children='This is an interactive map which show Alcohol Consumption per Captia, GDP per Capita and Population .'),
    
    html.H6("Use the slider below to change the figures:"),
    html.Div([
    html.Label(['Choose a graph:'],style={'font-weight': 'bold'}),
    dcc.RadioItems(
        id='radio_items',
        options=[
                 {'label': 'AlcoholConsumption', 'value': 'AlcoholConsumption'},
                 {'label': 'GDP', 'value': 'GDP'},
                 {'label': 'Population', 'value': 'Population'}
        ],
        value='AlcoholConsumption',
        style={"text-align": "right","width": "60%"}
    ),
    ]),
    
    html.Br(),
    dcc.Graph(id='Alcohol')

])  
## HI ME YO
@app.callback(
    Output('Alcohol', 'figure'),
    [Input('radio_items', 'value')])
def Makeplot(radio_items, df=df):
    df=pd.read_csv("alcohol-consumption-vs-gdp-per-capita.csv")
    df=df.iloc[:,0:6]
    df.rename(columns={"Total alcohol consumption per capita (liters of pure alcohol, projected estimates, 15+ years of age)": "AlcoholConsumption", "Population (historical estimates)": "Population", "GDP per capita, PPP (constant 2017 international $)": "GDP"}, inplace=True)

    df = df[df["Year"] > 1999]
    df.dropna(subset=["Entity", radio_items], inplace=True)
    df = df.sort_values(by=['Year'], ascending=True)

    data_slider = []
    years = df["Year"].unique()
    for year in years:
        df_segmented =  df[df['Year']== year]

        for col in df_segmented.columns:
            df_segmented[col] = df_segmented[col].astype(str)

        data_each_yr = dict(
                            type='choropleth',
                            locations = df_segmented['Entity'],
                            z=df_segmented[radio_items].astype(float),
                            locationmode='country names',
                            colorscale = 'inferno_r',
                            colorbar= {'title':radio_items})

        data_slider.append(data_each_yr)

    steps = []
    for i in range(len(data_slider)):
        step = dict(method='restyle',
                    args=['visible', [False] * len(data_slider)],
                    label='Year {}'.format(years[i]))
        step['args'][1][i] = True
        steps.append(step)

    sliders = [dict(active=0, pad={"t": 1}, steps=steps)]

    layout = dict(title = radio_items + ' Per Capita', geo=dict(scope='world',
                           projection={'type': 'natural earth'}), autosize=False, width=1000,
                  height = 600, sliders=sliders,annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href=https://www.kaggle.com/datasets/pralabhpoudel/alcohol-consumption-by-country">\
            Kaggle</a>',
        showarrow = False
    )])
    

    fig = dict(data=data_slider, layout=layout)
    return go.Figure(fig)
    


    # -------------------------- MAIN ---------------------------- #


# This is the code that gets run when we call this file from the terminal
# The port number can be changed to fit your particular needs
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
