from sqlalchemy import create_engine
from api.config.settings import settings

#DATABASE_URL = "postgresql://sam:123456@postgres:5432/mlops"
#Conectando ao banco de dados
DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:5432/{settings.DB_NAME}"
)
#Criando a engine
engine = create_engine(
    DATABASE_URL,
    echo=True
)