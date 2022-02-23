import pygame, sys, random
from pygame.locals import *
import configPenguin
import graphics

class monster(pygame.sprite.Sprite):

	def __init__(self, x, y, enemigo, resist):
		pygame.sprite.Sprite.__init__(self)
		self.image = graphics.load_image(enemigo)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		self.resistencia = resist
		self.type ="enemy"

	def mover(self):
		"Movimiento predefinido del enemigo"
		raise NoImplemented("Tiene que implementar el metodo mover.")

	def recibeGolpe(self):
		"Daño recibido"
		raise NoImplemented("Tiene que implementar el metodo dañar.")

	def draw(self, screen):
		"Dibujando enemigo"
		raise NoImplemented("Tiene que implementar el metodo draw.")




	