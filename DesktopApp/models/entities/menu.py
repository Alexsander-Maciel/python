# DesktopApp/models/entities/menu.py (CORRIGIDO: Removida a coluna 'description')

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from DesktopApp.models.database import Base

from DesktopApp.models.entities.user import User

class Menu(Base):
    """
    Entidade para o Controle de Menus, Rotas e Estrutura Hierárquica.
    """
    __tablename__ = "menu"
    
    # --- Campos Base ---
    id = Column(Integer, primary_key=True, index=True)
    
    # Nome do menu
    name = Column(String(100), unique=True, nullable=False)
    
    # Rota/Nome interno do módulo ou View
    route_name = Column(String(100), nullable=False) 
    
    # Ícone a ser exibido
    icon = Column(String(50)) 
    
    # Ordem de exibição
    order = Column(Integer, default=0) 
    
    # --- Estrutura Hierárquica (Submenus) ---
    parent_id = Column(Integer, ForeignKey('menu.id', ondelete='SET NULL'), nullable=True) 
    parent = relationship("Menu", remote_side=[id], backref="children")
    
    # --- Rastreabilidade e Auditoria ---
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Chave Estrangeira para o Usuário que criou/alterou
    created_by_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    updated_by_id = Column(Integer, ForeignKey('user.id'), nullable=True)

    created_by = relationship(User, foreign_keys=[created_by_id], backref="menus_created")
    updated_by = relationship(User, foreign_keys=[updated_by_id], backref="menus_updated")
    
    # --- Controle de Estado ---
    is_active = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f"<Menu(name='{self.name}', route='{self.route_name}', parent_id={self.parent_id})>"

# FIM DO ARQUIVO