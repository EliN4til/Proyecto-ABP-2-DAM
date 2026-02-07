"""
operaciones crud para la base de datos mongodb
este archivo contiene todas las funciones necesarias para crear, leer, actualizar y eliminar
documentos de las diferentes colecciones de la base de datos.
"""

from bson import ObjectId
from datetime import datetime
from typing import Tuple, List, Optional, Any
from modelos.init import db


# ============================================
# FUNCIONES AUXILIARES Y AUDITORÍA
# ============================================

def es_id_valido(id_str: str) -> bool:
    #comprueba si un string es un objectid válido de mongodb
    try:
        ObjectId(id_str)
        return True
    except:
        return False

def registrar_log(accion: str, modulo: str, descripcion: str, usuario: str = "Sistema"):
    #guarda un registro de actividad en la coleccion de auditoria de forma automatica
    try:
        db.auditoria.insert_one({
            "accion": accion,
            "modulo": modulo,
            "descripcion": descripcion,
            "usuario": usuario,
            "fecha_completa": datetime.now(),
            "ip": "127.0.0.1"
        })
    except Exception as e:
        print(f"error al registrar log: {e}")


# ============================================
# CRUD DE EMPLEADOS
# ============================================

def crear_empleado(datos: dict) -> Tuple[bool, Any]:
    #crea un nuevo empleado en la base de datos y genera log
    try:
        campos_requeridos = ["identificador", "nombre", "apellidos", "email", "contrasenya"]
        for campo in campos_requeridos:
            if campo not in datos or not datos[campo]:
                return (False, f"el campo '{campo}' es obligatorio")
        
        resultado = db.empleados.insert_one(datos)
        datos["_id"] = str(resultado.inserted_id)
        
        #registro en auditoria
        registrar_log("Crear", "Usuarios", f"usuario registrado: {datos['nombre']} {datos['apellidos']}")
        
        return (True, datos)
    except Exception as e:
        return (False, str(e))


def obtener_empleado(id_empleado: str) -> Tuple[bool, Any]:
    #obtiene un empleado por su id
    if not es_id_valido(id_empleado):
        return (False, "id no válido")
    
    empleado = db.empleados.find_one({"_id": ObjectId(id_empleado)})
    if empleado:
        empleado["_id"] = str(empleado["_id"])
        return (True, empleado)
    return (False, "empleado no encontrado")


def obtener_empleado_por_email(email: str) -> Tuple[bool, Any]:
    #obtiene un empleado por su email para login
    empleado = db.empleados.find_one({"email": email})
    if empleado:
        empleado["_id"] = str(empleado["_id"])
        return (True, empleado)
    return (False, "empleado no encontrado")


def obtener_todos_empleados() -> Tuple[bool, Any]:
    #obtiene todos los empleados de la base de datos
    try:
        empleados = list(db.empleados.find())
        for emp in empleados:
            emp["_id"] = str(emp["_id"])
        return (True, empleados)
    except Exception as e:
        return (False, str(e))


def actualizar_empleado(id_empleado: str, datos: dict) -> Tuple[bool, Any]:
    #actualiza los datos de un empleado y genera log
    if not es_id_valido(id_empleado):
        return (False, "id no válido")
    
    try:
        resultado = db.empleados.update_one(
            {"_id": ObjectId(id_empleado)},
            {"$set": datos}
        )
        if resultado.matched_count > 0:
            registrar_log("Editar", "Usuarios", f"datos actualizados del usuario id: {id_empleado}")
            return (True, "empleado actualizado")
        return (False, "no se encontró el empleado")
    except Exception as e:
        return (False, str(e))


def eliminar_empleado(id_empleado: str) -> Tuple[bool, Any]:
    #elimina un empleado de la base de datos y genera log
    if not es_id_valido(id_empleado):
        return (False, "id no válido")
    
    try:
        #obtenemos nombre para el log antes de borrar
        emp = db.empleados.find_one({"_id": ObjectId(id_empleado)})
        nom_complet = f"{emp['nombre']} {emp['apellidos']}" if emp else id_empleado
        
        resultado = db.empleados.delete_one({"_id": ObjectId(id_empleado)})
        if resultado.deleted_count > 0:
            registrar_log("Eliminar", "Usuarios", f"usuario eliminado: {nom_complet}")
            return (True, "empleado eliminado")
        return (False, "no se encontró el empleado")
    except Exception as e:
        return (False, str(e))


