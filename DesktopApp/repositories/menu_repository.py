# DesktopApp/models/repositories/menu_repository.py

from typing import List, Optional
from sqlalchemy.orm import Session
from DesktopApp.models.entities.menu import Menu

class MenuRepository:
    """
    Repositório para operações de CRUD e leitura de Menus.
    """
    def __init__(self, session: Session):
        self.session = session

    def get_all_active_menus(self) -> List[Menu]:
        """
        Retorna todos os menus que estão ativos e não deletados logicamente.
        Ordena pela coluna 'order' para a exibição no UI.
        """
        return (
            self.session.query(Menu)
            .filter(Menu.is_active == True, Menu.is_deleted == False)
            .order_by(Menu.order)
            .all()
        )

    def get_menu_by_route(self, route_name: str) -> Optional[Menu]:
        """
        Busca um menu pelo seu nome interno de rota.
        """
        return self.session.query(Menu).filter(Menu.route_name == route_name).first()
        
    # Adicionar, Update, Delete Lógico, etc., seriam implementados aqui.

# FIM DO ARQUIVO