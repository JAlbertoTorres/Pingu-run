import pygame, sys, random
from pygame.locals import *
import configPenguin
import graphics
import monster


class oso(monster.monster):
	def __init__(self,x, y,cara=True):
		monster.monster.__init__(self, x, y, enemigo='spritesP/oso_cam1.gif', resist=3)
		self.puntos = 50
		self.speed = 0.14
		self.factMov = 45
		#self.ataque = ataqueM()
		self.movSpace = 5
		self.contMov = 0
		self.cara = cara
		self.state = "normal"
		self.vivo = True
		self.termino = False
		self.timeG = 0 #Tiempo en que fue golpeado
		self.timeA = 0 #Tiempo en que atacó
		self.contAnim = 0 #Tiempo en para activar animacionvv
		self.contAnimAtk = 0 #Este contador indica que imagen se va a desplegar
		self.contMovAtk = 0 #Este contador indica en que momento se cambiara la imagen
		self.distAttack = 7 #La distancia, en bloques, a la cual se activa el ataque automatico
		self.inmune = False
		self.mov = True

	def mover(self):
		if self.cara:#derecha
			if(self.state=="golpeado"):
				self.image = graphics.load_image("spritesP/oso_attacked1.gif")	 
			if(self.state=="normal" and self.mov):
				self.image = graphics.load_image("spritesP/oso_cam11.gif")	

			if(self.state=="normal" and not(self.mov)):
				self.image = graphics.load_image("spritesP/oso_cam22.gif")
			#print("derecha")			
			self.rect.centerx+=int(0.5*self.factMov*self.speed)
			self.contMov+=0.04
			if(self.contMov>=self.movSpace):
				self.cara=not(self.cara)
				self.contMov=0
		#izquierda
		else:			
			if(self.state=="golpeado"):
				self.image = graphics.load_image("spritesP/oso_attacked2.gif")	 
			if(self.state=="normal" and self.mov):
				self.image=	graphics.load_image("spritesP/oso_cam2.gif")	
			if(self.state=="normal" and not(self.mov)):
				self.image=	graphics.load_image("spritesP/oso_cam1.gif")	
	#		print("izquierda")			
			self.rect.centerx-=int(0.5*self.factMov*self.speed)
			self.contMov+=0.04
			if(self.contMov>=self.movSpace):
				self.cara=not(self.cara)
				self.contMov=0

		if(self.contAnim>=1):
			self.mov=not(self.mov)
			self.contAnim=0
		self.contAnim+=0.1	

	def atack(self, time):
		if(self.vivo and not self.termino):
			#derecha
			self.timeA=time
			self.state="atacando"
			self.inmune=True
			if(self.cara):
				if(self.contAnimAtk==0):
					#self.image=	graphics.load_image("spritesP/oso_cam2.gif")
					self.image = graphics.load_image("spritesP/oso_attack1_1.gif")	 
				elif(self.contAnimAtk==1):
					#self.image=	graphics.load_image("spritesP/oso_cam2.gif")
					self.image = graphics.load_image("spritesP/oso_attack1_2.gif")	 
				elif(self.contAnimAtk==2):
					#self.image=	graphics.load_image("spritesP/oso_cam2.gif")
					self.image = graphics.load_image("spritesP/oso_attack1_3.gif")	 
			#izquierda
			else:
				if(self.contAnimAtk==0):
					self.image = graphics.load_image("spritesP/oso_attack2_1.gif")	 
				elif(self.contAnimAtk==1):
					self.image = graphics.load_image("spritesP/oso_attack2_2.gif")	 
				elif(self.contAnimAtk==2):
					self.image = graphics.load_image("spritesP/oso_attack2_3.gif")	 
			
			self.contMovAtk+=0.15
			if(self.contMovAtk>=1):
				self.contAnimAtk+=1
				self.contMovAtk=0
			if(self.contAnimAtk>2):
				self.contAnimAtk=0
				self.termino = True
				#self.state="normal"


	def recibeGolpe(self,time):
		if not self.inmune:
			if self.cara:
				self.image = graphics.load_image("spritesP/oso_attacked1.gif")	 
			else:
				self.image = graphics.load_image("spritesP/oso_attacked2.gif")	 
			self.state = "golpeado"
			self.timeG = time
			self.resistencia-=1
			if(self.resistencia<=0):
				self.kill()
				self.vivo=False
	#	else:
	#		print("jaja, se cubrio :D")

	def recupera(self, time):
		if(self.state=="golpeado" and time>=self.timeG+0.2):
			self.state="normal"
		if(self.state=="atacando" and time>=self.timeA+0.2):
			self.state="normal"
			self.inmune = False
			self.termino = False

	def draw(self, screen):
		screen.blit(self.image, self.rect)



