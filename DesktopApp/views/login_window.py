# DesktopApp/views/login_window.py (Adaptado para mostrar mensagens)

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QMessageBox, QLabel
from PyQt5.QtCore import Qt

class LoginWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Sistema Desktop - Login")
        self.setFixedSize(300, 200)

        self._init_ui()

    def _init_ui(self):
        # Layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Campos de entrada
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nome de Usuário")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        # Botões
        self.login_button = QPushButton("Entrar")
        self.register_button = QPushButton("Criar Nova Conta")

        # Adiciona widgets ao layout
        layout.addWidget(QLabel("Login:"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        # Conexões
        self.login_button.clicked.connect(self._on_login_clicked)
        self.register_button.clicked.connect(self._on_register_clicked)
        
        # DEBUG: Preenche campos com valores de teste (opcional)
        self.username_input.setText("admin") 
        self.password_input.setText("123")

    def _on_login_clicked(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        # Chama o método do Controller
        self.controller.handle_login_request(username, password)
    
    def _on_register_clicked(self):
        # AQUI VAMOS INSERIR O USUÁRIO DE TESTE SEMPRE QUE O BOTÃO FOR CLICADO
        username = "admin"
        password = "123" 
        full_name = "Administrador Local"
        
        try:
            self.controller.handle_register_request(username, password, full_name)
        
        except ValueError as e:
            # Erro de regra de negócio (ex: usuário já existe)
            self.show_error_message(f"Falha no Cadastro: {e}")
        
        except Exception as e:
            # Erro inesperado (ex: falha na conexão DB/hash)
            self.show_error_message("Erro no sistema ao cadastrar. Verifique o console.")
            
    # --- MÉTODOS PARA O CONTROLLER COMUNICAR COM A VIEW ---

    def show_error_message(self, message: str):
        """Exibe uma mensagem de erro na View."""
        QMessageBox.critical(self, "Erro de Autenticação", message)
        
    def show_success_message(self, message: str):
        """Exibe uma mensagem de sucesso na View."""
        QMessageBox.information(self, "Sucesso", message)
        # Limpa os campos após o sucesso para incentivar o login
        self.username_input.clear()
        self.password_input.clear()

# FIM DO ARQUIVO