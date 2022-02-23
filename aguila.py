import pygame, sys, random
from pygame.locals import *
import configPenguin
import graphics
import monster


class aguila(monster.monster):
	def __init__(self,x, y, cara=True):
		monster.monster.__init__(self, x, y, enemigo='spritesP/aguila1.gif', resist=2)
		self.puntos = 30
		self.speed = 0.14
		self.factMov = 90
		#self.ataque = ataqueM()
		self.movSpace =8
		self.contMov = 0
		self.cara = cara #Si esta en True, está bajando
		self.state = "normal"
		self.vivo = True
		self.timeG = 0 #Tiempo en que fue golpeado
		self.timeA = 0 #Tiempo en que atacó
		self.contAnim = 0 #Tiempo en para activar animacion
		self.contAnimAtk = 0 #Este contador indica que imagen se va a desplegar
		self.contMovAtk = 0 #Este contador indica en que momento se cambiara la imagen
		self.distAttack = 2 #La distancia, en bloques, a la cual se activa el ataque automatico
		self.type = "vertical"
		self.mov = True

	def mover(self):
		#Bajando			
		if self.cara:
			self.rect.centery+=int(0.7*self.factMov*self.speed)
		
		#Subiendo						
		if not self.cara: 
			self.rect.centery-=int(0.7*self.factMov*self.speed)

		if(self.state=="normal"):
			self.contMov+=0.1

		if(self.contMov>=self.movSpace):
			self.cara=not(self.cara)
			self.contMov=0			
#			print("Girando por limite de mov alcanzado")

		#if(self.rect.bottom>=configPenguin.height):
		#	self.cara=not(self.cara)
		#	self.contMov=0			
#			print("Girando por tocar límites de pantalla")

		if(self.state=="golpeado"):
			self.image = graphics.load_image("spritesP/aguila_attacked.gif")	 
		if(self.state=="normal" and self.mov):
			self.image = graphics.load_image("spritesP/aguila1.gif")	
		if(self.state=="normal" and not(self.mov)):
			self.image = graphics.load_image("spritesP/aguila2.gif")

		if(self.contAnim>=1):
			self.mov=not(self.mov)
			self.contAnim=0

		self.contAnim+=0.05	
		#print("contador", self.contMov)

	#def cambiaDir(self):

	def atack(self, time):
		if(self.vivo and self.state!="atacando"):
			#derecha
			self.state=="atacando"		


	def recibeGolpe(self,time):
		if self.cara:
			self.image = graphics.load_image("spritesP/aguila_attacked.gif")	 
		else:
			self.image = graphics.load_image("spritesP/aguila_attacked.gif")	 
		self.state = "golpeado"
		self.timeG = time
		self.resistencia-=1
		if(self.resistencia<=0):
			self.kill()
			self.vivo=False

	def recupera(self, time):
		if(self.state=="golpeado" and time>=self.timeG+0.5):
			self.state="normal"
			
		if(self.state=="girando" and time>=self.timeG+0.15):
			self.state="normal"

	def draw(self, screen):
		screen.blit(self.image, self.rect)



