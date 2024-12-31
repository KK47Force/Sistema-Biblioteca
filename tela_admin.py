import flet as ft

def tela_admin(page: ft.Page, on_exit):
    page.title = "Tela Admin"
    page.bgcolor = ft.colors.BLUE
    page.window_width = 800
    page.window_height = 600

    def create_menu_item(icon_name: str, text: str):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        name=icon_name,
                        color=ft.colors.WHITE,
                        size=24,
                    ),
                    ft.Text(
                        text,
                        color=ft.colors.WHITE,
                        size=16,
                        weight="w500"
                    )
                ],
                spacing=10,
            ),
            padding=ft.padding.only(left=20, top=10, bottom=10),
            margin=ft.margin.only(bottom=5),
        )

    # Menu lateral
    sidebar = ft.Container(
        width=230,
        height=600,
        content=ft.Column(
            [
                # Título "Menus"
                ft.Container(
                    content=ft.Text(
                        "Menus",
                        size=20,
                        color=ft.colors.WHITE,
                        weight="bold"
                    ),
                    padding=ft.padding.only(left=20, top=20, bottom=20),
                ),
                # Item de menu Usuários com ícone de engrenagem
                create_menu_item(ft.icons.SETTINGS, "Usuários"),
            ],
            spacing=0,
        ),
    )

    # Linha vertical preta
    vertical_line = ft.Container(
        width=3,
        height=600,
        bgcolor=ft.colors.BLACK,
        alignment=ft.alignment.center_left,
        margin=ft.margin.only(left=230)
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
        sidebar,  # Menu lateral adicionado
        vertical_line,
        ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=welcome_message,
                        expand=True,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=sair_button,
                        padding=ft.padding.only(right=10, top=10)
                    )
                ],
            )
        )
    ])

    page.add(main_stack)