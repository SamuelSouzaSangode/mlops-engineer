from api.ml.validation import validar_imovel
from api.ml.model import modelo

class InferencePipeline:
    def predict(self, imovel):
        validar_imovel(imovel)

        entrada = [[
                    imovel.area,
                    imovel.quartos,
                    imovel.banheiros,
                    imovel.garagem
        ]]
        preco = modelo.predict(entrada)[0]
        return preco

