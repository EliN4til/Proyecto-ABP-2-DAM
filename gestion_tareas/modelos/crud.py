"""
Operaciones CRUD para la base de datos MongoDB
Este archivo contiene todas las funciones necesarias para crear, leer, actualizar y eliminar
documentos de las diferentes colecciones de la base de datos.
"""

from bson import ObjectId
from datetime import datetime
from typing import Tuple, List, Optional, Any
from modelos.init import db


# ============================================
# FUNCIONES AUXILIARES
# ============================================

def es_id_valido(id_str: str) -> bool:
    """Comprueba si un string es un ObjectId válido de MongoDB"""
    try:
        ObjectId(id_str)
        return True
    except:
        return False


# ============================================
# CRUD DE EMPLEADOS
# ============================================

def crear_empleado(datos: dict) -> Tuple[bool, Any]:
    """
    Crea un nuevo empleado en la base de datos
    Devuelve (True, datos) si funciona o (False, error) si falla
    """
    try:
        #validamos campos obligatorios
        campos_requeridos = ["identificador", "nombre", "apellidos", "email", "contrasenya"]
        for campo in campos_requeridos:
            if campo not in datos or not datos[campo]:
                return (False, f"El campo '{campo}' es obligatorio")
        
        #insertamos el empleado
        resultado = db.empleados.insert_one(datos)
        datos["_id"] = str(resultado.inserted_id)
        return (True, datos)
    except Exception as e:
        return (False, str(e))


def obtener_empleado(id_empleado: str) -> Tuple[bool, Any]:
    """Obtiene un empleado por su ID"""
    if not es_id_valido(id_empleado):
        return (False, "ID no válido")
    
    empleado = db.empleados.find_one({"_id": ObjectId(id_empleado)})
    if empleado:
        empleado["_id"] = str(empleado["_id"])
        return (True, empleado)
    return (False, "Empleado no encontrado")


def obtener_empleado_por_email(email: str) -> Tuple[bool, Any]:
    """Obtiene un empleado por su email (para login)"""
    empleado = db.empleados.find_one({"email": email})
    if empleado:
        empleado["_id"] = str(empleado["_id"])
        return (True, empleado)
    return (False, "Empleado no encontrado")


def obtener_todos_empleados() -> Tuple[bool, Any]:
    """Obtiene todos los empleados de la base de datos"""
    try:
        empleados = list(db.empleados.find())
        for emp in empleados:
            emp["_id"] = str(emp["_id"])
        return (True, empleados)
    except Exception as e:
        return (False, str(e))


def actualizar_empleado(id_empleado: str, datos: dict) -> Tuple[bool, Any]:
    """Actualiza los datos de un empleado"""
    if not es_id_valido(id_empleado):
        return (False, "ID no válido")
    
    try:
        resultado = db.empleados.update_one(
            {"_id": ObjectId(id_empleado)},
            {"$set": datos}
        )
        if resultado.matched_count > 0:
            return (True, "Empleado actualizado")
        return (False, "No se encontró el empleado")
    except Exception as e:
        return (False, str(e))


def eliminar_empleado(id_empleado: str) -> Tuple[bool, Any]:
    """Elimina un empleado de la base de datos"""
    if not es_id_valido(id_empleado):
        return (False, "ID no válido")
    
    try:
        resultado = db.empleados.delete_one({"_id": ObjectId(id_empleado)})
        if resultado.deleted_count > 0:
            return (True, "Empleado eliminado")
        return (False, "No se encontró el empleado")
    except Exception as e:
        return (False, str(e))


# ============================================
# CRUD DE DEPARTAMENTOS
# ============================================

def crear_departamento(datos: dict) -> Tuple[bool, Any]:
    """Crea un nuevo departamento"""
    try:
        if "nombre" not in datos or not datos["nombre"]:
            return (False, "El nombre del departamento es obligatorio")
        
        resultado = db.departamentos.insert_one(datos)
        datos["_id"] = str(resultado.inserted_id)
        return (True, datos)
    except Exception as e:
        return (False, str(e))


def obtener_departamento(id_departamento: str) -> Tuple[bool, Any]:
    """Obtiene un departamento por su ID"""
    if not es_id_valido(id_departamento):
        return (False, "ID no válido")
    
    depto = db.departamentos.find_one({"_id": ObjectId(id_departamento)})
    if depto:
        depto["_id"] = str(depto["_id"])
        return (True, depto)
    return (False, "Departamento no encontrado")


