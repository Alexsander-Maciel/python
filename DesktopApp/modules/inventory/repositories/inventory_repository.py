# DesktopApp/modules/inventory/repositories/inventory_repository.py

from typing import Optional, List
from sqlalchemy.orm import Session
# Importamos a entidade do nosso pacote models/entities
from DesktopApp.models.entities.product import Product 

class InventoryRepository:
    """
    Repositório para operações CRUD da entidade Product.
    """
    def __init__(self, session: Session):
        self.session = session

    def add(self, product: Product) -> Product:
        """Adiciona um novo produto e comita a transação."""
        try:
            self.session.add(product)
            self.session.commit()
            self.session.refresh(product)
            return product
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Busca um produto pelo ID."""
        return self.session.query(Product).filter(Product.id == product_id).first()
        
    def get_all(self) -> List[Product]:
        """Retorna todos os produtos ativos."""
        return self.session.query(Product).filter(Product.is_active == True).all()

    def update(self, product: Product) -> Product:
        """Atualiza um produto existente (já anexado à sessão) e comita."""
        try:
            self.session.commit()
            self.session.refresh(product)
            return product
        except Exception as e:
            self.session.rollback()
            raise e

# FIM DO ARQUIVO