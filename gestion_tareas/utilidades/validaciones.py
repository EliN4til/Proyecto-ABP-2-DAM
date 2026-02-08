"""
Módulo de validaciones para formularios
Contiene funciones para validar emails, teléfonos y DNIs españoles
"""

from typing import Tuple, Optional


def validar_email(email: str) -> Tuple[bool, str]:
    """
    Valida que un email tenga un formato correcto de forma simple
    
    Args:
        email: El email a validar
        
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if not email or not email.strip():
        return (True, "")  # Email vacío es válido (campo opcional)
    
    email_limpio = email.strip()
    
    # Verificar que tenga el símbolo @
    if "@" not in email_limpio:
        return (False, "El email debe contener el símbolo @")
    
    # Dividir en dos partes: antes y después del @
    partes = email_limpio.split("@")
    
    # Debe haber exactamente un @
    if len(partes) != 2:
        return (False, "El email debe tener un solo símbolo @")
    
    nombre_usuario = partes[0]
    dominio = partes[1]
    
    # Verificar que el nombre de usuario no esté vacío
    if len(nombre_usuario) == 0:
        return (False, "El email debe tener un nombre antes del @")
    
    # Verificar que el dominio no esté vacío
    if len(dominio) == 0:
        return (False, "El email debe tener un dominio después del @")
    
    # Verificar que el dominio tenga un punto
    if "." not in dominio:
        return (False, "El dominio del email debe contener un punto (.)")
    
    # Verificar que haya contenido después del último punto
    partes_dominio = dominio.split(".")
    if len(partes_dominio[-1]) < 2:
        return (False, "El formato del email no es válido (ejemplo: usuario@dominio.com)")
    
    return (True, "")


def validar_telefono(telefono: str) -> Tuple[bool, str]:
    """
    Valida que un teléfono español tenga un formato correcto
    Acepta formatos: +34 XXX XXX XXX, +34 XXXXXXXXX, 6XXXXXXXX, 9XXXXXXXX, etc.
    
    Args:
        telefono: El número de teléfono a validar
        
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if not telefono or not telefono.strip():
        return (True, "")  # Teléfono vacío es válido (campo opcional)
    
    tel_limpio = telefono.strip().replace(" ", "").replace("-", "")
    
    # Comprobar longitud mínima (ej. al menos 6 dígitos para ser válido)
    if len(tel_limpio) < 6:
        return (False, "El teléfono es demasiado corto")
        
    # Caracteres válidos: dígitos y prefijo '+'
    if tel_limpio.startswith("+"):
        if not tel_limpio[1:].isdigit():
             return (False, "El teléfono solo puede contener números y el prefijo +")
    else:
        if not tel_limpio.isdigit():
            return (False, "El teléfono solo puede contener números")
            
    return (True, "")


def validar_dni(dni: str) -> Tuple[bool, str]:
    """
    Valida que un DNI español tenga un formato correcto
    Verifica tanto el formato (8 dígitos + letra) como la letra de control
    
    Args:
        dni: El DNI a validar
        
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if not dni or not dni.strip():
        return (True, "")  # DNI vacío es válido (campo opcional)
    
    dni_limpio = dni.strip().upper().replace(" ", "").replace("-", "")
    
    # Verificar longitud (debe ser 9 caracteres: 8 dígitos + 1 letra)
    if len(dni_limpio) != 9:
        return (False, "El formato del DNI no es válido (ejemplo: 12345678Z)")
    
    # Separar números y letra
    numeros = dni_limpio[0:8]
    letra = dni_limpio[8]
    
    # Verificar que los primeros 8 caracteres sean dígitos
    if not numeros.isdigit():
        return (False, "Los primeros 8 caracteres del DNI deben ser números")
    
    # Verificar que el último carácter sea una letra
    if not letra.isalpha():
        return (False, "El último carácter del DNI debe ser una letra")
    
    # Tabla de letras de control del DNI
    letras_control = "TRWAGMYFPDXBNJZSQVHLCKE"
    
    # Calcular la letra que debería tener
    numero_dni = int(numeros)
    posicion_letra = numero_dni % 23
    letra_esperada = letras_control[posicion_letra]
    
    # Verificar que la letra sea correcta
    if letra == letra_esperada:
        return (True, "")
    else:
        return (False, f"La letra del DNI no es correcta (debería ser {letra_esperada})")