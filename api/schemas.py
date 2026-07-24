from pydantic import BaseModel

class Imovel(BaseModel):
    area: float
    quartos: int
    banheiros: int
    garagem: int 