# views/main_window.py

from PyQt5.QtWidgets import (
    QMainWindow, QMdiArea, QAction, QMdiSubWindow, 
    QTextEdit, QWidget, QVBoxLayout, QLabel, 
    QToolBar, QMessageBox, QMenu 
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon 

class MainWindow(QMainWindow):
    """
    View Principal (V) no formato MDI (Multiple Document Interface).
    """
    
    count = 0 

    def __init__(self, user):
        super().__init__()
        
        self.user = user 
        
        self.setWindowTitle(f"Sistema Desktop MDI | Usuário: {user.username}")
        self.setGeometry(100, 100, 1000, 700) 
        
        # 1. Configuração do MDI (QMdiArea)
        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)
        self.mdi_area.subWindowActivated.connect(self.update_menu_status)
        
        # 2. Setup dos Componentes
        self.create_actions()
        # >>> MUDANÇA PRINCIPAL AQUI: Chamada da nova função
        self.setup_menu_structure() 
        self.create_tool_bar()
        self.create_status_bar()
        
        self.update_menu_status()
        self.open_dashboard_window() 
        
    # --- Componentes de Setup ---

    def create_actions(self):
        """ Cria as ações (QAction) que serão usadas nos menus e toolbar. """
        
        # Ações do Sistema
        self.exit_action = QAction(QIcon(), "&Sair", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.close)
        
        # Ações de Cadastro (Novo)
        self.new_action = QAction(QIcon(), "&Novo Cadastro", self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.triggered.connect(self.open_new_window)

        # Ações de Cadastro (Produtos - Exemplo de Sub-menu)
        self.products_action = QAction(QIcon(), "&Produtos", self)
        self.products_action.triggered.connect(lambda: self.open_generic_window("Cadastro de Produtos"))
        
        # Ações de Cadastro (Clientes - Exemplo de Sub-menu)
        self.clients_action = QAction(QIcon(), "&Clientes", self)
        self.clients_action.triggered.connect(lambda: self.open_generic_window("Cadastro de Clientes"))

        # Ações de Visualização (Exemplo de Menu de Relatórios)
        self.report_action = QAction(QIcon(), "&Relatório Geral", self)
        self.report_action.triggered.connect(lambda: self.open_generic_window("Relatório de Vendas"))

        # Ações de organização do MDI
        self.cascade_action = QAction(QIcon(), "&Cascata", self)
        self.cascade_action.triggered.connect(self.mdi_area.cascadeSubWindows)

        self.tile_action = QAction(QIcon(), "&Lado a Lado", self)
        self.tile_action.triggered.connect(self.mdi_area.tileSubWindows)

        # Ação de Ajuda
        self.about_action = QAction(QIcon(), "&Sobre", self)
        self.about_action.triggered.connect(self.show_about_dialog)
        
    def setup_menu_structure(self):
        """
        Define a estrutura hierárquica dos menus (Pai -> Filho).
        Esta função é o coração da flexibilidade do menu.
        """
        # A estrutura é uma lista de tuplas (Nome do Menu Pai, Lista de Ações/Sub-menus Filhos)
        menu_data = [
            ("&Cadastros", [
                self.new_action,
                None, # Adiciona um separador
                self.products_action,
                self.clients_action,
            ]),
            ("&Relatórios", [
                self.report_action
            ]),
            ("&Janela", [
                self.cascade_action,
                self.tile_action
            ]),
            ("&Sistema", [
                self.exit_action,
            ]),
            ("&Ajuda", [
                self.about_action
            ])
        ]
        
        self.create_menu_bar(menu_data)


    def create_menu_bar(self, menu_data):
        """ Configura a barra de menus principal com base nos dados fornecidos. """
        menu_bar = self.menuBar()
        
        for menu_title, items in menu_data:
            # 1. Cria o Menu Pai (Top-level)
            parent_menu = menu_bar.addMenu(menu_title)
            
            for item in items:
                # 2. Adiciona itens filhos (Ações ou Separadores)
                if item is None:
                    # Se o item for None, adiciona um separador
                    parent_menu.addSeparator()
                elif isinstance(item, QAction):
                    # Se for uma QAction, adiciona a ação diretamente
                    parent_menu.addAction(item)
                elif isinstance(item, tuple) and len(item) == 2:
                    # Se for uma tupla, assume que é um Sub-Menu (Pai-Filho)
                    sub_menu_title, sub_menu_items = item
                    sub_menu = QMenu(sub_menu_title, self)
                    parent_menu.addMenu(sub_menu)
                    
                    # Adiciona os itens do sub-menu recursivamente
                    for sub_item in sub_menu_items:
                        if sub_item is None:
                            sub_menu.addSeparator()
                        elif isinstance(sub_item, QAction):
                            sub_menu.addAction(sub_item)
                        # NOTA: Não implementamos sub-menus de 3º nível para simplicidade.

    def create_tool_bar(self):
        """ Configura a barra de ferramentas. """
        toolbar = QToolBar("Barra Principal")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        toolbar.addAction(self.new_action)
        toolbar.addAction(self.products_action)
        toolbar.addSeparator()
        toolbar.addAction(self.cascade_action)
        toolbar.addAction(self.tile_action)

    def create_status_bar(self):
        """ Configura a barra de status. """
        group_names = ', '.join([g.name for g in self.user.groups])
        self.statusBar().showMessage(f"Pronto. Logado como: {self.user.username} | Grupos: {group_names}")


    # --- Lógica do MDI ---

    def create_mdi_sub_window(self, widget, title="Nova Janela"):
        """ Função utilitária para criar e adicionar uma subjanela MDI. """
        MainWindow.count += 1
        sub = QMdiSubWindow()
        sub.setWidget(widget)
        sub.setWindowTitle(f"{title} - #{MainWindow.count}")
        
        self.mdi_area.addSubWindow(sub)
        sub.show()
        return sub
        
    def open_dashboard_window(self):
        """ Abre a tela inicial (Dashboard). """
        
        all_permissions = [
            p.name for g in self.user.groups 
            for p in g.permissions 
            if hasattr(p, 'name') 
        ]
        permissions_string = ', '.join(all_permissions)

        dashboard_widget = QWidget()
        layout = QVBoxLayout()
        
        welcome_label = QLabel(f"Olá, {self.user.username}!")
        welcome_label.setStyleSheet("font-size: 24pt; color: #1e8449;")
        
        info_label = QLabel(
            "Esta é a sua Área de Trabalho MDI.\n"
            f"Permissões carregadas: {permissions_string}" 
        )
        
        layout.addWidget(welcome_label)
        layout.addWidget(info_label)
        layout.addStretch() 
        dashboard_widget.setLayout(layout)
        
        sub_window = self.create_mdi_sub_window(dashboard_widget, title="Painel de Controle")
        
        sub_window.setWindowFlags(sub_window.windowFlags() & ~Qt.WindowCloseButtonHint)
        sub_window.setMinimumSize(400, 300)


    def open_new_window(self):
        """ Abre a janela acionada pela ação 'Novo Cadastro'. """
        self.open_generic_window("Novo Cadastro Principal")

    def open_generic_window(self, title):
        """ Função genérica para abrir uma subjanela com um título. """
        content_widget = QTextEdit()
        content_widget.setText(f"Tela de: {title}")
        self.create_mdi_sub_window(content_widget, title=title)


    def update_menu_status(self):
        """ Atualiza o estado da barra de status e ações. """
        active_sub = self.mdi_area.activeSubWindow()
        
        has_subwindows = bool(self.mdi_area.subWindowList())
        self.cascade_action.setEnabled(has_subwindows)
        self.tile_action.setEnabled(has_subwindows)
        
        if active_sub:
            self.statusBar().showMessage(f"Janela Ativa: {active_sub.windowTitle()} | Usuário: {self.user.username}")
        else:
            group_names = ', '.join([g.name for g in self.user.groups])
            self.statusBar().showMessage(f"Pronto. Logado como: {self.user.username} | Grupos: {group_names}")
            
    
    def show_about_dialog(self):
        """ Exibe a caixa de diálogo Sobre. """
        QMessageBox.about(self, "Sobre o Sistema MDI",
            "Desenvolvido com PyQt5 e SQLAlchemy."
        )

    def closeEvent(self, event):
        """ Pergunta ao usuário se ele realmente deseja sair. """
        reply = QMessageBox.question(
            self, 'Confirmar Saída',
            "Deseja realmente fechar o sistema?", 
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()