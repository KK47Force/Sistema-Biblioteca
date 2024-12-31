import flet as ft
from datetime import datetime

def adicionar_usuarios(page: ft.Page, on_exit):
    page.title = "Adicionar Usuários"
    page.bgcolor = ft.colors.BLUE
    page.window_width = 800
    page.window_height = 600
    page.scroll = "auto"  # Adiciona scroll à página

    # Obter a data atual
    data_atual = datetime.now().strftime("%d/%m/%Y")

    def voltar_click(e):
        page.clean()
        on_exit()  # Retorna à tela anterior

    def cadastrar_usuario(e):
        # Lógica para cadastrar o usuário pode ser implementada aqui
        page.snack_bar = ft.SnackBar(ft.Text("Usuário cadastrado com sucesso!"))
        page.snack_bar.open = True
        page.update()

    # Criar inputs
    def criar_input(label):
        return ft.Column(
            [
                ft.Text(label, color=ft.colors.WHITE, size=14),
                ft.TextField(expand=True, height=40),
            ],
            spacing=5,
        )

    # Layout do formulário
    form = ft.Column(
        [
            criar_input("Nome:"),
            criar_input("E-mail:"),
            criar_input("Confirmar e-mail:"),
            criar_input("Senha:"),
            criar_input("Confirmar senha:"),
            criar_input("Livros emprestados:"),
            criar_input("Livros comprados:"),
            criar_input("CPF:"),
            ft.Row(
                [
                    ft.Text("Data de criação:", color=ft.colors.WHITE, size=14, expand=True),
                    ft.Text(data_atual, color=ft.colors.WHITE, size=14),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ],
        spacing=20,
        scroll=ft.ScrollMode.AUTO,  # Adiciona scroll ao formulário
    )

    # Cabeçalho
    header = ft.Row(
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
        expand=False,
    )

    # Botão de cadastrar
    cadastrar_button = ft.ElevatedButton(
        text="Cadastrar usuário",
        on_click=cadastrar_usuario,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.WHITE,
            color=ft.colors.BLUE,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )

    # Layout principal
    page.add(
        ft.Row(
            [
                # Sidebar
                ft.Container(
                    width=200,
                    height=600,
                    bgcolor=ft.colors.BLUE,
                    content=ft.Column(
                        [
                            ft.Text("Menus", size=20, weight="bold", color=ft.colors.WHITE),
                            ft.ElevatedButton("Voltar", on_click=voltar_click),
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                    ),
                    padding=20,
                ),
                # Linha divisória
                ft.Container(width=3, height=600, bgcolor=ft.colors.BLACK),
                # Conteúdo principal
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        [
                            header,
                            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                            form,
                            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                            ft.Container(content=cadastrar_button, alignment=ft.alignment.center),
                        ],
                        spacing=20,
                        scroll=ft.ScrollMode.AUTO,  # Adiciona scroll ao conteúdo principal
                    ),
                    padding=ft.padding.symmetric(horizontal=20),
                ),
            ],
            spacing=0,
        )
    )

def tela_config(page: ft.Page, on_exit):
    page.title = "Tela Admin"
    page.bgcolor = ft.colors.BLUE
    page.window_width = 800
    page.window_height = 600
    page.scroll = "auto"  # Adiciona scroll à página

    def on_menu_click(e):
        if e.control.text == "Adicionar usuarios":
            page.clean()
            adicionar_usuarios(page, lambda: tela_config(page, on_exit))
        elif e.control.text == "Voltar":
            page.clean()
            on_exit()
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"{e.control.text} clicado!"))
            page.snack_bar.open = True
            page.update()

    def create_menu_button(text):
        return ft.ElevatedButton(
            text=text,
            on_click=on_menu_click,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=4),
                padding=ft.padding.symmetric(horizontal=10, vertical=8),
            ),
        )

    # Menu lateral
    sidebar = ft.Container(
        width=200,
        height=600,
        bgcolor=ft.colors.BLUE,
        content=ft.Column(
            [
                ft.Text("Menus", size=20, weight="bold", color=ft.colors.WHITE),
                create_menu_button("Adicionar usuarios"),
                create_menu_button("Editar usuarios"),
                create_menu_button("Excluir usuarios"),
                create_menu_button("Voltar"),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=20,
    )

    # Linha divisória
    vertical_line = ft.Container(
        width=3, height=600, bgcolor=ft.colors.BLACK, margin=ft.margin.only(left=230)
    )

    # Mensagem de boas-vindas
    welcome_message = ft.Text(
        "Bem-vindo, Admin!",
        size=24,
        weight="bold",
        color=ft.colors.WHITE
    )

    # Botão Sair
    sair_button = ft.ElevatedButton(
        text="Sair",
        on_click=lambda e: (page.clean(), on_exit()),
        style=ft.ButtonStyle(
            bgcolor=ft.colors.WHITE,
            color=ft.colors.BLUE,
            shape=ft.RoundedRectangleBorder(radius=8)
        )
    )

    # Layout principal usando Stack para sobreposição
    main_stack = ft.Stack([
        sidebar,  # Menu lateral
        vertical_line,  # Linha divisória
        ft.Container(
            content=ft.Column(
                [
                    # Cabeçalho no topo com mensagem de boas-vindas e botão "Sair"
                    ft.Row(
                        [
                            ft.Container(
                                content=welcome_message,  # Mensagem de boas-vindas
                                expand=True,
                                alignment=ft.alignment.center,
                            ),
                            ft.Container(
                                content=sair_button,  # Botão "Sair"
                                alignment=ft.alignment.center_right,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        expand=False,
                    ),
                    # Espaço vazio para expandir o restante
                    ft.Container(expand=True),
                ],
                expand=True,
                spacing=0,
                alignment=ft.MainAxisAlignment.START,
                scroll=ft.ScrollMode.AUTO,  # Adiciona scroll ao conteúdo principal
            ),
            expand=True,
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
        )
    ])

    page.add(main_stack)

def main(page: ft.Page):
    tela_config(page, lambda: page.window_close())

if __name__ == "__main__":
    ft.app(target=main)