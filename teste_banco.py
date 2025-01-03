from db import create_connection, get_todos_livros, get_foto_livro

def main():
    # Conecta ao banco de dados
    conn = create_connection("usuarios.db")
    
    # Lista todos os livros
    livros = get_todos_livros(conn)
    print("\nLivros encontrados:")
    for livro in livros:
        print(f"ID: {livro[0]}")
        print(f"Nome: {livro[1]}")
        print(f"Nota: {livro[2]}")
        print(f"Quantidade: {livro[3]}")
        
        # Verifica se tem foto
        foto = get_foto_livro(conn, livro[0])
        if foto:
            print(f"Foto encontrada: {len(foto)} bytes")
        else:
            print("Sem foto")
        print("-" * 50)
    
    conn.close()

if __name__ == "__main__":
    main()
