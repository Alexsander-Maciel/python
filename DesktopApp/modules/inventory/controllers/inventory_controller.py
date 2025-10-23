# DesktopApp/modules/inventory/controllers/inventory_controller.py (CÓDIGO COMPLETO FINAL)

from typing import TYPE_CHECKING, Dict, Any, List

if TYPE_CHECKING:
    from DesktopApp.modules.inventory.services.inventory_service import InventoryService
    from DesktopApp.modules.inventory.views.inventory_view import InventoryView
    from DesktopApp.models.entities.product import Product

class InventoryController:
    """
    Controlador para o Módulo de Inventário.
    Gerencia a lógica de negócios e a interação entre a View e o Service.
    """
    def __init__(self, service: 'InventoryService'):
        self.service = service
        self.view: 'InventoryView' = None
        # GARANTIA: NENHUM CÓDIGO DE TESTE AUTOMÁTICO DEVE EXISTIR AQUI!
        # Se você encontrar a linha de teste (Ex: self.service.create_product(...)), REMOVA-A!

    def set_view(self, view: 'InventoryView'):
        self.view = view

    def handle_load_products(self):
        """
        Carrega todos os produtos e atualiza a View.
        """
        try:
            products: List['Product'] = self.service.get_all_products()
            if self.view:
                self.view.display_products(products)
        except Exception as e:
            print(f"Controller Inventário: Erro ao carregar produtos: {e}")
            if self.view:
                self.view.show_error_message("Falha ao carregar lista de produtos.")


    def handle_create_product(self, data: Dict[str, Any]):
        """
        Recebe dados do formulário e cria um novo produto.
        """
        try:
            new_product = self.service.create_product(data)
            print(f"Controller Inventário: Produto '{new_product.name}' criado com sucesso.")
            
            # Recarrega a lista após a criação bem-sucedida
            self.handle_load_products() 
            
        except ValueError as e:
            raise e # Propaga erros de validação/negócio
        
        except Exception as e:
            # Captura e re-lança erros de sistema
            print(f"Controller Inventário: Erro inesperado ao criar produto: {e}")
            raise Exception("Erro fatal no sistema ao salvar o produto.")