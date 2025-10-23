# DesktopApp/views/main_window.py

from PyQt5.QtWidgets import QMainWindow, QWidget, QMenu, QAction, QMdiArea, QMdiSubWindow, QApplication
from PyQt5.QtCore import Qt
from typing import List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from DesktopApp.controllers.user_controller import UserController
    from DesktopApp.models.entities.user import User

class MainWindow(QMainWindow):
    """
    Janela Principal da Aplicação (Parent MDI).
    Responsável por gerenciar o layout, menus e janelas filhas (MDI SubWindows).
    """
    def __init__(self, user_controller: 'UserController', modules: List[Dict[str, Any]]):
        super().__init__()
        self.user_controller = user_controller
        self.modules = modules
        self.user = None
        
        self.setWindowTitle("Dra. Elara - Sistema de Gestão Empresarial (MDI)")
        self.setGeometry(100, 100, 1200, 800)

        # 1. CONFIGURAÇÃO MDI
        self.mdi_area = QMdiArea()
        self.mdi_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdi_area)
        
        self.open_subwindows = {}

        # 2. Setup inicial (Menu e Status Bar)
        self.statusBar().showMessage("Bem-vindo(a)! Faça o login para continuar.")
        self.init_menu()

    def init_menu(self):
        """Inicializa a estrutura básica do MenuBar."""
        self.menuBar().clear()
        
        self.file_menu = self.menuBar().addMenu("&Arquivo")
        self.window_menu = self.menuBar().addMenu("&Janelas")

        self.window_menu.addAction("Cascata", self.mdi_area.cascadeSubWindows)
        self.window_menu.addAction("Lado a Lado", self.mdi_area.tileSubWindows)
        self.window_menu.addAction("Fechar Todas", self.mdi_area.closeAllSubWindows)
        
        logout_action = QAction("&Logout", self)
        logout_action.triggered.connect(self.logout)
        self.file_menu.addAction(logout_action)
        
        # GARANTIA VISUAL
        self.menuBar().setVisible(True)

    def update_ui_after_login(self, user: 'User', accessible_routes: List[Dict[str, Any]]):
        """
        Monta a barra de menus com base nas permissões.
        """
        self.user = user
        
        # 1. Limpar e Reiniciar o Menu
        self.menuBar().clear()
        self.init_menu() 
        
        # 2. Adicionar o Menu de Módulos (Se houver rotas)
        if not accessible_routes:
             self.statusBar().showMessage(f"Bem-vindo(a), {user.full_name}. Sem módulos acessíveis.")
             return

        self.module_menu = self.menuBar().addMenu("&Módulos")
        
        # 3. Dicionário de rotas injetadas: {route_name: view_object}
        injected_views = {m['route_name']: m['view'] for m in self.modules}
        
        # 4. Criação dos Itens de Menu
        for route_info in accessible_routes:
            route_name = route_info.get("route") 
            menu_name = route_info.get("name")
            
            if route_name and menu_name and route_name in injected_views:
                view_widget = injected_views[route_name]
                
                action = QAction(menu_name, self)
                action.triggered.connect(lambda checked, widget=view_widget, name=menu_name: self.open_mdi_subwindow(widget, name))
                
                self.module_menu.addAction(action)
                
        # 5. GARANTIA VISUAL FINAL
        self.menuBar().setVisible(True)
        
        self.statusBar().showMessage(f"Bem-vindo(a), {user.full_name} ({user.username}).")
        
    
    def open_mdi_subwindow(self, widget: QWidget, title: str):
        """Abre a View do módulo dentro de uma QMdiSubWindow."""
        
        if title in self.open_subwindows:
            sub = self.open_subwindows[title]
            self.mdi_area.setActiveSubWindow(sub)
            return

        sub = QMdiSubWindow()
        sub.setWindowTitle(title)
        sub.setWidget(widget)
        self.mdi_area.addSubWindow(sub)
        
        sub.setAttribute(Qt.WA_DeleteOnClose)
        sub.destroyed.connect(lambda: self._remove_closed_subwindow(title))
        
        self.open_subwindows[title] = sub
        sub.show()

    def _remove_closed_subwindow(self, title: str):
        if title in self.open_subwindows:
            del self.open_subwindows[title]
            
    def logout(self):
        QApplication.quit()