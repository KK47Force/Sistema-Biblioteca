import sqlite3
import uuid
from datetime import datetime


def create_connection(db_file):
    """Cria uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(db_file)
    return conn


def create_table(conn):
    """Cria a tabela de login se não existir."""
    sql_create_login_table = """
    CREATE TABLE IF NOT EXISTS login (
        id TEXT PRIMARY KEY,
        email TEXT NOT NULL,
        senha TEXT NOT NULL,
        tipo TEXT NOT NULL DEFAULT 'usuario',
        nome TEXT NOT NULL,
        cpf INTEGER NOT NULL,
        livros_emprestados INTEGER DEFAULT 0,
        livros_comprados INTEGER DEFAULT 0,
        data_criacao TEXT NOT NULL
    );
    """
    cursor = conn.cursor()
    cursor.execute(sql_create_login_table)
    conn.commit()
    print("Tabela 'login' criada ou já existe.")  # Mensagem de depuração


def add_user(conn, email, senha, tipo='usuario', nome='', cpf=0):
    """Adiciona um novo usuário à tabela de login."""
    user_id = str(uuid.uuid4())  # Gera um UUID
    data_criacao = datetime.now().strftime("%d%m%Y")  # Formato D%M%Y
    sql = "INSERT INTO login (id, email, senha, tipo, nome, cpf, data_criacao) VALUES (?, ?, ?, ?, ?, ?, ?)"
    cursor = conn.cursor()
    cursor.execute(sql, (user_id, email, senha, tipo, nome, cpf, data_criacao))
    conn.commit()
    print(f"Usuário adicionado: {email} com tipo: {
          tipo}")  # Mensagem de depuração


def main():
    database = "usuarios.db"  # Nome do arquivo do banco de dados

    # Cria uma conexão com o banco de dados
    conn = create_connection(database)

    # Cria a tabela de login
    if conn:
        create_table(conn)

        # Adiciona um usuário de teste se a tabela estiver vazia
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM login")
        count = cursor.fetchone()[0]
        if count == 0:
            add_user(conn, "teste@exemplo.com", "senha123", "admin",
                     "Usuário Teste", 12345678900)  # Usuário de teste

        conn.close()


if __name__ == '__main__':
    main()
