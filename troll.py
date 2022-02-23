import pygame, sys, random
from pygame.locals import *
import configPenguin
import graphics
import json
import monster
import math 

class ataqueM(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = graphics.load_image("spritesP/fire.gif")
		self.rect = self.image.get_rect()
		self.speed = 0.15
		self.rect.centerx = -10
		self.rect.centery = -10
		self.existe = False
		self.timeShot = 0
		self.dir = False

	def atack(self,trol, time):
		if not(self.existe):	
			if trol.cara:
				self.dir = True
				self.image = graphics.load_image("spritesP/fire2.gif")			
			else:
				self.dir = False
				self.image = graphics.load_image("spritesP/fire.gif")
			self.rect.centerx = trol.rect.centerx -5	
			self.rect.centery = trol.rect.centery +25
			self.timeShot= time
			self.existe=True

	def mover(self, trol, time):
		if self.existe:
			if self.dir:
				self.rect.centerx += int(self.speed * trol.factMov)
			else:
				self.rect.centerx -= int(self.speed * trol.factMov)
			if time >= self.timeShot+1.5:
				self.timeShot=0
				self.existe=False				

	def draw(self, screen):
		screen.blit(self.image, self.rect)

class troll(monster.monster):
	def __init__(self,x, y, cara=True):
		monster.monster.__init__(self, x, y+25, enemigo='spritesP/Monster1.gif', resist=4)
		self.puntos = 80
		self.speed = 0.14
		self.factMov = 90
		self.ataque = ataqueM()
		self.movSpace = 2
		self.contMov = 0
		self.cara = True#cara
		self.Mov =True
		self.state = "normal"
		self.vivo = True
		self.timeG = 0 #Tiempo en que fue golpeado
		self.timeA = 0 #Tiempo en que atacó
		self.distAttack = 5 #La distancia, en bloques, a la cual se activa el ataque automatico
		self.contAnim = 0
		self.type="troll"

	def mover(self):
		if self.cara:
			#derecha
			if(self.state=="golpeado"):
				self.image = graphics.load_image("spritesP/Monster1_attacked.gif")	 
			if(self.state=="normal" and self.Mov):
				self.image = graphics.load_image("spritesP/Monster1.gif")					
			if(self.state=="normal" and not self.Mov):
				self.image = graphics.load_image("spritesP/Monster1_2.gif")		
			#print("derecha")			
			self.rect.centerx+=int(0.5*self.factMov*self.speed)
			self.contMov+=0.04
			if(self.contMov>=self.movSpace):
				self.cara=not(self.cara)
				self.contMov=0
		#izquierda
		else:			
			if(self.state=="golpeado"):
				self.image = graphics.load_image("spritesP/Monster2_attacked.gif")	 
			if(self.state=="normal" and self.Mov):
				self.image=	graphics.load_image("spritesP/Monster2.gif")
			if(self.state=="normal" and not self.Mov):
				self.image = graphics.load_image("spritesP/Monster2_2.gif")		
	#		print("izquierda")			
			self.rect.centerx-=int(0.5*self.factMov*self.speed)
			self.contMov+=0.04
			
			if(self.contMov>=self.movSpace):
				self.cara=not(self.cara)
				self.contMov=0

		if(self.contAnim>=1):			
			self.contAnim=0
			self.Mov=not(self.Mov)
		self.contAnim+=0.1
	
	def atack(self, time):
		if(self.vivo and self.state!="atacando"):
			self.state = "atacando"
			self.timeA = time
			self.ataque.atack(self,time)
#			print("ataque")

	def recibeGolpe(self,time):
		self.resistencia-=1
		self.state = "golpeado"
		self.timeG = time
		if(self.resistencia<=0):
			self.kill()
			self.vivo=False

	def recupera(self, time):
		if(self.state=="golpeado" and time>=self.timeG+0.5):
			self.state="normal"
		if(self.state=="atacando" and time>=self.timeA+0.5):
			self.state="normal"

	def draw(self, screen):
		screen.blit(self.image, self.rect)



