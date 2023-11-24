import pandas as pd

#def actualizar_diccionario(fila, diccionario):
#    for key, value in diccionario.items():
#        try:
#            if fila[key[0]] == key[1]:
#                diccionario[key] = 1
#        except:
#            pass
#    return diccionario

def actualizar_diccionario(fila, diccionario):
    for key, value in diccionario.items():
        if isinstance(key, tuple):  # Si la columna es una tupla
            if fila[key[0]] == key[1]:
                diccionario[key] = 1
        else:  # Si la columna es un string
            if isinstance(fila[key], int):
                diccionario[key] = fila[key]
            elif fila[key] == key:
                diccionario[key] = 1
    return diccionario

def limpiar_datos(df):

    df_poblacion = pd.read_excel('pages/inafed_bd_1679023638.xlsx', index_col=False)

    columnas_enteros = ['ID_ENTIDAD', 'ID_MUNICIPIO', 'ANIO', 'MES', 'ID_HORA', 'ID_MINUTO', 'ID_DIA',
                    'AUTOMOVIL', 'CAMPASAJ', 'MICROBUS', 'PASCAMION', 'OMNIBUS', 'TRANVIA', 'CAMIONETA',
                    'CAMION', 'TRACTOR', 'FERROCARRI', 'MOTOCICLET', 'BICICLETA', 'OTROVEHIC', 'ID_EDAD',
                    'CONDMUERTO', 'CONDHERIDO', 'PASAMUERTO', 'PASAHERIDO', 'PEATMUERTO', 'PEATHERIDO',
                    'CICLMUERTO', 'CICLHERIDO', 'OTROMUERTO', 'OTROHERIDO', 'NEMUERTO', 'NEHERIDO']

    # Convertir columnas a tipo int64
    df[columnas_enteros] = df[columnas_enteros].astype('int64')

    df['Cve_inegi'] = df['ID_ENTIDAD']*1000 + df.ID_MUNICIPIO

    df_2 = df.merge(df_poblacion, on='Cve_inegi', how='left')
    
    diccionario_columnas = {('DIASEMANA', 'Domingo'): 0, ('DIASEMANA', 'Jueves'): 0, ('DIASEMANA', 'Martes'): 0, 
                            ('DIASEMANA', 'Miercoles'): 0, ('DIASEMANA', 'Sabado'): 0, ('DIASEMANA', 'Viernes'): 0, 
                            ('DIASEMANA', 'lunes'): 0, ('URBANA', 'Accidente en intersección'): 0, ('URBANA', 'Accidente en no intersección'): 0, 
                            ('URBANA', 'Sin accidente en esta zona'): 0, ('SUBURBANA', 'Accidente en camino rural'): 0, 
                            ('SUBURBANA', 'Accidente en carretera estatal'): 0, ('SUBURBANA', 'Accidentes en otro camino'): 0, 
                            ('SUBURBANA', 'Sin accidente en esta zona'): 0, ('TIPACCID', 'Caída de pasajero'): 0, ('TIPACCID', 'Colisión con animal'): 0, 
                            ('TIPACCID', 'Colisión con ciclista'): 0, ('TIPACCID', 'Colisión con ferrocarril'): 0, 
                            ('TIPACCID', 'Colisión con motocicleta'): 0, ('TIPACCID', 'Colisión con objeto fijo'): 0, 
                            ('TIPACCID', 'Colisión con peatón (atropellamiento)'): 0, ('TIPACCID', 'Colisión con vehículo automotor'): 0, 
                            ('TIPACCID', 'Incendio'): 0, ('TIPACCID', 'Otro'): 0, ('TIPACCID', 'Salida del camino'): 0, ('TIPACCID', 'Volcadura'): 0, 
                            ('CAUSAACCI', 'Conductor'): 0, ('CAUSAACCI', 'Falla del vehículo'): 0, ('CAUSAACCI', 'Mala condición del camino'): 0, 
                            ('CAUSAACCI', 'Otra'): 0, ('CAUSAACCI', 'Peatón o pasajero'): 0, ('CAPAROD', 'No Pavimentada'): 0, 
                            ('CAPAROD', 'Pavimentada'): 0, ('SEXO', 'Hombre'): 0, ('SEXO', 'Mujer'): 0, ('SEXO', 'Se fugó'): 0,
                            ('ALIENTO', 'No'): 0, ('ALIENTO', 'Se ignora'): 0, ('ALIENTO', 'Sí'): 0, ('CINTURON', 'No'): 0, 
                            ('CINTURON', 'Se ignora'): 0, ('CINTURON', 'Sí'): 0, ('Clasificacion', 'Ciudad'): 0, 
                            ('Clasificacion', 'Ciudad Grande'): 0, ('Clasificacion', 'Municipio'): 0, ('Clasificacion', 'Municipio pequeño'): 0, 
                            'MES': 0, 'ID_HORA': 0, 'ID_DIA': 0, 'AUTOMOVIL': 0, 'CAMPASAJ': 0, 'MICROBUS': 0, 'PASCAMION': 0, 'OMNIBUS': 0, 
                            'TRANVIA': 0, 'CAMIONETA': 0, 'CAMION': 0, 'TRACTOR': 0, 'FERROCARRI': 0, 'MOTOCICLET': 0, 'BICICLETA': 0, 'OTROVEHIC': 0, 'ID_EDAD': 0}
    
    diccionario_actualizado = diccionario_columnas.copy()  # Crear una copia para no modificar el diccionario original
    df_2.apply(lambda fila: actualizar_diccionario(fila, diccionario_actualizado), axis=1)

    df_resultado = pd.DataFrame([diccionario_actualizado])

    # Obtener el array de valores
    array_resultado = df_resultado.to_numpy()

    # Imprimir el array de valores
    array_resultado

    return array_resultado