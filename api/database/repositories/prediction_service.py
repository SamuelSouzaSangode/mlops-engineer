#Finalização do salvamento dos bancos de dados
from api.database.repositories.prediction_repository import PredictionRepository ###
#Vai salvar o objeto python com os dados na tabela
from api.database.models import Previsao
#Modelo fazendo previsão
from api.services.predict import predict
from api.config.settings import settings

from api.ml.model import modelo
from api.ml.validation import validar_imovel

from pathlib import Path
import pandas as pd
import joblib

class PredictionService:
    def __init__(self, pipeline=None, repository=None):
        '''
        Isso serve para fazer os teste, se for none, 
        vai usar o que importamos, 
        se não for none, vai usar o que passamos 
        ao chamar a classe
        '''
        self.modelo_valor_casas = pipeline or modelo
        self.repository = repository or PredictionRepository()
        #Parte de salvamento do banco e etc

        #Se for None, usa o modelo e predictionRepository()

    def predict(self, db, imovel):
        #Passando dados e df para passar para o modelo
        dados = pd.DataFrame(
            {
                'area': [imovel.area],
                'quartos': [imovel.quartos],
                'banheiros': [imovel.banheiros],
                'garagem': [imovel.garagem]
            }
        )
        #Regras de negócio
        validar_imovel(imovel)

        #Predição com o modelo
        preco = float(self.modelo_valor_casas.predict(dados)[0])

        #Salvando a previsão na tabela do banco de dados
        #Criando objeto python
        previsao = Previsao(
            area=imovel.area,
            quartos=imovel.quartos,
            banheiros=imovel.banheiros,
            garagem=imovel.garagem,
            preco=preco,
            versao=settings.MODEL_VERSION
        )
        
        #Fazendo os commits, salvamentos e refreshes
        previsao = self.repository.create(db, previsao)

        #Retorna a previsão em JSON
        return {
            "id": previsao.id,
            "preco_previsto": previsao.preco
        }



