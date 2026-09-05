# MAPU — Agente Inteligente para el Cruce del Río

## Descripción

MAPU es un agente inteligente desarrollado para resolver el problema clásico de los **aldeanos y verdugos**, utilizando técnicas de búsqueda en espacios de estados.

El objetivo del problema consiste en trasladar tres aldeanos y tres verdugos desde una orilla del río hasta la otra utilizando una barca con capacidad máxima de dos personas, respetando las restricciones de seguridad establecidas para ambas orillas.

El proyecto combina la implementación de algoritmos de Inteligencia Artificial con una interfaz gráfica interactiva desarrollada mediante PyGame.

---

## Objetivo

Desarrollar un agente inteligente capaz de encontrar una secuencia válida de movimientos para resolver el problema de los aldeanos y verdugos, utilizando algoritmos de búsqueda y proporcionando asistencia al usuario durante la resolución.

---

## Características

- Representación del problema mediante un espacio de estados.
- Validación de estados y movimientos.
- Generación automática de estados sucesores.
- Implementación de búsqueda en amplitud (BFS).
- Implementación de búsqueda en profundidad (DFS).
- Registro de métricas de búsqueda.
- Interfaz gráfica interactiva mediante PyGame.
- Movimiento manual de los personajes.
- Asistencia mediante el botón **AGENTE**.
- Recomendación del siguiente movimiento.
- Explicación de movimientos inválidos.
- Síntesis de voz para las indicaciones del agente.
- Animación del movimiento de la barca.

---

## Algoritmos utilizados

### BFS — Búsqueda en Amplitud

BFS explora el espacio de estados por niveles utilizando una estrategia FIFO. Debido a que los movimientos tienen el mismo costo, permite obtener una solución de profundidad mínima.

### DFS — Búsqueda en Profundidad

DFS explora una rama del espacio de estados antes de continuar con otras alternativas utilizando una estrategia LIFO. La solución encontrada puede depender del orden de generación de los estados sucesores.

---

## Representación del estado

Cada estado del problema se representa mediante:

```text
[P, V, B]

Donde:

P = cantidad de aldeanos en la orilla izquierda.
V = cantidad de verdugos en la orilla izquierda.
B = posición de la barca.
1 = barca en la orilla izquierda.
0 = barca en la orilla derecha.
Estado inicial
[3, 3, 1]
Estado objetivo
[0, 0, 0]

La barca tiene una capacidad máxima de dos personas.

Resultados obtenidos

Durante las pruebas realizadas se obtuvieron los siguientes resultados:

Algoritmo	Movimientos	Nodos explorados	Frontera máxima
BFS	11	15	3
DFS	11	13	3

Ambos algoritmos encontraron una solución de 11 movimientos en la configuración utilizada.

La igualdad en la profundidad de las soluciones corresponde al orden de sucesores utilizado en esta implementación y no implica que DFS garantice una solución óptima en términos generales.

Tecnologías utilizadas
Python 3.12
PyGame
pyttsx4
collections
time
Estructura del proyecto
MAPU-Agente-Inteligente/
│
├── AgenteIA/
│   ├── Agente.py
│   ├── AgenteBuscador.py
│   └── Entorno.py
│
├── imagenes/
│
├── sonido/
│
├── AgenteMapu.py
├── Bote.py
├── Personaje.py
├── Rio.py
├── main.py
├── .gitignore
└── README.md
Instalación

Se recomienda utilizar Python 3.12.

Instalar las dependencias necesarias mediante:

pip install pygame pyttsx4
Ejecución

Desde la carpeta principal del proyecto ejecutar:

python main.py

En Windows, si existen varias versiones de Python instaladas, puede ser necesario utilizar específicamente Python 3.12:

& "C:\Users\Rodrigo\AppData\Local\Programs\Python\Python312\python.exe" main.py
Interacción con el sistema

El usuario puede interactuar con el juego mediante los controles disponibles en la interfaz.

AGENTE

Permite solicitar asistencia al agente MAPU. El agente analiza el estado actual y proporciona una recomendación sobre el siguiente movimiento.

MOVER

Ejecuta el movimiento seleccionado para la barca, siempre que este cumpla las restricciones del problema.

NUEVO JUEGO

Reinicia la partida y devuelve el problema a su estado inicial.

SONIDO

Permite activar o desactivar los efectos y las indicaciones de voz.

Autores
-Sarah Cazorla
-Tairin Muñoz

Proyecto académico de Inteligencia Artificial

Universidad Católica Boliviana
