# DesktopApp/modules/inventory/views/product_form_window.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDoubleSpinBox, QSpinBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from DesktopApp.modules.inventory.controllers.inventory_controller import InventoryController

class ProductFormWindow(QDialog):
    def __init__(self, controller: 'InventoryController', parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Cadastro de Novo Produto")
        self.setFixedSize(400, 300)
        
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # 1. Campos de Entrada
        self.name_input = QLineEdit()
        self.desc_input = QLineEdit()
        
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0.01, 999999.99)
        self.price_input.setDecimals(2)
        self.price_input.setPrefix("R$ ")
        
        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 99999)

        # Adicionar campos ao formulário
        form_layout.addRow("Nome:", self.name_input)
        form_layout.addRow("Descrição:", self.desc_input)
        form_layout.addRow("Preço:", self.price_input)
        form_layout.addRow("Estoque Inicial:", self.stock_input)

        main_layout.addLayout(form_layout)

        # 2. Botão de Salvar
        self.save_button = QPushButton("💾 Salvar Produto")
        self.save_button.setStyleSheet("background-color: #007BFF; color: white; padding: 10px;")
        self.save_button.clicked.connect(self._on_save_clicked)
        main_layout.addWidget(self.save_button)

    def _on_save_clicked(self):
        """Coleta dados, chama o Controller e fecha a janela."""
        data = {
            'name': self.name_input.text(),
            'description': self.desc_input.text(),
            'price': self.price_input.value(),
            'stock_quantity': self.stock_input.value()
        }

        if not data['name']:
            QMessageBox.warning(self, "Atenção", "O nome do produto é obrigatório.")
            return

        try:
            # CORREÇÃO: A chamada para o Controller deve passar APENAS o dicionário 'data'
            self.controller.handle_create_product(data) 
            
            QMessageBox.information(self, "Sucesso", f"Produto '{data['name']}' cadastrado com sucesso.")
            self.accept() 
            
        except ValueError as e:
            QMessageBox.critical(self, "Erro de Negócio", str(e))
            
        except Exception as e:
             # O erro de argumentos faltantes está sendo propagado até aqui.
             QMessageBox.critical(self, "Erro de Sistema", "Erro inesperado ao salvar produto.")
             print(f"ERRO NO CADASTRO DE PRODUTO: {e}")