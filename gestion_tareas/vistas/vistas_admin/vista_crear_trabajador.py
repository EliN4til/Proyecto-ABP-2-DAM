import flet as ft
from datetime import datetime
from modelos.crud import crear_empleado, obtener_todos_proyectos, obtener_todos_departamentos

def VistaCrearTrabajador(page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#66000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_BTN_CREAR = "#4682B4"

    # Listas maestras (datos brutos de la BD)
    proyectos_maestros = []
    departamentos_maestros = []

    empresas_dinamicas = []

    # Opciones estáticas
    CARGOS = ["Junior Developer", "Mid Developer", "Senior Developer", "Tech Lead", "Project Manager", "Scrum Master", "UX Designer", "QA Engineer", "DevOps Engineer"]
    UBICACIONES = ["Oficina Central - Madrid", "Oficina Barcelona", "Oficina Valencia", "Remoto"]
    ESTADOS = ["ACTIVO", "INACTIVO", "PENDIENTE"]

    # --- LÓGICA DE CARGA Y EXTRACCIÓN DINÁMICA ---

    def cargar_datos_maestros():
        """Carga datos de la BD y extrae nombres de empresas únicas"""
        nonlocal proyectos_maestros, departamentos_maestros, empresas_dinamicas
        
        # 1. Obtener datos de las colecciones
        exito_p, proys = obtener_todos_proyectos()
        if exito_p: proyectos_maestros = proys
        
        exito_d, deptos = obtener_todos_departamentos()
        if exito_d: departamentos_maestros = deptos

        # 2. Extraer empresas únicas (de Departamentos y Proyectos)
        set_empresas = set()
        
        # Extraemos del campo 'empresa' de departamentos
        for d in departamentos_maestros:
            if d.get("empresa"):
                set_empresas.add(d.get("empresa"))
        
        # Extraemos del campo 'cliente' de proyectos
        for p in proyectos_maestros:
            if p.get("cliente"):
                set_empresas.add(p.get("cliente"))
        
        # Convertimos a lista ordenada
        empresas_dinamicas = sorted(list(set_empresas))
        
        # Si no hay nada en la BD, ponemos una por defecto para que no explote
        if not empresas_dinamicas:
            empresas_dinamicas = ["Empresa General"]

        # 3. Llenar el dropdown de empresas
        dropdown_empresa.options = [ft.dropdownm2.Option(e) for e in empresas_dinamicas]
        page.update()

    def on_empresa_change(e):
        """Al cambiar la empresa, filtramos proyectos, departamentos y equipos"""
        empresa_sel = dropdown_empresa.value
        
        # 1. Filtrar Proyectos (donde el cliente coincide con la empresa seleccionada)
        proys_filtrados = [p["nombre"] for p in proyectos_maestros if p.get("cliente") == empresa_sel]
        dropdown_proyecto.options = [ft.dropdownm2.Option(p) for p in proys_filtrados]
        dropdown_proyecto.disabled = False
        dropdown_proyecto.value = None
        
        # 2. Filtrar Departamentos (donde la empresa coincide)
        deptos_filtrados = [d["nombre"] for d in departamentos_maestros if d.get("empresa") == empresa_sel]
        dropdown_departamento.options = [ft.dropdownm2.Option(d) for d in deptos_filtrados]
        dropdown_departamento.disabled = False
        dropdown_departamento.value = None
        
        page.update()

    async def btn_volver_click(e):
        """Acción al hacer clic en el botón volver atrás"""
        await page.push_route("/gestionar_trabajadores")

    async def btn_crear_click(e):
        """Valida y guarda el trabajador con la lógica de cascada aplicada"""
        
        if not input_nombre.value or not input_apellidos.value or not dropdown_empresa.value:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Nombre, Apellidos y Empresa son obligatorios"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        if not input_identificador.value:
            page.snack_bar = ft.SnackBar(ft.Text("❌ El DNI/NIE es obligatorio"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # Buscamos datos del departamento seleccionado para el modelo
        depto_info = {"nombre": dropdown_departamento.value if dropdown_departamento.value else "General", "ubicacion": "N/A"}
        for d in departamentos_maestros:
            if d["nombre"] == dropdown_departamento.value:
                depto_info["ubicacion"] = d.get("ubicacion", "N/A")
                break

        nuevo_trabajador = {
            "identificador": input_identificador.value,
            "nombre": input_nombre.value,
            "apellidos": input_apellidos.value,
            "email": input_correo.value,
            "contrasenya": "1234",
            "estado": dropdown_estado.value if dropdown_estado.value else "ACTIVO",
            "empresa": dropdown_empresa.value,
            "equipo": input_equipo.value if input_equipo.value else "Sin equipo",
            "proyecto": dropdown_proyecto.value if dropdown_proyecto.value else "Sin proyecto",
            "departamento": depto_info,
            "cargo": dropdown_cargo.value if dropdown_cargo.value else "Empleado",
            "id_empleado": input_id_empleado.value if input_id_empleado.value else f"EMP-{datetime.now().strftime('%H%M%S')}",
            "telefono": input_telefono.value if input_telefono.value else "N/A",
            "ubicacion": dropdown_ubicacion.value if dropdown_ubicacion.value else "Oficina Central",
            "fecha_incorporacion": datetime.now(),
            "es_admin": False
        }

        # Limpiar errores previos
        input_nombre.error_text = None
        input_apellidos.error_text = None
        input_identificador.error_text = None
        input_correo.error_text = None
        input_telefono.error_text = None
        page.update()

        exito, resultado = crear_empleado(nuevo_trabajador)

        if exito:
            page.snack_bar = ft.SnackBar(ft.Text(f"✅ {input_nombre.value} registrado correctamente"), bgcolor="green")
            page.snack_bar.open = True
            await page.push_route("/gestionar_trabajadores")
        else:
            if isinstance(resultado, list):
                errores_texto = []
                for err in resultado:
                    campo = err["loc"][0]
                    msg = err["msg"]
                    
                    if campo == "nombre": input_nombre.error_text = msg
                    elif campo == "apellidos": input_apellidos.error_text = msg
                    elif campo == "identificador": input_identificador.error_text = msg
                    elif campo == "email": input_correo.error_text = msg
                    elif campo == "telefono": input_telefono.error_text = msg
                    else:
                        errores_texto.append(f"{campo}: {msg}")
                
                page.update()
                
                if errores_texto:
                    page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {', '.join(errores_texto)}"), bgcolor="red")
                    page.snack_bar.open = True
            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {resultado}"), bgcolor="red")
                page.snack_bar.open = True
        
        page.update()

    # --- HELPERS DE INTERFAZ ---

    def crear_campo_texto(hint):
        return ft.TextField(
            hint_text=hint,
            hint_style=ft.TextStyle(size=11, color="#999999"),
            text_style=ft.TextStyle(size=12, color="black"),
            border_color=COLOR_BORDE,
            border_radius=5,
            height=40,
            content_padding=ft.Padding(left=10, right=10, top=8, bottom=8),
        )

    def crear_dropdown(opciones, hint, on_change=None, disabled=False):
        return ft.DropdownM2(
            hint_text=hint,
            hint_style=ft.TextStyle(size=11, color="#999999"),
            text_style=ft.TextStyle(size=12, color="black"),
            bgcolor="white",
            border_color=COLOR_BORDE,
            border_radius=5,
            height=40,
            expand=True,
            disabled=disabled,
            content_padding=ft.Padding(left=10, right=10),
            options=[ft.dropdownm2.Option(op) for op in opciones],
            on_change=on_change
        )

    def crear_label(texto):
        return ft.Text(texto, size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500)

    # Botón volver
    btn_volver = ft.Container(
        content=ft.Text("←", size=24, color="white", weight=ft.FontWeight.BOLD),
        on_click=btn_volver_click,
        ink=True,
        padding=10,
    )

    # --- CONTROLES DEL FORMULARIO ---
    input_nombre = crear_campo_texto("Nombre")
    input_apellidos = crear_campo_texto("Apellidos")
    input_identificador = crear_campo_texto("DNI / NIE")
    input_correo = crear_campo_texto("email@corporativo.com")
    input_telefono = crear_campo_texto("+34 000 000 000")
    input_id_empleado = crear_campo_texto("Código empleado")

    # Dropdowns dinámicos
    dropdown_empresa = crear_dropdown([], "1º Selecciona Empresa...", on_change=on_empresa_change)
    dropdown_proyecto = crear_dropdown([], "2º Proyecto (Selecciona empresa)", disabled=True)
    dropdown_departamento = crear_dropdown([], "3º Departamento (Selecciona empresa)", disabled=True)
    input_equipo = crear_campo_texto("Nombre del equipo")
    
    dropdown_cargo = crear_dropdown(CARGOS, "Selecciona cargo...")
    dropdown_ubicacion = crear_dropdown(UBICACIONES, "Ubicación física...")
    dropdown_estado = crear_dropdown(ESTADOS, "Estado inicial...")

    # Contenedor del formulario con Scroll
    formulario = ft.Column(
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Column([crear_label("Empresa Contratante (Detectada en BD) *"), dropdown_empresa], spacing=3),
            
            ft.Row([
                ft.Column([crear_label("Nombre *"), input_nombre], spacing=3, expand=True),
                ft.Column([crear_label("Apellidos *"), input_apellidos], spacing=3, expand=True),
            ], spacing=10),

            ft.Column([crear_label("Correo corporativo *"), input_correo], spacing=3),

            ft.Row([
                ft.Column([crear_label("Asignar Proyecto"), dropdown_proyecto], spacing=3, expand=True),
                ft.Column([crear_label("Departamento"), dropdown_departamento], spacing=3, expand=True),
            ], spacing=10),

            ft.Row([
                ft.Column([crear_label("Equipo"), input_equipo], spacing=3, expand=True),
                ft.Column([crear_label("Cargo"), dropdown_cargo], spacing=3, expand=True),
            ], spacing=10),

            ft.Row([
                ft.Column([crear_label("Identificador (DNI) *"), input_identificador], spacing=3, expand=True),
                ft.Column([crear_label("ID Interno"), input_id_empleado], spacing=3, expand=True),
            ], spacing=10),

            ft.Row([
                ft.Column([crear_label("Ubicación"), dropdown_ubicacion], spacing=3, expand=True),
                ft.Column([crear_label("Estado"), dropdown_estado], spacing=3, expand=True),
            ], spacing=10),
            
            ft.Column([crear_label("Teléfono"), input_telefono], spacing=3),
        ]
    )

    # Tarjeta Blanca Principal
    tarjeta_blanca = ft.Container(
        width=380,
        bgcolor="white",
        border_radius=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color="#40000000", offset=ft.Offset(0, 5)),
        content=ft.Container(
            padding=ft.Padding(left=20, right=20, top=55, bottom=25),
            content=ft.Column(
                spacing=15,
                controls=[
                    ft.Container(height=480, content=formulario),
                    ft.Row([
                        ft.Container(
                            width=180, height=44, bgcolor=COLOR_BTN_CREAR, border_radius=22,
                            alignment=ft.Alignment(0, 0), ink=True, on_click=btn_crear_click,
                            content=ft.Text("Registrar Trabajador", color="white", weight="bold", size=13)
                        )
                    ], alignment="center"),
                ]
            )
        )
    )

    header_flotante = ft.Container(
        width=240, height=50, bgcolor=COLOR_HEADER_BG, border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text("CREAR TRABAJADOR", size=18, weight="bold", color="white")
    )

    contenido_superpuesto = ft.Container(
        width=380, height=650,
        content=ft.Stack([
            ft.Container(content=tarjeta_blanca, top=30),
            ft.Container(content=header_flotante, top=0, left=70)
        ])
    )

    # --- INICIALIZACIÓN ---
    cargar_datos_maestros()

    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[COLOR_FONDO_TOP, COLOR_FONDO_BOT]),
        content=ft.Stack([
            ft.Container(expand=True, alignment=ft.Alignment(0, 0), content=contenido_superpuesto),
            ft.Container(content=btn_volver, top=10, left=10)
        ])
    )

def main(page):
    page.title = "Registro de Personal"
    page.window.width = 420
    page.window.height = 800
    page.padding = 0 
    vista = VistaCrearTrabajador(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)