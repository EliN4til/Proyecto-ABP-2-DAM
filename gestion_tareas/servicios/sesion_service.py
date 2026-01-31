_usuario_activo = None


def guardar_usuario(datos_usuario: dict):
    """Guarda los datos del usuario que ha iniciado sesión"""
    global _usuario_activo
    _usuario_activo = datos_usuario


def obtener_usuario() -> dict:
    """Devuelve los datos del usuario activo o None si no hay sesión"""
    return _usuario_activo


def obtener_nombre_usuario() -> str:
    """Devuelve el nombre del usuario activo o 'Usuario' si no hay sesión"""
    if _usuario_activo and "nombre" in _usuario_activo:
        return _usuario_activo["nombre"]
    return "Usuario"


def obtener_id_usuario() -> str:
    """Devuelve el id del usuario activo o None si no hay sesión"""
    if _usuario_activo and "_id" in _usuario_activo:
        return _usuario_activo["_id"]
    return None


def hay_sesion() -> bool:
    """Comprueba si hay un usuario con sesión activa"""
    return _usuario_activo is not None


def cerrar_sesion():
    """Cierra la sesión del usuario activo"""
    global _usuario_activo
    _usuario_activo = None
