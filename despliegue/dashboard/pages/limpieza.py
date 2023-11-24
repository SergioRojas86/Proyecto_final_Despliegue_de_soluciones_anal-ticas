from sklearn.model_selection import train_test_split
import pandas as pd

def pareto_entry(_col,_df):
    cuenta = []
    unicos = []
    porcentaje = []
    for i in list(_df[_col].unique()):
        tempy = pd.DataFrame(_df[_col])
        cuenta.append(tempy[tempy[_col]==i].count()[0])
        unicos.append(i)
        porcentaje.append(round(tempy[tempy[_col]==i].count()[0]/len(_df),3)*100)

    pareto_df = pd.DataFrame(unicos, columns=[_col])
    pareto_df['Count'] = cuenta
    pareto_df['Percentage'] = porcentaje
    pareto_df = pareto_df.sort_values(by=['Count'], ascending=False)
    pareto_df['Cum_Percentage'] = round(100*(pareto_df['Count'].cumsum()/pareto_df['Count'].sum()),1)

    return pareto_df

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
        Moda.append(_df[j].mode()[0])

    calidad_df['# Unicos']=unicidad
    calidad_df['# Distintos']=distintivo
    calidad_df['Tipo de Columna']=type_col
    calidad_df['Moda']=Moda

    return calidad_df

def limpiar_datos(df_initial_m):
    #df_initial_m = df_initial_m.drop(['ID_ENTIDAD','ANIO','ID_MINUTO','NEMUERTO','NEHERIDO','COBERTURA','ESTATUS','id','id_estado','id_municipio','Estado','Municipio',
    #                                'total','Hombres','Mujeres','ID_Mun'],axis=1)

    df_initial_m = df_initial_m.drop(['ID_ENTIDAD','ANIO','ID_MINUTO','NEMUERTO','NEHERIDO','COBERTURA','ESTATUS'],axis=1)


    df_initial_m = df_initial_m.drop([i for i in list(df_initial_m.columns) if "MUERTO" in i],axis=1)
    df_initial_m = df_initial_m.drop([i for i in list(df_initial_m.columns) if "HERIDO" in i],axis=1)
    df_initial_m = df_initial_m[df_initial_m['SEXO']!='Certificado cero']
    df_initial_m.CLASACC = df_initial_m.CLASACC.replace({'Sólo daños':'No fatal'})
    df_initial_m.CLASACC = df_initial_m.CLASACC.replace({'fatal':1,'No fatal':0,'Fatal':1})


    df_initial_mcopy = df_initial_m.copy()

    #Transformación de variables dummies
    desc_cat = crear_calidad(df_initial_mcopy)
    desc_cat = desc_cat[desc_cat['Tipo de Columna']=='object']
    df_initial_cat = df_initial_m[desc_cat.Columna.unique()]

    #Todas las variables categoricas las convertimos en variables dummies y las adjuntamos en una lista
    todas_dummies = []
    for i in list(df_initial_cat.columns):
        x = pd.get_dummies(df_initial_cat[i])
        x = x[pareto_entry(i,df_initial_cat)[i].unique()]
        x = x.iloc[:,:-1]
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
    print('hmmm')

    return XTotal