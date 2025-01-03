import os
from db import create_connection

def main():
    # Remove o banco de dados existente
    if os.path.exists("usuarios.db"):
        os.remove("usuarios.db")
        print("Banco de dados removido")
    
    # Cria novo banco de dados
    conn = create_connection("usuarios.db")
    
    # Importa e executa o arquivo db.py para criar as tabelas e dados iniciais
    import db
    db.main()
    
    print("Banco de dados reiniciado com sucesso")

if __name__ == "__main__":
    main()
