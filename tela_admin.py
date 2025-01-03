import flet as ft
import editor_usuarios
import tela_livros

def tela_admin(page: ft.Page, on_exit):
    page.title = "Tela Admin"
    page.window.width = 1200
    page.window.height = 800
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    def navigate_to_users(e):
        page.clean()
        editor_usuarios.tela_config(page, lambda: tela_admin(page, on_exit))

    def navigate_to_livros(e):
        page.clean()
        tela_livros.main(page, lambda: tela_admin(page, on_exit))

    def create_menu_item(icon_name: str, text: str, on_click):
        return ft.Container(
            content=ft.ElevatedButton(
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
                style=ft.ButtonStyle(
                    bgcolor={"": ft.colors.TRANSPARENT},
                    shape=ft.RoundedRectangleBorder(radius=0),
                ),
                on_click=on_click,
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
                # Item de menu Usuários com ícone de pessoa
                create_menu_item(ft.icons.PERSON, "Usuários", navigate_to_users),
                # Item de menu Livros com ícone de livro
                create_menu_item(ft.icons.BOOK, "Livros", navigate_to_livros),
            ],
            spacing=0,
        ),
        bgcolor=ft.colors.BLUE,
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
        color=ft.colors.BLACK
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
            ),
            margin=ft.margin.only(left=250)
        )
    ])

    page.add(main_stack)

if __name__ == "__main__":
    def main(page: ft.Page):
        tela_admin(page, lambda: page.window_destroy())
    ft.app(target=main)