
# Configurações do Banco de Dados MySQL
DB_CONFIG = {
    "host": "localhost:3306",
    "user": "root",
    "password": "",
    "database": "desktop_app_db"
}

# String de Conexão do SQLAlchemy (foco em Python/MySQL)
DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}/{DB_CONFIG['database']}"
)

# Outras configurações (ex: chave secreta para criptografia de senhas)
SECRET_KEY = "sua_chave_secreta_aqui"