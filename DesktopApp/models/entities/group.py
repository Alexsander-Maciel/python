# DesktopApp/models/entities/group.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from DesktopApp.models.database import Base

# Tabela auxiliar para a relação N:N entre User e Group
# Um usuário pode pertencer a vários grupos.
from sqlalchemy import Table, ForeignKey
user_group_association = Table(
    'user_group_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('group_id', Integer, ForeignKey('group.id'))
)

class Group(Base):
    """
    Entidade para Grupos de Usuários (RBAC).
    Permite atribuir permissões a múltiplos usuários de forma eficiente.
    """
    __tablename__ = "group"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relação N:N para vincular usuários a este grupo
    users = relationship(
        "User",
        secondary=user_group_association,
        backref="groups"
    )

    def __repr__(self):
        return f"<Group(name='{self.name}')>"

# FIM DO ARQUIVO