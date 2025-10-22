from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy.orm import Session
# CORREÇÃO: Usa importação RELATIVA para subir um nível (de repositories/ para models/)
# e acessar o módulo database.py, que é vizinho da pasta repositories.
from ..database import Base  # <--- CORREÇÃO AQUI

# Define um tipo genérico (T) que será a nossa entidade (ex: User, Group)
T = TypeVar('T', bound=Base)

class BaseRepository(Generic[T]):
    """
    Repositório base genérico para operações CRUD comuns.
    Isso centraliza a lógica de acesso à sessão do SQLAlchemy.
    """
    
    def __init__(self, session: Session, model: Type[T]):
        """
        Inicializa o repositório.
        
        Args:
            session: A sessão ativa do SQLAlchemy (injetada).
            model: A classe da entidade (ex: User) que este repositório gerencia.
        """
        self.session = session
        self.model = model

    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Busca uma entidade pelo ID."""
        return self.session.query(self.model).filter(self.model.id == entity_id).first()

    def get_all(self) -> List[T]:
        """Retorna todas as entidades."""
        return self.session.query(self.model).all()

    def add(self, entity: T) -> T:
        """Adiciona uma nova entidade e a persiste no banco de dados."""
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, entity: T) -> T:
        """Atualiza uma entidade existente."""
        self.session.merge(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, entity: T) -> None:
        """Deleta uma entidade."""
        self.session.delete(entity)
        self.session.commit()