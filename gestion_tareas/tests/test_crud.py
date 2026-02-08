import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

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
        # Fixture de Pytest para simular la base de datos.
        # Parcheamos 'gestion_tareas.modelos.crud.get_db' para que devuelva un objeto MagicMock
        # en lugar de conectarse a la base de datos real.
        mock_database = MagicMock()
        with patch('gestion_tareas.modelos.crud.get_db', return_value=mock_database) as patched_get_db:
            yield mock_database

    def test_crear_tarea_exito(self, mock_db):
        # Crear una tarea con datos válidos.
        datos_tarea = {
            "titulo": "Implementar Autenticación OAuth2",
            "requisitos": "Integrar Google y GitHub como proveedores de identidad.",
            "estado": "pendiente",
            "tags": ["Backend", "Seguridad"],
            "icono": "🔒",
            "id_proyecto": "000000000000000000000123", 
            "proyecto": "Plataforma E-learning V2",
            "prioridad": "alta",
            "asignados": [],
            "compartido_por": "Laura García",
            "fecha_inicio": datetime.now(),
            "fecha_limite": None,
            "atrasado": False
        }
        
        # Simular que la inserción en la BD devuelve un ID específico.
        mock_resultado = MagicMock()
        mock_resultado.inserted_id = "nuevo_id_123"
        mock_db.tareas.insert_one.return_value = mock_resultado

        exito, resultado = crear_tarea(datos_tarea)

        # Comprobamos que la operación fue exitosa y devuelve el ID correcto.
        assert exito is True
        assert resultado["_id"] == "nuevo_id_123"
        
        # Nos aseguramos que se llamó a insert_one en la colección 'tareas'
        # y que se registró la operación en 'auditoria'.
        mock_db.tareas.insert_one.assert_called_once()
        mock_db.auditoria.insert_one.assert_called()

    def test_crear_tarea_validacion_fallida(self, mock_db):
        # Intentar crear una tarea sin el campo obligatorio 'titulo'.
        datos_tarea = {
            "requisitos": "Solo requisitos, falta título"
        }

        exito, resultado = crear_tarea(datos_tarea)

        # Debe fallar y devolver un mensaje de error.
        assert exito is False
        assert isinstance(resultado, str) 

    def test_obtener_todas_tareas(self, mock_db):
        # Obtener la lista de todas las tareas.
        
        # Simular una lista de tareas devuelta por la BD.
        tareas_simuladas = [
            {"_id": "1", "titulo": "Revisión de Código API", "estado": "pendiente"},
            {"_id": "2", "titulo": "Actualizar Documentación", "estado": "completada"}
        ]
        mock_db.tareas.find.return_value = tareas_simuladas

        exito, tareas = obtener_todas_tareas()

        # Comprobamos que se reciben las tareas simuladas.
        assert exito is True
        assert len(tareas) == 2
        assert tareas[0]["titulo"] == "Revisión de Código API"

    def test_crear_empleado_exito(self, mock_db):
        # Crear un nuevo empleado.
        datos_empleado = {
            "identificador": "12345678Z", 
            "nombre": "Carlos",
            "apellidos": "Méndez Ruiz",
            "email": "carlos.mendez@techcorp.com",
            "contrasenya": "passSegura123",
            "empresa": "InnovaTech Solutions",
            "equipo": "Equipo Backend",
            "departamento": {"nombre": "Tecnología e Innovación", "ubicacion": "Madrid"},
            "cargo": "Ingeniero de Software Senior",
            "id_empleado": "EMP001",
            "ubicacion": "Remoto",
            "fecha_incorporacion": datetime.now()
        }
        
        # Simular que NO existe un empleado previo.
        mock_db.empleados.find_one.return_value = None
        
        # Simular inserción exitosa.
        mock_resultado = MagicMock()
        mock_resultado.inserted_id = "emp_id_123"
        mock_db.empleados.insert_one.return_value = mock_resultado

        exito, resultado = crear_empleado(datos_empleado)

        assert exito is True
        assert resultado["_id"] == "emp_id_123"

    def test_crear_empleado_duplicado(self, mock_db):
        # Intentar crear un empleado que ya existe.
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
        
        # Simular que SÍ existe un empleado.
        mock_db.empleados.find_one.return_value = {"_id": "existente"}

        exito, resultado = crear_empleado(datos_empleado)

        # Debe fallar indicando que ya está registrado.
        assert exito is False
        assert any("registrado" in err["msg"] for err in resultado)

    def test_crear_departamento_exito(self, mock_db):
        # Crear un nuevo departamento.
        datos_depto = {
            "nombre": "Tecnología e Innovación",
            "codigo": "TI-2024",
            "empresa": "InnovaTech Solutions",
            "responsable": "Admin",
            "email": "tecnologia@innovatech.com",
            "telefono": "912345678"
        }
        
        # Simular que no existe duplicado.
        mock_db.departamentos.find_one.return_value = None
        
        # Simular inserción exitosa.
        mock_resultado = MagicMock()
        mock_resultado.inserted_id = "dept_id_123"
        mock_db.departamentos.insert_one.return_value = mock_resultado

        exito, resultado = crear_departamento(datos_depto)

        assert exito is True
        assert resultado["_id"] == "dept_id_123"

    def test_crear_proyecto_exito(self, mock_db):
        # Crear un nuevo proyecto.
        datos_proy = {
            "nombre": "Rediseño Portal Cliente",
            "codigo": "WEB-24-001",
            "responsable": "Ana López",
            "cliente": "Banco Futuro",
            "presupuesto": "25000",
            "fecha_inicio": datetime.now()
        }
        
        # Simular que no existe duplicado.
        mock_db.proyectos.find_one.return_value = None
        
        # Simular inserción exitosa.
        mock_resultado = MagicMock()
        mock_resultado.inserted_id = "pry_id_123"
        mock_db.proyectos.insert_one.return_value = mock_resultado
        
        exito, resultado = crear_proyecto(datos_proy)
        
        assert exito is True
        assert resultado["_id"] == "pry_id_123"


    ID_TEST = "000000000000000000000123"

    # Tests para Empleados (Obtener, Actualizar, Eliminar)
    def test_obtener_empleado_exito(self, mock_db):
        # Obtener datos de un empleado por ID.
        
        # Simular que la base de datos devuelve un empleado.
        mock_db.empleados.find_one.return_value = {"_id": self.ID_TEST, "nombre": "Carlos"}
        
        from gestion_tareas.modelos.crud import obtener_empleado
        exito, resultado = obtener_empleado(self.ID_TEST)
            
        assert exito is True
        assert resultado["nombre"] == "Carlos"

    def test_actualizar_empleado_exito(self, mock_db):
        # Actualizar datos de un empleado.
        
        # Simular que la operación de update afectó a 1 documento.
        mock_resultado = MagicMock()
        mock_resultado.matched_count = 1
        mock_db.empleados.update_one.return_value = mock_resultado

        from gestion_tareas.modelos.crud import actualizar_empleado
        exito, msg = actualizar_empleado(self.ID_TEST, {"nombre": "Carlos Antonio"})

        assert exito is True
        assert msg == "empleado actualizado"

    def test_eliminar_empleado_exito(self, mock_db):
        # Eliminar un empleado.
        
        # Simular que la operación de delete eliminó 1 documento.
        mock_resultado = MagicMock()
        mock_resultado.deleted_count = 1
        mock_db.empleados.delete_one.return_value = mock_resultado
        
        # Simular busqueda previa para el log (nombre y apellidos)
        mock_db.empleados.find_one.return_value = {"nombre": "Carlos", "apellidos": "Méndez Ruiz"} 

        from gestion_tareas.modelos.crud import eliminar_empleado
        exito, msg = eliminar_empleado(self.ID_TEST)
            
        assert exito is True
        assert msg == "empleado eliminado"

    # Tests para Departamentos (Obtener, Actualizar, Eliminar)
    def test_obtener_departamento_exito(self, mock_db):
        # Obtener un departamento por ID.
        
        # Simular respuesta de la BD.
        mock_db.departamentos.find_one.return_value = {"_id": self.ID_TEST, "nombre": "Tecnología e Innovación"}
        
        from gestion_tareas.modelos.crud import obtener_departamento
        exito, res = obtener_departamento(self.ID_TEST)
            
        assert exito is True
        assert res["nombre"] == "Tecnología e Innovación"

    def test_actualizar_departamento_exito(self, mock_db):
        # Actualizar un departamento.
        
        # Simular actualización exitosa.
        mock_res = MagicMock()
        mock_res.matched_count = 1
        mock_db.departamentos.update_one.return_value = mock_res
        
        from gestion_tareas.modelos.crud import actualizar_departamento
        exito, msg = actualizar_departamento(self.ID_TEST, {"nombre": "Talento y Cultura"})
            
        assert exito is True
        assert msg == "departamento actualizado"

    def test_eliminar_departamento_exito(self, mock_db):
        # Eliminar un departamento.
        
        # Simular eliminación exitosa.
        mock_res = MagicMock()
        mock_res.deleted_count = 1
        mock_db.departamentos.delete_one.return_value = mock_res
        
        from gestion_tareas.modelos.crud import eliminar_departamento
        exito, msg = eliminar_departamento(self.ID_TEST)
            
        assert exito is True

    # Tests para Proyectos (Obtener, Actualizar, Eliminar)
    def test_obtener_proyecto_exito(self, mock_db):
        # Obtener un proyecto por ID.
        mock_db.proyectos.find_one.return_value = {"_id": self.ID_TEST, "nombre": "App Móvil Banca"}
        
        from gestion_tareas.modelos.crud import obtener_proyecto
        exito, res = obtener_proyecto(self.ID_TEST)
            
        assert exito is True
        assert res["nombre"] == "App Móvil Banca"

    def test_actualizar_proyecto_exito(self, mock_db):
        # Actualizar un proyecto.
        mock_res = MagicMock()
        mock_res.matched_count = 1
        mock_db.proyectos.update_one.return_value = mock_res
        
        from gestion_tareas.modelos.crud import actualizar_proyecto
        exito, msg = actualizar_proyecto(self.ID_TEST, {"presupuesto": 30000})
            
        assert exito is True

    def test_eliminar_proyecto_exito(self, mock_db):
        # Eliminar un proyecto.
        mock_res = MagicMock()
        mock_res.deleted_count = 1
        mock_db.proyectos.delete_one.return_value = mock_res
        
        from gestion_tareas.modelos.crud import eliminar_proyecto
        exito, msg = eliminar_proyecto(self.ID_TEST)
            
        assert exito is True

    # Tests adicionales para Tareas
    def test_actualizar_tarea_exito(self, mock_db):
        mock_res = MagicMock()
        mock_res.matched_count = 1
        mock_db.tareas.update_one.return_value = mock_res
        
        from gestion_tareas.modelos.crud import actualizar_tarea
        exito, msg = actualizar_tarea(self.ID_TEST, {"estado": "en progreso"})
            
        assert exito is True

    def test_completar_tarea_exito(self, mock_db):
        # completar_tarea llama a actualizar_tarea internamente
        # necesitamos mockear actualizar_tarea o dejar que corra con el mock de db
        mock_res = MagicMock()
        mock_res.matched_count = 1
        mock_db.tareas.update_one.return_value = mock_res # para el update interno
        
        from gestion_tareas.modelos.crud import completar_tarea
        exito, msg = completar_tarea(self.ID_TEST)
            
        assert exito is True
        # Verificar que se llamó a update con estado completada
        args, _ = mock_db.tareas.update_one.call_args
        assert args[1]["$set"]["estado"] == "completada"

    def test_eliminar_tarea_exito(self, mock_db):
        mock_res = MagicMock()
        mock_res.deleted_count = 1
        mock_db.tareas.delete_one.return_value = mock_res
        
        from gestion_tareas.modelos.crud import eliminar_tarea
        exito, msg = eliminar_tarea(self.ID_TEST)
            
        assert exito is True

    def test_obtener_tareas_pendientes_usuario(self, mock_db):
        # Simular tareas devueltas por $or
        tareas_simuladas = [
            {"_id": "t1", "titulo": "T1", "estado": "pendiente", "asignados": [{"id_usuario": "uid"}]},
            {"_id": "t2", "titulo": "T2", "estado": "pendiente", "compartido_por": "Juan"}
        ]
        mock_db.tareas.find.return_value = tareas_simuladas
        
        from gestion_tareas.modelos.crud import obtener_tareas_pendientes_usuario
        exito, tareas = obtener_tareas_pendientes_usuario("uid", "Juan")
        
        assert exito is True
        assert len(tareas) == 2
        
        # Verificar que se llamó a find con el filtro correcto
        args, _ = mock_db.tareas.find.call_args
        filtro = args[0]
        assert filtro["estado"] == "pendiente"
        assert "$or" in filtro

    # Tests para Empleados
    def test_obtener_empleado_exito(self, mock_db):
        mock_db.empleados.find_one.return_value = {"_id": self.ID_TEST, "nombre": "Juan"}
        
        from gestion_tareas.modelos.crud import obtener_empleado
        exito, resultado = obtener_empleado(self.ID_TEST)
            
        assert exito is True
        assert resultado["nombre"] == "Juan"

    def test_actualizar_empleado_exito(self, mock_db):
        mock_resultado = MagicMock()
        mock_resultado.matched_count = 1
        mock_db.empleados.update_one.return_value = mock_resultado

        from gestion_tareas.modelos.crud import actualizar_empleado
        with patch('gestion_tareas.modelos.crud.es_id_valido', return_value=True):
            exito, msg = actualizar_empleado(self.ID_TEST, {"nombre": "NuevoNombre"})

        assert exito is True
        assert msg == "empleado actualizado"

    def test_eliminar_empleado_exito(self, mock_db):
        mock_resultado = MagicMock()
        mock_resultado.deleted_count = 1
        mock_db.empleados.delete_one.return_value = mock_resultado
        mock_db.empleados.find_one.return_value = {"nombre": "Juan", "apellidos": "Pérez"} # Para el log

        from gestion_tareas.modelos.crud import eliminar_empleado
        with patch('gestion_tareas.modelos.crud.es_id_valido', return_value=True):
            exito, msg = eliminar_empleado(self.ID_TEST)
            
        assert exito is True
        assert msg == "empleado eliminado"

    # Tests para Departamentos (Obtener, Actualizar, Eliminar)
    def test_obtener_departamento_exito(self, mock_db):
        mock_db.departamentos.find_one.return_value = {"_id": "dept_id", "nombre": "IT"}
        
        from gestion_tareas.modelos.crud import obtener_departamento
        with patch('gestion_tareas.modelos.crud.es_id_valido', return_value=True):
            exito, res = obtener_departamento(self.ID_TEST)
            
        assert exito is True
        assert res["nombre"] == "IT"

    def test_actualizar_departamento_exito(self, mock_db):
        mock_res = MagicMock()
        mock_res.matched_count = 1
        mock_db.departamentos.update_one.return_value = mock_res
        
        from gestion_tareas.modelos.crud import actualizar_departamento
        with patch('gestion_tareas.modelos.crud.es_id_valido', return_value=True):
            exito, msg = actualizar_departamento(self.ID_TEST, {"nombre": "RRHH"})
            
        assert exito is True
        assert msg == "departamento actualizado"

    def test_eliminar_departamento_exito(self, mock_db):
        mock_res = MagicMock()
        mock_res.deleted_count = 1
        mock_db.departamentos.delete_one.return_value = mock_res
        
        from gestion_tareas.modelos.crud import eliminar_departamento
        with patch('gestion_tareas.modelos.crud.es_id_valido', return_value=True):
            exito, msg = eliminar_departamento(self.ID_TEST)
            
        assert exito is True

    # Tests para Proyectos (Obtener, Actualizar, Eliminar)
    def test_obtener_proyecto_exito(self, mock_db):
        mock_db.proyectos.find_one.return_value = {"_id": "pry_id", "nombre": "Web"}
        
        from gestion_tareas.modelos.crud import obtener_proyecto
        with patch('gestion_tareas.modelos.crud.es_id_valido', return_value=True):
            exito, res = obtener_proyecto(self.ID_TEST)
            
        assert exito is True
        assert res["nombre"] == "Web"

    def test_actualizar_proyecto_exito(self, mock_db):
        mock_res = MagicMock()
        mock_res.matched_count = 1
        mock_db.proyectos.update_one.return_value = mock_res
        
        from gestion_tareas.modelos.crud import actualizar_proyecto
        with patch('gestion_tareas.modelos.crud.es_id_valido', return_value=True):
            exito, msg = actualizar_proyecto(self.ID_TEST, {"presupuesto": 2000})
            
        assert exito is True

    def test_eliminar_proyecto_exito(self, mock_db):
        mock_res = MagicMock()
        mock_res.deleted_count = 1
        mock_db.proyectos.delete_one.return_value = mock_res
        
        from gestion_tareas.modelos.crud import eliminar_proyecto
        with patch('gestion_tareas.modelos.crud.es_id_valido', return_value=True):
            exito, msg = eliminar_proyecto(self.ID_TEST)
            
        assert exito is True

    # Tests adicionales para Tareas
    def test_actualizar_tarea_exito(self, mock_db):
        mock_res = MagicMock()
        mock_res.matched_count = 1
        mock_db.tareas.update_one.return_value = mock_res
        
        from gestion_tareas.modelos.crud import actualizar_tarea
        with patch('gestion_tareas.modelos.crud.es_id_valido', return_value=True):
            exito, msg = actualizar_tarea(self.ID_TEST, {"estado": "en progreso"})
            
        assert exito is True

    def test_completar_tarea_exito(self, mock_db):
        # completar_tarea llama a actualizar_tarea internamente
        # necesitamos mockear actualizar_tarea o dejar que corra con el mock de db
        mock_res = MagicMock()
        mock_res.matched_count = 1
        mock_db.tareas.update_one.return_value = mock_res # para el update interno
        
        from gestion_tareas.modelos.crud import completar_tarea
        with patch('gestion_tareas.modelos.crud.es_id_valido', return_value=True):
            exito, msg = completar_tarea(self.ID_TEST)
            
        assert exito is True
        # Verificar que se llamó a update con estado completada
        args, _ = mock_db.tareas.update_one.call_args
        assert args[1]["$set"]["estado"] == "completada"

    def test_eliminar_tarea_exito(self, mock_db):
        mock_res = MagicMock()
        mock_res.deleted_count = 1
        mock_db.tareas.delete_one.return_value = mock_res
        
        from gestion_tareas.modelos.crud import eliminar_tarea
        with patch('gestion_tareas.modelos.crud.es_id_valido', return_value=True):
            exito, msg = eliminar_tarea(self.ID_TEST)
            
        assert exito is True

    def test_obtener_tareas_pendientes_usuario(self, mock_db):
        # Obtener tareas pendientes para un usuario especifico.
        
        # Simular tareas devueltas.
        tareas_simuladas = [
            {"_id": "t1", "titulo": "Revisión de Código API", "estado": "pendiente", "asignados": [{"id_usuario": "uid"}]},
            {"_id": "t2", "titulo": "Optimizar Consultas BD", "estado": "pendiente", "compartido_por": "Carlos"}
        ]
        mock_db.tareas.find.return_value = tareas_simuladas
        
        from gestion_tareas.modelos.crud import obtener_tareas_pendientes_usuario
        exito, tareas = obtener_tareas_pendientes_usuario("uid", "Carlos")
        
        assert exito is True
        assert len(tareas) == 2
        
        args, _ = mock_db.tareas.find.call_args
        filtro = args[0]
        assert filtro["estado"] == "pendiente"
        assert "$or" in filtro