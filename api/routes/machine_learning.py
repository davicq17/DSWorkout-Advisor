#importaciones necesarias para uso de Machine learning
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

##predecir Ejercicio
@app.route('/predictWorkout',methods=['POST'])
def predictWorkout():
    data = request.get_json()
    Equipment=data['equipment']
    BodyPart=data['bodypart']
    Type=data['type']
    Level=data['level']
    file_path = 'api/megaGymDataset.csv'
    data = pd.read_csv(file_path)

    # Imputar valores faltantes
    data.fillna({'Rating':data['Rating'].mean()}, inplace=True)
    data.fillna({'RatingDesc':'No Description'}, inplace=True)

    # Seleccionar características y la variable objetivo
    features = ['Type', 'BodyPart', 'Equipment', 'Level']
    X = data[features]
    y = data['Rating']

    # Codificación de variables categóricas
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, features)
        ])

    # Dividir el conjunto de datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Definir el modelo Gradient Boosting Regressor
    model = GradientBoostingRegressor(random_state=42)

    # Crear el pipeline
    clf = Pipeline(steps=[('preprocessor', preprocessor),
                        ('regressor', model)])

    # Entrenar el modelo
    clf.fit(X_train, y_train)

    # Hacer predicciones
    y_pred = clf.predict(X_test)

    # Evaluar el modelo
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f'RMSE: {rmse}')

    # Ejemplo de predicción con nuevos datos
    new_data = pd.DataFrame({
        'Type': [Type],
        'BodyPart': [BodyPart],
        'Equipment': [Equipment],
        'Level': [Level]
    })

    # Predecir el rating para los nuevos datos
    new_pred = clf.predict(new_data)
    print(new_pred[0])
    return jsonify({'Rating': new_pred[0]})

   ####Filtro de ejercicios con rating####
@app.route('/ejercicioFiltro/<Rating>', methods=['GET'])
def ejercicioFiltro(Rating):
    try:
        rating=float(Rating)
        min=rating-1
        max=rating+1
        print(min,max)
        cur=mysql.connection.cursor()
        cur.execute("SELECT w.id_workout,w.nombre,w.tipo,w.rating FROM workout w where w.rating BETWEEN %s and %s",(min,max,))
        rv=cur.fetchall()
        cur.close()
        content={}
        payload=[]
        for result in rv:
            content={'id':result[0],
                     'nombre':result[1],
                     'tipo':result[2],
                     'rating':result[3]}
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        return jsonify({"error":str(e)})