def obtener_todos_departamentos() -> Tuple[bool, Any]:
    """Obtiene todos los departamentos"""
    try:
        deptos = list(db.departamentos.find())
        for d in deptos:
            d["_id"] = str(d["_id"])
        return (True, deptos)
    except Exception as e:
        return (False, str(e))


def actualizar_departamento(id_departamento: str, datos: dict) -> Tuple[bool, Any]:
    """Actualiza un departamento"""
    if not es_id_valido(id_departamento):
        return (False, "ID no válido")
    
    try:
        resultado = db.departamentos.update_one(
            {"_id": ObjectId(id_departamento)},
            {"$set": datos}
        )
        if resultado.matched_count > 0:
            return (True, "Departamento actualizado")
        return (False, "No se encontró el departamento")
    except Exception as e:
        return (False, str(e))


def eliminar_departamento(id_departamento: str) -> Tuple[bool, Any]:
    """Elimina un departamento"""
    if not es_id_valido(id_departamento):
        return (False, "ID no válido")
    
    try:
        resultado = db.departamentos.delete_one({"_id": ObjectId(id_departamento)})
        if resultado.deleted_count > 0:
            return (True, "Departamento eliminado")
        return (False, "No se encontró el departamento")
    except Exception as e:
        return (False, str(e))


# ============================================
# CRUD DE EQUIPOS
# ============================================

def crear_equipo(datos: dict) -> Tuple[bool, Any]:
    """Crea un nuevo equipo"""
    try:
        if "nombre" not in datos or not datos["nombre"]:
            return (False, "El nombre del equipo es obligatorio")
        
        resultado = db.equipos.insert_one(datos)
        datos["_id"] = str(resultado.inserted_id)
        return (True, datos)
    except Exception as e:
        return (False, str(e))


def obtener_equipo(id_equipo: str) -> Tuple[bool, Any]:
    """Obtiene un equipo por su ID"""
    if not es_id_valido(id_equipo):
        return (False, "ID no válido")
    
    equipo = db.equipos.find_one({"_id": ObjectId(id_equipo)})
    if equipo:
        equipo["_id"] = str(equipo["_id"])
        return (True, equipo)
    return (False, "Equipo no encontrado")


def obtener_todos_equipos() -> Tuple[bool, Any]:
    """Obtiene todos los equipos"""
    try:
        equipos = list(db.equipos.find())
        for e in equipos:
            e["_id"] = str(e["_id"])
        return (True, equipos)
    except Exception as e:
        return (False, str(e))


def actualizar_equipo(id_equipo: str, datos: dict) -> Tuple[bool, Any]:
    """Actualiza un equipo"""
    if not es_id_valido(id_equipo):
        return (False, "ID no válido")
    
    try:
        resultado = db.equipos.update_one(
            {"_id": ObjectId(id_equipo)},
            {"$set": datos}
        )
        if resultado.matched_count > 0:
            return (True, "Equipo actualizado")
        return (False, "No se encontró el equipo")
    except Exception as e:
        return (False, str(e))


def eliminar_equipo(id_equipo: str) -> Tuple[bool, Any]:
    """Elimina un equipo"""
    if not es_id_valido(id_equipo):
        return (False, "ID no válido")
    
    try:
        resultado = db.equipos.delete_one({"_id": ObjectId(id_equipo)})
        if resultado.deleted_count > 0:
            return (True, "Equipo eliminado")
        return (False, "No se encontró el equipo")
    except Exception as e:
        return (False, str(e))


# ============================================
# CRUD DE PROYECTOS
# ============================================

def crear_proyecto(datos: dict) -> Tuple[bool, Any]:
    """Crea un nuevo proyecto"""
    try:
        if "nombre" not in datos or not datos["nombre"]:
            return (False, "El nombre del proyecto es obligatorio")
        
        resultado = db.proyectos.insert_one(datos)
        datos["_id"] = str(resultado.inserted_id)
        return (True, datos)
    except Exception as e:
        return (False, str(e))


