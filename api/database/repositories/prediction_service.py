#Finalização do salvamento dos bancos de dados
from api.database.repositories.prediction_repository import PredictionRepository ###
#Vai salvar o objeto python com os dados na tabela
from api.database.models import Previsao
#Modelo fazendo previsão
from api.services.predict import predict

class PredictionService:
    def __init__(self):
        #Parte de salvamento do banco e etc
        self.repository = PredictionRepository()

    def predict(self, db, imovel):
        preco = predict(imovel) #Vai prever o preço

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

