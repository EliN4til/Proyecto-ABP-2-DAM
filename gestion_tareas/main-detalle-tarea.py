import flet as ft
from vistas.vista_detalle_tarea import VistaDetalleTarea

def main(page: ft.Page):
    page.title = "App Tareas - Detalle Tarea"
    
    page.window.width = 400
    page.window.height = 600
    page.window.min_width = 380
    page.window.min_height = 560
    page.padding = 0 
    
    vista = VistaDetalleTarea(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)