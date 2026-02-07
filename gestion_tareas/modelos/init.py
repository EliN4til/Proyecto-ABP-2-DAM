from pymongo import MongoClient
from pydantic import BaseModel, Field, EmailStr, BeforeValidator
from typing import List, Optional, Annotated, Literal
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

client = MongoClient("mongodb+srv://[USUARIO]:[CONTRASEÑA]@gestiontareas1.mgzio0n.mongodb.net/?appName=GestionTareas1")
db = client["tareas_db"]

class InfoDepartamento(BaseModel):
    nombre: str
    ubicacion: str

class UsuarioResumen(BaseModel):
    """
    Guardamos una copia pequeña de los datos del usuario
    en la colección de tareas para cargar las tareas más rapidamente.
    (Basicamente patrón Subset)
    """
    id_usuario: PyObjectId
    nombre: str
    foto: Optional[str] = None

class MiembroDepartamento(BaseModel):
    id_usuario: PyObjectId
    nombre: str
    apellidos: str
    identificador: str


class EmpleadoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    identificador: str
    nombre: str
    apellidos: str
    email: EmailStr
    contrasenya: str
    foto: Optional[str] = None
    estado: Literal["ACTIVO", "INACTIVO", "PENDIENTE"] = "ACTIVO"
    empresa: str
    equipo: str
    proyecto: Optional[str] = None
    departamento: InfoDepartamento 
    cargo: str
    id_empleado: str
    telefono: Optional[str] = None
    ubicacion: str
    fecha_incorporacion: datetime
    fecha_alta: Optional[datetime] = None
    es_admin: bool = False

class DepartamentoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    nombre: str
    codigo: str
    empresa: str
    responsable: str
    descripcion: Optional[str] = None
    ubicacion: Optional[str] = None
    email: str
    telefono: str
    presupuesto: Optional[float] = None
    estado: Literal["ACTIVO", "INACTIVO", "EN CREACIÓN"] = "ACTIVO"
    miembros: List[MiembroDepartamento] = []
    proyecto_asignado: Optional[str] = None
    fecha_creacion: Optional[datetime] = None


class ProyectoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    nombre: str
    codigo: str
    responsable: str
    cliente: str
    presupuesto: str
    estado: Literal["ACTIVO", "PAUSADO", "INACTIVO"] = "ACTIVO"
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    descripcion: Optional[str] = ""
    fecha_creacion: Optional[datetime] = None

class TareaModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    titulo: str
    requisitos: Optional[str] = None
    estado: Literal["pendiente", "en_proceso", "completado"] = "pendiente"
    tags: List[str] = []
    icono: str
    id_proyecto: PyObjectId
    proyecto: Optional[str] = None
    prioridad: Literal["alta", "media", "baja"] = "media"
    asignados: List[UsuarioResumen] = []
    compartido_por: Optional[str] = None
    atrasado: bool = False
    fecha_inicio: datetime
    fecha_limite: Optional[datetime] = None
    fecha_completado: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None

class RolModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    nombre: str
    codigo: str
    descripcion: Optional[str] = None
    usuarios: int = 0
    color: Optional[str] = "#4682B4"
    permisos: dict = {}

def cargar_datos_prueba():
    empleado = EmpleadoModel(
        identificador="26603992F",
        nombre="Laura",
        apellidos="García",
        email="laura@test.com",
        contrasenya="1234",
        estado="ACTIVO",
        empresa="TechSolutions S.L",
        equipo="Backend Team",
        departamento=InfoDepartamento(nombre="IT", ubicacion="Planta 1"),
        cargo="Desarrollador Backend",
        id_empleado="EMP001",
        telefono="+34 912 345 678",
        ubicacion="Oficina Central - Madrid",
        fecha_incorporacion=datetime(2021, 3, 15)
    )
    resumen_empleado = db.empleados.insert_one(empleado.model_dump(by_alias=True, exclude=["id"]))

    proy = ProyectoModel(
        nombre="App Gestión Empleados",
        codigo="PRY001",
        responsable="Laura García",
        cliente="Mercadona",
        presupuesto="1.500 €",
        fecha_inicio=datetime.today(),
        fecha_fin=datetime(2026, 6, 30)
    )
    resumen_proyecto = db.proyectos.insert_one(proy.model_dump(by_alias=True, exclude=["id"]))
    

    resumen_laura = UsuarioResumen(
        id_usuario=str(resumen_empleado.inserted_id),
        nombre="Laura",
        foto=None
    )
    
    tarea = TareaModel(
        titulo="Diseñar Base de Datos",
        requisitos="Hay que diseñar el modelo de la BBDD que usará la aplicación",
        icono="📋",
        id_proyecto=str(resumen_proyecto.inserted_id),
        prioridad="alta",
        asignados=[resumen_laura],
        fecha_inicio=datetime.now()
    )
    db.tareas.insert_one(tarea.model_dump(by_alias=True, exclude=["id"]))
    
    print("Se han insertado los datos de prueba correctamente")

if __name__ == "__main__":
    cargar_datos_prueba()