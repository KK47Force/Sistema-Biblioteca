import sqlite3
import uuid


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
        senha TEXT NOT NULL
    );
    """
    cursor = conn.cursor()
    cursor.execute(sql_create_login_table)
    conn.commit()


def add_user(conn, email, senha):
    """Adiciona um novo usuário à tabela de login."""
    user_id = str(uuid.uuid4())  # Gera um UUID
    sql = "INSERT INTO login (id, email, senha) VALUES (?, ?, ?)"
    cursor = conn.cursor()
    cursor.execute(sql, (user_id, email, senha))
    conn.commit()


def main():
    database = "usuarios.db"  # Nome do arquivo do banco de dados

    # Cria uma conexão com o banco de dados
    conn = create_connection(database)

    # Cria a tabela de login
    if conn:
        create_table(conn)
        conn.close()


if __name__ == '__main__':
    main()
