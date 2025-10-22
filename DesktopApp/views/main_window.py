# DesktopApp/views/main_window.py

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QMenuBar, QAction, QStackedWidget
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Sistema Desktop - Painel Principal")
        self.setFixedSize(800, 600)

        self._init_ui()

    def _init_ui(self):
        # 1. Layout Principal e Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        # 2. Área de Mensagem de Boas-Vindas (Top-Bar)
        self.welcome_label = QLabel("Carregando...")
        self.welcome_label.setAlignment(Qt.AlignLeft)
        self.welcome_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")
        self.main_layout.addWidget(self.welcome_label)

        # 3. Área de Conteúdo Dinâmico (QStackedWidget)
        # O StackedWidget permite trocar telas inteiras (ex: Gerenciamento, Relatórios)
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # 4. Adicionar Conteúdo Inicial (Exemplo)
        self._create_dashboard_view()
        
        # 5. Configurar o Menu Superior
        self._create_menu_bar()

    def _create_menu_bar(self):
        menu_bar = QMenuBar()
        
        # Menu Principal (Ex: Cadastro, Relatórios)
        system_menu = menu_bar.addMenu("Sistema")
        
        # Opção de Logout
        logout_action = QAction("Sair/Logout", self)
        logout_action.triggered.connect(self._on_logout_triggered)
        system_menu.addAction(logout_action)
        
        # Adicione a barra de menu à janela
        self.setMenuBar(menu_bar)

    def _create_dashboard_view(self):
        """Cria e adiciona a tela inicial de Dashboard."""
        dashboard = QWidget()
        layout = QVBoxLayout(dashboard)
        
        info_label = QLabel("BEM-VINDO AO PAINEL DE CONTROLE.")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("font-size: 30px; color: #1E90FF;")
        layout.addWidget(info_label)
        
        # Adiciona a tela ao StackedWidget
        self.stacked_widget.addWidget(dashboard)
        self.stacked_widget.setCurrentWidget(dashboard)

    def _on_logout_triggered(self):
        """Manipulador de Logout: Chama o Controller para reabrir a janela de Login."""
        print("Controller: Logout solicitado.")
        # Em uma arquitetura limpa, o controller deve coordenar o logout
        # Ex: self.controller.handle_logout() 
        
        # Simplificando para o teste:
        self.close()
        # Nota: Você precisaria de um método no controller para reabrir o LoginWindow.
        # Ex: self.controller.show_login_after_logout()

    # --- MÉTODO REQUERIDO PELO CONTROLLER ---
    
    def set_welcome_message(self, user_full_name: str):
        """
        Define a mensagem de boas-vindas na tela principal.
        """
        self.welcome_label.setText(f"Usuário Autenticado: {user_full_name}")
        print(f"VIEW: Mensagem de boas-vindas definida.")