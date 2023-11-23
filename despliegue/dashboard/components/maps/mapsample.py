import pandas as pd
from dash import html , dcc
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/kaefee/dash-template-repo/master/data/jsonmaps/colombia.geo.json') as json_file:
            departamentos = json.load(json_file)

#Dataframe Vehicles maps
df_vehicles = pd.read_csv("data/vehicles.csv", delimiter =";", encoding="utf-8")
df_vehicles['DPTO'] = df_vehicles['DPTO'].astype('str').replace({'5':'05', '8':'08'})

#Dataframe pets maps
df_mascotas = pd.read_csv("data/mascotas_mapa.csv", delimiter =";", encoding="utf-8")
df_mascotas['DPTO'] = df_mascotas['DPTO'].astype('str').replace({'5':'05', '8':'08'})

#Cycle FOR properties of the id the name of department in Colombia
for i, each in enumerate(departamentos["features"]):
    departamentos["features"][i]['id'] = departamentos["features"][i]['properties']['DPTO']


class mapsample:    
    """A class to represent a samplemap of Montreal Elections"""        
    def __init__(self,map_title,ID,vehicles):
        """__init__
        Construct all the attributes for the sample map
     
        Args:
            map_title (str): _Title for the map_
            ID (str): _div id to specify unique #id with callbacks and css_
        
        Methods:

        display()
            Function to display a sample map with no arguments, uses plotly express data.
            
            Arguments:
                None

            Returns:
                html.Div : A Div container with a dash core component dcc.Graph() inside
        """

        self.map_title = map_title
        self.id = ID
        self.vehicles = vehicles

    @staticmethod
    def figura(vehicles):
        if vehicles == "bicycle":
            map_vehicles = px.choropleth_mapbox(df_vehicles, geojson=departamentos, locations='DPTO', color='Percent_bicycle',
                           hover_name='name_dpto',
                           hover_data=['Number_of_bicycles'],
                           color_continuous_scale="Viridis",
                           labels = {
                            'Percent_bicycle':'Bicicletas (%)',
                            'Number_of_bicycles':'Cantidad de Bicicletas',
                            'DPTO':'Id departamento DANE'
                           },
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                          )
            map_vehicles.update_layout(
                            geo_scope='south america',
                            mapbox_style="carto-positron",
                            mapbox_zoom=3.9, 
                            mapbox_center = {"lat": 6.88970868, "lon": -74.2973328}, height=330),
            map_vehicles.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        elif vehicles == "car":
            map_vehicles = px.choropleth_mapbox(df_vehicles, geojson=departamentos, locations='DPTO', color='Percent_car',
                           hover_name='name_dpto',
                           hover_data=['Number_of_cars'],
                           color_continuous_scale="Viridis",
                           labels = {
                            'Percent_car':'Carros (%)',
                            'Number_of_cars':'Cantidad de Carros',
                            'DPTO':'Id departamento DANE'},
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                          )
            map_vehicles.update_layout(
                            geo_scope='south america',
                            mapbox_style="carto-positron",
                            mapbox_zoom=3.9, 
                            mapbox_center = {"lat": 6.88970868, "lon": -74.2973328}, height=330),
            map_vehicles.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        else:
            map_vehicles = px.choropleth_mapbox(df_vehicles, geojson=departamentos, locations='DPTO', color='Percent_motorcycle',
                           hover_name='name_dpto',
                           hover_data=['Number_of_motorcycles'],
                           color_continuous_scale="Viridis",
                           labels = {
                            'Percent_motorcycle':'Motos (%)',
                            'Number_of_motorcycles':'Cantidad de Motocicletas',
                            'DPTO':'Id departamento DANE'
                           },
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                          )
            map_vehicles.update_layout(
                            geo_scope='south america',
                            mapbox_style="carto-positron",
                            mapbox_zoom=3.9, 
                            mapbox_center = {"lat": 6.88970868, "lon": -74.2973328}, height=330),
            map_vehicles.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return map_vehicles

    def display(self):
       
        layout = html.Div(
            [
                html.H4([self.map_title]),
                html.Div([
                    dcc.Graph(figure=self.figura(self))
                ])
               
            ],id=self.id
        )
        return layout

