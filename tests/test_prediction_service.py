from api.database.repositories.prediction_service import PredictionService
from api.schemas import Imovel




class FakePipeline:
    def predict(self, imovel):
        return [500000.0]


class FakeRepository:
    def create(self, db, previsao):
        previsao.id = 1
        return previsao


def test_prediction_service():
    service = PredictionService(pipeline=FakePipeline(), repository=FakeRepository())
    #Passa os dados mokados para o prediction_service.py
    imovel = Imovel(
        area=120,
        quartos=3,
        banheiros=2,
        garagem=2
    )

    resultado = service.predict(db=None, imovel=imovel)

    print(resultado)

    assert resultado['id'] == 1
    assert resultado['preco_previsto'] == 500000.0
