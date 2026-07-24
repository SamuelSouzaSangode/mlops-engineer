from sqlalchemy import Float
from sqlalchemy import Integer


from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column



class Base(DeclarativeBase):
    pass



class Previsao(Base):


    __tablename__ = "previsoes"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )


    area: Mapped[float] = mapped_column(Float)


    quartos: Mapped[int] = mapped_column(Integer)


    banheiros: Mapped[int] = mapped_column(Integer)


    garagem: Mapped[int] = mapped_column(Integer)


    preco: Mapped[float] = mapped_column(Float)