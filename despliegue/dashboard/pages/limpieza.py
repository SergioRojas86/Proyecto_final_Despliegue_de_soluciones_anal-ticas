from sklearn.model_selection import train_test_split
import pandas as pd

def crear_calidad(_df):
    completitud = []
    for i in list(_df.columns):
        vacios = _df[(_df[i]=="")|(_df[i].isna())]
        count_vacios = vacios[i].count()
        medida = round((1-(count_vacios/len(_df)))*100)
        completitud.append([i,medida])

    calidad_df = pd.DataFrame(completitud, columns = ['Columna','Completitud de Col(%)'])
    unicidad=[]
    distintivo=[]
    type_col = []
    Moda= []
    for j in list(_df.columns):
        unico = len(_df[_df[j].duplicated()==False])
        temp_df = _df[_df[j].duplicated()==True]
        distinto = len(temp_df[j].unique())
        unicidad.append(unico-distinto)
        distintivo.append(distinto)
        type_col.append(_df[j].dtypes)

    calidad_df['# Unicos']=unicidad
    calidad_df['# Distintos']=distintivo
    calidad_df['Tipo de Columna']=type_col

    return calidad_df

def limpiar_datos(df_initial_m):
    df_initial_m = df_initial_m.drop(['ID_ENTIDAD','ANIO','ID_MINUTO','NEMUERTO','NEHERIDO','COBERTURA'],axis=1)


    df_initial_m = df_initial_m.drop([i for i in list(df_initial_m.columns) if "MUERTO" in i],axis=1)
    df_initial_m = df_initial_m.drop([i for i in list(df_initial_m.columns) if "HERIDO" in i],axis=1)
    df_initial_m = df_initial_m[df_initial_m['SEXO']!='Certificado cero']
    df_initial_m.CLASACC = df_initial_m.CLASACC.replace({'Sólo daños':'No fatal'})
    df_initial_m.CLASACC = df_initial_m.CLASACC.replace({'fatal':1,'No fatal':0,'Fatal':1})


    df_initial_mcopy = df_initial_m.copy()
    #Transformación de variables dummies
    desc_cat = crear_calidad(df_initial_mcopy)

    #Todas las variables categoricas las convertimos en variables dummies y las adjuntamos en una lista
    todas_dummies = []
    for i in list(desc_cat.columns):
        x = pd.get_dummies(desc_cat[i])
        column_index = []
        for j in list(x.columns):
            column_index.append((i,j))
        column_tuple = list(column_index)
        y = pd.DataFrame(x.values,index=x.index,columns=column_tuple)
        todas_dummies.append(y)
    
    df_initial_dummies = pd.concat([i for i in todas_dummies], axis=1)

    desc_con = crear_calidad(df_initial_m)
    desc_con = desc_con[desc_con['Tipo de Columna']=='int64']
    df_initial_con = df_initial_m[desc_con.Columna.unique()]

    #Unimos las columnas dummies a las columnas numericas
    df_initial_final = df_initial_dummies.join(df_initial_con,how="inner")

    # Separar las variables predictoras de la variable de respuesta
    XTotal = df_initial_final.to_numpy()
    

    return XTotal