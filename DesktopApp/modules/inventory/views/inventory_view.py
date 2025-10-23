from typing import List, TYPE_CHECKING
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableView, QMessageBox, QLabel, QHeaderView, QDialog
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant

# CORREÇÃO CRÍTICA: Mude de 'from modules.' para 'from DesktopApp.modules.'
from DesktopApp.modules.inventory.views.product_form_window import ProductFormWindow 
# ... (o resto do arquivo permanece igual)
# ====================================================================
# 1. MODELO DE DADOS PARA A TABELA (QAbstractTableModel)
# ====================================================================

class ProductTableModel(QAbstractTableModel):
    """Modelo de dados para exibir a lista de produtos na QTableView."""
    
    HEADERS = ["ID", "Nome", "Descrição", "Preço", "Estoque", "Ativo"]

    def __init__(self, products: List['Product'] = None):
        super().__init__()
        self._products = products or []

    def set_products(self, products: List['Product']):
        """Atualiza os dados da tabela."""
        self.beginResetModel()
        self._products = products
        self.endResetModel()

    def rowCount(self, parent=None):
        return len(self._products)

    def columnCount(self, parent=None):
        return len(self.HEADERS)

    def data(self, index, role=Qt.DisplayRole):
        """Método principal para fornecer dados à tabela."""
        if not index.isValid():
            return QVariant()
        
        product = self._products[index.row()]
        col = index.column()

        if role == Qt.DisplayRole:
            if col == 0: return product.id
            if col == 1: return product.name
            if col == 2: return product.description
            if col == 3: return f"R$ {product.price:.2f}"
            if col == 4: return product.stock_quantity
            if col == 5: return "Sim" if product.is_active else "Não"
        
        # Opcional: Alinhamento de colunas
        if role == Qt.TextAlignmentRole:
            if col in (0, 3, 4):
                return int(Qt.AlignRight | Qt.AlignVCenter)
        
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """Fornece os títulos das colunas."""
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.HEADERS[section]
        return QVariant()


# ====================================================================
# 2. VIEW PRINCIPAL (Widget)
# ====================================================================

class InventoryView(QWidget):
    """
    Interface Gráfica para o Gerenciamento de Produtos.
    """
    def __init__(self, controller: 'InventoryController'):
        super().__init__()
        self.controller = controller
        
        # Linka a View de volta ao Controller para comunicação
        self.controller.set_view(self) 

        self._init_ui()
        
        # Carrega os dados na inicialização
        self.controller.handle_load_products()

    def _init_ui(self):
        self.main_layout = QVBoxLayout(self)
        
        # --- Área de Título e Botões ---
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("<h2>Gerenciamento de Produtos</h2>"))
        
        # Botões de Ação
        self.add_button = QPushButton("➕ Novo Produto")
        self.add_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.add_button.clicked.connect(self._on_add_product_clicked)
        header_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("✏️ Editar Selecionado")
        # NOTE: Conexão para edição será implementada em breve.
        header_layout.addWidget(self.edit_button)

        self.refresh_button = QPushButton("🔄 Recarregar")
        self.refresh_button.clicked.connect(self.controller.handle_load_products)
        header_layout.addWidget(self.refresh_button)

        self.main_layout.addLayout(header_layout)

        # --- Tabela de Produtos ---
        self.table_view = QTableView()
        self.product_model = ProductTableModel()
        self.table_view.setModel(self.product_model)
        
        # Configurações de exibição da tabela
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        
        self.main_layout.addWidget(self.table_view)
        
    # --- MÉTODOS DE MANIPULAÇÃO DE DADOS E EVENTOS ---

    def _on_add_product_clicked(self):
        """
        Abre a janela de formulário para coletar dados de um novo produto (Modal).
        """
        # Passamos o Controller e a própria InventoryView como 'parent'
        form_window = ProductFormWindow(self.controller, self)
        
        # Executa como modal. Se o resultado for QDialog.Accepted (botão Save):
        if form_window.exec_() == QDialog.Accepted:
            # A lista será recarregada pelo Controller após a inserção bem-sucedida,
            # mas este é um ponto de garantia:
            pass 
            
    # --- MÉTODOS DE COMUNICAÇÃO (Chamados Pelo Controller) ---
    
    def display_products(self, products: List['Product']):
        """
        Recebe a lista de produtos do Controller e atualiza a tabela.
        """
        self.product_model.set_products(products)
        print(f"VIEW: Tabela de produtos atualizada com {len(products)} itens.")
        
    def show_error_message(self, message: str):
        """
        Exibe uma mensagem de erro na View.
        """
        QMessageBox.critical(self, "Erro de Operação", message)

# FIM DO ARQUIVO