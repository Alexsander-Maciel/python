# views/login_window.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, 
    QLabel, QLineEdit, QPushButton, QMessageBox
)

# Importações Essenciais
from controllers.auth_controller import AuthController
from views.main_window import MainWindow # Importa a View Principal (Você deve ter este arquivo)

# --- CLASSE DA JANELA DE LOGIN (V) ---

class LoginWindow(QWidget):
    """
    View (V) de Login: Interface gráfica e delegação ao Controller.
    """

    def __init__(self, main_app_controller):
        super().__init__()
        
        self.main_app_controller = main_app_controller
        self.auth_controller = AuthController()

        self.setWindowTitle("Sistema Desktop - Login")
        self.setGeometry(300, 300, 350, 200)

        self.init_ui()

    def init_ui(self):
        """ Configuração visual. """
        
        layout = QVBoxLayout()

        # ... (Configuração dos campos e botão)
        layout.addWidget(QLabel("Usuário:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("admin")
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Senha:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("123456")
        layout.addWidget(self.password_input)
        
        self.password_input.returnPressed.connect(self.handle_login) 

        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self.handle_login) 
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def handle_login(self):
        """ 
        Método de Slot: Processa a tentativa de login.
        Protegido com try/except para garantir a estabilidade do PyQt.
        """
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos.")
            return
            
        try:
            logged_user = self.auth_controller.authenticate(username, password)

            if logged_user:
                QMessageBox.information(self, "Sucesso", f"Bem-vindo, {logged_user.username}!")
                
                self.hide() 
                
                # Abre a janela principal (que agora não deve mais falhar no Lazy Loading)
                self.main_app_controller.show_main_window(logged_user) 
            else:
                QMessageBox.critical(self, "Erro de Login", "Usuário ou senha inválidos.")
                self.password_input.clear()
                
        except Exception as e:
            # Esta captura evita o crash SIGABRT do PyQt.
            error_message = f"Ocorreu um erro inesperado durante o login: {e}"
            print(f"ERRO CRÍTICO NO LOGIN: {error_message}")
            QMessageBox.critical(self, "Erro Crítico", error_message)
            
            
# --- CLASSE ORQUESTRADORA ---

class DesktopApplication:
    """ 
    Gerencia o ciclo de vida e a transição entre janelas.
    """
    def __init__(self):
        self.qt_app = QApplication(sys.argv)
        self.login_window = None
        self.main_window = None

    def show_login(self):
        """ Exibe a janela de login. """
        self.login_window = LoginWindow(self)
        self.login_window.show()
        
    def show_main_window(self, user):
        """ Exibe a janela principal após o login. """
        # Certifique-se de que a classe MainWindow aceita o objeto 'user' totalmente carregado.
        self.main_window = MainWindow(user) 
        self.main_window.show()

    def run(self):
        """ Inicia o loop principal. """
        self.show_login()
        sys.exit(self.qt_app.exec_())