# DesktopApp/controllers/user_controller.py (COMPLETO E CORRIGIDO - COM DEBUG)

from typing import TYPE_CHECKING, Tuple, List, Dict, Any
from DesktopApp.services.user_service import UserService 
from DesktopApp.services.rbac_service import RBACService 
from DesktopApp.models.entities.user import User 

if TYPE_CHECKING:
    from DesktopApp.views.login_window import LoginWindow
    from DesktopApp.views.main_window import MainWindow
    from DesktopApp.services.rbac_service import MenuStructure

class UserController:
    """
    Controlador responsável por manipular requisições do usuário,
    interagir com a camada de Serviço e coordenar a exibição das Views.
    """
    def __init__(self, user_service: UserService, rbac_service: RBACService):
        self.user_service = user_service
        self.rbac_service = rbac_service

    def handle_register_request(self, username: str, password: str, full_name: str):
        try:
            user = self.user_service.create_new_user(username, password, full_name)
            print(f"Controller: Usuário {user.username} criado com sucesso.")
            return user
                
        except ValueError as e:
            print(f"Controller: Erro no cadastro: {e}")
            raise e

        except Exception as e:
            print(f"Controller: Erro inesperado no cadastro: {e}")
            raise Exception("Erro ao salvar usuário. Tente novamente.")

    def handle_login(self, username: str, password: str) -> Tuple[User, List[Dict[str, Any]]]:
        """
        Processa a requisição de login.
        Retorna (User, accessible_menus) se for bem-sucedido.
        Levanta exceção em caso de falha.
        """
        
        # ==========================================================
        # 🚨 CONSOLE DEBUG (Dra. Elara) - INCLUSO NO ARQUIVO COMPLETO
        # ==========================================================
        print("\n[DEBUG - USER CONTROLLER]")
        print(f" -> Recebido Usuário: {username}")
        print(f" -> Recebido Senha (HINT): {password[0]}***{password[-1]}")
        print(f" -> Chamando Service: {self.user_service.__class__.__name__}")
        # AQUI VAMOS VERIFICAR SE O REPOSITÓRIO CARREGADO TEM O MÉTODO CORRETO
        repo_has_correct_method = hasattr(self.user_service.repo, 'get_by_username')
        print(f" -> Checando se repo tem 'get_by_username': {repo_has_correct_method}")
        # ==========================================================

        try:
            # CHAMA O SERVICE
            user = self.user_service.authenticate_user(username, password)

            if user:
                print(f"Controller: Login bem-sucedido para o usuário: {user.username}")
                # Obter a lista de menus permitidos
                accessible_menus = self.rbac_service.get_accessible_menu_routes(user)
                
                return user, accessible_menus
            else:
                # O Service deve retornar None se a autenticação falhar
                raise ValueError("Nome de usuário ou senha inválidos.")

        except ValueError as e:
            # Re-lança para ser capturada pela LoginWindow
            raise e

        except Exception as e:
            # Erros de sistema
            print(f"Controller: Erro inesperado durante o login: {e}")
            raise Exception("Erro fatal no sistema ao tentar login.")