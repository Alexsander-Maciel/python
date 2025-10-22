# DesktopApp/models/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Iterator

# ------------------------------------------------------------------
# CONFIGURAÇÃO DO BANCO DE DADOS
# ------------------------------------------------------------------

# IMPORTANTE: Ajuste as credenciais e o nome do banco de dados (desktop_app_db)
# Se você está usando XAMPP com senha vazia (o que é comum no Mac/Linux),
# a senha deve ser omitida no string.
DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/desktop_app_db" 

# Cria o motor de banco de dados
engine = create_engine(DATABASE_URL)

# ------------------------------------------------------------------
# SESSÃO E BASE
# ------------------------------------------------------------------

# A CLASSE SessionLocal é a fábrica para criar novas sessões.
# Esta é a classe que o app.py precisa importar.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para o mapeamento declarativo (entidades)
Base = declarative_base()

# ------------------------------------------------------------------
# FUNÇÕES DE UTILIDADE
# ------------------------------------------------------------------

def init_db():
    """
    Cria todas as tabelas no banco de dados, se não existirem.
    """
    # Importa as entidades aqui para garantir que Base as conheça
    from DesktopApp.models.entities.user import User
    # from DesktopApp.models.entities.group import Group # Importe suas outras entidades aqui
    
    # IMPORTANTE: Recria o esquema se você teve erros de coluna.
    # Base.metadata.drop_all(bind=engine) # Descomente se precisar limpar TUDO
    Base.metadata.create_all(bind=engine)
    print("Dra. Elara: Tabelas de banco de dados criadas/verificadas.")


def get_db_session() -> Iterator[sessionmaker]:
    """
    Gerador de sessão de banco de dados (útil para injeção de dependência em outras funções).
    Note que esta função retorna um gerador, não a sessão em si.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FIM DO ARQUIVO