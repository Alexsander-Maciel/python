# DesktopApp/app.py

import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog
from PyQt5.QtCore import Qt # Import necessário para a correção de menu no macOS
from sqlalchemy.orm import Session
from DesktopApp.models.database import engine, Base, SessionLocal
# Imports de Entidades e Serviços para Seeding
from DesktopApp.models.entities.user import User
from DesktopApp.models.entities.menu import Menu
from DesktopApp.views.main_window import MainWindow
from DesktopApp.views.login_window import LoginWindow

# Importações das Camadas Core
from DesktopApp.controllers.user_controller import UserController
from DesktopApp.services.rbac_service import RBACService
from DesktopApp.repositories.user_repository import UserRepository
from DesktopApp.repositories.menu_repository import MenuRepository 
from DesktopApp.services.user_service import UserService, get_password_hash # get_password_hash para Seeding

# Importações dos módulos para Injeção de Dependência (DI)
from DesktopApp.modules.inventory.repositories.inventory_repository import InventoryRepository 
from DesktopApp.modules.inventory.services.inventory_service import InventoryService           
from DesktopApp.modules.inventory.controllers.inventory_controller import InventoryController 
from DesktopApp.modules.inventory.views.inventory_view import InventoryView 


# ====================================================================
# 1. SETUP DO BANCO DE DADOS E SEEDING
# ====================================================================

def seed_database(db_session: Session):
    """Garante que dados essenciais (Admin e Menu Básico) existam."""
    
    # 1. Seed do Usuário Admin
    if db_session.query(User).filter(User.username == "admin").count() == 0:
        print("Dra. Elara: Criando usuário 'admin' inicial...")
        admin_user = User(
            username="admin",
            full_name="Administrador do Sistema",
            hashed_password=get_password_hash("123"),
            is_active=True
        )
        db_session.add(admin_user)

    # 2. Seed do Menu de Módulo (Garante que o RBAC encontre a rota 'inventory')
    if db_session.query(Menu).filter(Menu.route_name == "inventory").count() == 0:
        print("Dra. Elara: Criando menu 'Inventory' inicial...")
        inventory_menu = Menu(
            name="Produtos & Estoque",
            route_name="inventory", # Nome da rota CRÍTICO para a DI
            parent_id=None,
            icon="inventory.png",
            order=1,
            is_active=True
        )
        db_session.add(inventory_menu)

    db_session.commit()
    print("Dra. Elara: Seeding de dados essenciais concluído/verificado.")


def init_db():
    """Cria todas as tabelas e garante os dados iniciais."""
    print("Dra. Elara: Tabelas de banco de dados criadas/verificadas.")
    Base.metadata.create_all(bind=engine)
    
    session = SessionLocal()
    try:
        seed_database(session)
    finally:
        session.close()

# ====================================================================
# 2. INJEÇÃO DE DEPENDÊNCIA (DI)
# ====================================================================

def _inject_inventory_module(db_session: Session):
    """
    Cria e injeta as dependências específicas do Módulo Inventory.
    """
    repo = InventoryRepository(db_session)
    service = InventoryService(repo)
    controller = InventoryController(service)
    view = InventoryView(controller)

    print(" -> Injeção DI concluída para o módulo: inventory")

    return {
        "controller": controller,
        "view": view,
        "route_name": "inventory" # CRÍTICO: Nome de rota que o RBAC/DB espera
    }


def setup_dependencies(db_session: Session):
    """
    Configura todas as dependências e módulos da aplicação.
    """
    print("Dra. Elara: Inicializando a Injeção de Dependência...")

    # 1. Camadas Centrais (Core)
    
    # Usuários
    user_repo = UserRepository(db_session)
    user_service = UserService(user_repo) 

    # RBAC (Menus)
    menu_repo = MenuRepository(db_session) 
    rbac_service = RBACService(menu_repo) # Injeta o MenuRepository

    # Controller
    user_controller = UserController(user_service, rbac_service) 

    # 2. Módulos Funcionais
    modules = []
    inventory_module_data = _inject_inventory_module(db_session)
    modules.append(inventory_module_data)

    return {
        "user_controller": user_controller,
        "modules": modules
    }

# ====================================================================
# 3. PONTO DE ENTRADA
# ====================================================================

def main():
    app = QApplication(sys.argv)
    
    # CORREÇÃO CRÍTICA PARA MACOS: Força o menu a ficar na janela
    app.setAttribute(Qt.AA_DontUseNativeMenuBar, True)
    
    init_db()
    
    try:
        db_session = SessionLocal()
        
        dependencies = setup_dependencies(db_session)
        user_controller = dependencies["user_controller"]
        modules = dependencies["modules"]

        print("Dra. Elara: Arquitetura pronta. Iniciando a aplicação desktop...")

        main_window = MainWindow(user_controller, modules)
        
        login_window = LoginWindow(user_controller, main_window)
        
        if login_window.exec_() == QDialog.Accepted:
            sys.exit(app.exec_())
        else:
            sys.exit(0)

    except Exception as e:
        error_message = f"Erro fatal durante a inicialização do aplicativo: {e}"
        print(f"ERRO FATAL: {error_message}")
        QMessageBox.critical(None, "Erro Crítico", error_message)
        sys.exit(1)
        
    finally:
        if 'db_session' in locals() and db_session:
            db_session.close()


if __name__ == "__main__":
    main()