# ============================================
# CRUD DE DEPARTAMENTOS
# ============================================

def crear_departamento(datos: dict) -> Tuple[bool, Any]:
    #crea un nuevo departamento y genera log
    try:
        if "nombre" not in datos or not datos["nombre"]:
            return (False, "el nombre del departamento es obligatorio")
        
        resultado = db.departamentos.insert_one(datos)
        datos["_id"] = str(resultado.inserted_id)
        
        registrar_log("Crear", "Departamentos", f"departamento creado: {datos['nombre']}")
        return (True, datos)
    except Exception as e:
        return (False, str(e))


def obtener_departamento(id_departamento: str) -> Tuple[bool, Any]:
    #obtiene un departamento por su id
    if not es_id_valido(id_departamento):
        return (False, "id no válido")
    
    depto = db.departamentos.find_one({"_id": ObjectId(id_departamento)})
    if depto:
        depto["_id"] = str(depto["_id"])
        return (True, depto)
    return (False, "departamento no encontrado")


def obtener_todos_departamentos() -> Tuple[bool, Any]:
    #obtiene todos los departamentos
    try:
        deptos = list(db.departamentos.find())
        for d in deptos:
            d["_id"] = str(d["_id"])
        return (True, deptos)
    except Exception as e:
        return (False, str(e))


def actualizar_departamento(id_departamento: str, datos: dict) -> Tuple[bool, Any]:
    #actualiza un departamento y genera log
    if not es_id_valido(id_departamento):
        return (False, "id no válido")
    
    try:
        resultado = db.departamentos.update_one(
            {"_id": ObjectId(id_departamento)},
            {"$set": datos}
        )
        if resultado.matched_count > 0:
            registrar_log("Editar", "Departamentos", f"departamento actualizado id: {id_departamento}")
            return (True, "departamento actualizado")
        return (False, "no se encontró el departamento")
    except Exception as e:
        return (False, str(e))


def eliminar_departamento(id_departamento: str) -> Tuple[bool, Any]:
    #elimina un departamento y genera log
    if not es_id_valido(id_departamento):
        return (False, "id no válido")
    
    try:
        resultado = db.departamentos.delete_one({"_id": ObjectId(id_departamento)})
        if resultado.deleted_count > 0:
            registrar_log("Eliminar", "Departamentos", f"departamento borrado id: {id_departamento}")
            return (True, "departamento eliminado")
        return (False, "no se encontró el departamento")
    except Exception as e:
        return (False, str(e))


# ============================================
# CRUD DE EQUIPOS
# ============================================

def crear_equipo(datos: dict) -> Tuple[bool, Any]:
    #crea un nuevo equipo y genera log
    try:
        if "nombre" not in datos or not datos["nombre"]:
            return (False, "el nombre del equipo es obligatorio")
        
        resultado = db.equipos.insert_one(datos)
        datos["_id"] = str(resultado.inserted_id)
        
        registrar_log("Crear", "Equipos", f"nuevo equipo creado: {datos['nombre']}")
        return (True, datos)
    except Exception as e:
        return (False, str(e))


def obtener_equipo(id_equipo: str) -> Tuple[bool, Any]:
    #obtiene un equipo por su id
    if not es_id_valido(id_equipo):
        return (False, "id no válido")
    
    equipo = db.equipos.find_one({"_id": ObjectId(id_equipo)})
    if equipo:
        equipo["_id"] = str(equipo["_id"])
        return (True, equipo)
    return (False, "equipo no encontrado")


def obtener_todos_equipos() -> Tuple[bool, Any]:
    #obtiene todos los equipos
    try:
        equipos = list(db.equipos.find())
        for e in equipos:
            e["_id"] = str(e["_id"])
        return (True, equipos)
    except Exception as e:
        return (False, str(e))


