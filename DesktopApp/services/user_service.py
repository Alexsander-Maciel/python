# DesktopApp/services/user_service.py

from typing import Optional
# Requer: pip install passlib
from passlib.context import CryptContext 
from DesktopApp.repositories.user_repository import UserRepository 
from DesktopApp.models.entities.user import User

# ====================================================================
# CONFIGURAÇÃO DE CRIPTOGRAFIA DE SENHA
# ====================================================================

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto plano corresponde ao hash."""
    if not isinstance(hashed_password, str):
        hashed_password = str(hashed_password)
        
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Cria o hash da senha."""
    return pwd_context.hash(password)

# ====================================================================
# CLASSE DE SERVIÇO
# ====================================================================

class UserService:
    """
    Camada de Lógica de Negócio para gerenciar Usuários.
    """
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_new_user(self, username: str, password: str, full_name: str) -> User:
        """
        Cria um novo usuário, hasheia a senha e o salva no repositório.
        """
        if self.repo.get_by_username(username):
            raise ValueError(f"O nome de usuário '{username}' já existe.")

        hashed_password = get_password_hash(password)
        
        new_user = User(
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            is_active=True
        )

        return self.repo.add(new_user)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Autentica um usuário, comparando o hash da senha.
        """
        # 1. Buscar o usuário pelo nome de usuário
        # ESTA LINHA FOI A CAUSA DO ERRO E ESTÁ CORRIGIDA PARA get_by_username
        user = self.repo.get_by_username(username)
        
        if not user or not user.is_active:
            return None

        # 2. Verificar o hash da senha
        if not verify_password(password, user.hashed_password):
            return None

        # 3. Sucesso na autenticação
        return user