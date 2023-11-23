#Libraries for the data
from operator import contains
from pydoc import classname
from matplotlib.axis import Tick
from matplotlib.pyplot import xlabel
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as gp

#libraries
import dash
from dash import Dash, html , dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page
from xarray import align
import plotly.graph_objects as go

# dash-labs plugin call, menu name and route
register_page(__name__, path='/')

#Definition of map the contract
from components.maps.mapsample_home import mapsample_3
mapa_contratos = mapsample_3('Mapa de Contratos', 'id_mapa_contratos')

#Import dataframe graphs

df_edad_sexo = pd.read_csv("data/Edad_sexo.csv", delimiter =";", encoding ='utf-8')
df_TIPACCID_count = pd.read_csv("data/TIPACCID_count.csv", delimiter =",", encoding ='utf-8') 
diasemana_count = pd.read_csv("data/DIASEMANA_count.csv", delimiter =",", encoding ='utf-8') 
temp_df2 = pd.read_csv("data/GeneroEdad.csv")

fig_pie = px.pie(pd.read_csv("data/SEXO_count.csv"), values='y', names='x',
             labels={'y':'Porcentaje accidentes',
             'x':'Sexo'}
             #, title="Sexo del conductor"
             )

fig_pie.update_traces(hole=.3, textposition='inside', textinfo='percent')
fig_pie.update_layout(font=dict(
        size=10
      ))

fig_pie.layout.plot_bgcolor = 'rgba(0,0,0,0)'
fig_pie.layout.paper_bgcolor = 'rgba(0,0,0,0)'


#Funtion for the tipo de accidente 
def act_contract(data, tipo_contrato):
    fig_act_contract = px.bar(data, x="x", y="y", height=450,
            labels={
                "x":"Tipo de accidente",
                "y":"Número de fallecidos o heridos"
            }).update_xaxes(tickangle=290)
    fig_act_contract.update_layout(xaxis={"tickfont":{"size":8}})
    fig_act_contract.update_layout(yaxis={"tickfont":{"size":10}})
    fig_act_contract.layout.plot_bgcolor = 'rgba(0,0,0,0)'
    fig_act_contract.layout.paper_bgcolor = 'rgba(0,0,0,0)'

    return fig_act_contract

# Grafico de dia de la semana
fig_sem = px.bar(diasemana_count, x="x", y="y", 
             #color="z", 
             color = "z",
             title="Personas heridas y fallecidas por dia de la semana en accidente",
             labels={"x":"Dia semana", "y":"Conteo" }) 
fig_sem.layout.plot_bgcolor = 'rgba(0,0,0,0)'
fig_sem.layout.paper_bgcolor = 'rgba(0,0,0,0)'


#Grafico sexo
fig_gen2 = go.Figure()
fig_gen2.add_trace(go.Bar(x=-temp_df2["Mujer"].values,
                    y=temp_df2["RangoEdad"],
                    orientation='h',
                    name="Mujer",
                    customdata=temp_df2['Mujer'],
                    hovertemplate="Edad: %{y}<br>Accidentes:%{customdata}<br>Sexo:Mujer<extra></extra>",
                    marker_color="#F2B950"))
fig_gen2.add_trace(go.Bar(x=temp_df2["Hombre"].values,
                    y=temp_df2['RangoEdad'],
                    orientation='h',
                    name='Hombre',
                    hovertemplate="Edad: %{y}<br>Accidentes:%{x}<br>Sexo:Hombre<extra></extra>",
                    marker_color="#011C40"))

fig_gen2.update_layout(barmode='relative', 
                 height=500, 
                 width=400, 
                 yaxis_autorange='reversed',
                 bargap=0.01,
                 legend_orientation='h',
                 legend_x=0.07, legend_y=1.1)
                     #,"z":"Tipo de Accidente"})
fig_gen2.layout.plot_bgcolor = 'rgba(0,0,0,0)'
fig_gen2.layout.paper_bgcolor = 'rgba(0,0,0,0)'                     
                     
fig_sem.update_layout(font=dict(size = 11), height = 500)
fig_sem.update_traces(marker_color=1)
#Buttoms
Tipo_acc = [
    {"label":'Heridos', "value":"ACT"},
    {"label":'Fallecidos', "value":"OBSE"}
]


# specific layout for this page
layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                 html.H2(["Contexto de los accidentes automovilisticos en México"],className="title"),
            ], md=12)           
        ]),
        dbc.Row([
            dbc.Col([
                 html.H6([" El presente estudio, que pretende responder a la pregunta de ¿Cuál es la probabilidad de que haya un accidente fatal en un accidente automovilístico en México? Se basa en la necesidad de abordar esta problemática y reducir las consecuencias devastadoras que estos accidentes tienen en México. La información recopilada y analizada proporcionada por El instituto Nacional de Estadística y Geografía (INEGI) de México será fundamental para comprender las tendencias específicas de 2021 y contribuir a la implementación de estrategias efectivas de seguridad vial en el país. "],className="parrafo"),
            ], md=12)           
        ]),
        dbc.Row([
            dbc.Col([
                html.I(['  Mapa de Mexico Numero fallecidos Accidentes 2021'],className="fas fa-location-crosshairs me-2"),
                html.Br(),
                html.H6(className="subtitle"),
                html.Div([
                    dcc.Graph(figure=mapa_contratos.figura_3())])          
            ], md=7, className="border_columna"),
            dbc.Col([
                    html.I(['  Sexo del conductor'],className="fas fa-mars-and-venus me-2"),
                    dcc.Graph(id="Sexo", figure=fig_gen2) 
            ], md=5, className="border_columna")
        ]),        
        dbc.Row([
            dbc.Col([
                html.I([" Tipo accidente"],className="fas fa-file-lines me-2"),
                html.P("Resultados por tipo de accidente"),
                dcc.Dropdown(
                    id="accidentes",
                    options=Tipo_acc, multi=False),
                html.Br(),            
                html.H6("Distribución de Heridos o Fallecidos por tipo de accidente", className="title_graph"),
                dcc.Graph(id="Accidentes")  # No es necesario proporcionar la figura inicialmente                    
            ], md=12, className="border_columna")
        ]),
        dbc.Row([
            dbc.Col([
                html.I([" Distribucion semana"],className="fas fa-file-lines me-2"),
                dcc.Graph(id="Semana", figure=fig_sem) 
                ], md=12, className="border_columna")
        ])
        ]
)

@callback(
    Output("Accidentes", "figure"),
    Input("accidentes", "value")
)
def filter_contrato(select_contrato):
    if not select_contrato:
        filtered_data = df_TIPACCID_count
    elif select_contrato == 'ACT':
        filtered_data = df_TIPACCID_count[df_TIPACCID_count['z'] == 'No fatal']
    else:
        filtered_data = df_TIPACCID_count[df_TIPACCID_count['z'] == 'Fatal']

    fig_act_contract = act_contract(filtered_data, ['ACT', 'OBSE'])
    return fig_act_contract