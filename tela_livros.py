import flet as ft
from db import create_connection, get_todos_livros, get_livro_by_id
import adicionar_livro
import editar_excluir_livro
import os

def main(page: ft.Page, on_exit):
    page.title = "Gerenciamento de Livros"
    page.window.width = 1200
    page.window.height = 800
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    
    def navegar_para(destino):
        """Navega para a página especificada."""
        page.controls.clear()
        if destino == "adicionar":
            adicionar_livro.main(page, lambda: main(page, on_exit))
        elif destino == "editar":
            editar_excluir_livro.main(page, lambda: main(page, on_exit))
        elif destino == "excluir":
            editar_excluir_livro.main(page, lambda: main(page, on_exit))
    
    # Barra lateral
    sidebar = ft.Container(
        content=ft.Column(
            [
                ft.Text("MENU", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Divider(color=ft.colors.WHITE24),
                ft.TextButton(
                    text="Adicionar Livro",
                    on_click=lambda _: navegar_para("adicionar"),
                    style=ft.ButtonStyle(color=ft.colors.WHITE),
                ),
                ft.TextButton(
                    text="Editar Livro",
                    on_click=lambda _: navegar_para("editar"),
                    style=ft.ButtonStyle(color=ft.colors.WHITE),
                ),
                ft.TextButton(
                    text="Excluir Livro",
                    on_click=lambda _: navegar_para("excluir"),
                    style=ft.ButtonStyle(color=ft.colors.WHITE),
                ),
                ft.TextButton(
                    text="Voltar",
                    on_click=lambda _: (page.controls.clear(), on_exit()),
                    style=ft.ButtonStyle(color=ft.colors.WHITE),
                ),
            ],
            spacing=10,
        ),
        width=200,
        padding=20,
        bgcolor=ft.colors.BLUE,
    )
    
    # Container para exibir a imagem
    img_container = ft.Container(
        width=200,
        height=300,
        border=ft.border.all(1, ft.colors.BLACK),
        border_radius=10,
        padding=10,
        content=ft.Text("Selecione um livro", size=12, text_align=ft.TextAlign.CENTER),
    )
    
    # Container para informações do livro
    info_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Título: ", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("Avaliação: ", size=16),
                ft.Text("Quantidade: ", size=16),
            ],
            spacing=10,
        ),
        padding=10,
    )
    
    # Função para exibir as informações do livro
    def exibir_livro(livro_id):
        if not livro_id:
            return
            
        # Recupera o livro do banco de dados
        conn = create_connection("usuarios.db")
        livro = get_livro_by_id(conn, livro_id)
        conn.close()
        
        if livro:
            # Atualiza as informações do livro
            info_container.content = ft.Column(
                [
                    ft.Text(f"Título: {livro[1]}", size=16, weight=ft.FontWeight.BOLD),  # título
                    ft.Text(f"Avaliação: {livro[2]}", size=16),  # avaliação
                    ft.Text(f"Quantidade: {livro[3]}", size=16),  # quantidade
                ],
                spacing=10,
            )
            
            # Exibe a imagem se existir
            imagem_path = livro[4]  # imagem_path
            if imagem_path and os.path.exists(imagem_path):
                img_container.content = ft.Image(
                    src=imagem_path,
                    width=200,
                    height=300,
                    fit=ft.ImageFit.CONTAIN,
                )
            else:
                img_container.content = ft.Text(
                    "Sem imagem",
                    size=12,
                    text_align=ft.TextAlign.CENTER
                )
        
        page.update()
    
    # Recupera todos os livros
    conn = create_connection("usuarios.db")
    livros = get_todos_livros(conn)
    conn.close()
    
    # Dropdown para selecionar o livro
    dropdown_livros = ft.Dropdown(
        label="Selecione um livro",
        width=400,
        options=[ft.dropdown.Option(key=livro[0], text=livro[1]) for livro in livros],  # id e título
        on_change=lambda e: exibir_livro(e.control.value) if e.control.value else None
    )
    
    # Conteúdo principal com ScrollableColumn
    conteudo = ft.Container(
        content=ft.Column(
            [
                ft.Text("Visualizador de Livros", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                dropdown_livros,
                ft.Divider(),
                ft.Row(
                    [
                        img_container,
                        ft.VerticalDivider(width=20),
                        info_container,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            height=page.window.height - 40,  # 40 é o padding total (20 * 2)
        ),
        expand=True,
        padding=20,
    )
    
    # Layout principal
    page.add(
        ft.Row(
            [
                sidebar,
                ft.VerticalDivider(width=1),
                conteudo,
            ],
            expand=True,
        )
    )

if __name__ == "__main__":
    def app_main(page: ft.Page):
        main(page, lambda: page.window_destroy())
    ft.app(target=app_main)
