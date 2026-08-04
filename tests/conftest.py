import pytest 
from api.schemas import Imovel
from api.database.repositories.prediction_service import PredictionService

'''
Quando usamos o @ o pytest entende que essa função serve para criar 
objetos que outros testes podem utilizar, já chama como se fosse uma
variável, não precisa declarar com o por exemplo a = função(), pode chamar
logo a funçao

'''

@pytest.fixture
def imovel():
    return Imovel(
        area=120,
        quartos=3,
        banheiros=2,
        garagem=2
    )

class FakePipeline:
    def predict(self, imovel):
        return [500000]

class FakeRepository:
    def create(self, db, previsao):
        previsao.id = 1
        return previsao


@pytest.fixture
def pipeline():
    return FakePipeline()

@pytest.fixture
def repository():
    return FakeRepository()

@pytest.fixture
def service(pipeline, repository):
    return PredictionService(pipeline=pipeline, repository=repository)


#Tudo que começa com "test" será testado, então posso escrever vários testes
def test_prediction_service(service, imovel):
    resultado = service.predict(db=None, imovel=imovel)

    assert resultado['id'] == 1
    assert resultado['preco_previsto'] == 500000