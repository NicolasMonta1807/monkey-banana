import heapq
import time

# Dimensiones de la rejilla
FILAS, COLUMNAS = 5, 5

# Heurística que estima la distancia al objetivo
def heuristica(estado):
    posicion_mono, posicion_caja, sobre_caja, posicion_banana, tiene_banana = estado
    fila_mono, col_mono = posicion_mono
    fila_caja, col_caja = posicion_caja
    fila_banana, col_banana = posicion_banana
    
    if tiene_banana:
        return 0
    
    # Distancia de Manhattan del mono a la caja
    distancia_mono_caja = abs(fila_mono - fila_caja) + abs(col_mono - col_caja)
    
    # Distancia de Manhattan de la caja a la posición de la banana
    distancia_caja_banana = abs(fila_caja - fila_banana) + abs(col_caja - col_banana)
    
    # Si el mono no está sobre la caja y ya está en la misma posición, debe subirse
    costo_subirse = 1 if not sobre_caja and (fila_mono, col_mono) == (fila_caja, col_caja) else 0
    
    return distancia_mono_caja + distancia_caja_banana + costo_subirse

# Función para generar los estados sucesores
def obtener_sucesores(estado):
    sucesores = []
    (fila_mono, col_mono), (fila_caja, col_caja), sobre_caja, (fila_banana, col_banana), tiene_banana = estado
    
    if tiene_banana:
        return sucesores

    # Posibles movimientos (arriba, abajo, izquierda, derecha)
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Moverse a otra posición
    for d_fila, d_col in movimientos:
        nueva_fila_mono = fila_mono + d_fila
        nueva_col_mono = col_mono + d_col
        if 0 <= nueva_fila_mono < FILAS and 0 <= nueva_col_mono < COLUMNAS:
            sucesores.append(((nueva_fila_mono, nueva_col_mono), (fila_caja, col_caja), sobre_caja, (fila_banana, col_banana), tiene_banana))
    
    # Empujar la caja a otra posición (si el mono está en la misma posición que la caja y no está sobre ella)
    if (fila_mono, col_mono) == (fila_caja, col_caja) and not sobre_caja:
        for d_fila, d_col in movimientos:
            nueva_fila_caja = fila_caja + d_fila
            nueva_col_caja = col_caja + d_col
            if 0 <= nueva_fila_caja < FILAS and 0 <= nueva_col_caja < COLUMNAS:
                sucesores.append(((fila_mono + d_fila, col_mono + d_col), (nueva_fila_caja, nueva_col_caja), False, (fila_banana, col_banana), tiene_banana))
    
    # Subirse a la caja (si el mono está en la misma posición que la caja y no está sobre ella)
    if (fila_mono, col_mono) == (fila_caja, col_caja) and not sobre_caja:
        sucesores.append(((fila_mono, col_mono), (fila_caja, col_caja), True, (fila_banana, col_banana), tiene_banana))
    
    # Agarrar la banana (si el mono está sobre la caja en la posición de la banana)
    if sobre_caja and (fila_mono, col_mono) == (fila_banana, col_banana):
        sucesores.append(((fila_mono, col_mono), (fila_caja, col_caja), sobre_caja, (fila_banana, col_banana), True))
    
    return sucesores

# Algoritmo Best-First Search (BFS con prioridad por heurística)
def resolver_problema_mono_banana_best_first(estado_inicial):
    # Cola de prioridad
    cola_prioridad = []
    
    # Insertamos el estado inicial en la cola con la heurística calculada
    heapq.heappush(cola_prioridad, (heuristica(estado_inicial), estado_inicial, []))
    
    # Conjunto de estados visitados para evitar ciclos
    visitados = set()
    
    # Contador de sucesores analizados
    sucesores_analizados = 0
    
    while cola_prioridad:
        _, estado_actual, camino = heapq.heappop(cola_prioridad)
        
        # Si ya se alcanzó el objetivo
        if estado_actual[4]:  # estado_actual[4] es tiene_banana
            print("----------------------------------------")
            print(f"Sucesores analizados: {sucesores_analizados}")
            print("----------------------------------------")
            return camino + [estado_actual]
        
        if estado_actual not in visitados:
            visitados.add(estado_actual)
            
            # Generar sucesores y calcular sus heurísticas
            sucesores_con_heuristica = []
            for sucesor in obtener_sucesores(estado_actual):
                print("----------------------------------------")
                sucesores_analizados += 1
                h = heuristica(sucesor)
                sucesores_con_heuristica.append((h, sucesor))
                print(f"Evaluando sucesor: {sucesor}, Heurística: {h}")
            
            # Ordenar los sucesores por heurística y añadirlos a la cola de prioridad
            sucesores_con_heuristica.sort()  # Ordenar por heurística
            
            for h, sucesor in sucesores_con_heuristica:
                heapq.heappush(cola_prioridad, (h, sucesor, camino + [estado_actual]))
            
            # Mostrar el estado escogido para la siguiente evaluación
            if sucesores_con_heuristica:
                print(f"Escogiendo sucesor: {sucesores_con_heuristica[0][1]} con heurística: {sucesores_con_heuristica[0][0]}")
                print("----------------------------------------\n")
    
    return None  # No se encontró solución

# Estado inicial: (posición del mono, posición de la caja, sobre la caja, posición de la banana, tiene la banana)
estado_inicial = ((2, 3), (0, 2), False, (4, 1), False)
start = time.perf_counter_ns()
solucion = resolver_problema_mono_banana_best_first(estado_inicial)
end = time.perf_counter_ns()
if solucion:
    print("Solución encontrada:\n")
    for paso, estado in enumerate(solucion):
        print(f"Paso {paso}: {estado}")
    print("Tiempo de ejecución: ", end-start, " ns")
else:
    print("No se encontró solución")
