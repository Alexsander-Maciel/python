# DesktopApp/views/login_window.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QWidget
from PyQt5.QtCore import Qt
from typing import TYPE_CHECKING, List, Dict, Any

if TYPE_CHECKING:
    from DesktopApp.controllers.user_controller import UserController
    from DesktopApp.views.main_window import MainWindow
    from DesktopApp.models.entities.user import User

class LoginWindow(QDialog):
    """
    Janela modal para login de usuário.
    """
    def __init__(self, user_controller: 'UserController', main_window: 'MainWindow', parent: QWidget = None):
        super().__init__(parent)
        self.user_controller = user_controller
        self.main_window = main_window # Referência à MainWindow
        self.setWindowTitle("Login do Sistema")
        self.setFixedSize(350, 200)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Campo Usuário
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("Usuário:"))
        self.username_input = QLineEdit()
        self.username_input.setText("admin")
        user_layout.addWidget(self.username_input)
        layout.addLayout(user_layout)

        # Campo Senha
        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("Senha:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setText("123")
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        # Botão Login
        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self._handle_login)
        self.username_input.returnPressed.connect(self._handle_login)
        self.password_input.returnPressed.connect(self._handle_login)
        layout.addWidget(self.login_button)

    def _handle_login(self):
        """
        Tenta autenticar o usuário e, em caso de sucesso, abre a janela principal.
        """
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Aviso", "Por favor, preencha todos os campos.")
            return

        try:
            # 1. Chamar o Controller para autenticar e obter menus
            user, accessible_menus = self.user_controller.handle_login(username, password)
            
            # 2. Configurar a Janela Principal com os dados do usuário (Método Corrigido)
            self.main_window.update_ui_after_login(user, accessible_menus)
            
            # 3. Exibir a Janela Principal e fechar a de login
            self.main_window.show()
            self.accept() 

        except ValueError as e:
            QMessageBox.warning(self, "Erro de Login", str(e))
            self.password_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Erro Crítico", f"Erro fatal no sistema: {e}")
            print(f"ERRO FATAL NO LOGIN: {e}")