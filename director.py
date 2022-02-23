# Módulos
import pygame
import sys
import configPenguin

class Director:
    """Representa el objeto principal del juego.

    El objeto Director mantiene en funcionamiento el juego, se
    encarga de actualizar, dibujar y propagar eventos.

    Tiene que utilizar este objeto en conjunto con objetos
    derivados de Scene."""

    def __init__(self):
        self.screen = pygame.display.set_mode((1920, 1080))
        
        pygame.display.set_caption("Run Penguin! Run!")
        self.scene = None
        self.fullscreen = False
        self.quit_flag = False
        self.clock = pygame.time.Clock()                


    def loop(self):
        "Pone en funcionamiento el juego."    
        pygame.init()
        #pygame.display.set_mode((configPenguin.width, configPenguin.height))    
        while not self.quit_flag:
            self.time = self.clock.tick(60)
            
            # Eventos de Salida
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
                        
            # detecta eventos
            self.scene.on_event()

            # actualiza la escena
            self.scene.on_update()

            # dibuja la pantalla
            self.scene.on_draw(self.screen)
            pygame.display.flip()

    def change_scene(self, scene):
        "Altera la escena actual."
        self.scene = scene

    def quit(self):
        pygame.quit()