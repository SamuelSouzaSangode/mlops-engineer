from sqlalchemy import create_engine
#Conectando ao banco de dados
DATABASE_URL = (
    "postgresql://sam:123456@postgres:5432/mlops"
)
#Criando a engine
engine = create_engine(
    DATABASE_URL,
    echo=True
)