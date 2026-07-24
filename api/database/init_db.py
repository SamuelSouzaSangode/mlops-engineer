from api.database.connection import engine
from api.database.models import Base

Base.metadata.create_all(bind=engine)