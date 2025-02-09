import flet as ft
from datetime import datetime
import db
from editar_excluir_usuario import editar_usuarios, excluir_usuarios

def adicionar_usuarios(page: ft.Page, on_exit):
    def navegar_para(destino):
        """Função para navegar entre as telas"""
        page.controls.clear()  # Limpa todos os controles
        page.update()  # Atualiza a página para refletir a limpeza
        if destino == "adicionar":
            adicionar_usuarios(page, on_exit)
        elif destino == "editar":
            editar_usuarios(page, on_exit)
        elif destino == "excluir":
            excluir_usuarios(page, on_exit)
        elif destino == "voltar":
            on_exit()

    def criar_barra_lateral(page: ft.Page, navegar_para):
        """Cria a barra lateral padrão"""
        return ft.Container(
            width=200,
            height=page.height,
            bgcolor=ft.colors.BLUE,
            content=ft.Column(
                [
                    ft.Text("Menus", size=20, weight="bold", color=ft.colors.WHITE),
                    ft.TextButton(  # Mudado para TextButton
                        "Adicionar usuarios",
                        on_click=lambda e: navegar_para("adicionar"),
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,  # Apenas cor do texto
                            padding=10,  # Adicionado padding
                        ),
                    ),
                    ft.TextButton(  # Mudado para TextButton
                        "Editar usuarios",
                        on_click=lambda e: navegar_para("editar"),
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,  # Apenas cor do texto
                            padding=10,  # Adicionado padding
                        ),
                    ),
                    ft.TextButton(  # Mudado para TextButton
                        "Excluir usuarios",
                        on_click=lambda e: navegar_para("excluir"),
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,  # Apenas cor do texto
                            padding=10,  # Adicionado padding
                        ),
                    ),
                    ft.TextButton(  # Mudado para TextButton
                        "Voltar",
                        on_click=lambda e: navegar_para("voltar"),
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,  # Apenas cor do texto
                            padding=10,  # Adicionado padding
                        ),
                    ),
                ],
                spacing=0,  # Removido o espaçamento entre os botões
                expand=True,
            ),
            padding=ft.padding.only(top=20),  # Padding apenas no topo
        )

    page.title = "Adicionar Usuários"
    page.bgcolor = ft.colors.BLUE
    page.window_width = 800
    page.window_height = 600
    page.scroll = "auto"

    # Obter a data atual
    data_atual = datetime.now().strftime("%d/%m/%Y")

    def voltar_click(e):
        page.clean()
        on_exit()

    # Criar inputs com controle de estado
    def criar_input(label):
        if label == "Tipo de usuário:":
            return ft.Column(
                [
                    ft.Text(label, color=ft.colors.WHITE, size=14),
                    ft.Dropdown(
                        width=600,
                        height=40,
                        options=[
                            ft.dropdown.Option("admin"),
                            ft.dropdown.Option("usuario"),
                            ft.dropdown.Option("coordenador"),
                        ],
                        value="usuario",  # Valor padrão
                        text_size=14,
                    ),
                ],
                spacing=5,
            )
        return ft.Column(
            [
                ft.Text(label, color=ft.colors.WHITE, size=14),
                ft.TextField(
                    expand=True,
                    height=40,
                    password=True if label in ["Senha:", "Confirmar senha:"] else False
                ),
            ],
            spacing=5,
        )

    def mostrar_alerta(mensagem):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensagem),
            bgcolor=ft.colors.RED_400
        )
        page.snack_bar.open = True
        page.update()

    def cadastrar_usuario(e):
        # Obtendo os valores dos campos
        nome = form.controls[0].controls[1].value
        email = form.controls[1].controls[1].value
        confirmar_email = form.controls[2].controls[1].value
        senha = form.controls[3].controls[1].value
        confirmar_senha = form.controls[4].controls[1].value
        tipo_usuario = form.controls[5].controls[1].value  # Novo campo de tipo
        livros_emprestados = form.controls[6].controls[1].value or "0"
        livros_comprados = form.controls[7].controls[1].value or "0"
        cpf = form.controls[8].controls[1].value

        # Validações
        if not all([nome, email, confirmar_email, senha, confirmar_senha, cpf, tipo_usuario]):
            mostrar_alerta("Por favor, preencha todos os campos obrigatórios!")
            return

        if email != confirmar_email:
            mostrar_alerta("Os emails não correspondem!")
            return

        if senha != confirmar_senha:
            mostrar_alerta("As senhas não correspondem!")
            return

        try:
            # Conectar ao banco de dados
            conn = db.create_connection("usuarios.db")
            if conn:
                # Adicionar usuário
                db.add_user(
                    conn=conn,
                    email=email,
                    senha=senha,
                    tipo=tipo_usuario,  # Usando o tipo selecionado
                    nome=nome,
                    cpf=int(cpf)
                )
                conn.close()
                
                # Mostrar mensagem de sucesso
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Usuário cadastrado com sucesso!"),
                    bgcolor=ft.colors.GREEN_400
                )
                page.snack_bar.open = True
                page.update()

                # Limpar os campos
                for column in form.controls:
                    if isinstance(column, ft.Column) and len(column.controls) > 1:
                        if isinstance(column.controls[1], ft.Dropdown):
                            column.controls[1].value = "usuario"  # Resetar para o valor padrão
                        else:
                            column.controls[1].value = ""
                page.update()

        except Exception as e:
            mostrar_alerta(f"Erro ao cadastrar usuário: {str(e)}")

    # Layout do formulário
    form = ft.Column(
        [
            criar_input("Nome:"),
            criar_input("E-mail:"),
            criar_input("Confirmar e-mail:"),
            criar_input("Senha:"),
            criar_input("Confirmar senha:"),
            criar_input("Tipo de usuário:"),  # Novo campo
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
        scroll=ft.ScrollMode.AUTO,
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
                criar_barra_lateral(page, navegar_para),  # Usando a função para criar a barra lateral
                # Linha divisória
                ft.Container(
                    width=3,
                    height=page.height,
                    bgcolor=ft.colors.BLACK,
                ),
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
                        scroll=ft.ScrollMode.AUTO,
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
    page.scroll = "auto"

    def on_menu_click(e):
        if e.control.text == "Adicionar usuarios":
            page.clean()
            adicionar_usuarios(page, lambda: tela_config(page, on_exit))
        elif e.control.text == "Editar usuarios":
            page.clean()
            editar_usuarios(page, lambda: tela_config(page, on_exit))
        elif e.control.text == "Excluir usuarios":
            page.clean()
            excluir_usuarios(page, lambda: tela_config(page, on_exit))
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
                scroll=ft.ScrollMode.AUTO,
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