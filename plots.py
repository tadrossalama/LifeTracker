
from PIL.Image import NONE
from plotly import plot
import streamlit as st
from streamlit import delta_generator
from streamlit.elements import text
from notion import *
from statistics import mean
import plotly.graph_objects as go

def setupProjectsDf(projects_data,dates):
    df = pd.DataFrame(projects_data)
    df["Date"] = dates
    df["Date"] =pd.to_datetime(df["Date"])
    df = df.set_index("Date")
    df = df.sort_index()
    df= df.reset_index(inplace=False)
    df['Ticker'] = round(df.mean(axis=1) * (1.01**df.index),2)
    
    return df

def ticker_plot(df):
    ticker_plot = px.line(x=df['Date'], y=df['Ticker'], 
        template="plotly_dark", title=':)TDOT')
    ticker_plot.update_traces(mode='markers+lines')
    ticker_plot.update_layout(
        font_family="Courier New",title={ 
            'text': "Ticker: :)TDOT",  
            'y': 0.95,
            'x': 0.5, 
            'xanchor': 'center', 
            'yanchor': 'top'
            },
            xaxis_title="Date",
            yaxis_title="Ticker",
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor="black",
                font_size=12,
                font_family="Courier New",
            ))
    return ticker_plot


metric_calc = lambda x: round(mean(x)-x[:-1].mean(),2)


def metric_plot(df):
    metric_plot = px.area(df, x=df['Date'], y=df.columns[:-1],template="plotly_dark")        
    metric_plot.update_layout(font_family="Courier New",title={ 
            'text': "Metrics",  
            'y': 0.95,
            'x': 0.4, 
            'xanchor': 'center', 
            'yanchor': 'top'
            })
    metric_plot.update_traces(mode='markers+lines')
    return metric_plot


def metric_dash(x):
    plot = go.Figure(go.Indicator(
        value = mean(x),
        mode = "gauge+number+delta",
        delta = {'reference': mean(x)-metric_calc(x)},
        title = {'text': f'{x.name}'},
        domain = {'x': [0, 0.4], 'y': [0, 0.4]},
        gauge = {'axis': {'range': [0, 5]}},
    ))
    return plot



