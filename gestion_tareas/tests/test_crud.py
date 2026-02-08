import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
import sys
import os

# Añadir el directorio del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gestion_tareas.modelos.crud import (
    crear_tarea, 
    obtener_todas_tareas, 
    crear_empleado, 
    crear_departamento,
    crear_proyecto,
    get_db 
)

class TestCRUD:

    @pytest.fixture
    def mock_db(self):
        # Parchear get_db para devolver directamente nuestra base de datos simulada
        mock_database = MagicMock()
        with patch('modelos.crud.get_db', return_value=mock_database) as patched_get_db:
            yield mock_database

    def test_crear_tarea_exito(self, mock_db):
        datos_tarea = {
            "titulo": "Tarea de Prueba",
            "requisitos": "Requisitos de la tarea",
            "estado": "pendiente",
            "tags": ["Dev"],
            "icono": "📝",
            "id_proyecto": "000000000000000000000123", 
            "proyecto": "Proyecto A",
            "prioridad": "alta",
            "asignados": [],
            "compartido_por": "Usuario",
            "fecha_inicio": datetime.now(),
            "fecha_limite": None,
            "atrasado": False
        }
        
        # Configurar el retorno simulado para insert_one
        mock_resultado = MagicMock()
        mock_resultado.inserted_id = "nuevo_id_123"
        mock_db.tareas.insert_one.return_value = mock_resultado

        exito, resultado = crear_tarea(datos_tarea)

        assert exito is True
        assert resultado["_id"] == "nuevo_id_123"
        
        mock_db.tareas.insert_one.assert_called_once()
        mock_db.auditoria.insert_one.assert_called()

    def test_crear_tarea_validacion_fallida(self, mock_db):
        datos_tarea = {
            "requisitos": "Requisitos"
        }

        exito, resultado = crear_tarea(datos_tarea)

        assert exito is False
        # crear_tarea devuelve str(e) en error de validación
        assert isinstance(resultado, str) 

    def test_obtener_todas_tareas(self, mock_db):
        tareas_simuladas = [
            {"_id": "1", "titulo": "Tarea 1", "estado": "pendiente"},
            {"_id": "2", "titulo": "Tarea 2", "estado": "completada"}
        ]
        mock_db.tareas.find.return_value = tareas_simuladas

        exito, tareas = obtener_todas_tareas()

        assert exito is True
        assert len(tareas) == 2
        assert tareas[0]["titulo"] == "Tarea 1"

    def test_crear_empleado_exito(self, mock_db):
        datos_empleado = {
            "identificador": "12345678Z", 
            "nombre": "Juan",
            "apellidos": "Pérez",
            "email": "juan@test.com",
            "contrasenya": "pass",
            "empresa": "TechCorp",
            "equipo": "Equipo Dev",
            "departamento": {"nombre": "IT", "ubicacion": "Madrid"},
            "cargo": "Desarrollador",
            "id_empleado": "EMP001",
            "ubicacion": "Remoto",
            "fecha_incorporacion": datetime.now()
        }
        
        # Simular comprobación de duplicados (find_one devuelve None)
        # Nota: El código usa la colección 'empleados' para las comprobaciones
        mock_db.empleados.find_one.return_value = None
        
        mock_resultado = MagicMock()
        mock_resultado.inserted_id = "emp_id_123"
        mock_db.empleados.insert_one.return_value = mock_resultado

        exito, resultado = crear_empleado(datos_empleado)

        assert exito is True
        assert resultado["_id"] == "emp_id_123"

    def test_crear_empleado_duplicado(self, mock_db):
        datos_empleado = {
            "identificador": "12345678Z",
            "nombre": "Juan", 
            "apellidos": "Pérez",
            "email": "juan@test.com",
            "contrasenya": "pass",
            "empresa": "Tech",
            "equipo": "Equipo",
            "departamento": {"nombre": "IT", "ubicacion": "Madrid"},
            "cargo": "Desarrollador",
            "id_empleado": "EMP001",
            "ubicacion": "Remoto",
            "fecha_incorporacion": datetime.now()
        }
        
        mock_db.empleados.find_one.return_value = {"_id": "existente"}

        exito, resultado = crear_empleado(datos_empleado)

        assert exito is False
        assert any("registrado" in err["msg"] for err in resultado)

    def test_crear_departamento_exito(self, mock_db):
        datos_depto = {
            "nombre": "IT",
            "codigo": "IT01",
            "empresa": "Corp",
            "responsable": "Admin",
            "email": "it@corp.com",
            "telefono": "123456789"
        }
        
        mock_db.departamentos.find_one.return_value = None
        mock_resultado = MagicMock()
        mock_resultado.inserted_id = "dept_id_123"
        mock_db.departamentos.insert_one.return_value = mock_resultado

        exito, resultado = crear_departamento(datos_depto)

        assert exito is True
        assert resultado["_id"] == "dept_id_123"

    def test_crear_proyecto_exito(self, mock_db):
        datos_proy = {
            "nombre": "Nuevo Proyecto",
            "codigo": "PRY001",
            "responsable": "Manager",
            "cliente": "Cliente",
            "presupuesto": "1000",
            "fecha_inicio": datetime.now()
        }
        
        mock_db.proyectos.find_one.return_value = None
        mock_resultado = MagicMock()
        mock_resultado.inserted_id = "pry_id_123"
        mock_db.proyectos.insert_one.return_value = mock_resultado
        
        exito, resultado = crear_proyecto(datos_proy)
        
        assert exito is True