import flet as ft
import os
from db import create_connection, get_todos_livros, get_foto_livro, update_livro, delete_livro

def main(page: ft.Page):
    page.title = "Editar/Excluir Livro"
    page.window.width = 800
    page.window.height = 600
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Campos do formulário
    nome_livro = ft.TextField(label="Nome do Livro", width=400)
    nota = ft.TextField(label="Nota", width=400, keyboard_type=ft.KeyboardType.NUMBER)
    quantidade = ft.TextField(label="Quantidade", width=400, keyboard_type=ft.KeyboardType.NUMBER)
    
    # Container para a imagem
    img_preview = ft.Container(
        width=200,
        height=300,
        border=ft.border.all(1, ft.colors.BLACK),
        border_radius=10,
        padding=10,
        content=ft.Text("Arraste uma imagem ou clique para selecionar", 
                       size=12, 
                       text_align=ft.TextAlign.CENTER),
    )
    
    # Variáveis para armazenar dados do livro selecionado
    livro_selecionado = None
    caminho_imagem = None
    
    def selecionar_arquivo(e: ft.FilePickerResultEvent):
        if e.files:
            caminho_imagem = e.files[0].path
            img_preview.content = ft.Image(
                src=caminho_imagem,
                width=200,
                height=300,
                fit=ft.ImageFit.CONTAIN,
            )
            page.update()
    
    # File picker para selecionar imagem
    file_picker = ft.FilePicker(
        on_result=selecionar_arquivo,
        allow_multiple=False,
        allowed_extensions=["png", "jpg", "jpeg"]
    )
    page.overlay.append(file_picker)
    
    def on_drag_accept(e: ft.DragTargetAcceptEvent):
        caminho_imagem = e.data
        if os.path.exists(caminho_imagem):
            img_preview.content = ft.Image(
                src=caminho_imagem,
                width=200,
                height=300,
                fit=ft.ImageFit.CONTAIN,
            )
            page.update()
    
    # Drag target para arrastar imagem
    drag_target = ft.DragTarget(
        content=img_preview,
        on_accept=on_drag_accept,
    )
    
    def carregar_livro(livro_id):
        nonlocal livro_selecionado
        conn = create_connection("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM livros WHERE id = ?", (livro_id,))
        livro = cursor.fetchone()
        
        if livro:
            livro_selecionado = livro
            nome_livro.value = livro[1]
            nota.value = str(livro[2])
            quantidade.value = str(livro[4])
            
            # Carrega a foto
            foto_bytes = get_foto_livro(conn, livro_id)
            if foto_bytes:
                caminho_temp = f"temp/livro_{livro_id}.jpg"
                os.makedirs("temp", exist_ok=True)
                with open(caminho_temp, "wb") as f:
                    f.write(foto_bytes)
                img_preview.content = ft.Image(
                    src=caminho_temp,
                    width=200,
                    height=300,
                    fit=ft.ImageFit.CONTAIN,
                )
        
        conn.close()
        page.update()
    
    def salvar_alteracoes():
        if not livro_selecionado:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Selecione um livro primeiro"))
            )
            return
        
        try:
            conn = create_connection("usuarios.db")
            update_livro(
                conn,
                livro_selecionado[0],
                nome_livro=nome_livro.value,
                nota=float(nota.value),
                foto_path=caminho_imagem if caminho_imagem else None,
                quantidade=int(quantidade.value)
            )
            conn.close()
            
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Livro atualizado com sucesso!"))
            )
            
        except Exception as e:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text(f"Erro ao atualizar livro: {str(e)}"))
            )
    
    def excluir():
        if not livro_selecionado:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Selecione um livro primeiro"))
            )
            return
        
        try:
            conn = create_connection("usuarios.db")
            delete_livro(conn, livro_selecionado[0])
            conn.close()
            
            # Limpa os campos
            nome_livro.value = ""
            nota.value = ""
            quantidade.value = ""
            img_preview.content = ft.Text(
                "Arraste uma imagem ou clique para selecionar",
                size=12,
                text_align=ft.TextAlign.CENTER
            )
            
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Livro excluído com sucesso!"))
            )
            page.update()
            
        except Exception as e:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text(f"Erro ao excluir livro: {str(e)}"))
            )
    
    # Recupera todos os livros para o dropdown
    conn = create_connection("usuarios.db")
    livros = get_todos_livros(conn)
    conn.close()
    
    # Dropdown para selecionar o livro
    dropdown_livros = ft.Dropdown(
        label="Selecione um livro",
        width=400,
        options=[ft.dropdown.Option(key=livro[0], text=livro[1]) for livro in livros],
        on_change=lambda e: carregar_livro(e.control.value) if e.control.value else None
    )
    
    # Layout
    page.add(
        ft.Column(
            [
                ft.Text("Editar/Excluir Livro", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                dropdown_livros,
                nome_livro,
                nota,
                quantidade,
                ft.Text("Foto do Livro:", size=16),
                ft.Row(
                    [
                        drag_target,
                        ft.Column(
                            [
                                ft.ElevatedButton(
                                    "Selecionar Imagem",
                                    on_click=lambda _: file_picker.pick_files()
                                ),
                            ],
                            spacing=10,
                        ),
                    ],
                    spacing=20,
                ),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Salvar Alterações",
                            on_click=lambda _: salvar_alteracoes()
                        ),
                        ft.ElevatedButton(
                            "Excluir Livro",
                            on_click=lambda _: excluir(),
                            bgcolor=ft.colors.RED_400,
                            color=ft.colors.WHITE,
                        ),
                    ],
                    spacing=20,
                ),
            ],
            spacing=20,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
