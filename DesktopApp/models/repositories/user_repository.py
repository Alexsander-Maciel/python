from typing import Optional
from sqlalchemy.orm import Session
# CORREÇÃO 1: Módulo IRMÃO (no mesmo diretório repositories/)
from .base_repository import BaseRepository 
# CORREÇÃO 2: Módulo VIZINHO (volta para models/, desce para entities/)
from ..entities.user import User

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

    # Nota da Dra. Elara: Métodos como add, get_by_id, delete, 
    # já estão disponíveis por herança do BaseRepository!