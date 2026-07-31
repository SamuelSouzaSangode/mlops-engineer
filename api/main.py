from fastapi import FastAPI

from fastapi import Depends
from sqlalchemy.orm import Session

from api.schemas import Imovel
#from api.services.predict import predict
from fastapi import HTTPException
from api.database.session import SessionLocal
from api.database.models import Previsao
from api.database.repositories.prediction_service import PredictionService
from api.database.dependencies import get_db

from api.database.connection import engine
from api.database.models import Base


app = FastAPI(
    title="API de Predição de Imóveis",
    version="1.0.0",
    description="API utilizada para servir modelos de Machine Learning"
)

#Pegue todas as tabelas descritas no metadata e crie-as usando a conexão engine
Base.metadata.create_all(bind=engine)

#service = PredictionService()


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
def predict(imovel:Imovel, db: Session=Depends(get_db)):
    service=PredictionService()
    return service.predict(db, imovel)




'''
@app.post("/predict")
def predict(imovel:Imovel):
    #Prevendo o valor com os dados enviados pelo client
    preco = predict(imovel)

    #Abrinco sessão
    db = SessionLocal()
    try:
        #Criando o objeto python para ser enviado para o banco
        previsao = Previsao(
            area=imovel.area,
            quartos=imovel.quartos,
            banheiros=imovel.banheiros,
            garagem=imovel.garagem,
            preco=preco
        )

        db.add(previsao)
        db.commit()
        db.refresh(previsao)
        return {
            "id": previsao.id,
            "preco": preco
        }

    except Exception:  
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Erro ao realizar previsão"
        )      
    finally:
        db.close()
'''


'''
def prediction(imovel:Imovel):
    return predict(imovel)





    try:
        return predict(imovel)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro ao realizar previsão"
        )'''