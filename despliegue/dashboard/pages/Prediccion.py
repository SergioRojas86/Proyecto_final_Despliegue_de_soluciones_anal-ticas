#Libraries for the data
from pydoc import classname
from matplotlib.axis import Tick
from matplotlib.pyplot import xlabel
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pickle

#libraries
import dash
from dash import Dash, html , dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page
from xarray import align
from datetime import datetime as dt
from dash.exceptions import PreventUpdate

from .limpieza import limpiar_datos

import base64
import io



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
    dcc.Input(id='input-Id_municipio', type='number', value=4,
        max=570 )]),
    
    dbc.Row([html.Label('Escriba el ID del estado:'),
    dcc.Input(id='input-Id_estado', type='number', value=2,
        max=32 )]), 
           
        # Agrega más entradas para las otras variables según sea necesario
    dbc.Row([html.Label("Zona Urbana"),
    dcc.Dropdown(
        id='dropdown-zona_urbana',
        options=[
            {'label': 'Accidente en intersección', 'value': 'Accidente en intersección' },
            {'label': 'No fue en Intesección', 'value': 'Sin accidente en esta zona'},
            # Agrega más opciones según sea necesario
        ],
        value= 'Accidente en intersección'
    )]),
    dbc.Row([html.Label("Zona Suburbana"),    
    dcc.Dropdown(
        id='dropdown-zona_suburbana',
        options=[
            {'label': 'Sin accidente en esta zona', 'value': 'Sin accidente en esta zona'},
            {'label': 'Accidente en carretera estatal', 'value': 'Accidente en carretera estatal'},
            {'label': 'Accidente en camino rural', 'value': 'Accidente en camino rural'},
            # Agrega más opciones según sea necesario
        ],
        value='Sin accidente en esta zona'
    )]),
    dbc.Row([html.Label("Tipo de accidente"),    
    dcc.Dropdown(
        id='dropdown-tipo_accidente',
        options=[
            {'label': 'Colisión con vehículo automotor', 'value': 'Colisión con vehículo automotor'},
            {'label': 'Colisión con motocicleta', 'value': 'Colisión con motocicleta'},
            {'label': 'Colisión con objeto fijo', 'value': 'Colisión con objeto fijo'},
            {'label': 'Colisión con peatón (atropellamiento)', 'value': 'Colisión con peatón (atropellamiento)'},
            {'label': 'Volcadura', 'value': 'Volcadura'},
            {'label': 'Salida del camino', 'value': 'Salida del camino'},
            {'label': 'Otro', 'value': 'Otro'},
            {'label': 'Colisión con ciclista', 'value': 'Colisión con ciclista'},
            {'label': 'Caída de pasajero', 'value': 'Caída de pasajero'},
            {'label': 'Colisión con animal', 'value': 'Colisión con animal'},
            {'label': 'Incendio', 'value': 'Incendio'},
            # Agrega más opciones según sea necesario
        ],
        value='Colisión con vehículo automotor'
    )]),
    dbc.Row([html.Label("Causa Accidente"),    
    dcc.Dropdown(
        id='dropdown-causa_accidente',
        options=[
            {'label': 'Conductor', 'value': 'Conductor'},
            {'label': 'Falla de vehículo', 'value': 'Falla de vehículo'},
            {'label': 'Mala condición del camino', 'value': 'Mala condición del camino'},
            {'label': 'Otra', 'value': 'Otra'},
          # Agrega más opciones según sea necesario
        ],
        value='Conductor'
    )]),
    
    dbc.Row([html.Label('Escriba el número de automoviles involucrados:'),
    dcc.Input(id='input-automoviles', type='number', value=0)
    ]),
    
    dbc.Row([html.Label('Escriba el número de Camionetas de pasajeros involucradas:'),
    dcc.Input(id='input-camionetas', type='number', value=0)
    ]),

    dbc.Row([html.Label('Escriba el número de Microbuses de pasajeros involucradas:'),
    dcc.Input(id='input-Microbuses', type='number', value=0)
    ]),
        
    dbc.Row([html.Label('Escriba el número de Camiones involucrados:'),
    dcc.Input(id='input-camiones', type='number', value=0)
    ]),
    
    dbc.Row([html.Label('Escriba el número de Onmibuses involucrados:'),
    dcc.Input(id='input-ominibuses', type='number', value=0)
    ]),
    
    dbc.Row([html.Label('Escriba el número de Tranvias involucrados:'),
    dcc.Input(id='input-tranvias', type='number', value=0)
    ]),
    
    dbc.Row([html.Label('Escriba el número de Caminonetas de carga involucradas:'),
    dcc.Input(id='input-camionetas_carga', type='number', value=0)
    ]),
    
    dbc.Row([html.Label('Escriba el número de Camiones de carga involucrados:'),
    dcc.Input(id='input-camiones_de_carga', type='number', value=0)
    ]),
    
    dbc.Row([html.Label('Escriba el número de Tractores involucrados:'),
    dcc.Input(id='input-tractores', type='number', value=0)
    ]),
        
    dbc.Row([html.Label('Escriba el número de Ferrocarriles involucrados:'),
    dcc.Input(id='input-ferrocarril', type='number', value=0)
    ]),
        
    dbc.Row([html.Label('Escriba el número de Motocicletas involucrados:'),
    dcc.Input(id='input-motocicleta', type='number', value=0)
    ]),
        
    dbc.Row([html.Label('Escriba el número de Bicicletas involucrados:'),
    dcc.Input(id='input-bicicleta', type='number', value=0)
    ]),
        
    dbc.Row([html.Label('Escriba el número de Otros Vehiculos involucrados:'),
    dcc.Input(id='input-otros_vehiculos', type='number', value=0)
    ]),
    
    dbc.Row([html.Label("Superficie de rodamiento"),    
    dcc.Dropdown(
        id='dropdown-superficie_rodamiento',
        options=[
            {'label': 'Pavimentada', 'value': 'Pavimentada'},
     
          # Agrega más opciones según sea necesario
        ],
        value='Pavimentada'
    )]),    
    
    
    dbc.Row([html.Label("Sexo del Conductor"),    
    dcc.Dropdown(
        id='dropdown-sexo',
        options=[
            {'label': 'Hombre', 'value': 'Hombre'},
            {'label': 'Mujer', 'value': 'Mujer'},
          # Agrega más opciones según sea necesario
        ],
        value='Mujer'
    )]),
    
    dbc.Row([html.Label("Aliento alcoholico"),    
    dcc.Dropdown(
        id='dropdown-Aliento',
        options=[
            {'label': 'No', 'value': 'No'},
            {'label': 'Se ignora', 'value': 'Se ignora'},
          # Agrega más opciones según sea necesario
        ],
        value='Se ignora'
    )]),
    
    dbc.Row([html.Label("Cinturon de seguridad"),    
    dcc.Dropdown(
        id='dropdown-cinturon_seguridad',
        options=[
            {'label': 'Si', 'value': 'Si'},
            {'label': 'Se ignora', 'value': 'Se ignora'},
          # Agrega más opciones según sea necesario
        ],
        value='Se ignora'
    )]),

    dbc.Row([html.Label("Clasificación lugar"),    
    dcc.Dropdown(
        id='dropdown-cinturon_seguridad',
        options=[
            {'label': 'Ciudad Grande', 'value': 'Ciudad Grande'},
            {'label': 'Ciudad', 'value': 'Ciudad'},
             {'label': 'Municipio', 'value': 'Municipio'},
          # Agrega más opciones según sea necesario
        ],
        value='Municipio'
    )]),
    
    dbc.Row([html.Label('Escriba la edad de conductor:'),
    dcc.Input(id='input-edad_conductor', type='number', value=0)
    ]),
    
      
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
   html.Button('Predecir', id='predict-button'),
   
   html.A('Descargar CSV', id='download-link', download='archivo_prueba.csv', href='', target='_blank')
   
])



