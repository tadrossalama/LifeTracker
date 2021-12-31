import streamlit as st
from streamlit import delta_generator
from streamlit.elements import text
from LifeTracker import *
from statistics import mean
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Life Tracker")
user_dataId=st.text_input("Enter your dataId:")

user_integration_token=st.text_input("Enter your integration token:")
integration_token = user_integration_token
DATABASEID = user_dataId



if user_integration_token == None:
    pass
else:
    #from LifeTracker import NotionSync
    def load_data():
        nsync = NotionSync()
        data = nsync.query_databases(user_integration_token,user_dataId)
        projects = nsync.get_projects_titles(data)
        projects_data,dates = nsync.get_projects_data(data,projects)
        df = setupProjectsDf(projects_data,dates)
        return df
    df = load_data()


def main():
 

        df['Ticker'] = df.sum(axis=1) 
        df['Ticker'] = df['Ticker']+(1.01**df.index)




        st.dataframe(df)

        def metric(x):
            daily_score = x.mean()- x[:-1].mean()
            return round(daily_score,2)
        


        ticker_plot = px.line(x=df['Date'], y=df['Ticker'], 
            template="plotly_dark", title=':)TDOT')
        ticker_plot.update_layout(
            font_family="Courier New",title={ 
                'text': "Ticker: :)TDOT",  
                'y': 0.95,
                'x': 0.5, 
                'xanchor': 'center', 
                'yanchor': 'top'
                })
    
        

        metric_plot = px.area(df, x=df['Date'], y=df.columns[:-1],template="plotly_dark")
            
        metric_plot.update_layout(font_family="Courier New",title={ 
                'text': "Metrics",  
                'y': 0.95,
                'x': 0.4, 
                'xanchor': 'center', 
                'yanchor': 'top'
                })
    
        



        



        
        st.header("Ticker")
        st.latex("\displaystyle\sum_{i=1}^5x_i +k^n = (x_1 + x_2 + x_3 + x_4) + 0.01^{n})")
        row1_col1, row1_col2 = st.columns(2)
        row1_col1.plotly_chart(ticker_plot)
        row1_col2.plotly_chart(metric_plot)

        #metrics_plot = px.line(x=df['Date'], color='projects', template="plotly_dark")
        #st.plotly_chart(metrics_plot)
        st.header("Average Metric Scores:")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="Satisfaction", value=round(mean(df["Satisfaction"]), 2), delta= metric(df["Satisfaction"]))
        col2.metric(label="Personal Development", value=round(mean(df["Personal Development"])), delta= metric(df["Personal Development"]))
        col3.metric(label="Professional Development", value=round(mean(df["Professional Development"])), delta= metric(df["Professional Development"]))
        col4.metric(label="Health", value=round(mean(df["Health"]), 2), delta= metric(df["Health"]))


        fig2 = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            delta = {'reference': mean(df["Satisfaction"])-metric(df["Satisfaction"])},
            value = mean(df["Satisfaction"]),
            title = {'text': "Satisifaction"},
            domain = {'x': [0, 0.5], 'y': [0, 0.5]},
            gauge = {'axis': {'range': [0, 5]}},
        ))
        st.plotly_chart(fig2)


main()