import flet as ft
from db import create_connection, get_todos_livros, get_foto_livro, update_livro, delete_livro

def main(page: ft.Page, on_exit):
    page.title = "Editar/Excluir Livro"
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
        content=ft.Text("Selecione um livro primeiro", 
                       size=12, 
                       text_align=ft.TextAlign.CENTER),
    )
    
    # Variável para armazenar o caminho da imagem e ID do livro
    caminho_imagem = None
    livro_selecionado = None
    
    def selecionar_arquivo(e: ft.FilePickerResultEvent):
        if e.files:
            nonlocal caminho_imagem
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
        on_result=selecionar_arquivo
    )
    page.overlay.append(file_picker)
    
    def on_drag_accept(e: ft.DragTargetAcceptEvent):
        if e.data and "path" in e.data:
            nonlocal caminho_imagem
            caminho_imagem = e.data["path"]
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
    
    # Função para carregar os dados do livro selecionado
    def carregar_livro(e):
        nonlocal livro_selecionado, caminho_imagem
        if not e.control.value:
            return
            
        livro_selecionado = e.control.value
        conn = create_connection("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM livros WHERE id = ?", (livro_selecionado,))
        livro = cursor.fetchone()
        conn.close()
        
        if livro:
            nome_livro.value = livro[1]  # título
            nota.value = str(livro[2])  # avaliação
            quantidade.value = str(livro[3])  # quantidade
            caminho_imagem = livro[4]  # caminho da imagem
            
            # Atualiza a imagem
            if caminho_imagem:
                img_preview.content = ft.Image(
                    src=caminho_imagem,
                    width=200,
                    height=300,
                    fit=ft.ImageFit.CONTAIN,
                )
            else:
                img_preview.content = ft.Text("Sem imagem", 
                                            size=12, 
                                            text_align=ft.TextAlign.CENTER)
            
            page.update()
    
    # Função para editar o livro
    def editar_livro(e):
        try:
            if not livro_selecionado:
                raise ValueError("Selecione um livro primeiro")
                
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
            
            # Atualiza no banco de dados
            conn = create_connection("usuarios.db")
            sucesso = update_livro(conn, 
                                 livro_selecionado, 
                                 nome_livro.value, 
                                 nota_valor, 
                                 quantidade_valor, 
                                 caminho_imagem)
            conn.close()
            
            if not sucesso:
                raise Exception("Erro ao atualizar livro no banco de dados")
            
            # Mostra mensagem de sucesso
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Livro atualizado com sucesso!"))
            )
            
            # Volta para a tela de livros após 1 segundo
            page.window.set_timeout(lambda: (page.controls.clear(), on_exit()), 1000)
            
        except ValueError as e:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text(str(e)))
            )
        except Exception as e:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text(f"Erro ao atualizar livro: {str(e)}"))
            )
    
    # Função para excluir o livro
    def excluir_livro(e):
        try:
            if not livro_selecionado:
                raise ValueError("Selecione um livro primeiro")
            
            # Confirma a exclusão
            def confirmar_exclusao(e):
                try:
                    # Remove do banco de dados
                    conn = create_connection("usuarios.db")
                    sucesso = delete_livro(conn, livro_selecionado)
                    conn.close()
                    
                    if not sucesso:
                        raise Exception("Erro ao excluir livro do banco de dados")
                    
                    # Fecha o diálogo
                    dlg_modal.open = False
                    page.update()
                    
                    # Mostra mensagem de sucesso
                    page.show_snack_bar(
                        ft.SnackBar(content=ft.Text("Livro excluído com sucesso!"))
                    )
                    
                    # Volta para a tela de livros após 1 segundo
                    page.window.set_timeout(lambda: (page.controls.clear(), on_exit()), 1000)
                    
                except Exception as e:
                    page.show_snack_bar(
                        ft.SnackBar(content=ft.Text(f"Erro ao excluir livro: {str(e)}"))
                    )
            
            # Diálogo de confirmação
            dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirmar exclusão"),
                content=ft.Text("Tem certeza que deseja excluir este livro?"),
                actions=[
                    ft.TextButton("Sim", on_click=confirmar_exclusao),
                    ft.TextButton("Não", on_click=lambda e: setattr(dlg_modal, 'open', False) or page.update()),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()
            
        except ValueError as e:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text(str(e)))
            )
        except Exception as e:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text(f"Erro ao excluir livro: {str(e)}"))
            )
    
    # Recupera todos os livros
    conn = create_connection("usuarios.db")
    livros = get_todos_livros(conn)
    conn.close()
    
    # Dropdown para selecionar o livro
    dropdown_livros = ft.Dropdown(
        label="Selecione um livro",
        width=400,
        options=[ft.dropdown.Option(key=str(livro[0]), text=livro[1]) for livro in livros],
        on_change=carregar_livro
    )
    
    # Botões
    botoes = ft.Row(
        [
            ft.ElevatedButton(
                "Voltar",
                on_click=lambda _: (page.controls.clear(), on_exit()),
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.BLUE,
                    color=ft.colors.WHITE,
                )
            ),
            ft.ElevatedButton(
                "Editar",
                on_click=editar_livro,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.BLUE,
                    color=ft.colors.WHITE,
                )
            ),
            ft.ElevatedButton(
                "Excluir",
                on_click=excluir_livro,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.RED,
                    color=ft.colors.WHITE,
                )
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    
    # Layout principal com ScrollableColumn
    conteudo = ft.Column(
        [
            ft.Text("Editar/Excluir Livro", size=24, weight=ft.FontWeight.BOLD),
            dropdown_livros,
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
            botoes,
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
