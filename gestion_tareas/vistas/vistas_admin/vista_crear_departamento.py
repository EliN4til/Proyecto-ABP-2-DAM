import flet as ft
from gestion_tareas.modelos.crud import crear_departamento, obtener_todos_proyectos, obtener_todos_departamentos, obtener_todos_empleados
from gestion_tareas.utilidades.validaciones import validar_email, validar_telefono, validar_dni

def VistaCrearDepartamento(page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_BTN_CREAR = "#4682B4"

    # Listas para almacenar datos brutos de la BD
    proyectos_maestros = []
    departamentos_maestros = []
    empleados_db = []
    empresas_extraidas = []

    # Opciones estáticas
    ESTADOS = ["ACTIVO", "INACTIVO", "EN CREACIÓN"]

    # --- LÓGICA DE DATOS ---

    def cargar_datos_iniciales():
        """Carga datos de la BD y prepara los selectores dinámicos"""
        nonlocal proyectos_maestros, departamentos_maestros, empleados_db, empresas_extraidas
        
        exito_p, proys = obtener_todos_proyectos()
        if exito_p: proyectos_maestros = proys
        
        exito_d, deptos = obtener_todos_departamentos()
        if exito_d: departamentos_maestros = deptos

        exito_e, emps = obtener_todos_empleados()
        if exito_e: empleados_db = emps

        # Extraer nombres únicos de empresas/clientes
        set_empresas = set()
        for p in proyectos_maestros:
            if p.get("cliente"): set_empresas.add(p.get("cliente"))
        for d in departamentos_maestros:
            if d.get("empresa"): set_empresas.add(d.get("empresa"))
        
        empresas_extraidas = sorted(list(set_empresas))
        if not empresas_extraidas:
            empresas_extraidas = ["Empresa General"]

        # Llenar dropdowns iniciales
        dropdown_empresa.options = [ft.dropdownm2.Option(e) for e in empresas_extraidas]
        dropdown_responsable.options = [ft.dropdownm2.Option(f"{emp['nombre']} {emp['apellidos']}") for emp in empleados_db]
        page.update()

    def on_empresa_change(e):
        """Al seleccionar cliente, filtramos los proyectos de ese cliente"""
        empresa_sel = dropdown_empresa.value
        
        # Filtramos proyectos donde el cliente coincide
        proys_filtrados = [p["nombre"] for p in proyectos_maestros if p.get("cliente") == empresa_sel]
        
        dropdown_proyecto.options = [ft.dropdownm2.Option(p) for p in proys_filtrados]
        dropdown_proyecto.disabled = False
        dropdown_proyecto.value = None
        
        # Resetear responsable cuando cambia el cliente
        dropdown_responsable.options = []
        dropdown_responsable.disabled = True
        dropdown_responsable.value = None
        page.update()
    
    def on_proyecto_change(e):
        """Al seleccionar proyecto, filtramos los empleados asignados a ese proyecto"""
        proyecto_sel = dropdown_proyecto.value
        
        if not proyecto_sel:
            dropdown_responsable.options = []
            dropdown_responsable.disabled = True
            dropdown_responsable.value = None
            page.update()
            return
        
        # Filtramos empleados que estén asignados a este proyecto
        empleados_filtrados = [
            emp for emp in empleados_db 
            if emp.get("proyecto") == proyecto_sel
        ]
        
        if empleados_filtrados:
            dropdown_responsable.options = [
                ft.dropdownm2.Option(f"{emp['nombre']} {emp['apellidos']}") 
                for emp in empleados_filtrados
            ]
            dropdown_responsable.disabled = False
            dropdown_responsable.value = None
        else:
            dropdown_responsable.options = []
            dropdown_responsable.disabled = True
            dropdown_responsable.value = None
            page.snack_bar = ft.SnackBar(
                ft.Text(f"⚠️ No hay empleados asignados al proyecto '{proyecto_sel}'"), 
                bgcolor="orange"
            )
            page.snack_bar.open = True
        
        page.update()

    async def btn_volver_click(e):
        """Vuelve a la gestión de departamentos"""
        await page.push_route("/gestionar_departamentos")

    async def btn_crear_click(e):
        """Recopila datos y guarda el departamento real en MongoDB"""
        
        # Validaciones obligatorias
        if not input_nombre.value or not dropdown_empresa.value or not dropdown_proyecto.value:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Nombre, Cliente y Proyecto son obligatorios"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return
        
        if not input_email.value:
            page.snack_bar = ft.SnackBar(ft.Text("❌ El email es obligatorio"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        if not input_telefono.value:
            page.snack_bar = ft.SnackBar(ft.Text("❌ El teléfono es obligatorio"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return
        
        # Validar formato de email
        if input_email.value and input_email.value.strip():
            es_valido, mensaje = validar_email(input_email.value)
            if not es_valido:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ {mensaje}"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return
        
        # Validar formato de teléfono
        if input_telefono.value and input_telefono.value.strip():
            es_valido, mensaje = validar_telefono(input_telefono.value)
            if not es_valido:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ {mensaje}"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return
        
        # Procesar presupuesto
        try:
            pres_val = float(input_presupuesto.value.replace(",", ".")) if input_presupuesto.value else 0.0
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("❌ El presupuesto debe ser un número"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # Preparar datos
        datos_depto = {
            "nombre": input_nombre.value,
            "codigo": input_codigo.value if input_codigo.value else "DEPT",
            "empresa": dropdown_empresa.value,
            "proyecto_asignado": dropdown_proyecto.value, # Guardamos la relación con el proyecto
            "responsable": dropdown_responsable.value if dropdown_responsable.value else "Admin",
            "descripcion": input_descripcion.value if input_descripcion.value else "",
            "ubicacion": input_ubicacion.value if input_ubicacion.value else "N/A",
            "email": input_email.value if input_email.value else "",
            "telefono": input_telefono.value if input_telefono.value else "",
            "presupuesto": pres_val,
            "estado": dropdown_estado.value if dropdown_estado.value else "ACTIVO"
        }

        # Limpiar errores previos
        input_nombre.error_text = None
        input_codigo.error_text = None
        input_email.error_text = None
        input_telefono.error_text = None
        input_presupuesto.error_text = None
        dropdown_empresa.error_text = None
        page.update()

        # Guardar en BD
        exito, resultado = crear_departamento(datos_depto)

        if exito:
            page.snack_bar = ft.SnackBar(ft.Text(f"✅ Departamento '{input_nombre.value}' creado"), bgcolor="green")
            page.snack_bar.open = True
            await page.push_route("/gestionar_departamentos")
        else:
            if isinstance(resultado, list):
                # Errores de validación Pydantic
                errores_texto = []
                for err in resultado:
                    campo = err["loc"][0]
                    msg = err["msg"]
                    
                    if campo == "nombre": input_nombre.error_text = msg
                    elif campo == "codigo": input_codigo.error_text = msg
                    elif campo == "email": input_email.error_text = msg
                    elif campo == "telefono": input_telefono.error_text = msg
                    elif campo == "presupuesto": input_presupuesto.error_text = msg
                    elif campo == "empresa": dropdown_empresa.error_text = msg
                    elif campo == "responsable": dropdown_responsable.error_text = msg
                    else:
                        errores_texto.append(f"{campo}: {msg}")
                
                page.update()
                
                if errores_texto:
                    page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {', '.join(errores_texto)}"), bgcolor="red")
                    page.snack_bar.open = True
            else:
                # Error general
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {resultado}"), bgcolor="red")
                page.snack_bar.open = True
        
        page.update()

    # --- HELPERS DE INTERFAZ ---

    def crear_campo_texto(hint, multiline=False, min_lines=1):
        return ft.TextField(
            hint_text=hint,
            hint_style=ft.TextStyle(size=11, color="#999999"),
            text_style=ft.TextStyle(size=12, color="black"),
            border_color=COLOR_BORDE,
            border_radius=5,
            height=40 if not multiline else None,
            multiline=multiline,
            min_lines=min_lines if multiline else None,
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

    # --- CONTROLES ---
    input_nombre = crear_campo_texto("Nombre del departamento")
    input_codigo = crear_campo_texto("Código (Ej: RRHH, IT...)")
    input_descripcion = crear_campo_texto("Descripción...", multiline=True, min_lines=3)
    input_presupuesto = crear_campo_texto("Presupuesto anual (€)")
    input_email = crear_campo_texto("email@departamento.com")
    input_telefono = crear_campo_texto("+34 000 000 000")

    # Selectores dinámicos y dependientes
    dropdown_empresa = crear_dropdown([], "1º Selecciona Cliente...", on_change=on_empresa_change)
    dropdown_proyecto = crear_dropdown([], "2º Selecciona Proyecto...", disabled=True, on_change=on_proyecto_change)
    
    dropdown_responsable = crear_dropdown([], "Selecciona responsable...", disabled=True)
    input_ubicacion = crear_campo_texto("Ubicación del departamento")
    dropdown_estado = crear_dropdown(ESTADOS, "Estado...")

    # Formulario
    formulario = ft.Column(
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Column([crear_label("Cliente / Empresa *"), dropdown_empresa], spacing=3),
            ft.Column([crear_label("Proyecto Asignado *"), dropdown_proyecto], spacing=3),
            ft.Column([crear_label("Nombre del Departamento *"), input_nombre], spacing=3),
            
            ft.Row([
                ft.Column([crear_label("Código"), input_codigo], spacing=3, expand=True),
                ft.Column([crear_label("Responsable"), dropdown_responsable], spacing=3, expand=True),
            ], spacing=10),
            
            ft.Column([crear_label("Descripción"), input_descripcion], spacing=3),
            
            ft.Row([
                ft.Column([crear_label("Email contacto"), input_email], spacing=3, expand=True),
                ft.Column([crear_label("Teléfono"), input_telefono], spacing=3, expand=True),
            ], spacing=10),
            
            ft.Row([
                ft.Column([crear_label("Presupuesto Anual"), input_presupuesto], spacing=3, expand=True),
                ft.Column([crear_label("Ubicación"), input_ubicacion], spacing=3, expand=True),
            ], spacing=10),
            
            ft.Column([crear_label("Estado"), dropdown_estado], spacing=3),
        ]
    )

    # Botón Crear
    btn_crear = ft.Container(
        width=200,
        height=44,
        bgcolor=COLOR_BTN_CREAR,
        border_radius=22,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=btn_crear_click,
        content=ft.Text("Crear Departamento", color="white", weight=ft.FontWeight.BOLD, size=14),
    )

    # Tarjeta Blanca
    tarjeta_blanca = ft.Container(
        width=380,
        bgcolor="white",
        border_radius=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color=COLOR_SOMBRA, offset=ft.Offset(0, 5)),
        content=ft.Container(
            padding=ft.Padding(left=20, right=20, top=55, bottom=25),
            content=ft.Column(
                spacing=15,
                tight=True,
                controls=[
                    ft.Container(height=520, content=formulario),
                    ft.Row([btn_crear], alignment=ft.MainAxisAlignment.CENTER),
                ]
            )
        )
    )

    # Header flotante
    header_flotante = ft.Container(
        width=260,
        height=50,
        bgcolor=COLOR_HEADER_BG,
        border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text("CREAR DEPARTAMENTO", size=18, weight=ft.FontWeight.BOLD, color="white")
    )

    # Layout
    contenido_superpuesto = ft.Container(
        width=380,
        height=680,
        content=ft.Stack([
            ft.Container(content=tarjeta_blanca, top=30),
            ft.Container(content=header_flotante, top=0, left=60)
        ])
    )

    # Inicialización
    cargar_datos_iniciales()

    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[COLOR_FONDO_TOP, COLOR_FONDO_BOT],
        ),
        content=ft.Stack([
            ft.Container(expand=True, alignment=ft.Alignment(0, 0), content=contenido_superpuesto),
            ft.Container(content=btn_volver, top=10, left=10)
        ])
    )


#para probar directamente
def main(page):
    page.title = "App Tareas - Crear Departamento"
    page.window.width = 420
    page.window.height = 800
    page.padding = 0 
    vista = VistaCrearDepartamento(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)