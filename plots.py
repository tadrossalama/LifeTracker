
from PIL.Image import NONE
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

def metric_calc(x):
    daily_score = x.mean()- x[:-1].mean()
    return round(daily_score,2)

def metric_plot(df):

    metric_plot = px.area(df, x=df['Date'], y=df.columns[:-1],template="plotly_dark")        
    metric_plot.update_layout(font_family="Courier New",title={ 
            'text': "Metrics",  
            'y': 0.95,
            'x': 0.4, 
            'xanchor': 'center', 
            'yanchor': 'top'
            })
    return metric_plot


