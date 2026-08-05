from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

#Agora temos uma api funcionando apenas para testes.

#Testando o root
def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"mensagem": "API Funcionando",
    "status": "online"}

'''
#Testando predict com dados corretos
def test_predict_corretos():
    dados = {
        'area': 120,
        'quartos': 3,
        'banheiros': 2,
        'garagem': 2
            }
    
    response = client.post('/predict', json=dados)
    resultado = response.json()

    assert response.status_code == 200
    assert "preco_previsto" in resultado
    '''
'''
#Testando com dados faltando sem o "garagem"
def test_predict_semgaragem():
    dados = {
        'area': 120,
        'quartos': 3,
        'banheiros': 2,
            }
    response = client.post('/predict', json=dados)
    resultado = response.json()

    assert response.status_code == 400 or response.status_code == 422

#Testando com dados inválidos -120
def test_predict_invalido():
    dados = {
        'area': -120,
        'quartos': 3,
        'banheiros': 2,
        'garagem': 2
            }
    response = client.post('/predict', json=dados)
    assert response.status_code == 400 or response.status_code == 422'''