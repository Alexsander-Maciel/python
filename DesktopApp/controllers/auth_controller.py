# controllers/auth_controller.py

from sqlalchemy.orm import joinedload 
# CORREÇÃO: Importando get_session do arquivo database.py
from models.database import get_session 
from models.user import User, Group # Presume que Group está definido em models.user

class AuthController:
    """
    Controller (C) para a lógica de autenticação.
    Lida com a interação entre a View de Login e o Model (User/DB).
    """

    def authenticate(self, username, password):
        """
        Tenta autenticar um usuário.
        Usa Eager Loading ANINHADO para carregar User, Groups e Permissions
        em uma única consulta, resolvendo todos os erros de Lazy Loading.
        """
        print(f"Tentando autenticar o usuário: {username}")
        
        try:
            with get_session() as session: 
                # Adicionamos o carregamento aninhado (nested joinedload)
                user = session.query(User).options(
                    # 1. Carrega os Groups do User (User.groups)
                    joinedload(User.groups).options(
                        # 2. Carrega as Permissions de CADA Group (Group.permissions)
                        joinedload(Group.permissions) 
                    )
                ).filter(
                    User.username == username
                ).first()

                if user and user.check_password(password):
                    print(f"Usuário {username} autenticado com sucesso.")
                    # O objeto 'user' está totalmente carregado e pronto para a View.
                    return user
                
                print(f"Falha na autenticação para o usuário: {username}")
                return None
                
        except Exception as e:
            print(f"Erro de banco de dados ou consulta: {e}")
            return None 

    def create_initial_admin(self, username, password):
        """ Cria o usuário admin inicial se não existir. """
        
        try:
            with get_session() as session:
                if session.query(User).filter_by(username=username).first() is None:
                    # 1. Cria o Grupo Admin se não existir
                    admin_group = session.query(Group).filter_by(name='Admin').first()
                    if not admin_group:
                        # Assumindo que Group tem um campo 'permissions' que é uma lista
                        admin_group = Group(name='Admin', permissions=['admin_access', 'user_management'])
                        session.add(admin_group)
                        session.commit()
                        print("Grupo Admin criado.")

                    # 2. Cria o Usuário
                    admin = User(username=username, is_admin=True)
                    admin.set_password(password)
                    admin.groups.append(admin_group)
                    
                    session.add(admin)
                    session.commit()
                    print(f"Usuário administrador inicial '{username}' criado.")
                else:
                    print(f"Usuário administrador '{username}' já existe.")
        except Exception as e:
            print(f"Erro ao configurar o usuário admin: {e}")