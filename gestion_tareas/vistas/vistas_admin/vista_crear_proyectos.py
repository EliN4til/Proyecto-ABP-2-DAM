import flet as ft
from datetime import datetime
from modelos.crud import crear_proyecto, obtener_todos_empleados

def VistaCrearProyecto(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_BTN_CREAR = "#4682B4"

    # Listas para almacenar datos reales de la BD
    empleados_db = []

    # --- LÓGICA DE DATOS Y FECHAS ---

    def cargar_datos_iniciales():
        """Carga la lista de empleados para el selector de responsables"""
        nonlocal empleados_db
        exito, resultado = obtener_todos_empleados()
        if exito:
            empleados_db = resultado
            dropdown_responsable.options = [
                ft.dropdownm2.Option(f"{emp.get('nombre', '')} {emp.get('apellidos', '')}") 
                for emp in empleados_db
            ]
            page.update()

    # Variables para almacenar las fechas seleccionadas
    fecha_inicio_val = [None]
    fecha_fin_val = [None]

    def on_fecha_inicio_change(e):
        if e.control.value:
            fecha_inicio_val[0] = e.control.value
            txt_fecha_inicio.value = e.control.value.strftime("%d/%m/%Y")
            page.update()

    def on_fecha_fin_change(e):
        if e.control.value:
            fecha_fin_val[0] = e.control.value
            txt_fecha_fin.value = e.control.value.strftime("%d/%m/%Y")
            page.update()

    # Funciones para abrir los selectores de fecha
    def abrir_picker_inicio(e):
        date_picker_inicio.open = True
        page.update()

    def abrir_picker_fin(e):
        date_picker_fin.open = True
        page.update()

    # Componentes de selección de fecha
    date_picker_inicio = ft.DatePicker(
        on_change=on_fecha_inicio_change,
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2030, 12, 31),
    )
    date_picker_fin = ft.DatePicker(
        on_change=on_fecha_fin_change,
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2030, 12, 31),
    )
    page.overlay.append(date_picker_inicio)
    page.overlay.append(date_picker_fin)

    def btn_volver_click(e):
        """Acción al hacer clic en el botón volver atrás - CORREGIDO A GESTIONAR PROYECTOS"""
        page.go("/gestionar_proyectos")

    def btn_crear_click(e):
        """Valida y guarda el nuevo proyecto en la base de datos real"""
        
        # 1. Validaciones
        if not input_nombre.value or not input_cliente.value:
            page.snack_bar = ft.SnackBar(ft.Text("❌ El nombre y el cliente son obligatorios"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        if not fecha_inicio_val[0] or not fecha_fin_val[0]:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Debes seleccionar las fechas del proyecto"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # 2. Procesar Presupuesto
        presupuesto_val = "0"
        if input_presupuesto.value:
            presupuesto_val = input_presupuesto.value.replace("€", "").strip()

        # 3. Preparar datos para MongoDB
        nuevo_proyecto = {
            "nombre": input_nombre.value,
            "codigo": input_codigo.value if input_codigo.value else f"PRY-{datetime.now().strftime('%H%M')}",
            "responsable": dropdown_responsable.value if dropdown_responsable.value else "Admin",
            "cliente": input_cliente.value,
            "presupuesto": f"{presupuesto_val} €",
            "estado": dropdown_estado.value if dropdown_estado.value else "ACTIVO",
            "fecha_inicio": fecha_inicio_val[0],
            "fecha_fin": fecha_fin_val[0],
            "descripcion": input_descripcion.value if input_descripcion.value else ""
        }

        # 4. Llamada al CRUD
        exito, resultado = crear_proyecto(nuevo_proyecto)

        if exito:
            page.snack_bar = ft.SnackBar(ft.Text(f"✅ Proyecto '{input_nombre.value}' creado correctamente"), bgcolor="green")
            page.snack_bar.open = True
            page.go("/gestionar_proyectos")
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error al guardar: {resultado}"), bgcolor="red")
            page.snack_bar.open = True
        
        page.update()

    # --- HELPERS DE INTERFAZ ---

    def crear_label(texto: str):
        return ft.Text(texto, size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500)

    # Botón volver
    btn_volver = ft.Container(
        content=ft.Text("←", size=24, color="white", weight=ft.FontWeight.BOLD),
        on_click=btn_volver_click,
        ink=True,
        padding=10,
    )

    # --- CONTROLES DEL FORMULARIO ---
    input_nombre = ft.TextField(
        hint_text="Nombre del proyecto",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=40,
        content_padding=ft.padding.only(left=10, right=10, top=8, bottom=8),
    )

    input_codigo = ft.TextField(
        hint_text="Ej: PRY-001",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=40,
        content_padding=ft.padding.only(left=10, right=10, top=8, bottom=8),
    )

    input_cliente = ft.TextField(
        hint_text="Nombre de la empresa cliente",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=40,
        content_padding=ft.padding.only(left=10, right=10, top=8, bottom=8),
    )

    input_presupuesto = ft.TextField(
        hint_text="0.00",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=40,
        content_padding=ft.padding.only(left=10, right=10, top=8, bottom=8),
        suffix=ft.Text("€", color=COLOR_LABEL),
        keyboard_type=ft.KeyboardType.NUMBER
    )

    input_descripcion = ft.TextField(
        hint_text="Descripción breve del proyecto...",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        multiline=True,
        min_lines=3,
        max_lines=3,
        content_padding=ft.padding.all(10),
    )

    dropdown_responsable = ft.DropdownM2(
        hint_text="Selecciona responsable...",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        bgcolor="white",
        border_color=COLOR_BORDE,
        border_radius=5,
        height=40,
        expand=True,
        content_padding=ft.padding.only(left=10, right=10),
        options=[]
    )

    dropdown_estado = ft.DropdownM2(
        hint_text="Estado...",
        value="ACTIVO",
        text_style=ft.TextStyle(size=12, color="black"),
        bgcolor="white",
        border_color=COLOR_BORDE,
        border_radius=5,
        height=40,
        expand=True,
        content_padding=ft.padding.only(left=10, right=10),
        options=[
            ft.dropdownm2.Option("ACTIVO"),
            ft.dropdownm2.Option("PAUSADO"),
            ft.dropdownm2.Option("INACTIVO"),
        ]
    )

    # Componentes visuales para las fechas
    txt_fecha_inicio = ft.Text("Seleccionar...", size=12, color="black")
    txt_fecha_fin = ft.Text("Seleccionar...", size=12, color="black")

    # Contenedor del formulario con Scroll
    formulario = ft.Column(
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Column([crear_label("Nombre del Proyecto *"), input_nombre], spacing=3),
            ft.Column([crear_label("Cliente / Empresa *"), input_cliente], spacing=3),
            
            ft.Row([
                ft.Column([crear_label("Código"), input_codigo], spacing=3, expand=True),
                ft.Column([crear_label("Presupuesto"), input_presupuesto], spacing=3, expand=True),
            ], spacing=10),

            ft.Column([crear_label("Responsable del Proyecto"), dropdown_responsable], spacing=3),
            
            ft.Row([
                ft.Column([
                    crear_label("Fecha Inicio"),
                    ft.Container(
                        content=ft.Row([ft.Icon(ft.Icons.CALENDAR_MONTH, size=16, color=COLOR_LABEL), txt_fecha_inicio]),
                        on_click=abrir_picker_inicio,
                        padding=10, border=ft.border.all(1, COLOR_BORDE), border_radius=5
                    )
                ], expand=True),
                ft.Column([
                    crear_label("Fecha Fin"),
                    ft.Container(
                        content=ft.Row([ft.Icon(ft.Icons.CALENDAR_MONTH, size=16, color=COLOR_LABEL), txt_fecha_fin]),
                        on_click=abrir_picker_fin,
                        padding=10, border=ft.border.all(1, COLOR_BORDE), border_radius=5
                    )
                ], expand=True),
            ], spacing=10),

            ft.Column([crear_label("Estado del Proyecto"), dropdown_estado], spacing=3),
            ft.Column([crear_label("Descripción"), input_descripcion], spacing=3),
        ]
    )

    # Botón Crear
    btn_crear = ft.Container(
        width=170,
        height=44,
        bgcolor=COLOR_BTN_CREAR,
        border_radius=22,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=btn_crear_click,
        content=ft.Text("Crear Proyecto", color="white", weight=ft.FontWeight.BOLD, size=14),
    )

    # Tarjeta Blanca Principal
    tarjeta_blanca = ft.Container(
        width=380,
        bgcolor="white",
        border_radius=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color=COLOR_SOMBRA, offset=ft.Offset(0, 5)),
        content=ft.Container(
            padding=ft.padding.only(left=18, right=18, top=55, bottom=20),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Container(height=520, content=formulario),
                    ft.Row([btn_crear], alignment=ft.MainAxisAlignment.CENTER),
                ]
            )
        )
    )

    # Header flotante
    header_flotante = ft.Container(
        width=220,
        height=50,
        bgcolor=COLOR_HEADER_BG,
        border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text("CREAR PROYECTO", size=18, weight=ft.FontWeight.BOLD, color="white")
    )

    # Layout de la vista
    contenido_superpuesto = ft.Container(
        width=380,
        height=680,
        content=ft.Stack(
            controls=[
                ft.Container(content=tarjeta_blanca, top=30),
                ft.Container(content=header_flotante, top=0, left=80)
            ]
        )
    )

    # --- INICIALIZACIÓN ---
    cargar_datos_iniciales()

    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[COLOR_FONDO_TOP, COLOR_FONDO_BOT],
        ),
        content=ft.Stack(
            expand=True,
            controls=[
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment(0, 0),
                    content=contenido_superpuesto
                ),
                ft.Container(
                    content=btn_volver,
                    top=10,
                    left=10,
                )
            ]
        )
    )

# Para probar directamente
def main(page: ft.Page):
    page.title = "App Tareas - Crear Proyecto"
    page.window.width = 420
    page.window.height = 800
    page.padding = 0 
    vista = VistaCrearProyecto(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)