def obtener_proyecto(id_proyecto: str) -> Tuple[bool, Any]:
    """Obtiene un proyecto por su ID"""
    if not es_id_valido(id_proyecto):
        return (False, "ID no válido")
    
    proyecto = db.proyectos.find_one({"_id": ObjectId(id_proyecto)})
    if proyecto:
        proyecto["_id"] = str(proyecto["_id"])
        return (True, proyecto)
    return (False, "Proyecto no encontrado")


def obtener_todos_proyectos() -> Tuple[bool, Any]:
    """Obtiene todos los proyectos"""
    try:
        proyectos = list(db.proyectos.find())
        for p in proyectos:
            p["_id"] = str(p["_id"])
        return (True, proyectos)
    except Exception as e:
        return (False, str(e))


def actualizar_proyecto(id_proyecto: str, datos: dict) -> Tuple[bool, Any]:
    """Actualiza un proyecto"""
    if not es_id_valido(id_proyecto):
        return (False, "ID no válido")
    
    try:
        resultado = db.proyectos.update_one(
            {"_id": ObjectId(id_proyecto)},
            {"$set": datos}
        )
        if resultado.matched_count > 0:
            return (True, "Proyecto actualizado")
        return (False, "No se encontró el proyecto")
    except Exception as e:
        return (False, str(e))


def eliminar_proyecto(id_proyecto: str) -> Tuple[bool, Any]:
    """Elimina un proyecto"""
    if not es_id_valido(id_proyecto):
        return (False, "ID no válido")
    
    try:
        resultado = db.proyectos.delete_one({"_id": ObjectId(id_proyecto)})
        if resultado.deleted_count > 0:
            return (True, "Proyecto eliminado")
        return (False, "No se encontró el proyecto")
    except Exception as e:
        return (False, str(e))


# ============================================
# CRUD DE TAREAS
# ============================================

def crear_tarea(datos: dict) -> Tuple[bool, Any]:
    """Crea una nueva tarea"""
    try:
        if "titulo" not in datos or not datos["titulo"]:
            return (False, "El título de la tarea es obligatorio")
        
        #ponemos valores por defecto si no existen
        if "estado" not in datos:
            datos["estado"] = "pendiente"
        if "fecha_inicio" not in datos:
            datos["fecha_inicio"] = datetime.now()
        
        resultado = db.tareas.insert_one(datos)
        datos["_id"] = str(resultado.inserted_id)
        return (True, datos)
    except Exception as e:
        return (False, str(e))


def obtener_tarea(id_tarea: str) -> Tuple[bool, Any]:
    """Obtiene una tarea por su ID"""
    if not es_id_valido(id_tarea):
        return (False, "ID no válido")
    
    tarea = db.tareas.find_one({"_id": ObjectId(id_tarea)})
    if tarea:
        tarea["_id"] = str(tarea["_id"])
        return (True, tarea)
    return (False, "Tarea no encontrada")


def obtener_todas_tareas() -> Tuple[bool, Any]:
    """Obtiene todas las tareas"""
    try:
        tareas = list(db.tareas.find())
        for t in tareas:
            t["_id"] = str(t["_id"])
        return (True, tareas)
    except Exception as e:
        return (False, str(e))


def obtener_tareas_por_estado(estado: str) -> Tuple[bool, Any]:
    """Obtiene tareas filtradas por estado (pendiente, completada, etc)"""
    try:
        tareas = list(db.tareas.find({"estado": estado}))
        for t in tareas:
            t["_id"] = str(t["_id"])
        return (True, tareas)
    except Exception as e:
        return (False, str(e))


def obtener_tareas_por_usuario(id_usuario: str) -> Tuple[bool, Any]:
    """Obtiene las tareas asignadas a un usuario específico"""
    try:
        tareas = list(db.tareas.find({"asignados.id_usuario": id_usuario}))
        for t in tareas:
            t["_id"] = str(t["_id"])
        return (True, tareas)
    except Exception as e:
        return (False, str(e))


def obtener_tareas_atrasadas() -> Tuple[bool, Any]:
    """Obtiene las tareas que están atrasadas y NO completadas"""
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


def actualizar_tarea(id_tarea: str, datos: dict) -> Tuple[bool, Any]:
    """Actualiza una tarea"""
    if not es_id_valido(id_tarea):
        return (False, "ID no válido")
    
    try:
        resultado = db.tareas.update_one(
            {"_id": ObjectId(id_tarea)},
            {"$set": datos}
        )
        if resultado.matched_count > 0:
            return (True, "Tarea actualizada")
        return (False, "No se encontró la tarea")
    except Exception as e:
        return (False, str(e))


