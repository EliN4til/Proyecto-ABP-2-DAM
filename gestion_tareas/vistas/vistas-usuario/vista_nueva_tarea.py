import flet as ft
from datetime import datetime

def VistaNuevaTarea(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#66000000"
    COLOR_SOMBRA_TARJETAS = "#40000000"
    COLOR_BTN_CREAR = "#4682B4"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"

    TAGS_EMOJIS = {
        "Desarrollo": "👨‍💻",
        "Bug Fix": "🐛",
        "Testing": "🧪",
        "Diseño": "🎨",
        "Documentación": "📝",
        "DevOps": "⚙️",
        "Base de Datos": "🗄️",
        "API": "🔌",
        "Frontend": "🖥️",
        "Backend": "🔧",
    }

    PERSONAS_DEMO = [
        "Ana García (EMP001 - Desarrollo)",
        "Carlos López (EMP002 - Diseño)",
        "María Rodríguez (EMP003 - QA)",
        "Pedro Martínez (EMP004 - DevOps)",
        "Laura Sánchez (EMP005 - Backend)",
        "Juan Fernández (EMP006 - Frontend)",
        "Sofia Ruiz (EMP007 - Documentación)",
        "Diego Torres (EMP008 - Base de Datos)",
    ]

    tags_seleccionados = []
    personas_seleccionadas = []
    emoji_index_actual = [0] 

    fecha_inicio_texto = ft.Text("DD/MM/AA", size=12, color="black", weight=ft.FontWeight.W_500)
    fecha_fin_texto = ft.Text("DD/MM/AA", size=12, color="black", weight=ft.FontWeight.W_500)

    emoji_text = ft.Text("📋", size=35)

    texto_personas_seleccionadas = ft.Text(
        "Selecciona personas...", 
        size=11, 
        color="#999999",
        overflow=ft.TextOverflow.ELLIPSIS,
        max_lines=1,
    )
    
    texto_tags_seleccionados = ft.Text(
        "Selecciona...", 
        size=11, 
        color="#999999",
        overflow=ft.TextOverflow.ELLIPSIS,
        max_lines=1,
    )

    def on_fecha_inicio_change(e):
        if e.control.value:
            fecha_inicio_texto.value = e.control.value.strftime("%d/%m/%y")
            page.update()

    def on_fecha_fin_change(e):
        if e.control.value:
            fecha_fin_texto.value = e.control.value.strftime("%d/%m/%y")
            page.update()

    date_picker_inicio = ft.DatePicker(
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2030, 12, 31),
        on_change=on_fecha_inicio_change,
    )

    date_picker_fin = ft.DatePicker(
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2030, 12, 31),
        on_change=on_fecha_fin_change,
    )

    page.overlay.append(date_picker_inicio)
    page.overlay.append(date_picker_fin)

    def btn_volver_click(e):
        page.snack_bar = ft.SnackBar(ft.Text("Volver atrás"))
        page.snack_bar.open = True
        page.update()

    def btn_crear_click(e):
        page.snack_bar = ft.SnackBar(ft.Text("Crear tarea"))
        page.snack_bar.open = True
        page.update()

    def abrir_fecha_inicio(e):
        date_picker_inicio.open = True
        page.update()

    def abrir_fecha_fin(e):
        date_picker_fin.open = True
        page.update()

    def cambiar_emoji(e):
        if len(tags_seleccionados) > 1:
            emoji_index_actual[0] = (emoji_index_actual[0] + 1) % len(tags_seleccionados)
            tag_actual = tags_seleccionados[emoji_index_actual[0]]
            emoji_text.value = TAGS_EMOJIS[tag_actual]
            page.update()

    emoji_container = ft.Container(
        content=emoji_text,
        padding=ft.padding.only(top=12),
        on_click=cambiar_emoji,
        tooltip="Click para cambiar emoji",
    )

    def actualizar_emoji():
        if len(tags_seleccionados) == 0:
            emoji_text.value = "📋"
            emoji_index_actual[0] = 0
        elif len(tags_seleccionados) == 1:
            emoji_text.value = TAGS_EMOJIS[tags_seleccionados[0]]
            emoji_index_actual[0] = 0
        else:
            emoji_index_actual[0] = 0
            emoji_text.value = TAGS_EMOJIS[tags_seleccionados[0]]

    def crear_dialog_personas():
        checkboxes_personas = []
        
        def on_checkbox_change(e):
            persona = e.control.data
            if e.control.value:
                if persona not in personas_seleccionadas:
                    personas_seleccionadas.append(persona)
            else:
                if persona in personas_seleccionadas:
                    personas_seleccionadas.remove(persona)
        
        for persona in PERSONAS_DEMO:
            cb = ft.Checkbox(
                label=persona,
                value=persona in personas_seleccionadas,
                data=persona,
                on_change=on_checkbox_change,
                label_style=ft.TextStyle(size=12, color="black"),
            )
            checkboxes_personas.append(cb)
        
        def cerrar_dialog(e):
            dialog_personas.open = False
            if len(personas_seleccionadas) == 0:
                texto_personas_seleccionadas.value = "Selecciona personas..."
                texto_personas_seleccionadas.color = "#999999"
            elif len(personas_seleccionadas) == 1:
                texto_personas_seleccionadas.value = personas_seleccionadas[0]
                texto_personas_seleccionadas.color = "black"
            else:
                texto_personas_seleccionadas.value = f"{len(personas_seleccionadas)} personas seleccionadas"
                texto_personas_seleccionadas.color = "black"
            page.update()
        
        dialog_personas = ft.AlertDialog(
            modal=True,
            title=ft.Text("Compartir con", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=300,
                bgcolor="white",
                content=ft.ListView(
                    controls=checkboxes_personas,
                    spacing=5,
                ),
            ),
            actions=[
                ft.TextButton("Aceptar", on_click=cerrar_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return dialog_personas

    def abrir_dialog_personas(e):
        dialog = crear_dialog_personas()
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def crear_dialog_tags():
        checkboxes_tags = []
        
        def on_checkbox_change(e):
            tag = e.control.data
            if e.control.value:
                if tag not in tags_seleccionados:
                    tags_seleccionados.append(tag)
            else:
                if tag in tags_seleccionados:
                    tags_seleccionados.remove(tag)
        
        for tag in TAGS_EMOJIS.keys():
            cb = ft.Checkbox(
                label=f"{TAGS_EMOJIS[tag]} {tag}",
                value=tag in tags_seleccionados,
                data=tag,
                on_change=on_checkbox_change,
                label_style=ft.TextStyle(size=12, color="black"),
            )
            checkboxes_tags.append(cb)
        
        def cerrar_dialog(e):
            dialog_tags.open = False
            if len(tags_seleccionados) == 0:
                texto_tags_seleccionados.value = "Selecciona..."
                texto_tags_seleccionados.color = "#999999"
            elif len(tags_seleccionados) == 1:
                texto_tags_seleccionados.value = tags_seleccionados[0]
                texto_tags_seleccionados.color = "black"
            else:
                texto_tags_seleccionados.value = f"{len(tags_seleccionados)} tags"
                texto_tags_seleccionados.color = "black"
            actualizar_emoji()
            page.update()
        
        dialog_tags = ft.AlertDialog(
            modal=True,
            title=ft.Text("Seleccionar Tags", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=280,
                height=350,
                bgcolor="white",
                content=ft.ListView(
                    controls=checkboxes_tags,
                    spacing=5,
                ),
            ),
            actions=[
                ft.TextButton("Aceptar", on_click=cerrar_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return dialog_tags

    def abrir_dialog_tags(e):
        dialog = crear_dialog_tags()
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    selector_personas = ft.Container(
        content=ft.Row(
            controls=[
                texto_personas_seleccionadas,
                ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=20, color="#666666"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor="white",
        border=ft.border.all(1, COLOR_BORDE),
        border_radius=5,
        padding=ft.padding.only(left=10, right=5, top=8, bottom=8),
        on_click=abrir_dialog_personas,
        ink=True,
    )

    selector_tags = ft.Container(
        content=ft.Row(
            controls=[
                texto_tags_seleccionados,
                ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=20, color="#666666"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor="white",
        border=ft.border.all(1, COLOR_BORDE),
        border_radius=5,
        padding=ft.padding.only(left=10, right=5, top=8, bottom=8),
        width=130,
        on_click=abrir_dialog_tags,
        ink=True,
    )

    input_titulo = ft.TextField(
        hint_text="Escribe el título de la tarea",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=38,
        content_padding=ft.padding.only(left=10, right=10, top=8, bottom=8),
    )

    seccion_superior = ft.Container(
        bgcolor="white",
        border_radius=10,
        padding=ft.padding.all(15),
        border=ft.border.all(1, COLOR_BORDE),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=12,
            color=COLOR_SOMBRA_TARJETAS,
            offset=ft.Offset(0, 4),
        ),
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Row(
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        emoji_container,
                        ft.Column(
                            spacing=3,
                            expand=True,
                            controls=[
                                ft.Text("Título", size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                input_titulo,
                            ]
                        ),
                    ]
                ),
                ft.Column(
                    spacing=3,
                    controls=[
                        ft.Text("Compartir con", size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                        selector_personas,
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Column(
                            spacing=3,
                            controls=[
                                ft.Text("Tag(s)", size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                selector_tags,
                            ]
                        ),
                        ft.Column(
                            spacing=5,
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                            controls=[
                                ft.Container(
                                    content=ft.Row(
                                        spacing=5,
                                        controls=[
                                            ft.Text("Fecha Inicio:", size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                            fecha_inicio_texto,
                                        ]
                                    ),
                                    on_click=abrir_fecha_inicio,
                                    ink=True,
                                    border_radius=5,
                                    padding=3,
                                ),
                                ft.Container(
                                    content=ft.Row(
                                        spacing=5,
                                        controls=[
                                            ft.Text("Fecha Fin:", size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                            fecha_fin_texto,
                                        ]
                                    ),
                                    on_click=abrir_fecha_fin,
                                    ink=True,
                                    border_radius=5,
                                    padding=3,
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        )
    )

    texto_requerimientos = ft.TextField(
        hint_text="Escribe aquí los requerimientos...",
        hint_style=ft.TextStyle(size=12, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        multiline=True,
        min_lines=8,
        max_lines=8,
        expand=True,
        content_padding=ft.padding.all(12),
    )

    seccion_requerimientos = ft.Container(
        bgcolor="white",
        border_radius=10,
        padding=ft.padding.all(15),
        border=ft.border.all(1, COLOR_BORDE),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=12,
            color=COLOR_SOMBRA_TARJETAS,
            offset=ft.Offset(0, 4),
        ),
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Text(
                    "Escribe los requerimientos de la tarea",
                    size=13,
                    color="black",
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Row(
                    controls=[texto_requerimientos],
                ),
            ]
        )
    )

    btn_crear = ft.Container(
        width=160,
        height=44,
        bgcolor=COLOR_BTN_CREAR,
        border_radius=22,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=btn_crear_click,
        content=ft.Text("Crear Tarea", color="white", weight=ft.FontWeight.BOLD, size=14),
    )

    fila_boton = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[btn_crear]
    )

    tarjeta_blanca = ft.Container(
        width=400,
        bgcolor="white",
        border_radius=25,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=COLOR_SOMBRA),
        content=ft.Column(
            spacing=0,
            tight=True,
            controls=[
                ft.Container(
                    padding=ft.padding.only(left=15, top=10, bottom=5),
                    alignment=ft.Alignment(-1, 0),
                    content=ft.Container(
                        content=ft.Text("←", size=26, color="black", weight="bold"),
                        on_click=btn_volver_click,
                        ink=True,
                        border_radius=50,
                        padding=3,
                    ),
                ),

                ft.Container(
                    height=55,
                    width=400,
                    bgcolor=COLOR_HEADER_BG,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("NUEVA TAREA", size=18, weight=ft.FontWeight.BOLD, color="white")
                ),
                
                ft.Container(
                    padding=ft.padding.only(left=18, right=18, top=18, bottom=22),
                    content=ft.Column(
                        spacing=15,
                        tight=True,
                        controls=[
                            seccion_superior,
                            seccion_requerimientos,
                            fila_boton,
                        ]
                    )
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
        alignment=ft.Alignment(0, 0), 
        content=tarjeta_blanca
    )


def main(page: ft.Page):
    page.title = "App Tareas - Nueva Tarea"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 380
    page.window.min_height = 780
    page.padding = 0 
    
    vista = VistaNuevaTarea(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)