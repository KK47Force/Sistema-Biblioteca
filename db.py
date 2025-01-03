import sqlite3
import os
import shutil
from datetime import datetime
import tempfile

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables(conn):
    """Cria as tabelas necessárias no banco de dados"""
    try:
        cursor = conn.cursor()
        
        # Remove a tabela antiga de livros se existir
        cursor.execute('DROP TABLE IF EXISTS livros')
        cursor.execute('DROP TABLE IF EXISTS usuarios')
        
        # Cria a nova tabela de livros
        cursor.execute('''
            CREATE TABLE livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_livro TEXT NOT NULL,
                nota REAL,
                quantidade INTEGER NOT NULL DEFAULT 0,
                imagem_path TEXT
            )
        ''')
        
        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL,
                cpf INTEGER,
                livros_emprestados INTEGER DEFAULT 0,
                livros_comprados INTEGER DEFAULT 0,
                data_criacao TEXT
            )
        ''')
        
        conn.commit()
        print("Tabelas criadas com sucesso")
    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")

def ensure_image_dir():
    """Garante que o diretório de imagens existe"""
    img_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagens")
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        print(f"Diretório de imagens criado: {img_dir}")
    return img_dir

def save_temp_image(image_path):
    """Salva a imagem em um arquivo temporário e retorna o caminho"""
    if not image_path or not os.path.exists(image_path):
        print(f"Caminho da imagem inválido: {image_path}")
        return None
        
    try:
        # Cria um arquivo temporário com a extensão correta
        _, ext = os.path.splitext(image_path)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        temp_path = temp_file.name
        
        # Copia a imagem para o arquivo temporário
        shutil.copy2(image_path, temp_path)
        print(f"Imagem temporária salva em: {temp_path}")
        
        return temp_path
    except Exception as e:
        print(f"Erro ao salvar imagem temporária: {e}")
        return None

def save_image(image_path):
    """Salva a imagem no diretório de imagens e retorna o caminho"""
    if not image_path or not os.path.exists(image_path):
        print(f"Caminho da imagem inválido: {image_path}")
        return None
        
    try:
        # Primeiro salva em um arquivo temporário
        temp_path = save_temp_image(image_path)
        if not temp_path:
            return None
            
        # Depois move para o diretório final
        img_dir = ensure_image_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"livro_{timestamp}{os.path.splitext(image_path)[1]}"
        dest_path = os.path.join(img_dir, filename)
        
        # Move o arquivo temporário para o destino final
        shutil.move(temp_path, dest_path)
        print(f"Imagem movida para: {dest_path}")
        
        return dest_path
    except Exception as e:
        print(f"Erro ao salvar imagem: {e}")
        return None

def add_livro(conn, nome_livro, nota, quantidade, imagem_path=None):
    """Adiciona um novo livro à tabela de livros."""
    try:
        # Primeiro salva a imagem
        saved_image_path = None
        if imagem_path:
            saved_image_path = save_image(imagem_path)
            if not saved_image_path:
                print("Falha ao salvar a imagem")
                return None
        
        # Insere o livro no banco de dados
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO livros (nome_livro, nota, quantidade, imagem_path)
            VALUES (?, ?, ?, ?)
        """, (nome_livro, nota, quantidade, saved_image_path))
        
        conn.commit()
        livro_id = cursor.lastrowid
        print(f"Livro adicionado com sucesso. ID: {livro_id}")
        return livro_id
        
    except sqlite3.Error as e:
        print(f"Erro ao adicionar livro no banco de dados: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado ao adicionar livro: {e}")
        return None

def get_livro_by_id(conn, livro_id):
    """Retorna um livro específico do banco de dados"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nome_livro, nota, quantidade, imagem_path
            FROM livros 
            WHERE id = ?
        """, (livro_id,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Erro ao buscar livro: {e}")
        return None

def get_todos_livros(conn):
    """Retorna todos os livros do banco de dados"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nome_livro, nota, quantidade, imagem_path
            FROM livros
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao buscar livros: {e}")
        return []

def update_livro(conn, livro_id, nome_livro=None, nota=None, quantidade=None, imagem_path=None):
    """Atualiza os dados de um livro."""
    try:
        # Primeiro recupera o livro atual
        livro_atual = get_livro_by_id(conn, livro_id)
        if not livro_atual:
            print(f"Livro não encontrado: {livro_id}")
            return False
        
        # Prepara os valores para atualização
        novo_nome = nome_livro if nome_livro is not None else livro_atual[1]
        nova_nota = nota if nota is not None else livro_atual[2]
        nova_qtd = quantidade if quantidade is not None else livro_atual[3]
        
        # Se uma nova imagem foi fornecida, salva ela
        nova_imagem_path = livro_atual[4]  # mantém a imagem atual por padrão
        if imagem_path:
            # Remove a imagem antiga se existir
            if livro_atual[4] and os.path.exists(livro_atual[4]):
                try:
                    os.remove(livro_atual[4])
                except OSError as e:
                    print(f"Erro ao remover imagem antiga: {e}")
            
            # Salva a nova imagem
            nova_imagem_path = save_image(imagem_path)
            if not nova_imagem_path:
                print("Falha ao salvar a nova imagem")
                return False
        
        # Atualiza o banco de dados
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE livros
            SET nome_livro = ?,
                nota = ?,
                quantidade = ?,
                imagem_path = ?
            WHERE id = ?
        """, (novo_nome, nova_nota, nova_qtd, nova_imagem_path, livro_id))
        
        conn.commit()
        print(f"Livro atualizado com sucesso: {livro_id}")
        return True
        
    except sqlite3.Error as e:
        print(f"Erro ao atualizar livro no banco de dados: {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado ao atualizar livro: {e}")
        return False

def delete_livro(conn, livro_id):
    """Remove um livro do banco de dados."""
    try:
        # Primeiro recupera o livro para obter o caminho da imagem
        livro = get_livro_by_id(conn, livro_id)
        if not livro:
            print(f"Livro não encontrado: {livro_id}")
            return False
        
        # Remove a imagem se existir
        if livro[4] and os.path.exists(livro[4]):
            try:
                os.remove(livro[4])
                print(f"Imagem removida: {livro[4]}")
            except OSError as e:
                print(f"Erro ao remover imagem: {e}")
        
        # Remove o registro do banco de dados
        cursor = conn.cursor()
        cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
        conn.commit()
        
        print(f"Livro removido com sucesso: {livro_id}")
        return True
        
    except sqlite3.Error as e:
        print(f"Erro ao remover livro do banco de dados: {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado ao remover livro: {e}")
        return False

def add_user(conn, email, senha, tipo='usuario', nome='', cpf=None):
    """Adiciona um novo usuário à tabela de usuários."""
    try:
        data_criacao = datetime.now().strftime("%d%m%Y")
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha, tipo, cpf, data_criacao)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, email, senha, tipo, cpf, data_criacao))
        
        conn.commit()
        user_id = cursor.lastrowid
        print(f"Usuário adicionado com sucesso. ID: {user_id}")
        return user_id
    except sqlite3.Error as e:
        print(f"Erro ao adicionar usuário: {e}")
        return None

def get_foto_livro(conn, livro_id):
    """Recupera a foto de um livro do banco de dados.
    
    Args:
        conn: Conexão com o banco de dados
        livro_id: ID do livro
    
    Returns:
        bytes: Dados binários da foto ou None se não encontrada
    """
    cursor = conn.cursor()
    cursor.execute("SELECT imagem_path FROM livros WHERE id = ?", (livro_id,))
    imagem_path = cursor.fetchone()
    
    if imagem_path and imagem_path[0]:
        try:
            with open(imagem_path[0], 'rb') as file:
                return file.read()
        except Exception as e:
            print(f"Erro ao ler a imagem: {e}")
    return None

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

def init_db():
    """Inicializa o banco de dados"""
    try:
        # Remove o banco de dados antigo se existir
        db_file = "usuarios.db"
        if os.path.exists(db_file):
            os.remove(db_file)
            print("Banco de dados antigo removido")
        
        # Cria a conexão
        conn = create_connection(db_file)
        if conn is None:
            print("Erro! Não foi possível criar a conexão com o banco de dados.")
            return
        
        # Cria as tabelas
        create_tables(conn)
        
        # Garante que o diretório de imagens existe
        ensure_image_dir()
        
        # Adiciona um usuário administrador padrão
        add_user(conn, 
                email="admin@admin.com",
                senha="admin123",
                tipo="admin",
                nome="Administrador")
        
        conn.close()
        print("Banco de dados inicializado com sucesso")
        
    except Exception as e:
        print(f"Erro ao inicializar banco de dados: {e}")

if __name__ == "__main__":
    init_db()
