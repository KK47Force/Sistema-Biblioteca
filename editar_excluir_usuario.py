import flet as ft
import db
from datetime import datetime

def get_all_users():
    """Retorna todos os usuários do banco de dados"""
    conn = db.create_connection("usuarios.db")
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login")
        users = cursor.fetchall()
        conn.close()
        return users
    return []

def mostrar_dialogo(page: ft.Page, titulo, mensagem, on_confirm):
    """Função global para mostrar diálogo de confirmação"""
    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text(titulo),
        content=ft.Text(mensagem),
        actions=[
            ft.TextButton(
                "Sim",
                on_click=lambda e: (
                    setattr(dlg, 'open', False),
                    page.update(),
                    on_confirm()
                ),
            ),
            ft.TextButton(
                "Não",
                on_click=lambda e: (
                    setattr(dlg, 'open', False),
                    page.update()
                ),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.dialog = dlg
    dlg.open = True
    page.update()

def mostrar_alerta(page: ft.Page, mensagem, cor=ft.colors.RED_400):
    """Função global para mostrar alertas"""
    page.snack_bar = ft.SnackBar(
        content=ft.Text(mensagem),
        bgcolor=cor
    )
    page.snack_bar.open = True
    page.update()

def editar_usuarios(page: ft.Page, on_exit):
    page.title = "Editar Usuários"
    page.bgcolor = ft.colors.BLUE
    page.window_width = 800
    page.window_height = 600
    page.scroll = "auto"

    def voltar_click(e):
        page.clean()
        on_exit()

    def criar_input(label, valor_inicial="", is_password=False, on_submit=None):
        """Cria um campo de entrada com botão de confirmação"""
        input_field = ft.TextField(
            value=str(valor_inicial) if valor_inicial is not None else "",
            expand=True,
            height=40,
            password=is_password,
            on_submit=lambda e: on_submit(e, input_field) if on_submit else None,  
        )
        
        confirm_button = ft.IconButton(
            icon=ft.icons.CHECK_CIRCLE_OUTLINE,
            icon_color=ft.colors.GREEN_400,
            tooltip="Confirmar alteração",
            on_click=lambda e: on_submit(e, input_field) if on_submit else None,  
        )
        
        return ft.Column(
            [
                ft.Text(label, color=ft.colors.WHITE, size=14),
                ft.Row(
                    [
                        input_field,
                        confirm_button,
                    ],
                    spacing=5,
                ),
            ],
            spacing=5,
        )

    def criar_dropdown_tipo(valor_inicial="usuario", on_submit=None):
        """Cria um dropdown com botão de confirmação"""
        dropdown = ft.Dropdown(
            width=550,  
            height=40,
            options=[
                ft.dropdown.Option("admin"),
                ft.dropdown.Option("usuario"),
                ft.dropdown.Option("coordenador"),
            ],
            value=valor_inicial,
            text_size=14,
            on_change=lambda e: None,  
        )
        
        confirm_button = ft.IconButton(
            icon=ft.icons.CHECK_CIRCLE_OUTLINE,
            icon_color=ft.colors.GREEN_400,
            tooltip="Confirmar alteração",
            on_click=lambda e: on_submit(e, dropdown) if on_submit else None,  
        )
        
        return ft.Column(
            [
                ft.Text("Tipo de usuário:", color=ft.colors.WHITE, size=14),
                ft.Row(
                    [
                        dropdown,
                        confirm_button,
                    ],
                    spacing=5,
                ),
            ],
            spacing=5,
        )

    def atualizar_usuario(user_id, campo, novo_valor):
        """Atualiza um campo específico do usuário no banco de dados"""
        try:
            conn = db.create_connection("usuarios.db")
            if conn:
                cursor = conn.cursor()
                if campo in ['cpf', 'livros_emprestados', 'livros_comprados']:
                    novo_valor = int(novo_valor)
                cursor.execute(f"UPDATE login SET {campo} = ? WHERE id = ?", (novo_valor, user_id))
                conn.commit()
                conn.close()
                mostrar_alerta(page, "Informação atualizada com sucesso!", ft.colors.GREEN_400)
                return True
        except Exception as e:
            mostrar_alerta(page, f"Erro ao atualizar: {str(e)}")
            return False

    def on_field_submit(e, user_id, campo, valor_atual, input_field):
        """Chamado quando um campo é submetido (Enter ou botão)"""
        novo_valor = input_field.value  
        if str(valor_atual) != str(novo_valor):
            mostrar_dialogo(
                page,
                "Confirmação",
                f"Deseja alterar o campo {campo} para {novo_valor}?",
                lambda: atualizar_usuario(user_id, campo, novo_valor)
            )

    def criar_formulario_edicao(user_data):
        """Cria formulário de edição para um usuário"""
        user_id, email, senha, tipo, nome, cpf, livros_emprestados, livros_comprados, data_criacao = user_data
        
        campos = {
            'nome': nome,
            'email': email,
            'senha': senha,
            'tipo': tipo,
            'cpf': cpf,
            'livros_emprestados': livros_emprestados,
            'livros_comprados': livros_comprados
        }
        
        form = ft.Column(
            [
                criar_input(
                    "Nome:", 
                    campos['nome'],
                    on_submit=lambda e, field, c='nome', v=campos['nome']: on_field_submit(e, user_id, c, v, field)
                ),
                criar_input(
                    "E-mail:", 
                    campos['email'],
                    on_submit=lambda e, field, c='email', v=campos['email']: on_field_submit(e, user_id, c, v, field)
                ),
                criar_input(
                    "Senha:", 
                    campos['senha'],
                    True,
                    on_submit=lambda e, field, c='senha', v=campos['senha']: on_field_submit(e, user_id, c, v, field)
                ),
                criar_dropdown_tipo(
                    campos['tipo'],
                    on_submit=lambda e, field, c='tipo', v=campos['tipo']: on_field_submit(e, user_id, c, v, field)
                ),
                criar_input(
                    "CPF:", 
                    campos['cpf'],
                    on_submit=lambda e, field, c='cpf', v=campos['cpf']: on_field_submit(e, user_id, c, v, field)
                ),
                criar_input(
                    "Livros emprestados:", 
                    campos['livros_emprestados'],
                    on_submit=lambda e, field, c='livros_emprestados', v=campos['livros_emprestados']: on_field_submit(e, user_id, c, v, field)
                ),
                criar_input(
                    "Livros comprados:", 
                    campos['livros_comprados'],
                    on_submit=lambda e, field, c='livros_comprados', v=campos['livros_comprados']: on_field_submit(e, user_id, c, v, field)
                ),
                ft.Row(
                    [
                        ft.Text("Data de criação:", color=ft.colors.WHITE, size=14, expand=True),
                        ft.Text(data_criacao, color=ft.colors.WHITE, size=14),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        )

        return form

    def on_user_select(e):
        """Quando um usuário é selecionado da lista"""
        if e.control.value:
            selected_user = next((user for user in users if str(user[0]) == e.control.value), None)
            if selected_user:
                content.content = criar_formulario_edicao(selected_user)
                page.update()

    users = get_all_users()
    
    user_dropdown = ft.Dropdown(
        width=600,
        label="Selecione um usuário",
        options=[ft.dropdown.Option(key=str(user[0]), text=f"{user[4]} ({user[1]})") for user in users],
        on_change=on_user_select
    )

    content = ft.Container(expand=True)

    page.add(
        ft.Row(
            [
                ft.Container(
                    width=200,
                    height=page.height,
                    bgcolor=ft.colors.BLUE,
                    content=ft.Column(
                        [
                            ft.Text("Menus", size=20, weight="bold", color=ft.colors.WHITE),
                            ft.ElevatedButton(
                                "Adicionar usuarios",
                                on_click=voltar_click,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.BLUE,
                                    color=ft.colors.WHITE,
                                ),
                            ),
                            ft.ElevatedButton(
                                "Editar usuarios",
                                on_click=voltar_click,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.BLUE,
                                    color=ft.colors.WHITE,
                                ),
                            ),
                            ft.ElevatedButton(
                                "Excluir usuarios",
                                on_click=voltar_click,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.BLUE,
                                    color=ft.colors.WHITE,
                                ),
                            ),
                            ft.ElevatedButton(
                                "Voltar",
                                on_click=voltar_click,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.BLUE,
                                    color=ft.colors.WHITE,
                                ),
                            ),
                        ],
                        spacing=20,
                        expand=True,
                    ),
                    padding=20,
                ),
                ft.Container(
                    width=3,
                    height=page.height,
                    bgcolor=ft.colors.BLACK,
                ),
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text("Bem-vindo, Admin!", size=24, weight="bold", color=ft.colors.WHITE, expand=True),
                                    ft.ElevatedButton(
                                        text="Sair",
                                        on_click=lambda e: (page.clean(), on_exit()),
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.colors.WHITE,
                                            color=ft.colors.BLUE,
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                            user_dropdown,
                            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                            content,
                        ],
                        spacing=20,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    padding=ft.padding.symmetric(horizontal=20),
                ),
            ],
            spacing=0,
        )
    )

