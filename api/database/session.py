from sqlalchemy.orm import sessionmaker
from api.database.connection import engine

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

'''
sesionmaker é uma fábrica de sessões ele não cria uma sessão imediatamente
ele cria um molde
Cada requisição da API utilizará uma sessão diferente

bind=engine -> Todas as sessões criadas por esta fábrica utilização esta conexção
Session -> Engine -> PostgreSQL
autoflush=False -> Imagine session.add(previsao), o objeto ainda não foi
enviado ao banco, o flush envia os comandos antes do commit,
ao usar autoflush=False você controla quando isso acontece, evita 
comportamentos inesperados no aprendizado
autocommit=False -> Sem o autocommit cada operação seria salva automaticamente 
isso é perigoso.

session.add(previsa)
session.commit()
session.rollback()
session.close()
Abrir Session

↓

Executar consultas

↓

Salvar alterações

↓

Commit

↓

Fechar Session

'''