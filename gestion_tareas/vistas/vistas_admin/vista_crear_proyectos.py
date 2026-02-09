import flet as ft
import inspect
from datetime import datetime
from gestion_tareas.modelos.crud import crear_proyecto, crear_departamento, obtener_todos_empleados, obtener_todos_proyectos, obtener_todos_departamentos

def VistaCrearProyecto(page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_BTN_CREAR = "#4682B4"
    COLOR_VERDE = "#4CAF50"
    COLOR_ROJO = "#E53935"

    # Listas para almacenar datos reales de la BD
    empleados_db = []
    proyectos_db = []

    # --- LÓGICA DE DATOS Y FECHAS ---

    def cargar_datos_iniciales():
        """Carga la lista de empleados para el selector de responsables y los proyectos para el contador"""
        nonlocal empleados_db, proyectos_db
        exito_e, resultado_e = obtener_todos_empleados()
        if exito_e:
            empleados_db = resultado_e
            dropdown_responsable.options = [
                ft.dropdownm2.Option(f"{emp.get('nombre', '')} {emp.get('apellidos', '')}") 
                for emp in empleados_db
            ]
        
        exito_p, resultado_p = obtener_todos_proyectos()
        if exito_p:
            proyectos_db = resultado_p
            
        page.update()

    # Variables para almacenar las fechas seleccionadas
    fecha_inicio_val = [None]
    fecha_fin_val = [None]

    def on_fecha_inicio_change(e):
        if e.control.value:
            fecha_inicio_val[0] = e.control.value
            txt_fecha_inicio.value = e.control.value.strftime("%d/%m/%Y")
            txt_fecha_inicio.color = "black"
            page.update()

    def on_fecha_fin_change(e):
        if e.control.value:
            fecha_fin_val[0] = e.control.value
            txt_fecha_fin.value = e.control.value.strftime("%d/%m/%Y")
            txt_fecha_fin.color = "black"
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

    async def btn_volver_click(e):
        await page.push_route("/gestionar_proyectos")

    def mostrar_mensaje_dialog(page, titulo, mensaje, color, on_close=None):
        """Muestra un diálogo de alerta visible compatible con versiones antiguas"""
        async def cerrar_y_seguir(e):
            dlg.open = False
            page.update()
            if on_close:
                if callable(on_close):
                    if inspect.iscoroutinefunction(on_close):
                        await on_close()
                    else:
                        on_close()

        dlg = ft.AlertDialog(
            title=ft.Text(titulo, color="black", weight="bold"),
            content=ft.Text(mensaje, color="black", size=14),
            bgcolor="white",
            actions=[
                ft.TextButton("Entendido", on_click=cerrar_y_seguir)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()


    # ============================================
    # CREAR PROYECTO CON DEPARTAMENTOS
    # ============================================

    async def btn_crear_click(e):
        """Valida y guarda el nuevo proyecto con sus departamentos en la base de datos"""
        nonlocal proyectos_db
        
        # 1. Validaciones
        if not input_nombre.value or not input_cliente.value:
            mostrar_mensaje_dialog(page, "⚠️ Campos obligatorios", "❌ El nombre y el cliente son obligatorios", "red")
            page.update()
            return

        if not fecha_inicio_val[0] or not fecha_fin_val[0]:
            mostrar_mensaje_dialog(page, "⚠️ Campos obligatorios", "❌ Debes seleccionar las fechas del proyecto", "red")
            page.update()
            return

        if fecha_fin_val[0] < fecha_inicio_val[0]:
            mostrar_mensaje_dialog(page, "📅 Error en Fechas", "❌ La fecha de fin no puede ser anterior a la fecha de inicio", "red")
            page.update()
            return

        # 2. Procesar Presupuesto
        presupuesto_val = 0.0
        if input_presupuesto.value:
            try:
                # Limpiar cualquier símbolo o espacio y convertir a float
                limpio = input_presupuesto.value.replace("€", "").replace(",", ".").strip()
                if limpio:
                    presupuesto_val = float(limpio)
            except ValueError:
                 mostrar_mensaje_dialog(page, "❌ Error de Formato", "El presupuesto debe ser un número válido", "red")
                 page.update()
                 return

        # 3. Preparar datos para MongoDB
        nombre_proyecto = input_nombre.value.strip()
        
        if not input_codigo.value:
            contador = len(proyectos_db) + 1
            nuevo_codigo = f"PRY-{contador:03d}"
            # Verificar si existe y buscar el siguiente libre
            while any(p["codigo"] == nuevo_codigo for p in proyectos_db):
                contador += 1
                nuevo_codigo = f"PRY-{contador:03d}"
        else:
            nuevo_codigo = input_codigo.value

        nuevo_proyecto = {
            "nombre": nombre_proyecto,
            "codigo": nuevo_codigo,
            "responsable": dropdown_responsable.value if dropdown_responsable.value else "Admin",
            "cliente": input_cliente.value,
            "presupuesto": presupuesto_val,
            "estado": dropdown_estado.value if dropdown_estado.value else "ACTIVO",
            "fecha_inicio": fecha_inicio_val[0],
            "fecha_fin": fecha_fin_val[0],
            "descripcion": input_descripcion.value if input_descripcion.value else "",
            "fecha_creacion": datetime.now(),
        }

        # Limpiar errores previos
        input_nombre.error_text = None
        input_codigo.error_text = None
        input_cliente.error_text = None
        input_presupuesto.error_text = None
        page.update()

        # 4. Crear el proyecto
        exito, resultado = crear_proyecto(nuevo_proyecto)

        if not exito:
            if isinstance(resultado, list):
                errores_texto = []
                for err in resultado:
                    campo = err["loc"][0]
                    msg = err["msg"]
                    
                    if campo == "nombre": input_nombre.error_text = msg
                    elif campo == "codigo": input_codigo.error_text = msg
                    elif campo == "cliente": input_cliente.error_text = msg
                    elif campo == "presupuesto": input_presupuesto.error_text = msg
                    else:
                        errores_texto.append(f"{campo}: {msg}")
                
                page.update()
                
                if errores_texto:
                    mostrar_mensaje_dialog(page, "❌ Error de Validación", f"❌ Error: {', '.join(errores_texto)}", "red")
                    page.update()
            else:
                mostrar_mensaje_dialog(page, "❌ Error de Sistema", f"❌ Error al guardar proyecto: {resultado}", "red")
                page.update()
            return

        # 5. Mensaje de éxito o advertencia
        async def ir_a_gestion():
            await page.push_route("/gestionar_proyectos")
            page.update()

        mostrar_mensaje_dialog(page, "✅ Éxito", f"✅ Proyecto '{nombre_proyecto}' creado correctamente", "green", on_close=ir_a_gestion)
        page.update()

    # --- HELPERS DE INTERFAZ ---

    def crear_label(texto, obligatorio: bool = False):
        if obligatorio:
            return ft.Row([
                ft.Text(texto, size=11, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                ft.Text("*", size=11, color=COLOR_ROJO, weight=ft.FontWeight.BOLD),
            ], spacing=2)
        return ft.Text(texto, size=11, color=COLOR_LABEL, weight=ft.FontWeight.W_500)

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
        content_padding=ft.Padding(left=10, right=10, top=8, bottom=8),
    )

    input_codigo = ft.TextField(
        hint_text="Ej: PRY-001",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=40,
        content_padding=ft.Padding(left=10, right=10, top=8, bottom=8),
    )

    input_cliente = ft.TextField(
        hint_text="Nombre de la empresa cliente",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=40,
        content_padding=ft.Padding(left=10, right=10, top=8, bottom=8),
    )

    input_presupuesto = ft.TextField(
        hint_text="0.00",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=40,
        content_padding=ft.Padding(left=10, right=10, top=8, bottom=8),
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
        min_lines=2,
        max_lines=2,
        content_padding=10,
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
        content_padding=ft.Padding(left=10, right=10),
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
        content_padding=ft.Padding(left=10, right=10),
        options=[
            ft.dropdownm2.Option("ACTIVO"),
            ft.dropdownm2.Option("PAUSADO"),
            ft.dropdownm2.Option("INACTIVO"),
        ]
    )

    # Componentes visuales para las fechas
    txt_fecha_inicio = ft.Text("Seleccionar...", size=11, color="#999999")
    txt_fecha_fin = ft.Text("Seleccionar...", size=11, color="#999999")


    # Contenedor del formulario con Scroll
    formulario = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Column([crear_label("Nombre del Proyecto", True), input_nombre], spacing=3),
            ft.Column([crear_label("Cliente / Empresa", True), input_cliente], spacing=3),
            
            ft.Row([
                ft.Column([crear_label("Código"), input_codigo], spacing=3, expand=True),
                ft.Column([crear_label("Presupuesto"), input_presupuesto], spacing=3, expand=True),
            ], spacing=10),

            ft.Column([crear_label("Responsable del Proyecto"), dropdown_responsable], spacing=3),
            
            ft.Row([
                ft.Column([
                    crear_label("Fecha Inicio", True),
                    ft.Container(
                        content=ft.Row([ft.Icon(ft.Icons.CALENDAR_MONTH, size=14, color=COLOR_LABEL), txt_fecha_inicio], spacing=5),
                        on_click=abrir_picker_inicio,
                        padding=ft.Padding(left=10, right=10, top=8, bottom=8), 
                        border=ft.Border(top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)), 
                        border_radius=5,
                        height=40,
                    )
                ], expand=True, spacing=3),
                ft.Column([
                    crear_label("Fecha Fin", True),
                    ft.Container(
                        content=ft.Row([ft.Icon(ft.Icons.CALENDAR_MONTH, size=14, color=COLOR_LABEL), txt_fecha_fin], spacing=5),
                        on_click=abrir_picker_fin,
                        padding=ft.Padding(left=10, right=10, top=8, bottom=8), 
                        border=ft.Border(top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)), 
                        border_radius=5,
                        height=40,
                    )
                ], expand=True, spacing=3),
            ], spacing=10),

            ft.Row([
                ft.Column([crear_label("Estado"), dropdown_estado], spacing=3, expand=True),
            ]),
            
            ft.Column([crear_label("Descripción"), input_descripcion], spacing=3),
            
            
            # Leyenda
            ft.Row([
                ft.Text("*", size=10, color=COLOR_ROJO, weight="bold"),
                ft.Text("Campos obligatorios", size=9, color="#666666", italic=True),
            ], spacing=2),
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
            padding=ft.Padding(left=18, right=18, top=55, bottom=15),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Container(height=480, content=formulario),
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
def main(page):
    page.title = "App Tareas - Crear Proyecto"
    page.window.width = 420
    page.window.height = 800
    page.padding = 0 
    vista = VistaCrearProyecto(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)