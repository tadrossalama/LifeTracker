import requests
import json
import pandas as pd
import plotly.express as px
import streamlit as st
from statistics import mean



NOTION_URL = 'https://api.notion.com/v1/databases/'

class NotionSync:
    def __init__(self):
        pass    

    def query_databases(self,integration_token, DATABASE_ID):
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


def setupProjectsDf(projects_data,dates):
    df = pd.DataFrame(projects_data)
    df["Date"] = dates
    df["Date"] =pd.to_datetime(df["Date"])
    df = df.sort_values('Date')
    return df
