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
        
        #filtro por prioridad
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