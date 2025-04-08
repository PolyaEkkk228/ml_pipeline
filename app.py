from fastapi import FastAPI, File, UploadFile
import pandas as pd
import joblib
from io import BytesIO

app = FastAPI(title="Laptop Price Predictor")

model_path = "/content/drive/MyDrive/ml_pipeline/laptop_price_model.pkl"
model = joblib.load(model_path)

@app.get("/")
def root():
    return {"message": "Добро пожаловать в API предсказания цены ноутбуков!"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """
    Маршрут для получения предсказаний.
    Принимает CSV-файл и возвращает предсказания модели.
    """
    try:
        content = await file.read()
        df = pd.read_csv(BytesIO(content))

        predictions = model.predict(df)

        return {"predictions": predictions.tolist()}
    
    except Exception as e:
        return {"error": str(e)}