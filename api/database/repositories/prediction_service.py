#Finalização do salvamento dos bancos de dados
from api.database.repositories.prediction_repository import PredictionRepository ###
#Vai salvar o objeto python com os dados na tabela
from api.database.models import Previsao
#Modelo fazendo previsão
from api.services.predict import predict

from pathlib import Path
import pandas as pd
import joblib

class PredictionService:
    def __init__(self):
        #Parte de salvamento do banco e etc
        self.repository = PredictionRepository()
        BASE_DIR = Path(__file__).resolve().parents[3]
        MODEL_PATH = BASE_DIR / "modelos" / "modelo.pkl"

        self.modelo_valor_casas = joblib.load(MODEL_PATH)


    def predict(self, db, imovel):
        dados = pd.DataFrame(
            {
                'area': [imovel.area],
                'quartos': [imovel.quartos],
                'banheiros': [imovel.banheiros],
                'garagem': [imovel.garagem]
            }
        )

        preco = float(self.modelo_valor_casas.predict(dados)[0])

        #Salvando a previsão na tabela do banco de dados
        previsao = Previsao(
            area=imovel.area,
            quartos=imovel.quartos,
            banheiros=imovel.banheiros,
            garagem=imovel.garagem,
            preco=preco
        )

        #Fazendo os commits, salvamentos e refreshes
        previsao = self.repository.create(db, previsao)

        #Retorna a previsão em JSON
        return {
            "id": previsao.id,
            "preco_previsto": previsao.preco
        }