def actualizar_equipo(id_equipo: str, datos: dict) -> Tuple[bool, Any]:
    #actualiza un equipo y genera log
    if not es_id_valido(id_equipo):
        return (False, "id no válido")
    
    try:
        resultado = db.equipos.update_one(
            {"_id": ObjectId(id_equipo)},
            {"$set": datos}
        )
        if resultado.matched_count > 0:
            registrar_log("Editar", "Equipos", f"equipo editado id: {id_equipo}")
            return (True, "equipo actualizado")
        return (False, "no se encontró el equipo")
    except Exception as e:
        return (False, str(e))


def eliminar_equipo(id_equipo: str) -> Tuple[bool, Any]:
    #elimina un equipo y genera log
    if not es_id_valido(id_equipo):
        return (False, "id no válido")
    
    try:
        resultado = db.equipos.delete_one({"_id": ObjectId(id_equipo)})
        if resultado.deleted_count > 0:
            registrar_log("Eliminar", "Equipos", f"equipo eliminado id: {id_equipo}")
            return (True, "equipo eliminado")
        return (False, "no se encontró el equipo")
    except Exception as e:
        return (False, str(e))


# ============================================
# CRUD DE PROYECTOS
# ============================================

def crear_proyecto(datos: dict) -> Tuple[bool, Any]:
    #crea un nuevo proyecto y genera log
    try:
        if "nombre" not in datos or not datos["nombre"]:
            return (False, "el nombre del proyecto es obligatorio")
        
        resultado = db.proyectos.insert_one(datos)
        datos["_id"] = str(resultado.inserted_id)
        
        registrar_log("Crear", "Proyectos", f"proyecto iniciado: {datos['nombre']}")
        return (True, datos)
    except Exception as e:
        return (False, str(e))


def obtener_proyecto(id_proyecto: str) -> Tuple[bool, Any]:
    #obtiene un proyecto por su id
    if not es_id_valido(id_proyecto):
        return (False, "id no válido")
    
    proyecto = db.proyectos.find_one({"_id": ObjectId(id_proyecto)})
    if proyecto:
        proyecto["_id"] = str(proyecto["_id"])
        return (True, proyecto)
    return (False, "proyecto no encontrado")


def obtener_todos_proyectos() -> Tuple[bool, Any]:
    #obtiene todos los proyectos
    try:
        proyectos = list(db.proyectos.find())
        for p in proyectos:
            p["_id"] = str(p["_id"])
        return (True, proyectos)
    except Exception as e:
        return (False, str(e))


def actualizar_proyecto(id_proyecto: str, datos: dict) -> Tuple[bool, Any]:
    #actualiza un proyecto y genera log
    if not es_id_valido(id_proyecto):
        return (False, "id no válido")
    
    try:
        resultado = db.proyectos.update_one(
            {"_id": ObjectId(id_proyecto)},
            {"$set": datos}
        )
        if resultado.matched_count > 0:
            registrar_log("Editar", "Proyectos", f"proyecto actualizado id: {id_proyecto}")
            return (True, "proyecto actualizado")
        return (False, "no se encontró el proyecto")
    except Exception as e:
        return (False, str(e))


def eliminar_proyecto(id_proyecto: str) -> Tuple[bool, Any]:
    #elimina un proyecto y genera log
    if not es_id_valido(id_proyecto):
        return (False, "id no válido")
    
    try:
        resultado = db.proyectos.delete_one({"_id": ObjectId(id_proyecto)})
        if resultado.deleted_count > 0:
            registrar_log("Eliminar", "Proyectos", f"proyecto borrado id: {id_proyecto}")
            return (True, "proyecto eliminado")
        return (False, "no se encontró el proyecto")
    except Exception as e:
        return (False, str(e))


# ============================================
# CRUD DE TAREAS
# ============================================

