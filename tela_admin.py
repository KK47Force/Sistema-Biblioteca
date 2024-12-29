import flet as ft


def tela_admin(page: ft.Page, on_exit):
    page.title = "Tela Admin"
    page.bgcolor = ft.Colors.BLUE  # Cor de fundo

    # Centraliza a página
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Mensagem de boas-vindas
    welcome_message = ft.Text(
        "Bem-vindo, Admin!",
        size=24,
        weight="bold",
        color=ft.Colors.WHITE
    )

    # Layout
    page.add(
        ft.Column(
            [
                welcome_message,
                ft.Container(height=20),  # Adiciona um espaço fixo
                ft.ElevatedButton(
                    text="Sair",
                    on_click=lambda e: on_exit(),  # Chama a função de saída
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.WHITE,
                        color=ft.Colors.BLUE,
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )
