import flet as ft
from tela_inicial import tela_inicial  # Importa a função da tela inicial

def main(page: ft.Page):
    tela_inicial(page)  # Chama a função da tela inicial

ft.app(target=main)