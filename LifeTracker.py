import requests
import json
import pandas as pd
import plotly.express as px
import streamlit as st
from statistics import mean


#"24edfc00c602424c97ef163ddbf0b62e"
DATABASE_ID = "24edfc00c602424c97ef163ddbf0b62e"
NOTION_URL = 'https://api.notion.com/v1/databases/'

class NotionSync:
    def __init__(self):
        pass    

    def query_databases(self,integration_token="secret_AueOazcWhfdetCH6dN4leUC49kiW27RvJN01J7zPgsF"):
        database_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(database_url, headers={"Authorization":"Bearer " + f"{integration_token}",
                                                        "Notion-Version": "2021-08-16"})
        if response.status_code != 200:
            print(f'Response Status: {response.status_code}')
        else:
            return response.json()
    
    def get_projects_titles(self,data_json):
        return list(data_json["results"][0]["properties"].keys())
    

    def get_projects_data(self,data_json,projects):
        projects_data = {}
        for p in projects:
            if p!="Name" and p !="Date":
                projects_data[p] = [data_json["results"][i]["properties"][p]["number"]
                                    for i in range(len(data_json["results"]))]
            elif p=="Date":
                dates = [data_json["results"][i]["properties"]["Date"]["date"]["start"]
                                    for i in range(len(data_json["results"]))]

        
        return projects_data,dates

nsync = NotionSync()
data = nsync.query_databases()
projects = nsync.get_projects_titles(data)
projects_data,dates = nsync.get_projects_data(data,projects)

def setupProjectsDf(projects_data,dates):
    df = pd.DataFrame(projects_data)
    df["Date"] = dates
    df["Date"] =pd.to_datetime(df["Date"])
    df = df.sort_values('Date')
    



    return df

'''''
def main():
    
    st.title("Life Tracker")
    user_dataId=st.text_input("Enter your dataId:")
    user_integration_token=st.text_input("Enter your integration token:")

    if user_dataId and user_integration_token == "" or None:
        exit()
    else:
        def load_data():
            nsync = NotionSync()
            DATABASE_ID=user_dataId
            data = nsync.query_databases(integration_token=user_integration_token)
            projects = nsync.get_projects_titles(data)
            projects_data,dates = nsync.get_projects_data(data,projects)
            df = setupProjectsDf(projects_data,dates)
            return df
        df = load_data()


        df['Ticker'] = df.sum(axis=1) 
        df['Ticker'] = df['Ticker']+(1.01**df.index)




        st.dataframe(df)

        def metric(x):
            daily_score = x.mean()- x[:-1].mean()
            return round(daily_score,2)
        


        ticker_plot = px.line(x=df['Date'], y=df['Ticker'], 
            template="plotly_dark", title=':)TDOT')
        ticker_plot.update_layout(
            font_family="Courier New")


        
        st.header("Ticker")
        st.latex("\displaystyle\sum_{i=1}^5x_i +k^n = (x_1 + x_2 + x_3 + x_4) + 0.01^{n})")
        st.plotly_chart(ticker_plot)

        #metrics_plot = px.line(x=df['Date'], color='projects', template="plotly_dark")
        #st.plotly_chart(metrics_plot)

        st.metric(label="Satisfaction", value=round(mean(df["Satisfaction"]), 2), delta= metric(df["Satisfaction"]))
        st.metric(label="Personal Development", value=round(mean(df["Personal Development"])), delta= metric(df["Personal Development"]))
        st.metric(label="Professional Development", value=round(mean(df["Professional Development"])), delta= metric(df["Professional Development"]))
        st.metric(label="Health", value=round(mean(df["Health"]), 2), delta= metric(df["Health"]))
main()
'''

