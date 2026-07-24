from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql://sam:123456@postgres:5432/mlops"
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)