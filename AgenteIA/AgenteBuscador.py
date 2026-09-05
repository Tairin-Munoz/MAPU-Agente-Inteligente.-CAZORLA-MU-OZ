                                                            
                                                            
                                                            
                                                            
                                                            
                                                            
                                                            

from AgenteIA.Agente import Agente
from copy import deepcopy
from collections import deque
import time


class AgenteBuscador(Agente):
    def __init__(self):
        Agente.__init__(self)
        self.__estado_inicial = None
        self.__estado_meta = None
        self.__funcion_sucesor = []
        self.__tecnica = "anchura"
        self.nodos_expandidos = 0
        self.profundidad_maxima = 0
        self.max_frontera = 0
        self.tiempo_respuesta = 0
        self.ultima_solucion = []

    def set_estado_inicial(self, e0):
        self.__estado_inicial = e0

    def set_estado_meta(self, ef):
        self.__estado_meta = ef

    def get_estado_inicial(self):
        return self.__estado_inicial

    def get_estado_meta(self):
        return self.__estado_meta

    def set_tecnica(self, t):
        self.__tecnica = t

    def add_funcion(self, f):
        self.__funcion_sucesor.append(f)

    def test_objetivo(self, e):
        return e == self.__estado_meta

    def generar_hijos(self, e):
        hijos = []
        for fun in self.__funcion_sucesor:
            h = fun(e)
            if h is None:
                continue
            if isinstance(h, list):
                for hijo in h:
                    if hijo is not None:
                        hijos.append(hijo)
            else:
                hijos.append(h)
        return hijos

    def mide_tiempo(funcion):
        def funcion_medida(*args, **kwards):
            inicio = time.time()
            c = funcion(*args, **kwards)
            print("Tiempo de ejecucion: ", time.time() - inicio)
            return c
        return funcion_medida

    @mide_tiempo
    def programa(self):
        if self.__estado_inicial is None or self.__estado_meta is None:
            return []

        inicio = time.perf_counter()
        frontera = deque([[list(self.__estado_inicial)]])
        visitados = {tuple(self.__estado_inicial)}
        self.nodos_expandidos = 0
        self.profundidad_maxima = 0
        self.max_frontera = 1

        while frontera:
            if self.__tecnica == "profundidad":
                camino = frontera.pop()
            else:
                camino = frontera.popleft()

            nodo = camino[-1]
            self.nodos_expandidos += 1
            self.profundidad_maxima = max(self.profundidad_maxima, len(camino) - 1)

            if self.test_objetivo(nodo):
                self.ultima_solucion = camino
                self.set_acciones(camino)
                self.tiempo_respuesta = time.perf_counter() - inicio
                return camino

            for hijo in self.generar_hijos(nodo):
                hijo_t = tuple(hijo)
                if hijo_t in visitados:
                    continue
                visitados.add(hijo_t)
                aux = deepcopy(camino)
                aux.append(hijo)
                frontera.append(aux)
                self.max_frontera = max(self.max_frontera, len(frontera))

        self.tiempo_respuesta = time.perf_counter() - inicio
        return []

