from collections import deque
import time
from AgenteIA.AgenteBuscador import AgenteBuscador


class AgenteMapu(AgenteBuscador):

    def __init__(self):
        AgenteBuscador.__init__(self)
        self.set_estado_inicial([3, 3, 1])
        self.set_estado_meta([0, 0, 0])
        self.nodos_expandidos = 0
        self.profundidad_maxima = 0
        self.max_frontera = 0
        self.tiempo_respuesta = 0
        self.acciones = []
        self.solucion = []
        self.add_funcion(self.get_hijos)

    def pasa_aa(self, e):
        if e is None:
            return None
        if isinstance(e, tuple):
            e = list(e)
        if not isinstance(e, list):
            return None
        if len(e) != 3:
            return None
        return [int(e[0]), int(e[1]), int(e[2])]

    def valida_estado(self, estado):
        if estado is None:
            return False
        if not isinstance(estado, (list, tuple)) or len(estado) != 3:
            return False

        try:
            p, v, b = [int(x) for x in estado]
        except (TypeError, ValueError):
            return False

        if p < 0 or v < 0 or b not in (0, 1):
            return False
        if p > 3 or v > 3:
            return False

        if p + v > 6:
            return False

        def valida_orilla(pac, ver):
            if pac == 0:
                return True
            return ver <= pac

        if not valida_orilla(p, v):
            return False

        p_der = 3 - p
        v_der = 3 - v
        if not valida_orilla(p_der, v_der):
            return False

        return True

    def get_hijos(self, estado):
        estado = self.pasa_aa(estado)
        if not self.valida_estado(estado):
            return []

        p, v, b = estado
        hijos = []
        combinaciones = [(1, 0), (0, 1), (2, 0), (0, 2), (1, 1)]

        if b == 1:
            np = p
            nv = v
            lado = "izquierda"
        else:
            np = 3 - p
            nv = 3 - v
            lado = "derecha"

        for pm, vm in combinaciones:
            if pm > np or vm > nv:
                continue
            if pm + vm == 0 or pm + vm > 2:
                continue
            if b == 1:
                nuevo = [p - pm, v - vm, 0]
            else:
                nuevo = [p + pm, v + vm, 1]
            if self.valida_estado(nuevo):
                hijos.append(nuevo)

        return hijos

    def bfs(self):
        estado_inicial = self.pasa_aa(self.get_estado_inicial())
        estado_meta = self.pasa_aa(self.get_estado_meta())
        if not self.valida_estado(estado_inicial):
            return []
        self.set_estado_inicial(estado_inicial)
        self.set_estado_meta(estado_meta)

        frontera = deque([[estado_inicial]])
        visitados = {tuple(estado_inicial)}
        self.nodos_expandidos = 0
        self.profundidad_maxima = 0
        self.max_frontera = 1
        inicio = time.perf_counter()

        while frontera:
            camino = frontera.popleft()
            nodo = camino[-1]
            self.nodos_expandidos += 1
            self.profundidad_maxima = max(self.profundidad_maxima, len(camino) - 1)

            if self.test_objetivo(nodo):
                self.tiempo_respuesta = time.perf_counter() - inicio
                self.solucion = camino
                return camino

            for hijo in self.generar_hijos(nodo):
                hijo_t = tuple(hijo)
                if hijo_t in visitados:
                    continue
                visitados.add(hijo_t)
                aux = list(camino)
                aux.append(hijo)
                frontera.append(aux)
                self.max_frontera = max(self.max_frontera, len(frontera))

        self.tiempo_respuesta = time.perf_counter() - inicio
        return []

    def dfs(self):
        estado_inicial = self.pasa_aa(self.get_estado_inicial())
        estado_meta = self.pasa_aa(self.get_estado_meta())
        if not self.valida_estado(estado_inicial):
            return []
        self.set_estado_inicial(estado_inicial)
        self.set_estado_meta(estado_meta)

        frontera = [[estado_inicial]]
        visitados = {tuple(estado_inicial)}
        self.nodos_expandidos = 0
        self.profundidad_maxima = 0
        self.max_frontera = 1
        inicio = time.perf_counter()

        while frontera:
            camino = frontera.pop()
            nodo = camino[-1]
            self.nodos_expandidos += 1
            self.profundidad_maxima = max(self.profundidad_maxima, len(camino) - 1)

            if self.test_objetivo(nodo):
                self.tiempo_respuesta = time.perf_counter() - inicio
                self.solucion = camino
                return camino

            for hijo in reversed(self.generar_hijos(nodo)):
                hijo_t = tuple(hijo)
                if hijo_t in visitados:
                    continue
                visitados.add(hijo_t)
                aux = list(camino)
                aux.append(hijo)
                frontera.append(aux)
                self.max_frontera = max(self.max_frontera, len(frontera))

        self.tiempo_respuesta = time.perf_counter() - inicio
        return []

    def obtener_instrucciones(self, camino):
        if not camino or len(camino) < 2:
            return []

        instrucciones = []
        for i in range(len(camino) - 1):
            actual = self.pasa_aa(camino[i])
            siguiente = self.pasa_aa(camino[i + 1])

            p_actual, v_actual, bote_actual = actual
            p_siguiente, v_siguiente, bote_siguiente = siguiente

            p_mov = abs(p_siguiente - p_actual)
            v_mov = abs(v_siguiente - v_actual)
            direccion = "derecha" if bote_actual == 1 else "izquierda"
            verbo = "Lleva" if bote_actual == 1 else "Trae"

            partes = []
            if p_mov > 0:
                nombre_p = "pacífico" if p_mov == 1 else "pacíficos"
                partes.append(f"{p_mov} {nombre_p}")
            if v_mov > 0:
                nombre_v = "verdugo" if v_mov == 1 else "verdugos"
                partes.append(f"{v_mov} {nombre_v}")

            if not partes:
                continue
            if len(partes) == 2:
                instruccion = f"{verbo} {partes[0]} y {partes[1]} a la {direccion}."
            else:
                instruccion = f"{verbo} {partes[0]} a la {direccion}."
            instrucciones.append(instruccion)

        return instrucciones

    def comparar_algoritmos(self):
        bfs = self.bfs()
        metricas_bfs = {
            "solucion": bfs,
            "movimientos": max(0, len(bfs) - 1),
            "nodos_expandidos": self.nodos_expandidos,
            "profundidad": self.profundidad_maxima,
            "tiempo": self.tiempo_respuesta,
            "max_frontera": self.max_frontera,
        }

        dfs = self.dfs()
        metricas_dfs = {
            "solucion": dfs,
            "movimientos": max(0, len(dfs) - 1),
            "nodos_expandidos": self.nodos_expandidos,
            "profundidad": self.profundidad_maxima,
            "tiempo": self.tiempo_respuesta,
            "max_frontera": self.max_frontera,
        }

        return {"bfs": metricas_bfs, "dfs": metricas_dfs}

    def explicacion_movimiento_invalido(self, estado):
        if self.valida_estado(estado):
            return "El movimiento es válido."

        estado = self.pasa_aa(estado)
        if estado is None:
            return "Movimiento inválido: el estado no tiene un formato válido."

        p, v, b = estado
        if b not in (0, 1):
            return "Movimiento inválido: la posición del bote no es válida."

        p_der = 3 - p
        v_der = 3 - v

        if p > 0 and v > p:
            return f"Movimiento inválido: en la orilla izquierda hay más verdugos ({v}) que pacíficos ({p}), y eso rompe la regla del juego."

        if p_der > 0 and v_der > p_der:
            return f"Movimiento inválido: en la orilla derecha hay más verdugos ({v_der}) que pacíficos ({p_der}), y eso rompe la regla del juego."

        return "Movimiento inválido: no cumple las reglas del bote o los límites del problema."

    def programa(self):
        self.set_tecnica("anchura")
        inicio = self.pasa_aa(self.get_estado_inicial())
        meta = self.pasa_aa(self.get_estado_meta())
        if inicio is None or meta is None:
            self.acciones = ["No existe un estado inicial o meta válido."]
            self.set_acciones(self.acciones)
            return self.acciones

        if not self.valida_estado(inicio):
            self.acciones = ["El estado inicial es inválido para el problema."]
            self.set_acciones(self.acciones)
            return self.acciones

        camino = self.bfs()
        if not camino:
            self.acciones = ["No se encontró una solución válida."]
            self.set_acciones(self.acciones)
            return self.acciones

        self.solucion = camino
        self.acciones = self.obtener_instrucciones(camino)
        self.set_acciones(self.acciones)
        return self.acciones
