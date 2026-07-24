from fastapi import FastAPI
from api.schemas import Imovel
from api.services.predict import predict
from fastapi import HTTPException


app = FastAPI(
    title="API de Predição de Imóveis",
    version="1.0.0",
    description="API utilizada para servir modelos de Machine Learning"
)


@app.get("/")
def home():
    return {
        "mensagem": "API Funcionando",
        "status": "online"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/info")
def info():
    return {
        "modelo": "Predição de imóveis",
        "versao": "1.0",
        "framework": "FastAPI"


    }


@app.get("/autor")
def autor():
    return {
        "autor": "Sam Souza"
    }


@app.get("/empresa")
def empresa():
    return {
        "empresa":"Imobiliária X"
    }



@app.post("/predict")
def prediction(imovel:Imovel):
    return predict(imovel)
    '''
    try:
        return predict(imovel)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro ao realizar previsão"
        )'''