
import streamlit as st
from streamlit import delta_generator
from streamlit.elements import image, text
from notion import *
from plots import *
from statistics import mean
import plotly.graph_objects as go
from modulefinder import ModuleFinder
import pandas as pd


st.set_page_config(layout="wide")
st.title(" 🏗️ Life Tracker")
st.caption("Enter your notion api info up there to get started!")

user_dataId=st.sidebar.text_input("Database ID:").strip('"')
integration_token=st.sidebar.text_input("Integration Token:").strip('"')

if len(integration_token and user_dataId):
    def load_data():
        nsync = NotionSync()
        data = nsync.query_databases(integration_token,user_dataId)
        metrics = nsync.get_metrics_titles(data)
        metrics_data = nsync.get_metrics_data(data,metrics)
        df = setupProjectsDf(metrics_data)
        return df
    df = load_data()

    with st.expander("History"):
        st.dataframe(df.tail())

    st.header("Ticker")
    
    with st.expander("See how your ticker is calculated:"):
        st.latex("\sum\limits_{i=1}^5 x_i= (\frac{x_1+ ... +x_5}{5})\cdot 1.01^{n}")
        st.markdown("""
            * $$x1, x2, x3, x4, x5$$: metrics, rated from 0 to 5.           
            * $k$: constant, $1.01$ is the growth rate
            * $n$: the number of days you have tracked
            """)
        
    row1_col1,row1_col2 = st.columns(2)
    row1_col1.plotly_chart(ticker_plot(df))
    row1_col2.plotly_chart(metric_plot(df))

    st.markdown("---")
    
    st.header("Average Metric Scores")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.plotly_chart(metric_dash(df.iloc[:, 1]))
    col2.plotly_chart(metric_dash(df.iloc[:, 2]))
    col3.plotly_chart(metric_dash(df.iloc[:, 3]))
    col4.plotly_chart(metric_dash(df.iloc[:, 4]))
    col5.plotly_chart(metric_dash(df.iloc[:, 5]))

else:
    pass

        


