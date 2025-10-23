# DesktopApp/models/entities/product.py

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from DesktopApp.models.database import Base

class Product(Base):
    """
    Entidade (Tabela) para o Gerenciamento de Produtos.
    Define a estrutura da tabela 'product'.
    """
    __tablename__ = "product"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False) # Float é usado para simplicidade; Decimal seria mais preciso financeiramente.
    stock_quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, stock={self.stock_quantity})>"

# FIM DO ARQUIVO