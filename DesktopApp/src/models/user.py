# models/user.py

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base
from passlib.hash import pbkdf2_sha256 as pwd_context # Para hash de senha

# ----------------------------------------------------
# Tabelas de Associação (Many-to-Many)
# ----------------------------------------------------

# M-N: User <-> Group
user_group = Table('user_group', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('group.id'), primary_key=True)
)

# M-N: Group <-> Permission
group_permission = Table('group_permission', Base.metadata,
    Column('group_id', Integer, ForeignKey('group.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permission.id'), primary_key=True)
)

# ----------------------------------------------------
# Classes do Model (O Esquema)
# ----------------------------------------------------

class Permission(Base):
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False) # Ex: 'can_edit_product', 'can_view_reports'

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False) # Ex: 'Administrador', 'Gerente'
    
    # Relação M-N com Permission
    permissions = relationship("Permission", secondary=group_permission, backref="groups")

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Relação M-N com Group
    groups = relationship("Group", secondary=user_group, backref="users")

    # Métodos de Classe para Lógica de Negócio (Permissão e Senha)
    
    def set_password(self, password):
        """ Gera o hash da senha para armazenamento seguro. """
        self.password_hash = pwd_context.hash(password)

    def check_password(self, password):
        """ Verifica se a senha fornecida corresponde ao hash armazenado. """
        return pwd_context.verify(password, self.password_hash)

    def has_permission(self, permission_name):
        """ Verifica se o usuário tem a permissão através de seus grupos. """
        for group in self.groups:
            for permission in group.permissions:
                if permission.name == permission_name:
                    return True
        return False