def crear_tarea(datos: dict) -> Tuple[bool, Any]:
    #crea una nueva tarea y genera log
    try:
        if "titulo" not in datos or not datos["titulo"]:
            return (False, "el título de la tarea es obligatorio")
        
        if "estado" not in datos:
            datos["estado"] = "pendiente"
        if "fecha_inicio" not in datos:
            datos["fecha_inicio"] = datetime.now()
        
        resultado = db.tareas.insert_one(datos)
        datos["_id"] = str(resultado.inserted_id)
        
        registrar_log("Crear", "Tareas", f"tarea creada: {datos['titulo']}")
        return (True, datos)
    except Exception as e:
        return (False, str(e))


def obtener_tarea(id_tarea: str) -> Tuple[bool, Any]:
    #obtiene una tarea por su id
    if not es_id_valido(id_tarea):
        return (False, "id no válido")
    
    tarea = db.tareas.find_one({"_id": ObjectId(id_tarea)})
    if tarea:
        tarea["_id"] = str(tarea["_id"])
        return (True, tarea)
    return (False, "tarea no encontrada")


def obtener_todas_tareas() -> Tuple[bool, Any]:
    #obtiene todas las tareas
    try:
        tareas = list(db.tareas.find())
        for t in tareas:
            t["_id"] = str(t["_id"])
        return (True, tareas)
    except Exception as e:
        return (False, str(e))


def obtener_tareas_por_estado(estado: str) -> Tuple[bool, Any]:
    #obtiene tareas filtradas por estado
    try:
        tareas = list(db.tareas.find({"estado": estado}))
        for t in tareas:
            t["_id"] = str(t["_id"])
        return (True, tareas)
    except Exception as e:
        return (False, str(e))


def obtener_tareas_pendientes_usuario(id_usuario: str, nombre_usuario: str) -> Tuple[bool, Any]:
    #obtiene las tareas pendientes que el usuario creó O tiene asignadas
    try:
        tareas = list(db.tareas.find({
            "estado": "pendiente",
            "$or": [
                {"asignados.id_usuario": id_usuario},  # Asignadas al usuario
                {"compartido_por": nombre_usuario}      # Creadas por el usuario
            ]
        }))
        for t in tareas:
            t["_id"] = str(t["_id"])
        return (True, tareas)
    except Exception as e:
        return (False, str(e))


def obtener_tareas_por_usuario(id_usuario: str) -> Tuple[bool, Any]:
    #obtiene las tareas asignadas a un usuario específico
    try:
        tareas = list(db.tareas.find({"asignados.id_usuario": id_usuario}))
        for t in tareas:
            t["_id"] = str(t["_id"])
        return (True, tareas)
    except Exception as e:
        return (False, str(e))


def obtener_tareas_atrasadas() -> Tuple[bool, Any]:
    #obtiene las tareas que están atrasadas y no completadas
    try:
        ahora = datetime.now()
        tareas = list(db.tareas.find({
            "estado": {"$ne": "completada"},
            "fecha_limite": {"$lt": ahora}
        }))
        for t in tareas:
            t["_id"] = str(t["_id"])
        return (True, tareas)
    except Exception as e:
        return (False, str(e))


def actualizar_tarea(id_tarea, datos: dict) -> Tuple[bool, Any]:
    #actualiza una tarea y genera log
    #convierte a string si viene como ObjectId
    id_str = str(id_tarea) if isinstance(id_tarea, ObjectId) else id_tarea
    
    if not es_id_valido(id_str):
        return (False, "id no válido")
    
    try:
        #añadimos fecha de modificación automáticamente
        datos["fecha_modificacion"] = datetime.now()
        
        resultado = db.tareas.update_one(
            {"_id": ObjectId(id_str)},
            {"$set": datos}
        )
        if resultado.matched_count > 0:
            titulo = datos.get("titulo", id_str)
            registrar_log("Editar", "Tareas", f"tarea actualizada: {titulo}")
            return (True, "tarea actualizada")
        return (False, "no se encontró la tarea")
    except Exception as e:
        return (False, str(e))