# Callback para la actualización de la salida
@callback(
    [Output('prediction-output', 'children'),
     Output('download-link', 'href')],
    [Input('predict-button', 'n_clicks')],
    [   Input('date-picker', 'date'),
        Input('time-picker', 'value'),
        Input('input-Id_municipio', 'value'),
        Input('input-Id_estado', 'value'),
        Input('dropdown-zona_urbana', 'value'),
        Input('dropdown-zona_suburbana', 'value'),
        Input('dropdown-tipo_accidente', 'value'),
        Input('input-automoviles', 'value'),
        Input('input-camionetas', 'value'),
        Input('input-Microbuses', 'value'),
        Input('input-camiones', 'value'),
        Input('input-ominibuses', 'value'),
        Input('input-tranvias', 'value'),
        Input('input-camionetas_carga', 'value'),
        Input('input-camiones_de_carga', 'value'),
        Input('input-tractores', 'value'),
        Input('input-ferrocarril', 'value'),
        Input('input-motocicleta', 'value'),
        Input('input-bicicleta', 'value'),
        Input('input-otros_vehiculos', 'value'),
        Input('dropdown-causa_accidente', 'value'),
        Input('dropdown-superficie_rodamiento', 'value'),
        Input('dropdown-sexo', 'value'),
        Input('dropdown-Aliento', 'value'),
        Input('dropdown-cinturon_seguridad', 'value'),
        Input('input-edad_conductor', 'value')
    ]
)
def update_output(n_clicks, selected_date, selected_time, id_municipio, id_estado, zona_urbana, 
                  zona_suburbana, tipo_accidente, automoviles, camionetas, Microbuses, camiones, 
                  omnibuses, tranvias, camionetas_carga, camiones_de_carga, tractores, ferrocarril, 
                  motocicleta, bicicleta, otros_vehiculos, causa_accidente, superficie_rodamiento, sexo, aliento, 
                  cinturon_seguridad, edad_conductor):
    
    #Consolidado de respuestas
    # if selected_date:
    #     mes =  dt.strptime(selected_date, '%Y-%m-%d').month
    #     hour = dt.strptime(selected_time, '%H:%M:%S').hour
    #     day = dt.strptime(selected_date, '%Y-%m-%d').day
    #     dia_sem = dt.strptime(selected_date, '%Y-%m-%d').strftime('%A')
    dias_semana = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miercoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sabado',
    'Sunday': 'Domingo'
    }    
    
    fecha_hora_obj = dt.fromisoformat(selected_date)
    month = fecha_hora_obj.month
    dia = fecha_hora_obj.day
    dia_sem = fecha_hora_obj.strftime('%A')
    dia_en_espanol = dias_semana[dia_sem]
    hora, minutos = selected_time.split(":")
    hora = int(hora)
    list_respuestas = ["Municipal",
        id_estado,
        id_municipio,  
        2021,
        month,
        #dt.strptime(selected_date, '%m/%d/%Y').month,
        hora,
        #dt.strptime(selected_time, '%H:%M:%S').hour,
        0,
        dia,
        #selected_date,
        dia_en_espanol,
        #selected_date,        
        #dt.strptime(selected_date, '%Y-%m-%d').day,
        #dt.strptime(selected_date, '%Y-%m-%d').strftime('%A'),
        zona_urbana,
        zona_suburbana,
        tipo_accidente,
        automoviles, 
        camionetas, 
        Microbuses,
        camiones,
        omnibuses,
        tranvias, 
        camionetas_carga,
        camiones_de_carga, 
        tractores, 
        ferrocarril,
        motocicleta, 
        bicicleta,
        otros_vehiculos,
        causa_accidente,
        superficie_rodamiento,
        sexo, 
        aliento,
        cinturon_seguridad, 
        edad_conductor,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        "NA",
        "NA"
        ]
    Lista_col = ['COBERTURA',
    'ID_ENTIDAD',
    'ID_MUNICIPIO',
    'ANIO',
    'MES',
    'ID_HORA',
    'ID_MINUTO',
    'ID_DIA',
    'DIASEMANA',
    'URBANA',
    'SUBURBANA',
    'TIPACCID',
    'AUTOMOVIL',
    'CAMPASAJ',
    'MICROBUS',
    'PASCAMION',
    'OMNIBUS',
    'TRANVIA',
    'CAMIONETA',
    'CAMION',
    'TRACTOR',
    'FERROCARRI',
    'MOTOCICLET',
    'BICICLETA',
    'OTROVEHIC',
    'CAUSAACCI',
    'CAPAROD',
    'SEXO',
    'ALIENTO',
    'CINTURON',
    'ID_EDAD',
    'CONDMUERTO',
    'CONDHERIDO',
    'PASAMUERTO',
    'PASAHERIDO',
    'PEATMUERTO',
    'PEATHERIDO',
    'CICLMUERTO',
    'CICLHERIDO',
    'OTROMUERTO',
    'OTROHERIDO',
    'NEMUERTO',
    'NEHERIDO',
    'CLASACC',
    'ESTATUS']
    
    df_respuestas = pd.DataFrame(np.column_stack(list_respuestas),columns=Lista_col) 

    clean_data = limpiar_datos(df_respuestas)
    #clean_data = clean_data.reshape(1, -1)

    with open('pages/GBC.pkl', 'rb') as file:
        modelo = pickle.load(file)

    resultado_predict = modelo.predict_proba(clean_data)[:, 1] * 100 

    print("resultado")   
    
    if n_clicks is None:
        raise PreventUpdate
    
    # Crear un DataFrame de ejemplo con la palabra "prueba"

    df_download = pd.DataFrame(clean_data)

    # Guardar el DataFrame en un archivo CSV en memoria
    csv_data = df_download.to_csv(index=False, encoding='utf-8-sig')

    # Convertir el archivo CSV en formato base64 para la descarga
    csv_base64 = base64.b64encode(csv_data.encode()).decode('utf-8')

    # Crear el enlace de descarga
    download_link = f'data:text/csv;base64,{csv_base64}'
    # dataframe_texto = str(df_respuestas)
    
    # Lógica de predicción (puedes cambiar esto según tu implementación real)
    
    #resultado_prediccion = 27.75 +10 # Esto debe ser tu resultado de la predicción
    
    return f"Resultado de la predicción: {float(floatresultado_predict):.2f}%" , download_link 

