#Libraries for the data
from pydoc import classname
from matplotlib.axis import Tick
from matplotlib.pyplot import xlabel
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

#libraries
import dash
from dash import Dash, html , dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page
from xarray import align
from datetime import datetime as dt
from dash.exceptions import PreventUpdate

# dash-labs plugin call, menu name and route
register_page(__name__, path='/Prediccion')

layout = html.Div([
    dbc.Row([html.H6("En esta página podrás realizar la predicción de la falalidad con el fin de dar prioridad al accidente"),
    
    html.Label('Selecciona una fecha:'),
    dcc.DatePickerSingle(
        id='date-picker',
        date=dt.now(),
    )]),
    
    dbc.Row([html.Label('Selecciona una hora:'),
    dcc.Input(
        id='time-picker',
        type='time',
        value='12:00',
    )]),
    

    
    dbc.Row([html.Label('Escriba el ID del municipio:'),
    dcc.Input(id='input-variable2', type='number', value=0)]),
    # Agrega más entradas para las otras variables según sea necesario
    dbc.Row([html.Label("Zona Urbana"),
    dcc.Dropdown(
        id='dropdown-variable1',
        options=[
            {'label': 'En zona suburbana', 'value': 0},
            {'label': 'En Intersecciòn', 'value': 1 },
            {'label': 'No fue en Intesección', 'value': 2},
            # Agrega más opciones según sea necesario
        ],
        value='opcion1'
    )]),
    dbc.Row([html.Label("Zona Suburbana"),    
    dcc.Dropdown(
        id='dropdown-variable2',
        options=[
            {'label': 'Evento vial en zona urbana', 'value': 0},
            {'label': 'Camino rural', 'value': 1},
            {'label': 'Carretera estatal', 'value': 2},
            {'label': 'Otro Camino', 'value': 3},
            # Agrega más opciones según sea necesario
        ],
        value='opcionA'
    )]),
    dbc.Row([html.Label("Tipo de accidente"),    
    dcc.Dropdown(
        id='dropdown-variable2',
        options=[
            {'label': 'Certificado cero', 'value': 0},
            {'label': 'Colisión con vehículo automotor', 'value': 1},
            {'label': 'Colisión con peaton', 'value': 2},
            {'label': 'Colisión con animal', 'value': 3},
            {'label': 'Colisión con objeto fijo', 'value': 4},
            {'label': 'Volcadura', 'value': 5},
            {'label': 'Caída de pasajero', 'value': 6},
            {'label': 'Salida de camión', 'value': 7},
            {'label': 'Incendio', 'value': 8},
            {'label': 'Colisión con ferrocarril', 'value': 9},
            {'label': 'Colisión con motocicleta','value': 10},
            {'label': 'Colisión con ciclista', 'value': 11},
            {'label': 'Otro', 'value': 12},
            # Agrega más opciones según sea necesario
        ],
        value='opcionA'
    )]),
    dbc.Row([html.Label("Causa Accidente"),    
    dcc.Dropdown(
        id='dropdown-variable2',
        options=[
            {'label': 'Certificado cero', 'value': 0},
            {'label': 'Conductor', 'value': 1},
            {'label': 'Peaton o pasajero', 'value': 2},
            {'label': 'Falla de vehículo', 'value': 3},
            {'label': 'Mala condición del camino', 'value': 4},
            {'label': 'Otra', 'value': 5},
          # Agrega más opciones según sea necesario
        ],
        value='Certificado cero'
    )]),
    
    dbc.Row([html.Label('Escriba el número de automoviles involucrados:'),
    dcc.Input(id='input-variable1', type='number', value=0)
    ]),
    
    dbc.Row([html.Label('Escriba el número de Camionetas de pasajeros involucradas:'),
    dcc.Input(id='input-variable1', type='number', value=0)
    ]),
    
    dbc.Row([html.Label('Escriba el número de Camion de pasajeros involucrados:'),
    dcc.Input(id='input-variable1', type='number', value=0)
    ]),
    
    dbc.Row([html.Label('Escriba el número de Onmibuses involucrados:'),
    dcc.Input(id='input-variable1', type='number', value=0)
    ]),
    
    dbc.Row([html.Label('Escriba el número de Tranvias involucrados:'),
    dcc.Input(id='input-variable1', type='number', value=0)
    ]),
    
    dbc.Row([html.Label('Escriba el número de Caminonetas de carga involucradas:'),
    dcc.Input(id='input-variable1', type='number', value=0)
    ]),
    
    dbc.Row([html.Label('Escriba el número de Camiones de carga involucrados:'),
    dcc.Input(id='input-variable1', type='number', value=0)
    ]),
    
    dbc.Row([html.Label('Escriba el número de Tractores involucrados:'),
    dcc.Input(id='input-variable1', type='number', value=0)
    ]),
        
    dbc.Row([html.Label('Escriba el número de Ferrocarriles involucrados:'),
    dcc.Input(id='input-variable1', type='number', value=0)
    ]),
        
    dbc.Row([html.Label('Escriba el número de Motocicletas involucrados:'),
    dcc.Input(id='input-variable1', type='number', value=0)
    ]),
        
    dbc.Row([html.Label('Escriba el número de Bicicletas involucrados:'),
    dcc.Input(id='input-variable1', type='number', value=0)
    ]),
        
    dbc.Row([html.Label('Escriba el número de Otros Vehiculos involucrados:'),
    dcc.Input(id='input-variable1', type='number', value=0)
    ]),
        
    dbc.Row([html.Label('Estimaciòn de daños en propiedad:'),
    dcc.Input(id='input-variable1', type='number', value=0)
    ]),
    
    dbc.Row([html.Label("Sexo del Conductor"),    
    dcc.Dropdown(
        id='dropdown-variable2',
        options=[
            {'label': 'Certificado cero', 'value': 0},
            {'label': 'Se fugó', 'value': 1},
            {'label': 'Hombre', 'value': 2},
            {'label': 'Mujer', 'value': 3},
          # Agrega más opciones según sea necesario
        ],
        value='Certificado cero'
    )]),
    
#     dbc.Row([
#         dbc.Col([
#         html.Label('col1 :'),
#         dcc.Input(id='input-variable1', type='number', value=0)
#     ]),
#         dbc.Col([
#         html.Label('Col 2:') ,
#         dcc.Input(id='input-variable1', type='number', value=0)
#         ], md=12,) ,
# ]),
    
   html.Div(id='prediction-output', style={'font-size': '40px', 'margin-top': '20px'})  
  ,
   html.Button('Predecir', id='predict-button')
    
   
])
# Callback para la actualización de la salida
@callback(
    Output('prediction-output', 'children'),
    [Input('predict-button', 'n_clicks')],
    [Input('input-variable1', 'value'),
     Input('input-variable2', 'value'),
     Input('dropdown-variable1', 'value'),
     Input('dropdown-variable2', 'value')]
)
def update_output(n_clicks, var1, var2, var3, var4):
    if n_clicks is None:
        raise PreventUpdate
    
    # Lógica de predicción (puedes cambiar esto según tu implementación real)
    resultado_prediccion = 27.75+10 * np.random.random() # Esto debe ser tu resultado de la predicción
    
    return f"Resultado de la predicción: {resultado_prediccion:.2f}%"