# Exemplo de como deve estar em config/settings.py
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_HOST = "localhost" # ou IP do servidor
MYSQL_PORT = "3306"
MYSQL_DB = "nome_do_banco"

DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"