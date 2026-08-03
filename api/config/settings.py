from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_PORT: int

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    MODEL_VERSION: str
    class Config:
        env_file = ".env"

settings=Settings()