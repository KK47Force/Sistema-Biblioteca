import sqlite3
import uuid
from datetime import datetime
import os


def create_connection(db_file):
    """Cria uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(db_file)
    return conn


def create_table(conn):
    """Cria as tabelas se não existirem."""
    # Tabela de login
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
    
    # Nova tabela de livros
    sql_create_livros_table = """
    CREATE TABLE IF NOT EXISTS livros (
        id TEXT PRIMARY KEY,
        nome_livro TEXT NOT NULL,
        nota REAL,
        foto BLOB,
        quantidade INTEGER NOT NULL DEFAULT 0
    );
    """
    
    cursor = conn.cursor()
    cursor.execute(sql_create_login_table)
    cursor.execute(sql_create_livros_table)
    conn.commit()
    print("Tabelas 'login' e 'livros' criadas ou já existem.")


def add_user(conn, email, senha, tipo='usuario', nome='', cpf=0):
    """Adiciona um novo usuário à tabela de login."""
    user_id = str(uuid.uuid4())  # Gera um UUID
    data_criacao = datetime.now().strftime("%d%m%Y")  # Formato D%M%Y
    sql = "INSERT INTO login (id, email, senha, tipo, nome, cpf, data_criacao) VALUES (?, ?, ?, ?, ?, ?, ?)"
    cursor = conn.cursor()
    cursor.execute(sql, (user_id, email, senha, tipo, nome, cpf, data_criacao))
    conn.commit()
    print(f"Usuário adicionado: {email} com tipo: {tipo}")  # Mensagem de depuração


def add_livro(conn, nome_livro, nota, foto_path=None, quantidade=0):
    """Adiciona um novo livro à tabela de livros.
    
    Args:
        conn: Conexão com o banco de dados
        nome_livro (str): Nome do livro
        nota (float): Nota do livro
        foto_path (str, optional): Caminho para o arquivo da foto
        quantidade (int): Quantidade disponível do livro
    """
    livro_id = str(uuid.uuid4())
    foto_blob = None
    
    if foto_path and os.path.exists(foto_path):
        try:
            with open(foto_path, 'rb') as file:
                foto_blob = file.read()
            print(f"Foto lida com sucesso: {len(foto_blob)} bytes")
        except Exception as e:
            print(f"Erro ao ler a imagem: {e}")
            return None
    else:
        print(f"Arquivo não encontrado: {foto_path}")
        return None
    
    try:
        sql = "INSERT INTO livros (id, nome_livro, nota, foto, quantidade) VALUES (?, ?, ?, ?, ?)"
        cursor = conn.cursor()
        cursor.execute(sql, (livro_id, nome_livro, nota, foto_blob, quantidade))
        conn.commit()
        print(f"Livro adicionado: {nome_livro} (ID: {livro_id})")
        return livro_id
    except Exception as e:
        print(f"Erro ao adicionar livro: {e}")
        return None


def get_livro(conn, livro_id):
    """Recupera um livro pelo ID.
    
    Args:
        conn: Conexão com o banco de dados
        livro_id (str): ID do livro
    
    Returns:
        tuple: Dados do livro ou None se não encontrado
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros WHERE id = ?", (livro_id,))
    return cursor.fetchone()


def update_livro(conn, livro_id, nome_livro=None, nota=None, foto_path=None, quantidade=None):
    """Atualiza os dados de um livro.
    
    Args:
        conn: Conexão com o banco de dados
        livro_id (str): ID do livro
        nome_livro (str, optional): Novo nome do livro
        nota (float, optional): Nova nota
        foto_path (str, optional): Novo caminho da foto
        quantidade (int, optional): Nova quantidade
    """
    updates = []
    values = []
    
    if nome_livro is not None:
        updates.append("nome_livro = ?")
        values.append(nome_livro)
    
    if nota is not None:
        updates.append("nota = ?")
        values.append(nota)
    
    if foto_path is not None:
        try:
            with open(foto_path, 'rb') as file:
                foto_blob = file.read()
                updates.append("foto = ?")
                values.append(foto_blob)
        except Exception as e:
            print(f"Erro ao ler a nova imagem: {e}")
    
    if quantidade is not None:
        updates.append("quantidade = ?")
        values.append(quantidade)
    
    if updates:
        sql = f"UPDATE livros SET {', '.join(updates)} WHERE id = ?"
        values.append(livro_id)
        
        cursor = conn.cursor()
        cursor.execute(sql, tuple(values))
        conn.commit()
        print(f"Livro {livro_id} atualizado com sucesso")


def delete_livro(conn, livro_id):
    """Remove um livro do banco de dados.
    
    Args:
        conn: Conexão com o banco de dados
        livro_id (str): ID do livro a ser removido
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
    conn.commit()
    print(f"Livro {livro_id} removido com sucesso")


def add_exemplo_livro(conn):
    """Adiciona um livro de exemplo ao banco de dados."""
    # Caminho para a imagem local
    imagem_path = "imagem.jpg"
    
    # Adiciona o livro com a imagem local
    add_livro(
        conn,
        nome_livro="Dom Quixote",
        nota=4.8,
        foto_path=imagem_path,
        quantidade=5
    )


def get_foto_livro(conn, livro_id):
    """Recupera a foto de um livro do banco de dados.
    
    Args:
        conn: Conexão com o banco de dados
        livro_id: ID do livro
    
    Returns:
        bytes: Dados binários da foto ou None se não encontrada
    """
    cursor = conn.cursor()
    cursor.execute("SELECT foto FROM livros WHERE id = ?", (livro_id,))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None


def salvar_foto_temp(foto_bytes, nome_arquivo="temp_foto.jpg"):
    """Salva os dados binários da foto em um arquivo temporário.
    
    Args:
        foto_bytes: Dados binários da foto
        nome_arquivo: Nome do arquivo temporário
    
    Returns:
        str: Caminho do arquivo temporário ou None se houver erro
    """
    if foto_bytes:
        try:
            # Cria diretório temp se não existir
            if not os.path.exists("temp"):
                os.makedirs("temp")
            
            caminho_temp = os.path.join("temp", nome_arquivo)
            with open(caminho_temp, "wb") as f:
                f.write(foto_bytes)
            return caminho_temp
        except Exception as e:
            print(f"Erro ao salvar foto temporária: {e}")
    return None


def get_todos_livros(conn):
    """Recupera todos os livros do banco de dados.
    
    Args:
        conn: Conexão com o banco de dados
    
    Returns:
        list: Lista de tuplas com os dados dos livros
    """
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome_livro, nota, quantidade FROM livros")
    return cursor.fetchall()


def main():
    database = "usuarios.db"  # Nome do arquivo do banco de dados

    # Cria uma conexão com o banco de dados
    conn = create_connection(database)

    # Cria as tabelas
    if conn:
        create_table(conn)

        # Adiciona um usuário de teste se a tabela estiver vazia
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM login")
        count = cursor.fetchone()[0]
        if count == 0:
            add_user(conn, "teste@exemplo.com", "senha123", "admin",
                     "Usuário Teste", 12345678900)  # Usuário de teste

        # Adiciona um livro de exemplo se a tabela estiver vazia
        cursor.execute("SELECT COUNT(*) FROM livros")
        count = cursor.fetchone()[0]
        if count == 0:
            add_exemplo_livro(conn)

        conn.close()


if __name__ == '__main__':
    main()
