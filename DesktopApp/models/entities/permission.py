# DesktopApp/models/entities/permission.py

from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from DesktopApp.models.database import Base

# Importa as entidades necessárias para as FKs
from DesktopApp.models.entities.user import User
from DesktopApp.models.entities.group import Group
from DesktopApp.models.entities.menu import Menu


class Permission(Base):
    """
    Entidade de Permissão (Role-Based Access Control - RBAC).
    Define qual Grupo (ou Usuário) tem acesso a qual Menu/Funcionalidade.
    """
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, index=True)

    # --- Permissão Base ---
    
    # 1. Qual Menu/Funcionalidade está sendo controlada
    menu_id = Column(Integer, ForeignKey('menu.id'), nullable=False)
    menu = relationship("Menu")

    # 2. A Quem a permissão se aplica (Apenas UM dos dois campos deve ser preenchido)
    
    # Aplica-se a um Grupo (Permissão mais comum)
    group_id = Column(Integer, ForeignKey('group.id'), nullable=True) 
    group = relationship("Group")
    
    # Aplica-se a um Usuário individual (Permissão de exceção)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True) 
    user = relationship("User", foreign_keys=[user_id])
    
    # --- Tipos de Acesso (Exemplos de Nível de Permissão) ---
    can_read = Column(Boolean, default=False, nullable=False)   # Ver a View/Menu
    can_write = Column(Boolean, default=False, nullable=False)  # Criar/Editar
    can_delete = Column(Boolean, default=False, nullable=False) # Deleção física/lógica
    
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Garante que um Grupo/Usuário tenha apenas uma permissão por Menu
    __table_args__ = (
        UniqueConstraint('menu_id', 'group_id', name='_menu_group_uc'),
        UniqueConstraint('menu_id', 'user_id', name='_menu_user_uc'),
    )

    def __repr__(self):
        target = f"Group ID: {self.group_id}" if self.group_id else f"User ID: {self.user_id}"
        return f"<Permission(Menu ID: {self.menu_id}, Target: {target}, Read: {self.can_read})>"

# FIM DO ARQUIVO