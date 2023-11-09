import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import accuracy_score, precision_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier

import mlflow
import mlflow.sklearn

import warnings
warnings.filterwarnings("ignore")

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

# Leer el numero de registro de cada variable (si existen)
def leer_registro(archivo_registro):
    try:
        with open(archivo_registro, 'r') as file:
            numero = int(file.read())
    except FileNotFoundError:
        # Si el archivo no existe, inicializa el numero en 1 y crea el archivo
        numero = 0
        with open(archivo_registro, 'w') as file:
            file.write(str(numero))
    return numero

def modelos(models_group, _model=None, n_estimators=None, max_samples=None, learning_rate=None, max_features=None, max_depth=None, threshold=None):
   
    models = []
    # si se desea solo ejecutar un modelo
    if _model is None:
         models = models_group   
    elif isinstance(_model, list):
        for modelo in models_group:
            if modelo["name"] in _model:
                models.append(modelo)
    else:
        # Si _model no es una lista, buscar un solo modelo por su nombre
        for modelo in models_group:
            if modelo["name"] == _model:
                models.append(modelo)
        
    # Iterar a traves de los modelos
    for model_info in models:
        model_name_or = model_info["name"]

        # Aca se lleva un control de cuantos experimentos se han hecho para cada modelo
        # Incrementar el numero de registro para cada variable y guardarlo en su archivo respectivo
        # Definiendo las variables con el numero de experimento respectivo

        if model_name_or == 'Decision Tree':
            Decision_Tree_file = 'conteo_experimentos/registro_Decision_Tree.txt'
            numero_Decision_Tree = leer_registro(Decision_Tree_file)
            numero_Decision_Tree += 1
            exp_Decision_Tree = f'Experimento_{numero_Decision_Tree}'
            model_name = exp_Decision_Tree+' '+model_name_or

            with open(Decision_Tree_file, 'w') as file:
                file.write(str(numero_Decision_Tree))
        

        if model_name_or == 'Bagging':
            Bagging_file  = 'conteo_experimentos/registro_Bagging.txt'
            numero_Bagging = leer_registro(Bagging_file)
            numero_Bagging += 1
            exp_Bagging = f'Experimento_{numero_Bagging}'
            model_name = exp_Bagging+' '+model_name_or

            with open(Bagging_file, 'w') as file:
                file.write(str(numero_Bagging))
        

        if model_name_or == 'Random Forest':
            Random_Forest_file  = 'conteo_experimentos/registro_Random_Forest.txt'
            numero_Random_Forest = leer_registro(Random_Forest_file)
            numero_Random_Forest += 1
            exp_Random_Forest = f'Experimento_{numero_Random_Forest}'
            model_name = exp_Random_Forest+' '+model_name_or

            with open(Random_Forest_file, 'w') as file:
                file.write(str(numero_Random_Forest))


        if model_name_or == 'Gradient Boosting':
            Gradient_Boosting_file  = 'conteo_experimentos/registro_Gradient_Boosting.txt'
            numero_Gradient_Boosting = leer_registro(Gradient_Boosting_file)
            numero_Gradient_Boosting += 1
            exp_Gradient_Boosting = f'Experimento_{numero_Gradient_Boosting}'
            model_name = exp_Gradient_Boosting+' '+model_name_or

            with open(Gradient_Boosting_file, 'w') as file:
                file.write(str(numero_Gradient_Boosting))

        
        if model_name_or == 'XGBoost':
            XGBoost_file  = 'conteo_experimentos/registro_XGBoost.txt'
            numero_XGBoost = leer_registro(XGBoost_file)
            numero_XGBoost += 1
            exp_XGBoost = f'Experimento_{numero_XGBoost}'
            model_name = exp_XGBoost+' '+model_name_or

            with open(XGBoost_file, 'w') as file:
                file.write(str(numero_XGBoost))
        
        
        with mlflow.start_run(experiment_id=experiment, run_name=model_name):
            model = model_info["model"]
            run_id = mlflow.active_run().info.run_id
                
            #if n_estimators is not None and model_name in ("Bagging", "Random Forest","Gradient Boosting","XGBoost"):
            if model_name_or in ("Bagging", "Random Forest","Gradient Boosting","XGBoost"):
                if n_estimators is not None:
                    model.set_params(n_estimators=n_estimators)
                params = model.get_params()
                n_estimators_value = params['n_estimators']
                mlflow.log_param("n_estimators", n_estimators_value)
    
            #if max_samples is not None and model_name in ("Bagging", "Random Forest"):
            if model_name_or in ("Bagging", "Random Forest"):
                if max_samples is not None:
                    model.set_params(max_samples=max_samples)
                params = model.get_params()
                max_samples_value = params['max_samples']
                mlflow.log_param("max_samples", max_samples_value)
    
            #if learning_rate is not None and model_name in ("Gradient Boosting","XGBoost"):
            if model_name_or in ("Gradient Boosting","XGBoost"):
                if learning_rate is not None:
                    model.set_params(learning_rate=learning_rate)
                params = model.get_params()
                learning_rate_value = params['learning_rate']
                mlflow.log_param("learning_rate", learning_rate_value)
    
            #if max_features is not None and model_name in ("Decision Tree", "Bagging", "Random Forest","Gradient Boosting"):
            if model_name_or in ("Decision Tree", "Bagging", "Random Forest","Gradient Boosting"):
                if max_features is not None:
                    model.set_params(max_features=max_features)
                params = model.get_params()
                max_features_value = params['max_features']
                mlflow.log_param("max_features", max_features_value)
    
            #if max_depth is not None and model_name in ("Decision Tree", "Random Forest","Gradient Boosting","XGBoost"):
            if model_name_or in ("Decision Tree", "Random Forest","Gradient Boosting","XGBoost"):
                if max_depth is not None:
                    model.set_params(max_depth=max_depth)
                params = model.get_params()
                max_depth_value = params['max_depth']
                mlflow.log_param("max_depth", max_depth_value)
    
    
            # Entrenar el modelo
            model.fit(XTrain, yTrain)
    
            # Realizar predicciones
            if model_name_or == 'XGBoost':
                predictions_proba = model.predict_proba(XTest)
                if threshold is None:
                    predictions = model.predict(XTest)
                else:
                    predictions = (predictions_proba[:,1] >= threshold).astype(int)
                    mlflow.log_param("threshold", threshold)
            else:
                predictions_proba = model.predict_proba(XTest)[:,0]
                predictions = model.predict(XTest)
    
    
            # Calcular metricas
            if model_name_or == 'XGBoost':
                fpr, tpr, thresholds = metrics.roc_curve(yTest, predictions_proba[:,1], pos_label=1)
            else:
                fpr, tpr, thresholds = metrics.roc_curve(yTest, predictions_proba, pos_label=0)
    
            AUC = metrics.auc(fpr, tpr)
            Accuracy = accuracy_score(y_true=yTest, y_pred=predictions)
            precision = precision_score(y_true=yTest, y_pred=predictions)
    
            # Registrar parametros y metricas en MLflow
            mlflow.log_param("semilla", random_state)
            mlflow.log_param("Model Name", model_name)
            mlflow.log_metric("AUC", AUC)
            mlflow.log_metric("Accuracy", Accuracy)
            mlflow.log_metric("precision", precision)
    
            #Registra el modelo
            mlflow.sklearn.log_model(model, "model")
    
            print(f"Run ID de la ejecucion actual ({model_name}): {run_id}")
            print(f"{model_name} - AUC: {AUC}")
            print(f"{model_name} - Accuracy: {Accuracy}")
            print(f"{model_name} - precision: {precision}")
    
    mlflow.end_run(status='FINISHED')