def completar_tarea(id_tarea: str) -> Tuple[bool, Any]:
    #marca una tarea como completada en la bd y genera log
    exito, msg = actualizar_tarea(id_tarea, {
        "estado": "completada",
        "fecha_completado": datetime.now()
    })
    if exito:
        registrar_log("Editar", "Tareas", f"tarea marcada como finalizada id: {id_tarea}")
    return exito, msg


def eliminar_tarea(id_tarea: str) -> Tuple[bool, Any]:
    #elimina una tarea y genera log
    if not es_id_valido(id_tarea):
        return (False, "id no válido")
    
    try:
        resultado = db.tareas.delete_one({"_id": ObjectId(id_tarea)})
        if resultado.deleted_count > 0:
            registrar_log("Eliminar", "Tareas", f"tarea borrada id: {id_tarea}")
            return (True, "tarea eliminada")
        return (False, "no se encontró la tarea")
    except Exception as e:
        return (False, str(e))


# ============================================
# CRUD DE ROLES
# ============================================

def crear_rol(datos: dict) -> Tuple[bool, Any]:
    #crea un nuevo rol y genera log
    try:
        if "nombre" not in datos or not datos["nombre"]:
            return (False, "el nombre del rol es obligatorio")
        
        resultado = db.roles.insert_one(datos)
        datos["_id"] = str(resultado.inserted_id)
        
        registrar_log("Crear", "Roles", f"nuevo rol definido: {datos['nombre']}")
        return (True, datos)
    except Exception as e:
        return (False, str(e))


def obtener_rol(id_rol: str) -> Tuple[bool, Any]:
    #obtiene un rol por su id
    if not es_id_valido(id_rol):
        return (False, "id no válido")
    
    rol = db.roles.find_one({"_id": ObjectId(id_rol)})
    if rol:
        rol["_id"] = str(rol["_id"])
        return (True, rol)
    return (False, "rol no encontrado")


def obtener_todos_roles() -> Tuple[bool, Any]:
    #obtiene todos los roles
    try:
        roles = list(db.roles.find())
        for r in roles:
            r["_id"] = str(r["_id"])
        return (True, roles)
    except Exception as e:
        return (False, str(e))


def actualizar_rol(id_rol: str, datos: dict) -> Tuple[bool, Any]:
    #actualiza un rol y genera log
    if not es_id_valido(id_rol):
        return (False, "id no válido")
    
    try:
        resultado = db.roles.update_one(
            {"_id": ObjectId(id_rol)},
            {"$set": datos}
        )
        if resultado.matched_count > 0:
            registrar_log("Editar", "Roles", f"rol actualizado id: {id_rol}")
            return (True, "rol actualizado")
        return (False, "no se encontró el rol")
    except Exception as e:
        return (False, str(e))


def eliminar_rol(id_rol: str) -> Tuple[bool, Any]:
    #elimina un rol y genera log
    if not es_id_valido(id_rol):
        return (False, "id no válido")
    
    try:
        resultado = db.roles.delete_one({"_id": ObjectId(id_rol)})
        if resultado.deleted_count > 0:
            registrar_log("Eliminar", "Roles", f"rol eliminado id: {id_rol}")
            return (True, "rol eliminado")
        return (False, "no se encontró el rol")
    except Exception as e:
        return (False, str(e))


# ============================================
# FUNCIONES DE AUTENTICACIÓN
# ============================================

def validar_login(email: str, contrasenya: str) -> Tuple[bool, Any]:
    #valida las credenciales de un usuario y genera logs
    if not email or not contrasenya:
        return (False, "email y contraseña son obligatorios")
    
    empleado = db.empleados.find_one({"email": email})
    
    if not empleado:
        registrar_log("Login", "Sistema", f"fallo de acceso: email {email} no existe")
        return (False, "usuario no encontrado")
    
    if empleado["contrasenya"] != contrasenya:
        registrar_log("Login", "Sistema", f"fallo de acceso: password incorrecta para {email}")
        return (False, "contraseña incorrecta")
    
    # login exitoso
    empleado["_id"] = str(empleado["_id"])
    registrar_log("Login", "Sistema", f"sesión iniciada correctamente: {email}")
    return (True, empleado)


