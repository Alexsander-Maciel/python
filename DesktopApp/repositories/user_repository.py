# DesktopApp/repositories/user_repository.py

from typing import Optional
from sqlalchemy.orm import Session
# CORREÇÃO CRÍTICA: Importação ABSOLUTA para resolver ModuleNotFoundError
from DesktopApp.models.entities.user import User 
from .base_repository import BaseRepository 
# Nota: O BaseRepository deve estar no mesmo diretório ou ter um caminho de importação definido.


class UserRepository(BaseRepository[User]):
    """
    Repositório específico para a entidade User. 
    Contém métodos específicos que não estão no BaseRepository.
    """
    
    def __init__(self, session: Session):
        # Chama o construtor do BaseRepository, passando a sessão e a classe User
        super().__init__(session, User)

    def get_by_username(self, username: str) -> Optional[User]:
        """Busca um usuário pelo seu nome de usuário único."""
        return self.session.query(User).filter(User.username == username).first()