class mapsample_1:    
    """A class to represent a samplemap of Montreal Elections"""        
    def __init__(self,map_title,ID,pets):
        self.map_title = map_title
        self.id = ID
        self.pets = pets
        
    @staticmethod
    def figura_1(pets):
        if pets == "con_perro":
            map_pets = px.choropleth_mapbox(df_mascotas, geojson=departamentos, locations='DPTO', color='Mascotas_count',
                           hover_name='NOMBRE_DPT',
                           hover_data=['con_perro'],
                           color_continuous_scale="Viridis",
                           labels = {
                            'Mascotas_count':'Mascotas en 2021',
                            'con_perro':'Hogares en Colombia con Perro',
                            'NOMBRE_DPT':'Nombre departamento DANE'
                           },
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                          )            
            map_pets.update_layout(
                            geo_scope='south america',
                            mapbox_style="carto-positron",
                            mapbox_zoom=3.9, 
                            mapbox_center = {"lat": 6.88970868, "lon": -74.2973328}, height=460),
            map_pets.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        elif pets == "con_gato":
            map_pets = px.choropleth_mapbox(df_mascotas, geojson=departamentos, locations='DPTO', color='Mascotas_count',
                           hover_name='NOMBRE_DPT',
                           hover_data=['con_gato'],
                           color_continuous_scale="Viridis",
                           labels = {
                            'Mascotas_count':'Mascotas en 2021',
                            'con_gato':'Hogares en Colombia con Gato',
                            'NOMBRE_DPT':'Nombre departamento DANE'
                           },
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                          )
            map_pets.update_layout(
                            geo_scope='south america',
                            mapbox_style="carto-positron",
                            mapbox_zoom=3.9, 
                            mapbox_center = {"lat": 6.88970868, "lon": -74.2973328}, height=460),
            map_pets.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        elif pets == "perro_y_gato":
            map_pets = px.choropleth_mapbox(df_mascotas, geojson=departamentos, locations='DPTO', color='Mascotas_count',
                           hover_name='NOMBRE_DPT',
                           hover_data=['perro_y_gato'],
                           color_continuous_scale="Viridis",
                           labels = {
                            'Mascotas_count':'Mascotas en 2021',
                            'perro_y_gato':'Hogares en Colombia con Perro y Gato',
                            'NOMBRE_DPT':'Nombre departamento DANE'
                           },
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                          )
            map_pets.update_layout(
                            geo_scope='south america',
                            mapbox_style="carto-positron",
                            mapbox_zoom=3.9, 
                            mapbox_center = {"lat": 6.88970868, "lon": -74.2973328}, height=460),
            map_pets.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        else:
            map_pets = px.choropleth_mapbox(df_mascotas, geojson=departamentos, locations='DPTO', color='Mascotas_count',
                           hover_name='NOMBRE_DPT',
                           hover_data=['sin_mascota'],
                           color_continuous_scale="Viridis",
                           labels = {
                            'Mascotas_count':'Mascotas en 2021',
                            'sin_mascota':'Hogares en Colombia sin mascotas',
                            'NOMBRE_DPT':'Nombre departamento DANE'
                           },
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                          )
            map_pets.update_layout(
                            geo_scope='south america',
                            mapbox_style="carto-positron",
                            mapbox_zoom=3.9, 
                            mapbox_center = {"lat": 6.88970868, "lon": -74.2973328}, height=460),
            map_pets.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return map_pets

    def display_1(self):
       
        layout = html.Div(
            [
                html.H4([self.map_title]),
                html.Div([
                    dcc.Graph(figure=self.figura(self))
                ])
               
            ],id=self.id
        )
        return layout 