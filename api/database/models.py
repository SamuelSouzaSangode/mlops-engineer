from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String


from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column



class Base(DeclarativeBase):
    pass



class Previsao(Base):
    __tablename__ = "previsao"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    versao: Mapped[str] = mapped_column(String(20), nullable=True)
    area: Mapped[float] = mapped_column(Float)
    quartos: Mapped[int] = mapped_column(Integer)
    banheiros: Mapped[int] = mapped_column(Integer)
    garagem: Mapped[int] = mapped_column(Integer)
    preco: Mapped[float] = mapped_column(Float)
    horario: Mapped[str] = mapped_column(String(20), nullable=True)
