from sklearn.model_selection import train_test_split
import pandas as pd

def limpiar_datos(df_initial_m):
    df_initial_m = df_initial_m.drop(['ID_ENTIDAD','ANIO','ID_MINUTO','NEMUERTO','NEHERIDO','COBERTURA','ESTATUS','id','id_estado','id_municipio','Estado','Municipio',
                                    'total','Hombres','Mujeres','ID_Mun'],axis=1)


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

    df_initial_final = df_initial_final.drop(['ID_MUNICIPIO','Cve_inegi'],axis=1)

    # Separar las variables predictoras de la variable de respuesta
    yTotal = df_initial_final.pop('CLASACC').to_numpy()
    XTotal = df_initial_final.to_numpy()

    return XTotal