# DesktopApp/controllers/services/user_service.py

from typing import Optional
from passlib.context import CryptContext
from DesktopApp.models.repositories.user_repository import UserRepository
from DesktopApp.models.entities.user import User

# ====================================================================
# CONFIGURAÇÃO DE CRIPTOGRAFIA DE SENHA (Passlib - HASH SEGURO)
# ====================================================================

# REATIVAÇÃO: Usando sha256_crypt, um esquema seguro e estável.
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto plano corresponde ao hash."""
    # Garante que o hash é uma string, caso o DB o leia diferente (última correção)
    if not isinstance(hashed_password, str):
        hashed_password = str(hashed_password)
        
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Cria o hash da senha usando o esquema configurado."""
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

        # 1. Hashear a senha (AGORA COM SEGURANÇA)
        hashed_password = get_password_hash(password)
        
        # 2. Criar a entidade
        new_user = User(
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            is_active=True
        )

        # 3. Salvar no DB via repositório
        return self.repo.add(new_user)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Autentica um usuário verificando a senha e o estado de ativo.
        """
        # 1. Buscar o usuário pelo nome de usuário
        user = self.repo.get_by_username(username)
        
        if not user or not user.is_active:
            return None

        # 2. Verificar o hash da senha (AGORA COM SEGURANÇA)
        if not verify_password(password, user.hashed_password):
            return None

        # 3. Sucesso na autenticação
        return user