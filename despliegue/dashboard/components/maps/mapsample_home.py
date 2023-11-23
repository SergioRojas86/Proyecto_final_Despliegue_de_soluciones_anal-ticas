import pandas as pd
from dash import html , dcc
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json

            
with urlopen('https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json') as response:
    counties = json.load(response)

#Dataframe fatal accidents  maps
mapa_estado = pd.read_csv("data/mapa_estado.csv", sep=",")

class mapsample_3:    
    def __init__(self,map_title,ID):
        self.map_title = map_title
        self.id = ID

    @staticmethod
    def figura_3():
        map_contract = px.choropleth_mapbox(mapa_estado, geojson=counties, featureidkey="properties.name",
                           locations="x",center={"lat": 23.6345, "lon": -102.5528},zoom=2.6, color_continuous_scale="Viridis",
                          color= 'y', mapbox_style="carto-positron", labels={"x":"Estado", "y":"Acc Fatales"})
        map_contract.update_layout(
                        mapbox_style="carto-positron",
                        mapbox_zoom=2.8, 
                        mapbox_center = {"lat": 23.6345, "lon": -102.5528}, height=430),
        map_contract.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        return map_contract

    def display_3(self):
       
        layout = html.Div(
            [
                html.H4([self.map_title]),
                html.Div([
                    dcc.Graph(figure=self.figura_3)
                ])
               
            ],id=self.id
        )
        return layout