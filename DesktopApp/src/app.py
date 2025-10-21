# app.py

import sys
import os

# ----------------------------------------------------
# 1. Configuração de Paths para Importação
# ----------------------------------------------------
# Obtém o caminho do diretório atual (onde app.py está: .../DesktopApp/src/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Adiciona o diretório 'src' ao sys.path para que importações como 'models.database' funcionem
sys.path.append(current_dir)

# ----------------------------------------------------
# 2. Importações dos Módulos Essenciais (M e C)
# ----------------------------------------------------
from models.database import create_tables # Presume que esta função cria as tabelas
from controllers.auth_controller import AuthController 

# ----------------------------------------------------
# 3. Importação da Orquestração da View (V)
# ----------------------------------------------------
from views.login_window import DesktopApplication


def setup_database():
    """ 
    Função de setup inicial.
    1. Cria todas as tabelas no MySQL via SQLAlchemy.
    2. Garante a existência do usuário administrador inicial.
    """
    print("--- 1. Configurando Base de Dados ---")
    
    create_tables()
    
    auth_controller = AuthController()
    auth_controller.create_initial_admin("admin", "123456")
    
    print(">>> Tabelas criadas com sucesso no MySQL!")
    print("--- Configuração de BD Finalizada ---\n")


def run_application():
    """ Inicia o ciclo de vida da aplicação PyQt5. """
    print("--- 2. Iniciando Aplicação Desktop ---")
    
    app_runner = DesktopApplication()
    app_runner.run()


if __name__ == '__main__':
    setup_database() 
    run_application()
    print("\nSistema Desktop encerrado.")