def cambiar_contrasenya(id_empleado: str, contrasenya_actual: str, contrasenya_nueva: str) -> Tuple[bool, Any]:
    #cambia la contraseña de un empleado y genera log
    exito, resultado = obtener_empleado(id_empleado)
    
    if not exito:
        return (False, "empleado no encontrado")
    
    if resultado["contrasenya"] != contrasenya_actual:
        return (False, "la contraseña actual no es correcta")
    
    exito_upd, msg = actualizar_empleado(id_empleado, {"contrasenya": contrasenya_nueva})
    if exito_upd:
        registrar_log("Editar", "Usuarios", f"contraseña cambiada para id: {id_empleado}")
    return exito_upd, msg


# ============================================
# FUNCIONES DE FILTRADO Y ORDENACIÓN
# ============================================

def filtrar_tareas(tareas, filtros, texto_busqueda=""):
    """
    Filtra las tareas según los criterios especificados
    
    Parámetros:
    - tareas: lista de diccionarios con las tareas
    - filtros: diccionario con los filtros activos
        - prioridad: "Todas", "Alta", "Media", "Baja"
        - tag: "Todos" o el tag específico
        - proyecto: "Todos" o el proyecto específico
    - texto_busqueda: texto para buscar en título y proyecto
    
    Retorna: lista de tareas filtradas
    """
    resultado = []
    
    #recorremos todas las tareas
    for tarea in tareas:
        incluir = True
        
        #filtro por búsqueda de texto
        if texto_busqueda:
            texto = texto_busqueda.lower()
            titulo = tarea.get("titulo", "").lower()
            proyecto = tarea.get("proyecto", "").lower()
            if texto not in titulo and texto not in proyecto:
                incluir = False
        
        #filtro por prioridad (comparamos en minúsculas para evitar problemas)
        filtro_prioridad = filtros.get("prioridad", "Todas")
        if filtro_prioridad != "Todas":
            prioridad_tarea = tarea.get("prioridad", "").lower()
            prioridad_filtro = filtro_prioridad.lower()
            if prioridad_tarea != prioridad_filtro:
                incluir = False
        
        #filtro por tag
        filtro_tag = filtros.get("tag", "Todos")
        if filtro_tag != "Todos":
            if tarea.get("tag") != filtro_tag:
                incluir = False
        
        #filtro por proyecto
        filtro_proyecto = filtros.get("proyecto", "Todos")
        if filtro_proyecto != "Todos":
            if tarea.get("proyecto") != filtro_proyecto:
                incluir = False
        
        #si pasa todos los filtros, la añadimos
        if incluir:
            resultado.append(tarea)
    
    return resultado


