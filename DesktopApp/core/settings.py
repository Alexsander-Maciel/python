# DesktopApp/core/settings.py

# ====================================================================
# CONFIGURAÇÃO DE MÓDULOS DO SISTEMA
# ====================================================================

# Dicionário que mapeia o NOME de exibição do módulo para o NOME da pasta
# Se o valor for True, o módulo será carregado e aparecerá no menu.

ENABLED_MODULES = {
    "Produtos & Estoque": True,     # Vamos manter este módulo como nosso primeiro foco
    "Contabilidade": False,         # Desabilitado, não aparecerá no Menu
    "Financeiro": True,             # Habilitado, aparecerá no Menu
    "Módulo Jurídico": False,
    "Módulo de Jogos": False,
    "Vendas & Faturamento": True,
}

# FIM DO ARQUIVO