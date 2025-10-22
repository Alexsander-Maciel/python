# DesktopApp/app.py

import sys
from PyQt5.QtWidgets import QApplication

# ------------------------------------------------------------------
# IMPORTS DO PACOTE
# ------------------------------------------------------------------

from DesktopApp.models.database import init_db, SessionLocal
from DesktopApp.models.repositories.user_repository import UserRepository

from DesktopApp.controllers.services.user_service import UserService
from DesktopApp.controllers.user_controller import UserController

from DesktopApp.views.login_window import LoginWindow 
from DesktopApp.views.main_window import MainWindow

# ------------------------------------------------------------------
# VARIÁVEIS GLOBAIS PARA INJEÇÃO DE DEPENDÊNCIA
# ------------------------------------------------------------------

user_controller: UserController | None = None
login_window: LoginWindow | None = None
main_window: MainWindow | None = None

# ------------------------------------------------------------------
# FUNÇÃO DE CONFIGURAÇÃO (INJEÇÃO DE DEPENDÊNCIA)
# ------------------------------------------------------------------

def setup_dependencies():
    """
    Configura todas as dependências do sistema.
    """
    global user_controller, login_window, main_window
    
    print("Dra. Elara: Inicializando a Injeção de Dependência...")

    # Cria a sessão de banco de dados
    db_session = SessionLocal() 

    # --- Configuração das camadas ---
    user_repo = UserRepository(db_session)
    user_service = UserService(user_repo)
    user_controller = UserController(user_service)

    # Criação e vinculação das Views
    login_window = LoginWindow(user_controller)
    main_window = MainWindow(user_controller)

    user_controller.set_views(login_window, main_window)

    print("Dra. Elara: Arquitetura pronta. Iniciando a aplicação desktop...")

# ------------------------------------------------------------------
# FUNÇÃO PRINCIPAL DE INICIALIZAÇÃO
# ------------------------------------------------------------------

def main():
    """
    Ponto de entrada principal da aplicação.
    """
    app = QApplication(sys.argv)

    # 1. Inicializa o banco de dados
    try:
        init_db() 
        print(" Tabelas de banco de dados criadas/verificadas.")
    except Exception as e:
        print(f"ERRO CRÍTICO ao inicializar o banco de dados: {e}")
        sys.exit(1)


    # 2. Executa a Injeção de Dependência
    setup_dependencies()

    # O bloco de criação automática de usuário continua DESATIVADO

    # 3. Exibe a janela de Login e inicia o loop
    if login_window:
        login_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()