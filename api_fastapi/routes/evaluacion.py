from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from api_fastapi.db import get_conn

router = APIRouter(prefix="/Evalucion", tags=["Evaluacion"])

#PREDICCION DE EJERCICIOS CON MSCHINE LEARNING 
class WorkoutInput(BaseModel):
    equipment: str
    bodypart: str
    type: str
    level: str

@router.post("/predictWorkout")
def predict_worjout(data:WorkoutInput):
    # SE LEE EL DATA SET
    file_path = "api_fastapi/megaGymDataset.csv"
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="El archivo megaGymDataset.csv no existe")

    # Imputar valores faltantes
    df.fillna({'Rating': df['Rating'].mean()}, inplace=True)
    df.fillna({'RatingDesc': 'No Description'}, inplace=True)

    # Seleccionar caracteristicas y variablees objetivo
    features = ['Type', 'BodyPart', 'Equipment', 'Level']
    X = df[features]
    y = df['Rating']

    # codificacion de variables de categoria
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, features)
        ])

    # divider el conjunto de datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Definir el modelo Gradient Boosting Regresso
    model = GradientBoostingRegressor(random_state=42)
    
    # Crear el pipeline
    clf = Pipeline(steps=[('preprocessor', preprocessor),('regressor', model)])

    # Entrenar el modelo
    clf.fit(X_train, y_train)

    # ====== (REAGREGAMOS ESTAS LÍNEAS) =========
    # Hacer predicciones
    y_pred = clf.predict(X_test)

    # Evaluar el modelo
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f'RMSE: {rmse}')

    # Predicción con datos nuevos
    new_data = pd.DataFrame({
        'Type': [data.type],
        'BodyPart': [data.bodypart],
        'Equipment': [data.equipment],
        'Level': [data.level]
    })
    #predice el raiting para los nuevos datos
    prediction = clf.predict(new_data)[0]
    print(prediction)

    return {
        "Rating": float(prediction)
    }
