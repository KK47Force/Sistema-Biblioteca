import flet as ft
from db import add_user, create_connection
from tela_admin import tela_admin  # Importa a tela admin


def tela_inicial(page: ft.Page):
    page.title = "Tela 1: Login"
    page.window_width = 800
    page.window_height = 600
    page.bgcolor = ft.Colors.BLUE  # Atualiza para Colors

    # Centraliza a página
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Nome do sistema
    nome_sistema = ft.Text(
        "SISTEMA DE BIBLIOTECA",
        size=24,
        weight="bold",
        color=ft.Colors.WHITE  # Atualiza para Colors
    )

    # Campo de email
    email_label = ft.Text("EMAIL:", color=ft.Colors.WHITE)
    email_input = ft.TextField(
        hint_text="DIGITE O EMAIL",
        width=300,
        border_color=ft.Colors.WHITE  # Atualiza para Colors
    )

    # Campo de senha
    senha_label = ft.Text("SENHA:", color=ft.Colors.WHITE)
    senha_input = ft.TextField(
        hint_text="DIGITE A SENHA",
        width=300,
        password=True,
        border_color=ft.Colors.WHITE  # Atualiza para Colors
    )

    # Botão de login
    login_button = ft.ElevatedButton(
        text="Login",
        on_click=lambda e: handle_login(
            email_input.value, senha_input.value),  # Ação do botão
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLUE,
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    # Função para lidar com o login
    def handle_login(email, senha):
        conn = create_connection("usuarios.db")  # Conecta ao banco de dados
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM login WHERE email = ? AND senha = ?", (email, senha))
            user = cursor.fetchone()
            conn.close()

            if user:
                # Verifica o tipo do usuário
                if user[3] == 'admin':  # Supondo que o tipo está na quarta coluna
                    page.clean()  # Limpa a tela
                    # Chama a tela de admin
                    tela_admin(page, lambda: tela_inicial(page))
                else:

                    # Limpa a tela anterior
                    page.clean()  # Limpa a tela
                    # Exibe a tela de boas-vindas
                    page.add(
                        ft.Column(
                            [
                                ft.Text(f"Bem-vindo, {email}!",
                                        size=24, color=ft.Colors.WHITE),
                                ft.ElevatedButton(
                                    text="Sair",
                                    on_click=lambda e: page.clean() or tela_inicial(
                                        page),  # Volta para a tela de login
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.WHITE,
                                        color=ft.Colors.BLUE,
                                        shape=ft.RoundedRectangleBorder(
                                            radius=10)
                                    )
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20
                        )
                    )
            else:
                print("Email ou senha incorretos.")

    # Layout
    page.add(
        ft.Column(
            [
                nome_sistema,
                email_label,
                email_input,
                senha_label,
                senha_input,
                login_button  # Adiciona o botão de login
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centraliza verticalmente
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza horizontalmente
            spacing=20
        )
    )
