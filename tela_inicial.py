import flet as ft
# Importa as funções do banco de dados
from db import add_user, create_connection


def tela_inicial(page: ft.Page):
    page.title = "Tela 1: Login"
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
            add_user(conn, email, senha)  # Adiciona o usuário
            conn.close()
            print("Usuário adicionado:", email)

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
