import flet as ft


def tela_config(page: ft.Page, on_exit):
    page.title = "Tela Admin"
    page.bgcolor = ft.colors.BLUE
    page.window_width = 800
    page.window_height = 600

    def on_menu_click(e):
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
        ),
        expand=True,
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
    )
])

    page.add(main_stack)