if __name__ == "__main__":

    # Lectura de los datos
    df_initial = pd.read_csv('/home/ubuntu/proyecto_final_dsa/Sergio/data/atus_anual_2021.csv', index_col=False)
    df_poblacion = pd.read_excel('/home/ubuntu/proyecto_final_dsa/Sergio/data/inafed_bd_1679023638.xlsx', index_col=False)
    
    # Hacemos Join de las tablas de población y accidentes para clasificar por tipo de ciudad.
    df_initial['Cve_inegi'] = df_initial['ID_ENTIDAD']*1000 + df_initial.ID_MUNICIPIO
    
    df_initial_D = df_initial.copy()
    df_poblacion_D = df_poblacion.copy()
    
    # Reiniciar
    df_initial = df_initial_D
    
    df_poblacion = df_poblacion_D
    df_initial_m = df_initial.merge(df_poblacion, on='Cve_inegi', how='left')
    
    
    
    # Eliminamos variables que no ofrecen información relevante para el objeto de estudio
    # como ID_Entidad que es la codificación del instituto y Anio ya que la información
    # se conoce con antelación que es del año 2021. Dado que la variable objetivo del estudio
    # es 'CLASACC', que nos dirá si el accidente puede ser fatal o no, eliminaremos las
    # variables que contengan muertos o heridos, que conceptualmente, tienen una relación
    # fuerte con la variable de respuesta.
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
    
    # obtener las muestras
    XTrain, XTest, yTrain, yTest = train_test_split(XTotal, yTotal, test_size=0.33, random_state=0)
    
    # Definir una lista de modelos con sus respectivos parametros
    random_state = 123
    models_group = [
        {"name": "Decision Tree", "model": DecisionTreeClassifier(random_state=random_state)},
        {"name": "Bagging", "model": BaggingClassifier(random_state=random_state)},
        {"name": "Random Forest", "model": RandomForestClassifier(random_state=random_state)},
        {"name": "Gradient Boosting", "model": GradientBoostingClassifier(random_state=random_state)},
        {"name": "XGBoost", "model":XGBClassifier(random_state=random_state)}
    ]
    # Nombre del experimento
    experiment_name = "Atus-models"
    
    # Obtener el experimento por su nombre
    existing_experiment = mlflow.get_experiment_by_name(experiment_name)
    
    # Verifica si el experimento ya existe
    if existing_experiment is None:
        # Si no existe, crea el experimento
        experiment = mlflow.create_experiment(experiment_name)
    else:
        # Si ya existe, usa el experimento existente
        experiment = existing_experiment.experiment_id

    """
    # Parametros y modelos a los cuales aplican en parentesis se muestra si tienen algun valor por default
    #n_estimators = BaggingClassifier(10), RandomForestClassifier(100), GradientBoostingClassifier(100), XGBClassifier(100)
    #max_samples = BaggingClassifier(1.0), RandomForestClassifier
    #learning_rate = GradientBoostingClassifier(0.1), XGBClassifier
    #max_features = DecisionTreeClassifier, BaggingClassifier(1.0), RandomForestClassifier('Auto'), GradientBoostingClassifier
    #max_depth = DecisionTreeClassifier, RandomForestClassifier, GradientBoostingClassifier(3), XGBClassifier
    #threshold = XGBClassifier
    
    _model se utiliza si no se quieren ejecutar todos los modelos en un experimento puede ser una lista [] o un solo nombre.
    Estos son los valores a utilizar: Decision Tree, Bagging, Random Forest, Gradient Boosting, XGBoost
    si _model es None, se ejecutan todos los modelos del diccionario models_group

    """               
    #modelos(models_group, _model=None, n_estimators=None, max_samples=None, learning_rate=None, max_features=None, max_depth=None, threshold=None)
    #modelos(models_group, _model='Bagging', n_estimators=100, max_samples=None, learning_rate=None, max_features=None, max_depth=None, threshold=None)
    #modelos(models_group, _model='Gradient Boosting', n_estimators=None, max_samples=None, learning_rate=1.0, max_features=None, max_depth=1, threshold=None)
    modelos(models_group, _model='XGBoost', n_estimators=None, max_samples=None, learning_rate=None, max_features=None, max_depth=None, threshold=0.5)
