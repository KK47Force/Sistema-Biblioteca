import flet as ft
import os
from db import create_connection, add_livro

def main(page: ft.Page, on_exit):
    page.title = "Adicionar Livro"
    page.window.width = 800
    page.window.height = 600
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Campos do formulário
    nome_livro = ft.TextField(label="Título do Livro", width=400)
    nota = ft.TextField(label="Avaliação (0-10)", width=400, keyboard_type=ft.KeyboardType.NUMBER)
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
    
    # Variável para armazenar o caminho da imagem
    caminho_imagem = None
    
    def selecionar_arquivo(e: ft.FilePickerResultEvent):
        if e.files:
            nonlocal caminho_imagem
            caminho_imagem = e.files[0].path
            # Atualiza a visualização da imagem
            img_preview.content = ft.Image(
                src=caminho_imagem,
                width=200,
                height=300,
                fit=ft.ImageFit.CONTAIN,
            )
            page.update()
    
    # File picker para selecionar imagem
    file_picker = ft.FilePicker(
        on_result=selecionar_arquivo
    )
    page.overlay.append(file_picker)
    
    def on_drag_accept(e: ft.DragTargetAcceptEvent):
        if e.data and "path" in e.data:
            nonlocal caminho_imagem
            caminho_imagem = e.data["path"]
            # Atualiza a visualização da imagem
            img_preview.content = ft.Image(
                src=caminho_imagem,
                width=200,
                height=300,
                fit=ft.ImageFit.CONTAIN,
            )
            page.update()
    
    # Drag target para arrastar imagem
    drag_target = ft.DragTarget(
        group="img",
        content=img_preview,
        on_accept=on_drag_accept,
    )
    
    def salvar_livro(e):
        try:
            # Valida os campos
            if not nome_livro.value:
                raise ValueError("Título do livro é obrigatório")
            if not nota.value:
                raise ValueError("Avaliação é obrigatória")
            if not quantidade.value:
                raise ValueError("Quantidade é obrigatória")
            
            # Converte nota e quantidade para números
            try:
                nota_valor = float(nota.value)
                if nota_valor < 0 or nota_valor > 10:
                    raise ValueError("Avaliação deve estar entre 0 e 10")
            except ValueError:
                raise ValueError("Avaliação deve ser um número válido")
            
            try:
                quantidade_valor = int(quantidade.value)
                if quantidade_valor < 0:
                    raise ValueError("Quantidade não pode ser negativa")
            except ValueError:
                raise ValueError("Quantidade deve ser um número inteiro")
            
            # Salva no banco de dados
            conn = create_connection("usuarios.db")
            livro_id = add_livro(conn, nome_livro.value, nota_valor, quantidade_valor, caminho_imagem)
            conn.close()
            
            if livro_id is None:
                raise Exception("Erro ao salvar no banco de dados")
            
            # Limpa os campos
            nome_livro.value = ""
            nota.value = ""
            quantidade.value = ""
            img_preview.content = ft.Text("Arraste uma imagem ou clique para selecionar", 
                                        size=12, 
                                        text_align=ft.TextAlign.CENTER)
            page.update()
            
            # Mostra mensagem de sucesso
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Livro adicionado com sucesso!"))
            )
            
            # Volta para a tela de livros após 1 segundo
            page.window.set_timeout(lambda: (page.controls.clear(), on_exit()), 1000)
            
        except ValueError as e:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text(str(e)))
            )
        except Exception as e:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text(f"Erro ao salvar livro: {str(e)}"))
            )
    
    # Botão voltar
    voltar_button = ft.ElevatedButton(
        "Voltar",
        on_click=lambda _: (page.controls.clear(), on_exit()),
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
        )
    )
    
    # Botão salvar
    salvar_button = ft.ElevatedButton(
        "Salvar",
        on_click=salvar_livro,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
        )
    )
    
    # Layout principal com ScrollableColumn
    conteudo = ft.Column(
        [
            ft.Text("Adicionar Livro", size=24, weight=ft.FontWeight.BOLD),
            nome_livro,
            nota,
            quantidade,
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Capa do Livro"),
                            drag_target,
                            ft.ElevatedButton(
                                "Selecionar Imagem",
                                on_click=lambda _: file_picker.pick_files(
                                    allow_multiple=False,
                                    allowed_extensions=["png", "jpg", "jpeg"]
                                )
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [voltar_button, salvar_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ],
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        height=page.window.height - 40,  # 40 é o padding total (20 * 2)
    )
    
    page.add(conteudo)

if __name__ == "__main__":
    def app_main(page: ft.Page):
        main(page, lambda: page.window_destroy())
    ft.app(target=app_main)
