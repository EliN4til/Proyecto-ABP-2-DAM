_usuario_activo = None
#variable para saber si el usuario viene de admin o de personal
_contexto_dashboard = "personal" 

def guardar_usuario(datos_usuario: dict):
    #guarda los datos del usuario que ha iniciado sesión
    global _usuario_activo
    _usuario_activo = datos_usuario

def obtener_usuario() -> dict:
    #devuelve los datos del usuario activo o none si no hay sesión
    return _usuario_activo

def obtener_nombre_usuario() -> str:
    #devuelve el nombre del usuario activo o 'usuario' si no hay sesión
    if _usuario_activo and "nombre" in _usuario_activo:
        return _usuario_activo["nombre"]
    return "Usuario"

def obtener_id_usuario() -> str:
    #devuelve el id del usuario activo o none si no hay sesión
    if _usuario_activo and "_id" in _usuario_activo:
        return _usuario_activo["_id"]
    return None

def hay_sesion() -> bool:
    #comprueba si hay un usuario con sesión activa
    return _usuario_activo is not None

def cerrar_sesion():
    #cierra la sesión del usuario activo
    global _usuario_activo
    _usuario_activo = None

def establecer_contexto(contexto: str):
    #guarda de qué panel venimos (admin o personal)
    global _contexto_dashboard
    _contexto_dashboard = contexto

def obtener_contexto() -> str:
    #recupera el contexto guardado
    return _contexto_dashboard