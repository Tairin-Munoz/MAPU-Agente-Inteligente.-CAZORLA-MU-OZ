from AgenteIA.Entorno import Entorno
import pygame
import pyttsx4
import threading
import queue
from AgenteMapu import AgenteMapu
from Bote import Bote
from Personaje import Personaje


class Rio(Entorno):
    def __init__(self):
        Entorno.__init__(self)
        pygame.init()
        self.habla = None
        self.cola_voz = queue.Queue()
        self.detener_voz = False
        self.hilo_voz = threading.Thread(target=self.procesar_voz, daemon=True)
        self.hilo_voz.start()
        self.estado_juego = [3, 3, 1]

    def procesar_voz(self):
        try:
            habla = pyttsx4.init()
            try:
                voces = habla.getProperty("voices")
                voz_es = None
                for voz in voces:
                    idiomas = getattr(voz, "languages", [])
                    if any("spa" in str(lang).lower() for lang in idiomas):
                        voz_es = voz
                        break
                if voz_es is not None:
                    habla.setProperty("voice", voz_es.id)
                habla.setProperty("rate", 150)
            except Exception:
                pass
            while not self.detener_voz:
                texto = self.cola_voz.get()
                if texto is None:
                    break
                try:
                    habla.say(texto)
                    habla.runAndWait()
                except Exception:
                    pass
        except Exception:
            pass

    def hablar_async(self, texto):
        if not texto:
            return
        try:
            while True:
                self.cola_voz.get_nowait()
        except queue.Empty:
            pass
        self.cola_voz.put(texto)

    def get_percepciones(self, agente):
        if hasattr(agente, "set_estado_inicial"):
            agente.set_estado_inicial(list(self.estado_juego))
        if hasattr(agente, "set_estado_meta"):
            agente.set_estado_meta([0, 0, 0])
        agente.programa()

    def ejecutar(self, agente):
        ancho = 1280
        altura = 650
        ventana = pygame.display.set_mode((ancho, altura))
        pygame.display.set_caption("Inteligencia Artificial I")

        negro = (0, 0, 0)

        agente_img = pygame.image.load("imagenes/agente.png")
        bote_img = pygame.image.load("imagenes/bote.png")
        fondo_img = pygame.image.load("imagenes/fondo.png")
        pacifico_img = pygame.image.load("imagenes/pacifico.png")
        pacifico1_img = pygame.image.load("imagenes/pacifico1.png")
        verdugo_img = pygame.image.load("imagenes/verdugo.png")
        verdugo1_img = pygame.image.load("imagenes/verdugo1.png")
        nuevo_img = pygame.image.load("imagenes/nuevo.png")
        nuevo1_img = pygame.image.load("imagenes/nuevo1.png")
        agente_btn_img = pygame.image.load("imagenes/agente_btn.png")
        agente_btn1_img = pygame.image.load("imagenes/agente_btn1.png")
        fin_img = pygame.image.load("imagenes/fin.png")
        victoria_img = pygame.image.load("imagenes/victoria.png")
        go_img = pygame.image.load("imagenes/go.png")
        go1_img = pygame.image.load("imagenes/go1.png")
        sonido_on_img = pygame.image.load("imagenes/sonidoon.png")
        sonido_off_img = pygame.image.load("imagenes/sonidooff.png")

        snd_fin = pygame.mixer.Sound("sonido/sonido_fin.wav")
        snd_victoria = pygame.mixer.Sound("sonido/sonido_ganador.wav")

        font = pygame.font.SysFont(None, 25)
        x = ancho * 0.1
        y = altura * 0.8
        x_nuevo = 0

        personajes = [
            Personaje(x - 135, y - 100, 0, 0, "P", "izquierda", pacifico_img, pacifico1_img, ventana),
            Personaje(x - 90, y - 100, 0, 0, "P", "izquierda", pacifico_img, pacifico1_img, ventana),
            Personaje(x - 45, y - 100, 0, 0, "P", "izquierda", pacifico_img, pacifico1_img, ventana),
            Personaje(x - 135, y - 250, 0, 0, "V", "izquierda", verdugo_img, verdugo1_img, ventana),
            Personaje(x - 90, y - 250, 0, 0, "V", "izquierda", verdugo_img, verdugo1_img, ventana),
            Personaje(x - 45, y - 250, 0, 0, "V", "izquierda", verdugo_img, verdugo1_img, ventana)
        ]

        en_bote = [
            Bote(157, 478, 2, pacifico1_img, verdugo1_img, ventana),
            Bote(656, 478, 3, pacifico1_img, verdugo1_img, ventana),
            Bote(318, 478, 4, pacifico1_img, verdugo1_img, ventana),
            Bote(817, 478, 5, pacifico1_img, verdugo1_img, ventana)
        ]

        clock = pygame.time.Clock()
        finalizado = False
        pos_bote = 0
        a, b = 0, 0
        accion = [a, b]
        estado = [3, 3, 1]
        self.estado_juego = list(estado)

        fin_juego = False
        fin_jugador = False
        victoria_jugador = False
        izquierda = False
        derecha = False
        victoria = False
        num_movida = 0
        sonido = True
        con_agente = False
        mensaje_invalido = ""
        ayudante = AgenteMapu()
        pista_actual = ""

        try:
            pygame.mixer.music.load("sonido/sonido_fondo.mp3")
            pygame.mixer.music.play(-1)
        except Exception:
            pass

        while not finalizado:
            ventana.blit(fondo_img, (0, 0))
            ventana.blit(nuevo_img, (1000, 45))
            ventana.blit(agente_btn_img, (700, 45))
            ventana.blit(sonido_on_img if sonido else sonido_off_img, (1150, 40))
            ventana.blit(go_img, (590, 300))

            for personaje in personajes:
                personaje.mostrar()

            msg_estado = font.render("Estado: " + str(estado), True, negro)
            ventana.blit(msg_estado, [20, 20])
            msg_accion = font.render("Accion: " + str(accion), True, negro)
            ventana.blit(msg_accion, [20, 50])
            msg_movidas = font.render("Movidas: " + str(num_movida), True, negro)
            ventana.blit(msg_movidas, [20, 80])

            if mensaje_invalido:
                msg_invalido = font.render(mensaje_invalido, True, (160, 0, 0))
                ventana.blit(msg_invalido, [20, 110])

            if pista_actual:
                msg_pista = font.render("Pista: " + pista_actual, True, (0, 80, 160))
                ventana.blit(msg_pista, [20, 140])

            if con_agente:
                ventana.blit(agente_img, (200, 40))

            cursor = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    finalizado = True
                    agente.inhabilitar()

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    mx, my = evento.pos

                    if 1150 < mx < 1200 and 40 < my < 90:
                        sonido = not sonido
                        if sonido:
                            try:
                                pygame.mixer.music.unpause()
                            except Exception:
                                pass
                        else:
                            try:
                                pygame.mixer.music.pause()
                            except Exception:
                                pass

                    elif 1000 < mx < 1119 and 45 < my < 81:
                        finalizado = True
                        try:
                            pygame.mixer.music.stop()
                        except Exception:
                            pass
                        return

                    elif 700 < mx < 819 and 45 < my < 81:
                        self.get_percepciones(agente)
                        con_agente = True
                        pista_actual = agente.acciones[0] if agente.acciones else "No se encontró una solución."
                        self.hablar_async(pista_actual)

                    elif 590 < mx < 678 and 300 < my < 390 and not fin_juego and not victoria and accion != [0, 0]:
                        if pos_bote == 0:
                            proximo_estado = [estado[0] - accion[0], estado[1] - accion[1], 0]
                        else:
                            proximo_estado = [estado[0] + accion[0], estado[1] + accion[1], 1]

                        if not ayudante.valida_estado(proximo_estado):
                            mensaje_invalido = ayudante.explicacion_movimiento_invalido(proximo_estado)
                            pista_actual = mensaje_invalido
                            self.hablar_async(mensaje_invalido)
                            x_nuevo = 0
                        else:
                            mensaje_invalido = ""
                            pista_actual = ""
                            if pos_bote == 0:
                                x_nuevo = 10
                                for i in range(6):
                                    if personajes[i].pos in (2, 4):
                                        personajes[i].x_mas = 10
                            else:
                                x_nuevo = -10
                                for i in range(6):
                                    if personajes[i].pos in (3, 5):
                                        personajes[i].x_mas = -10

                    else:
                        for i in range(6):
                            p = personajes[i]
                            if p.rect_x < mx < p.rect_x + p.ancho and p.rect_y < my < p.rect_y + p.altura:
                                if p.pos == 0 and p.izq_der == "izquierda" and pos_bote == 0 and a + b < 2:
                                    if p.personaje == "P":
                                        a += 1
                                    else:
                                        b += 1
                                    if accion in ([0, 1], [1, 0]):
                                        izquierda = any(q.pos == 2 for q in personajes)
                                        derecha = any(q.pos == 4 for q in personajes)
                                        if izquierda:
                                            p.x, p.y, p.pos = x + 180, y - 50, 4
                                        elif derecha:
                                            p.x, p.y, p.pos = x + 20, y - 50, 2
                                    else:
                                        p.x, p.y, p.pos = x + 20, y - 50, 2

                                elif p.pos == 1 and p.izq_der == "derecha" and pos_bote == 1 and a + b < 2:
                                    if p.personaje == "P":
                                        a += 1
                                    else:
                                        b += 1
                                    if accion in ([0, 1], [1, 0]):
                                        izquierda = any(q.pos == 3 for q in personajes)
                                        derecha = any(q.pos == 5 for q in personajes)
                                        if izquierda:
                                            p.x, p.y, p.pos = x + 180, y - 50, 5
                                        elif derecha:
                                            p.x, p.y, p.pos = x + 20, y - 50, 3
                                    else:
                                        p.x, p.y, p.pos = x + 20, y - 50, 3

                        for j in range(4):
                            slot = en_bote[j]
                            if slot.x < mx < slot.x + slot.ancho and slot.y < my < slot.y + slot.altura:
                                k = next((i for i in range(6) if personajes[i].pos == slot.pos), None)
                                if k is not None:
                                    p = personajes[k]
                                    if p.personaje == "P":
                                        a -= 1
                                    else:
                                        b -= 1
                                    p.x, p.y = p.rect_x - 12, p.rect_y
                                    p.pos = 0 if p.izq_der == "izquierda" else 1
                                    if slot.pos in (2, 3):
                                        izquierda = False
                                    else:
                                        derecha = False

            x += x_nuevo
            for i in range(6):
                personajes[i].x += personajes[i].x_mas
            accion = [a, b]

            if x >= 620 and pos_bote == 0:
                x_nuevo = 0
                for i in range(6):
                    personajes[i].x_mas = 0
                pos_bote = 1
                if accion != [0, 0]:
                    num_movida += 1
                    estado[0] -= accion[0]
                    estado[1] -= accion[1]
                    estado[2] = 0
                    self.estado_juego = list(estado)
                for i in range(6):
                    if personajes[i].pos == 2:
                        personajes[i].pos = 3
                        personajes[i].izq_der = "derecha"
                        personajes[i].rect_x += 900
                    elif personajes[i].pos == 4:
                        personajes[i].pos = 5
                        personajes[i].izq_der = "derecha"
                        personajes[i].rect_x += 900

            if x <= 128 and pos_bote == 1:
                x_nuevo = 0
                for i in range(6):
                    personajes[i].x_mas = 0
                pos_bote = 0
                if accion != [0, 0]:
                    num_movida += 1
                    estado[0] += accion[0]
                    estado[1] += accion[1]
                    estado[2] = 1
                    self.estado_juego = list(estado)
                for i in range(6):
                    if personajes[i].pos == 3:
                        personajes[i].pos = 2
                        personajes[i].rect_x -= 900
                        personajes[i].izq_der = "izquierda"
                    elif personajes[i].pos == 5:
                        personajes[i].pos = 4
                        personajes[i].rect_x -= 900
                        personajes[i].izq_der = "izquierda"

            if fin_juego and not fin_jugador:
                try:
                    pygame.mixer.music.stop()
                    snd_fin.play(0)
                except Exception:
                    pass
                fin_jugador = True

            if victoria and not victoria_jugador:
                try:
                    pygame.mixer.music.stop()
                    snd_victoria.play(0)
                except Exception:
                    pass
                victoria_jugador = True

            ventana.blit(bote_img, (int(x), int(y)))

            if (estado[1] > estado[0] > 0) or (estado[1] < estado[0] < 3):
                ventana.blit(fin_img, (400, 250))
                fin_juego = True

            if estado == [0, 0, 0] and accion == [0, 0]:
                ventana.blit(victoria_img, (400, 250))
                victoria = True

            pygame.display.update()
            clock.tick(25)

        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

        pygame.quit()
        self.detener_voz = True
        self.cola_voz.put(None)


if __name__ == "__main__":
    juego = Rio()
    agente = AgenteMapu()
    juego.insertar(agente)
    juego.run()
