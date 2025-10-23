# controllers/main_controller.py

from models.user import User

class MainController:
    """
    Controller central de orquestração do sistema.
    Gerencia o usuário logado e a navegação da aplicação principal.
    """
    
    def __init__(self, logged_user: User):
        # Armazena o objeto User logado (com seus grupos e permissões)
        self.user = logged_user
        print(f"MainController inicializado para o usuário: {self.user.username}")

    def check_access(self, required_permission_name):
        """
        Verifica se o usuário logado tem a permissão para acessar um recurso/módulo.
        """
        if self.user.has_permission(required_permission_name):
            return True
        else:
            # Em um sistema real, isso registraria o evento e negaria o acesso.
            print(f"Acesso negado: Usuário '{self.user.username}' não tem a permissão '{required_permission_name}'.")
            return False

    # Exemplo de uma ação que exige permissão
    def load_user_management_data(self):
        """
        Carrega dados do módulo de Gerenciamento de Usuários.
        Requer a permissão 'admin_access'.
        """
        if self.check_access('admin_access'):
            # Lógica para buscar dados de todos os usuários no Model/DB.
            # (Implementaremos isso em um Controller de Dados mais tarde, por enquanto é um mock)
            return [
                {"username": "admin", "status": "Ativo", "grupo": "Administrador"},
                {"username": "fulano", "status": "Inativo", "grupo": "Funcionário"}
            ]
        
        return [] # Retorna lista vazia se não tiver permissão