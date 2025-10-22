# DesktopApp/models/repositories/user_repository.py

from typing import Optional
from sqlalchemy.orm import Session
from DesktopApp.models.entities.user import User

class UserRepository:
    """
    Responsável pelas operações CRUD (Criação, Leitura, Atualização, Deleção)
    da entidade User no banco de dados.
    """
    def __init__(self, session: Session):
        self.session = session

    def add(self, user: User) -> User:
        """Adiciona um novo usuário e comita a transação."""
        try:
            self.session.add(user)
            self.session.commit() # ESSENCIAL: Comita a transação para salvar no DB
            self.session.refresh(user)
            return user
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_username(self, username: str) -> Optional[User]:
        """Busca um usuário pelo nome de usuário."""
        # Note: A sessão deve ser capaz de buscar sem ser um gerador.
        return self.session.query(User).filter(User.username == username).first()

    # Outras funções como get_all, update, delete podem ser adicionadas aqui.