import flet as ft
from vistas.vista_compartido_conmigo import VistaCompartidoConmigo

def main(page: ft.Page):
    page.title = "App Tareas - Compartido Conmigo"
    
    page.window.width = 1200
    page.window.height = 820
    page.window.min_width = 380
    page.window.min_height = 780
    page.padding = 0 
    
    vista = VistaCompartidoConmigo(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)