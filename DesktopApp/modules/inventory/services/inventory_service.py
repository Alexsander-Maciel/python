# DesktopApp/modules/inventory/services/inventory_service.py

from typing import List, Optional
from DesktopApp.models.entities.product import Product
from DesktopApp.modules.inventory.repositories.inventory_repository import InventoryRepository

class InventoryService:
    """
    Camada de Lógica de Negócio para o gerenciamento de Produtos.
    Garante que as regras de negócio sejam aplicadas antes da persistência.
    """
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    def create_product(self, name: str, description: str, price: float, stock_quantity: int) -> Product:
        """
        Cria um novo produto após validar as regras de negócio.
        """
        # 1. Regra de Negócio: O preço não pode ser negativo
        if price < 0:
            raise ValueError("O preço do produto não pode ser negativo.")

        # 2. Regra de Negócio: O nome do produto deve ser único (verificação simples)
        # Note: Esta verificação é mais eficiente se for feita no Repository com uma query.
        # No entanto, a lógica está aqui para fins de demonstração do Service.
        # Por enquanto, confiamos na restrição UNIQUE do DB para o nome.

        # 3. Cria a entidade e salva
        new_product = Product(
            name=name,
            description=description,
            price=price,
            stock_quantity=stock_quantity
        )
        return self.repo.add(new_product)

    def get_all_products(self) -> List[Product]:
        """Retorna todos os produtos ativos do inventário."""
        return self.repo.get_all()

    def update_product_stock(self, product_id: int, quantity_change: int) -> Product:
        """
        Atualiza o estoque de um produto.
        """
        product = self.repo.get_by_id(product_id)
        
        if not product:
            raise ValueError(f"Produto com ID {product_id} não encontrado.")

        new_stock = product.stock_quantity + quantity_change
        
        # 4. Regra de Negócio: O estoque não pode ficar negativo
        if new_stock < 0:
            raise ValueError("A operação resultaria em estoque negativo.")

        product.stock_quantity = new_stock
        
        # O Repository apenas commita, já que o objeto já está na sessão
        return self.repo.update(product)

    # Note: Mais métodos (delete, get_by_name, etc.) seriam adicionados aqui.