def excluir_usuarios(page: ft.Page, on_exit):
    page.title = "Excluir Usuários"
    page.bgcolor = ft.colors.BLUE
    page.window_width = 800
    page.window_height = 600
    page.scroll = "auto"

    def voltar_click(e):
        page.clean()
        on_exit()

    def excluir_usuario(user_id):
        """Exclui um usuário do banco de dados"""
        try:
            conn = db.create_connection("usuarios.db")
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM login WHERE id = ?", (user_id,))
                conn.commit()
                conn.close()
                mostrar_alerta(page, "Usuário excluído com sucesso!", ft.colors.GREEN_400)
                atualizar_lista_usuarios()
        except Exception as e:
            mostrar_alerta(page, f"Erro ao excluir usuário: {str(e)}")

    def criar_card_usuario(user):
        """Cria um card para exibir informações do usuário"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.PERSON),
                            title=ft.Text(f"Nome: {user[4]}", size=16),
                            subtitle=ft.Text(f"Email: {user[1]}\nTipo: {user[3]}", size=14),
                        ),
                        ft.Row(
                            [
                                ft.TextButton(
                                    "Excluir",
                                    on_click=lambda e, u=user: mostrar_dialogo(
                                        page,
                                        "Confirmação",
                                        f"Tem certeza que deseja excluir o usuário {u[4]}?",
                                        lambda: excluir_usuario(u[0])
                                    ),
                                    style=ft.ButtonStyle(
                                        color=ft.colors.RED_400,
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                padding=10,
            )
        )

    def atualizar_lista_usuarios():
        """Atualiza a lista de usuários"""
        users = get_all_users()
        lista_usuarios.controls = [criar_card_usuario(user) for user in users]
        page.update()

    lista_usuarios = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
    atualizar_lista_usuarios()

    page.add(
        ft.Row(
            [
                ft.Container(
                    width=200,
                    height=page.height,
                    bgcolor=ft.colors.BLUE,
                    content=ft.Column(
                        [
                            ft.Text("Menus", size=20, weight="bold", color=ft.colors.WHITE),
                            ft.ElevatedButton(
                                "Adicionar usuarios",
                                on_click=voltar_click,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.BLUE,
                                    color=ft.colors.WHITE,
                                ),
                            ),
                            ft.ElevatedButton(
                                "Editar usuarios",
                                on_click=voltar_click,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.BLUE,
                                    color=ft.colors.WHITE,
                                ),
                            ),
                            ft.ElevatedButton(
                                "Excluir usuarios",
                                on_click=voltar_click,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.BLUE,
                                    color=ft.colors.WHITE,
                                ),
                            ),
                            ft.ElevatedButton(
                                "Voltar",
                                on_click=voltar_click,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.BLUE,
                                    color=ft.colors.WHITE,
                                ),
                            ),
                        ],
                        spacing=20,
                        expand=True,
                    ),
                    padding=20,
                ),
                ft.Container(
                    width=3,
                    height=page.height,
                    bgcolor=ft.colors.BLACK,
                ),
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text("Bem-vindo, Admin!", size=24, weight="bold", color=ft.colors.WHITE, expand=True),
                                    ft.ElevatedButton(
                                        text="Sair",
                                        on_click=lambda e: (page.clean(), on_exit()),
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.colors.WHITE,
                                            color=ft.colors.BLUE,
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                            lista_usuarios,
                        ],
                        spacing=20,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    padding=ft.padding.symmetric(horizontal=20),
                ),
            ],
            spacing=0,
        )
    )
