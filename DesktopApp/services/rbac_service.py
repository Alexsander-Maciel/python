# DesktopApp/services/rbac_service.py

from typing import List, Dict, Any, Optional
from DesktopApp.models.entities.user import User
from DesktopApp.models.entities.menu import Menu
from DesktopApp.repositories.menu_repository import MenuRepository

# NOVO: Vamos definir uma estrutura para o menu retornado
MenuStructure = List[Dict[str, Any]]

class RBACService:
    """
    Service de Controle de Acesso Baseado em Papéis (RBAC).
    Determina quais menus e funcionalidades o usuário logado pode acessar.
    """
    def __init__(self, menu_repo: MenuRepository): # Receberá mais repos no futuro (Group/Permission)
        self.menu_repo = menu_repo

    def get_accessible_menu_routes(self, user: User) -> MenuStructure:
        """
        Retorna a estrutura completa de menus que o usuário TEM PERMISSÃO para ver.
        """
        # 1. Obter todos os menus ativos do banco de dados
        # Assume que o MenuRepository tem o método get_all_active_menus
        all_menus: List[Menu] = self.menu_repo.get_all_active_menus()
        
        # 2. Lógica Futura de Permissão (Placeholder de Segurança)
        is_admin = (user.username == "admin") # Simplificacao temporaria

        accessible_menus: List[Menu] = []
        
        if is_admin:
            accessible_menus = all_menus
        else:
            # Lógica REAL: Filtrar 'all_menus' contra as permissões do usuário/grupos
            pass

        # 3. Converter a lista de objetos Menu em uma estrutura hierárquica
        menu_structure: MenuStructure = []
        
        for menu in accessible_menus:
            # Por enquanto, apenas menus de primeiro nível
            if menu.parent_id is None:
                # É CRÍTICO que as chaves sejam 'route' e 'name' para a MainWindow funcionar
                menu_structure.append({
                    "name": menu.name,
                    "route": menu.route_name, # CHAVE 'route'
                    "icon": menu.icon,
                    "id": menu.id,
                    "children": [] # Lógica para submenus viria aqui
                })
                
        print(f"RBAC Service: {len(menu_structure)} rotas de menu permitidas para {user.username}.")
        
        # ==========================================================
        # 🚨 CONSOLE DEBUG (Dra. Elara) - Mostra a Estrutura
        # ==========================================================
        print(f" -> Estrutura RBAC retornada: {menu_structure}")
        # ==========================================================
        
        return menu_structure