def ordenar_tareas(tareas, criterio_orden, campo_fecha="fecha_fin"):
    """
    Ordena las tareas según el criterio especificado usando bubble sort
    
    Parámetros:
    - tareas: lista de tareas a ordenar
    - criterio_orden: string con el criterio de ordenación
    - campo_fecha: nombre del campo de fecha a usar para ordenar
    
    Retorna: lista de tareas ordenadas
    """
    resultado = tareas.copy()
    
    #ordenamos usando bubble sort
    for i in range(len(resultado)):
        for j in range(len(resultado) - 1):
            intercambiar = False
            
            #ordenar alfabéticamente A-Z
            if criterio_orden == "Alfabético A-Z":
                titulo_j = resultado[j].get("titulo", "").lower()
                titulo_j1 = resultado[j+1].get("titulo", "").lower()
                if titulo_j > titulo_j1:
                    intercambiar = True
            
            #ordenar alfabéticamente Z-A
            elif criterio_orden == "Alfabético Z-A":
                titulo_j = resultado[j].get("titulo", "").lower()
                titulo_j1 = resultado[j+1].get("titulo", "").lower()
                if titulo_j < titulo_j1:
                    intercambiar = True
            
            #ordenar por prioridad alta primero
            elif criterio_orden == "Por prioridad alta":
                #soportamos mayúsculas y minúsculas
                orden_prioridad = {"alta": 0, "media": 1, "baja": 2}
                prioridad_j = resultado[j].get("prioridad", "media").lower()
                prioridad_j1 = resultado[j+1].get("prioridad", "media").lower()
                valor_j = orden_prioridad.get(prioridad_j, 1)
                valor_j1 = orden_prioridad.get(prioridad_j1, 1)
                if valor_j > valor_j1:
                    intercambiar = True
            
            #ordenar por prioridad baja primero
            elif criterio_orden == "Por prioridad baja":
                #soportamos mayúsculas y minúsculas
                orden_prioridad = {"alta": 2, "media": 1, "baja": 0}
                prioridad_j = resultado[j].get("prioridad", "media").lower()
                prioridad_j1 = resultado[j+1].get("prioridad", "media").lower()
                valor_j = orden_prioridad.get(prioridad_j, 1)
                valor_j1 = orden_prioridad.get(prioridad_j1, 1)
                if valor_j > valor_j1:
                    intercambiar = True
            
            #ordenar por proyecto
            elif criterio_orden == "Por proyecto":
                proyecto_j = resultado[j].get("proyecto", "").lower()
                proyecto_j1 = resultado[j+1].get("proyecto", "").lower()
                if proyecto_j > proyecto_j1:
                    intercambiar = True
            
            #ordenar por fecha ascendente
            elif criterio_orden == "Fecha ascendente":
                fecha_j = resultado[j].get(campo_fecha, "")
                fecha_j1 = resultado[j+1].get(campo_fecha, "")
                #si no hay fecha, ponemos una muy alta
                if not fecha_j:
                    fecha_j = "99/99/99"
                if not fecha_j1:
                    fecha_j1 = "99/99/99"
                if fecha_j > fecha_j1:
                    intercambiar = True
            
            #ordenar por fecha descendente
            elif criterio_orden == "Fecha descendente":
                fecha_j = resultado[j].get(campo_fecha, "")
                fecha_j1 = resultado[j+1].get(campo_fecha, "")
                #si no hay fecha, ponemos una muy baja
                if not fecha_j:
                    fecha_j = "00/00/00"
                if not fecha_j1:
                    fecha_j1 = "00/00/00"
                if fecha_j < fecha_j1:
                    intercambiar = True
            
            #ordenar por más atrasado primero
            elif criterio_orden == "Más atrasado primero":
                dias_j = resultado[j].get("dias_atrasado", 0)
                dias_j1 = resultado[j+1].get("dias_atrasado", 0)
                if dias_j < dias_j1:
                    intercambiar = True
            
            #ordenar por menos atrasado primero
            elif criterio_orden == "Menos atrasado primero":
                dias_j = resultado[j].get("dias_atrasado", 0)
                dias_j1 = resultado[j+1].get("dias_atrasado", 0)
                if dias_j > dias_j1:
                    intercambiar = True
            
            #intercambiamos si es necesario
            if intercambiar:
                temporal = resultado[j]
                resultado[j] = resultado[j+1]
                resultado[j+1] = temporal
    
    return resultado


def filtrar_y_ordenar(tareas, filtros, texto_busqueda="", criterio_orden="", campo_fecha="fecha_fin"):
    """
    Función que combina filtrado y ordenación
    
    Parámetros:
    - tareas: lista de tareas
    - filtros: diccionario con los filtros
    - texto_busqueda: texto para buscar
    - criterio_orden: criterio de ordenación
    - campo_fecha: campo de fecha para ordenar
    
    Retorna: lista de tareas filtradas y ordenadas
    """
    #primero filtramos
    tareas_filtradas = filtrar_tareas(tareas, filtros, texto_busqueda)
    
    #luego ordenamos si hay criterio
    if criterio_orden:
        tareas_ordenadas = ordenar_tareas(tareas_filtradas, criterio_orden, campo_fecha)
        return tareas_ordenadas
    
    return tareas_filtradas