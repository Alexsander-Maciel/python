from sqlalchemy import Column, Integer, String, Boolean, DateTime
from DesktopApp.models.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    
    # CORREÇÃO CRÍTICA: Garanta que o String seja grande o suficiente para o hash
    # O sha256_crypt usa cerca de 60-65 caracteres. 255 é seguro.
    hashed_password = Column(String(255), nullable=False) 
    
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        """Representação de objeto útil para debug."""
        return f"<User(id={self.id}, username='{self.username}', is_active={self.is_active})>"