def validar_imovel(imovel):
    if imovel.area <= 0:
        raise ValueError (
            "Área Inválida."
        )
    if imovel.quartos <= 0:
        raise ValueError (
            "Quartos Inválidos."
        )

    if imovel.banheiros < 0:
        raise ValueError (
            "Banheiros Inválidos."
        )

    if imovel.garagem < 0:
        raise ValueError (
            "Garagem Inválida."
        )