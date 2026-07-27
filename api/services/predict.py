from api.schemas import Imovel

def predict(imovel: Imovel):
    preco = (
        imovel.area * 5000 +
        imovel.quartos * 30000 +
        imovel.banheiros * 15000 +
        imovel.garagem * 10000

    )
    return preco