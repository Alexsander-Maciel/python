# DesktopApp/controllers/user_controller.py

from typing import TYPE_CHECKING
from DesktopApp.controllers.services.user_service import UserService

# Evita dependências circulares com as Views usando type checking
if TYPE_CHECKING:
    from DesktopApp.views.login_window import LoginWindow
    from DesktopApp.views.main_window import MainWindow

class UserController:
    """
    Controlador responsável por manipular requisições do usuário,
    interagir com a camada de Serviço e coordenar a exibição das Views.
    """
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.login_window: 'LoginWindow' = None  # Inicializado por set_views
        self.main_window: 'MainWindow' = None    # Inicializado por set_views

    def set_views(self, login_window: 'LoginWindow', main_window: 'MainWindow'):
        """
        Define as referências das janelas para permitir a transição.
        """
        self.login_window = login_window
        self.main_window = main_window

    def handle_register_request(self, username: str, password: str, full_name: str):
        """
        Tenta registrar um novo usuário.
        """
        try:
            user = self.user_service.create_new_user(username, password, full_name)
            print(f"Controller: Usuário {user.username} criado com sucesso.")
            # A view (login_window) deve ser notificada para mostrar a mensagem
            if self.login_window:
                self.login_window.show_success_message(f"Usuário '{username}' criado. Faça login.")
                
        except ValueError as e:
            # Erro de usuário já existente ou regras de negócio
            print(f"Controller: Erro no cadastro: {e}")
            raise e # Levanta para a View tratar a mensagem

        except Exception as e:
            # Erro de DB/Commit/Hash
            print(f"Controller: Erro inesperado no cadastro: {e}")
            raise Exception("Erro ao salvar usuário. Tente novamente.")

    def handle_login_request(self, username: str, password: str):
        """
        Processa a requisição de login e transiciona as janelas em caso de sucesso.
        """
        try:
            user = self.user_service.authenticate_user(username, password)

            if user:
                # SUCESSO na autenticação
                print(f"Controller: Login bem-sucedido para o usuário: {username}")
                
                # 1. Exibe a janela principal (PRIORIDADE)
                if self.main_window:
                    self.main_window.set_welcome_message(user.full_name)
                    self.main_window.show()

                # 2. Fecha a janela de login
                if self.login_window:
                    self.login_window.close()
            else:
                # FALHA na autenticação
                print("Controller: Falha no login.")
                if self.login_window:
                    # Informa a View para mostrar a mensagem de erro
                    self.login_window.show_error_message("Nome de usuário ou senha inválidos.")

        except Exception as e:
            print(f"Controller: Erro inesperado durante o login: {e}")
            if self.login_window:
                self.login_window.show_error_message(f"Erro inesperado: {e}")