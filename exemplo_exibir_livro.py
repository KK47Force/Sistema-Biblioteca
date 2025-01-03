import flet as ft
from db import create_connection, get_foto_livro, salvar_foto_temp, get_todos_livros
import os

def main(page: ft.Page):
    page.title = "Exemplo - Exibir Livro"
    page.window_width = 800  # Corrigido
    page.window_height = 600  # Corrigido
    page.padding = 20
    
    # Conecta ao banco de dados
    conn = create_connection("usuarios.db")
    
    # Container para exibir a imagem
    img_container = ft.Container(
        width=200,
        height=300,
        border=ft.border.all(1, ft.colors.BLACK),  # Corrigido
        border_radius=10,
        padding=10,
    )
    
    # Status text para debug
    status_text = ft.Text("", color="red")
    
    # Função para exibir a foto de um livro
    def exibir_foto_livro(livro_id):
        status_text.value = f"Tentando exibir livro ID: {livro_id}"
        page.update()
        
        # Recupera a foto do livro
        foto_bytes = get_foto_livro(conn, livro_id)
        
        if foto_bytes:
            status_text.value = f"Foto recuperada, tamanho: {len(foto_bytes)} bytes"
            page.update()
            
            # Salva em arquivo temporário
            caminho_temp = salvar_foto_temp(foto_bytes)
            
            if caminho_temp:
                status_text.value = f"Foto salva em: {caminho_temp}"
                page.update()
                
                # Verifica se o arquivo existe
                if os.path.exists(caminho_temp):
                    status_text.value += f"\nArquivo existe, tamanho: {os.path.getsize(caminho_temp)} bytes"
                else:
                    status_text.value += "\nArquivo não existe!"
                page.update()
                
                # Atualiza o container com a imagem
                img_container.content = ft.Image(
                    src=caminho_temp,
                    width=200,
                    height=300,
                    fit=ft.ImageFit.CONTAIN,
                )
                page.update()
        else:
            status_text.value = "Nenhuma foto encontrada para este livro"
            img_container.content = None
            page.update()
    
    # Recupera todos os livros
    livros = get_todos_livros(conn)
    print(f"Livros encontrados: {livros}")  # Debug
    
    # Dropdown para selecionar o livro
    dropdown_livros = ft.Dropdown(
        label="Selecione um livro",
        width=400,
        options=[ft.dropdown.Option(key=livro[0], text=livro[1]) for livro in livros],
        on_change=lambda e: exibir_foto_livro(e.control.value) if e.control.value else None
    )
    
    # Layout
    page.add(
        ft.Column(
            [
                ft.Text("Visualizador de Livros", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                dropdown_livros,
                status_text,  # Adicionado texto de status
                ft.Divider(),
                img_container,
            ],
            spacing=20,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
