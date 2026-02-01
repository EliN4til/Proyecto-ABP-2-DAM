import flet as ft
from datetime import datetime
from modelos.crud import crear_empleado

def VistaCrearTrabajador(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#66000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_BTN_CREAR = "#4682B4"

    #opciones para los dropdowns
    EMPRESAS = ["TechSolutions S.L", "InnovateTech Corp", "Digital Systems S.A", "CloudNet Solutions"]
    DEPARTAMENTOS = ["Desarrollo", "Diseño", "QA", "DevOps", "Backend", "Frontend", "Documentación", "Base de Datos", "Recursos Humanos", "Finanzas"]
    EQUIPOS = ["Cloud Infrastructure & DevOps", "Frontend Team", "Backend Team", "Mobile Team", "QA Team", "Design Team", "Data Team"]
    CARGOS = ["Junior Developer", "Mid Developer", "Senior Developer", "Tech Lead", "Project Manager", "Scrum Master", "UX Designer", "QA Engineer", "DevOps Engineer"]
    UBICACIONES = ["Oficina Central - Madrid", "Oficina Barcelona", "Oficina Valencia", "Remoto"]
    ESTADOS = ["ACTIVO", "INACTIVO", "PENDIENTE"]

    def btn_volver_click(e):
        """Acción al hacer clic en el botón volver atrás - CORREGIDO A GESTIONAR TRABAJADORES"""
        page.go("/gestionar_trabajadores")

    def btn_crear_click(e):
        """Recopila los datos del formulario e inserta el trabajador en la base de datos real"""
        
        # 1. Validar campos obligatorios
        if not input_nombre.value or not input_apellidos.value or not input_correo.value:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Nombre, Apellidos y Correo son obligatorios"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # 2. Preparar los datos para el modelo MongoDB
        # Nota: Adaptamos al esquema EmpleadoModel que requiere 'departamento' como un objeto
        nuevo_empleado = {
            "identificador": input_identificador.value if input_identificador.value else "N/A",
            "nombre": input_nombre.value,
            "apellidos": input_apellidos.value,
            "email": input_correo.value,
            "contrasenya": "1234", # Contraseña por defecto para el primer acceso
            "estado": dropdown_estado.value if dropdown_estado.value else "ACTIVO",
            "empresa": dropdown_empresa.value if dropdown_empresa.value else "TechSolutions S.L",
            "equipo": dropdown_equipo.value if dropdown_equipo.value else "General",
            "proyecto": "Sin asignar",
            "departamento": {
                "nombre": dropdown_departamento.value if dropdown_departamento.value else "General",
                "ubicacion": dropdown_ubicacion.value if dropdown_ubicacion.value else "N/A"
            },
            "cargo": dropdown_cargo.value if dropdown_cargo.value else "Empleado",
            "id_empleado": input_id_empleado.value if input_id_empleado.value else f"EMP-{datetime.now().strftime('%M%S')}",
            "telefono": input_telefono.value if input_telefono.value else "N/A",
            "ubicacion": dropdown_ubicacion.value if dropdown_ubicacion.value else "Oficina Central",
            "fecha_incorporacion": datetime.now(),
            "es_admin": False
        }

        # 3. Llamada al CRUD
        exito, resultado = crear_empleado(nuevo_empleado)

        if exito:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"✅ Trabajador {input_nombre.value} creado con éxito"),
                bgcolor="green"
            )
            page.snack_bar.open = True
            # Volvemos a la lista de trabajadores para ver el nuevo registro
            page.go("/gestionar_trabajadores")
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error al guardar: {resultado}"), bgcolor="red")
            page.snack_bar.open = True
        
        page.update()

    def crear_campo_texto(hint: str, expand: bool = False):
        """Crea un campo de texto estándar"""
        return ft.TextField(
            hint_text=hint,
            hint_style=ft.TextStyle(size=11, color="#999999"),
            text_style=ft.TextStyle(size=12, color="black"),
            border_color=COLOR_BORDE,
            border_radius=5,
            height=40,
            expand=expand,
            content_padding=ft.padding.only(left=10, right=10, top=8, bottom=8),
        )

    def crear_dropdown(opciones: list, hint: str):
        """Crea un dropdown con las opciones dadas"""
        return ft.DropdownM2(
            hint_text=hint,
            hint_style=ft.TextStyle(size=11, color="#999999"),
            text_style=ft.TextStyle(size=12, color="black"),
            bgcolor="white",
            fill_color="white",
            border_color=COLOR_BORDE,
            border_radius=5,
            height=40,
            expand=True,
            content_padding=ft.padding.only(left=10, right=10),
            options=[ft.dropdownm2.Option(opcion) for opcion in opciones],
        )

    def crear_label(texto: str):
        """Crea una etiqueta de campo"""
        return ft.Text(texto, size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500)

    #botón volver
    btn_volver = ft.Container(
        content=ft.Text("←", size=24, color="white", weight=ft.FontWeight.BOLD),
        on_click=btn_volver_click,
        ink=True,
        padding=10,
    )

    #campos del formulario (Controles guardados en variables para acceder a su .value)
    input_nombre = crear_campo_texto("Nombre del trabajador")
    input_apellidos = crear_campo_texto("Apellidos del trabajador")
    input_identificador = crear_campo_texto("DNI / NIE / Pasaporte")
    input_correo = crear_campo_texto("correo@empresa.com")
    input_telefono = crear_campo_texto("+34 XXX XXX XXX")
    input_id_empleado = crear_campo_texto("ID automático o manual")

    dropdown_empresa = crear_dropdown(EMPRESAS, "Selecciona empresa...")
    dropdown_departamento = crear_dropdown(DEPARTAMENTOS, "Selecciona departamento...")
    dropdown_equipo = crear_dropdown(EQUIPOS, "Selecciona equipo...")
    dropdown_cargo = crear_dropdown(CARGOS, "Selecciona cargo...")
    dropdown_ubicacion = crear_dropdown(UBICACIONES, "Selecciona ubicación...")
    dropdown_estado = crear_dropdown(ESTADOS, "Selecciona estado...")

    #contenido del formulario
    formulario = ft.Column(
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            #nombre y apellidos
            ft.Column(spacing=3, controls=[
                crear_label("Nombre *"),
                input_nombre,
            ]),
            ft.Column(spacing=3, controls=[
                crear_label("Apellidos *"),
                input_apellidos,
            ]),
            
            #identificador
            ft.Column(spacing=3, controls=[
                crear_label("Identificador"),
                input_identificador,
            ]),
            
            #empresa y departamento
            ft.Row(spacing=10, controls=[
                ft.Column(spacing=3, expand=True, controls=[
                    crear_label("Empresa"),
                    dropdown_empresa,
                ]),
            ]),
            ft.Row(spacing=10, controls=[
                ft.Column(spacing=3, expand=True, controls=[
                    crear_label("Departamento"),
                    dropdown_departamento,
                ]),
            ]),
            
            #equipo y cargo
            ft.Row(spacing=10, controls=[
                ft.Column(spacing=3, expand=True, controls=[
                    crear_label("Equipo"),
                    dropdown_equipo,
                ]),
            ]),
            ft.Row(spacing=10, controls=[
                ft.Column(spacing=3, expand=True, controls=[
                    crear_label("Cargo"),
                    dropdown_cargo,
                ]),
            ]),
            
            #id empleado
            ft.Column(spacing=3, controls=[
                crear_label("ID Empleado"),
                input_id_empleado,
            ]),
            
            #correo y teléfono
            ft.Column(spacing=3, controls=[
                crear_label("Correo corporativo *"),
                input_correo,
            ]),
            ft.Column(spacing=3, controls=[
                crear_label("Teléfono"),
                input_telefono,
            ]),
            
            #ubicación y estado
            ft.Row(spacing=10, controls=[
                ft.Column(spacing=3, expand=True, controls=[
                    crear_label("Ubicación"),
                    dropdown_ubicacion,
                ]),
            ]),
            ft.Row(spacing=10, controls=[
                ft.Column(spacing=3, expand=True, controls=[
                    crear_label("Estado"),
                    dropdown_estado,
                ]),
            ]),
        ]
    )

    #botón crear trabajador
    btn_crear = ft.Container(
        width=180,
        height=44,
        bgcolor=COLOR_BTN_CREAR,
        border_radius=22,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=btn_crear_click,
        content=ft.Text("Crear Trabajador", color="white", weight=ft.FontWeight.BOLD, size=14),
    )

    #tarjeta blanca principal
    tarjeta_blanca = ft.Container(
        width=380,
        bgcolor="white",
        border_radius=25,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=15,
            color="#40000000",
            offset=ft.Offset(0, 5),
        ),
        content=ft.Container(
            padding=ft.padding.only(left=20, right=20, top=55, bottom=25),
            content=ft.Column(
                spacing=15,
                tight=True,
                controls=[
                    ft.Container(
                        height=520,
                        content=formulario,
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[btn_crear],
                    ),
                ]
            )
        )
    )

    #header flotante
    header_flotante = ft.Container(
        width=240,
        height=50,
        bgcolor=COLOR_HEADER_BG,
        border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            "CREAR TRABAJADOR",
            size=18,
            weight=ft.FontWeight.BOLD,
            color="white"
        )
    )

    #contenido superpuesto (tarjeta + header)
    contenido_superpuesto = ft.Container(
        width=380,
        height=680,
        content=ft.Stack(
            controls=[
                ft.Container(
                    content=tarjeta_blanca,
                    top=30,
                ),
                ft.Container(
                    content=header_flotante,
                    top=0,
                    left=70,
                )
            ]
        )
    )

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


#para probar directamente
def main(page: ft.Page):
    page.title = "App Tareas - Crear Trabajador"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 400
    page.window.min_height = 700
    page.padding = 0 
    
    vista = VistaCrearTrabajador(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)