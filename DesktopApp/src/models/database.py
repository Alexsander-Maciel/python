# models/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import DATABASE_URL

# 1. Cria o 'Engine' (motor de conexão)
# 'echo=True' mostra as queries SQL no console (útil para debug)
engine = create_engine(DATABASE_URL, echo=False)

# 2. Cria a 'Base' declarativa para definir as classes do Model
Base = declarative_base()

# 3. Cria o 'Session Maker' (fábrica de sessões)
Session = sessionmaker(bind=engine)

def get_session():
    """ Função utilitária para obter uma nova sessão de banco. """
    return Session()

def create_tables():
    """ Cria todas as tabelas definidas na Base no banco de dados. """
    Base.metadata.create_all(engine)
    print(">>> Tabelas criadas com sucesso no MySQL!")

# Executar a criação das tabelas (opcionalmente pode ser movido para app.py)
if __name__ == '__main__':
    create_tables()