def completar_tarea(id_tarea: str) -> Tuple[bool, Any]:
    """Marca una tarea como completada en la BD"""
    return actualizar_tarea(id_tarea, {
        "estado": "completada",
        "fecha_completado": datetime.now()
    })


def eliminar_tarea(id_tarea: str) -> Tuple[bool, Any]:
    """Elimina una tarea"""
    if not es_id_valido(id_tarea):
        return (False, "ID no válido")
    
    try:
        resultado = db.tareas.delete_one({"_id": ObjectId(id_tarea)})
        if resultado.deleted_count > 0:
            return (True, "Tarea eliminada")
        return (False, "No se encontró la tarea")
    except Exception as e:
        return (False, str(e))


# ============================================
# CRUD DE ROLES
# ============================================

def crear_rol(datos: dict) -> Tuple[bool, Any]:
    """Crea un nuevo rol"""
    try:
        if "nombre" not in datos or not datos["nombre"]:
            return (False, "El nombre del rol es obligatorio")
        
        resultado = db.roles.insert_one(datos)
        datos["_id"] = str(resultado.inserted_id)
        return (True, datos)
    except Exception as e:
        return (False, str(e))


def obtener_rol(id_rol: str) -> Tuple[bool, Any]:
    """Obtiene un rol por su ID"""
    if not es_id_valido(id_rol):
        return (False, "ID no válido")
    
    rol = db.roles.find_one({"_id": ObjectId(id_rol)})
    if rol:
        rol["_id"] = str(rol["_id"])
        return (True, rol)
    return (False, "Rol no encontrado")


def obtener_todos_roles() -> Tuple[bool, Any]:
    """Obtiene todos los roles"""
    try:
        roles = list(db.roles.find())
        for r in roles:
            r["_id"] = str(r["_id"])
        return (True, roles)
    except Exception as e:
        return (False, str(e))


def actualizar_rol(id_rol: str, datos: dict) -> Tuple[bool, Any]:
    """Actualiza un rol"""
    if not es_id_valido(id_rol):
        return (False, "ID no válido")
    
    try:
        resultado = db.roles.update_one(
            {"_id": ObjectId(id_rol)},
            {"$set": datos}
        )
        if resultado.matched_count > 0:
            return (True, "Rol actualizado")
        return (False, "No se encontró el rol")
    except Exception as e:
        return (False, str(e))


def eliminar_rol(id_rol: str) -> Tuple[bool, Any]:
    """Elimina un rol"""
    if not es_id_valido(id_rol):
        return (False, "ID no válido")
    
    try:
        resultado = db.roles.delete_one({"_id": ObjectId(id_rol)})
        if resultado.deleted_count > 0:
            return (True, "Rol eliminado")
        return (False, "No se encontró el rol")
    except Exception as e:
        return (False, str(e))


# ============================================
# FUNCIONES DE AUTENTICACIÓN
# ============================================

def validar_login(email: str, contrasenya: str) -> Tuple[bool, Any]:
    """
    Valida las credenciales de un usuario
    Devuelve (True, empleado) si son correctas o (False, error) si no
    """
    if not email or not contrasenya:
        return (False, "Email y contraseña son obligatorios")
    
    empleado = db.empleados.find_one({"email": email})
    
    if not empleado:
        return (False, "Usuario no encontrado")
    
    if empleado["contrasenya"] != contrasenya:
        return (False, "Contraseña incorrecta")
    
    #convertimos el ObjectId a string
    empleado["_id"] = str(empleado["_id"])
    return (True, empleado)


def cambiar_contrasenya(id_empleado: str, contrasenya_actual: str, contrasenya_nueva: str) -> Tuple[bool, Any]:
    """Cambia la contraseña de un empleado"""
    exito, resultado = obtener_empleado(id_empleado)
    
    if not exito:
        return (False, "Empleado no encontrado")
    
    if resultado["contrasenya"] != contrasenya_actual:
        return (False, "La contraseña actual no es correcta")
    
    return actualizar_empleado(id_empleado, {"contrasenya": contrasenya_nueva})