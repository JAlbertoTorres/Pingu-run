	#sp_penguin.py#
import pygame, sys, random
from pygame.locals import *
import configPenguin
import graphics
import json
#vec = pygame.math.Vector2

def texto(texto, posx, posy, color=(171,13,78)):
	fuente = pygame.font.Font("images/DroidSans.ttf",40)
	salida = pygame.font.Font.render(fuente,texto,1, color)
	salida_rect=salida.get_rect()
	salida_rect.centerx = posx
	salida_rect.centery = posy
	return salida, salida_rect

class ataqueP(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		
		self.speed = 20 
		self.dir = True
		#self.state 
		self.existe = False
		self.cargado = True
		self.timeShot = 0
		self.image = graphics.load_image("images/mini_atackP.gif")
		self.rect = self.image.get_rect()
		self.rect.centerx = -10
		self.rect.centery = -10

	def atack(self, penguin):
		if self.cargado and penguin.timeS == 0:
			self.image = graphics.load_image("images/atackP.gif")
			if(penguin.cara):
				self.dir = True
				self.rect.centerx = penguin.rect.centerx + configPenguin.wbloque*1.25
			else:
				self.dir = False
				self.rect.centerx = penguin.rect.centerx - configPenguin.wbloque*1.25
			
			self.rect.centery = penguin.rect.centery -25
			self.existe = True
			self.cargado = False 
			self.timeShot = penguin.time
			#print("disparando ataque ", penguin.ataques)
			
			


	def mover(self,penguin):
		if self.existe:
			#print("burbuja en ", self.rect.centerx)
			if(self.dir):
				#print("moviendo ataque", penguin.ataques)
				self.rect.centerx += 0.5*self.speed
				if self.rect.centerx>=configPenguin.width or self.cargado:
					#print("eliminando ataque", penguin.ataques)
					
					self.existe = False
		
			else:
				self.rect.centerx -= 0.5*self.speed
				#print("moviendo ataque", penguin.ataques)
				if self.rect.centerx<=0 or self.cargado:
					#print("eliminando ataque", penguin.ataques)
					self.existe = False

	def moverInv(self,penguin):
		if self.existe:
			#print("burbuja en ", self.rect.centerx)
			if (penguin.cara) and not self.dir:
				#print("moviendo ataque", penguin.ataques)
				self.rect.centerx -= 0.5*self.speed
				if self.rect.centerx>=configPenguin.width or self.cargado:
					#print("eliminando ataque", penguin.ataques)					
					self.existe = False
		
			elif self.dir and not (penguin.cara):
				self.rect.centerx += 0.5*self.speed
				#print("moviendo ataque", penguin.ataques)
				if self.rect.centerx<=0 or self.cargado:
					#print("eliminando ataque", penguin.ataques)
					self.existe = False
					
					
	def draw(self, screen):
		screen.blit(self.image, self.rect)	

class pingu(pygame.sprite.Sprite):
	def __init__(self, plats, limMax):
		pygame.sprite.Sprite.__init__(self)
		self.image = graphics.load_image(configPenguin.sprites+"pingu2.gif")
		self.rect = self.image.get_rect()
		self.plats = plats
		self.limMax = limMax
		self.rect.centerx = 0+configPenguin.wbloque/2
		self.rect.centery = 0
		self.goal = False
		self.posicion = self.rect.centerx/configPenguin.wbloque
		self.altura = 0
		self.movVert_mapa = 0
		self.Dorados = []
		self.TotalD = 0
		self.pinkPingu = False		
		self.speed = 0.14
		self.factMov = 90
		self.inAir = False
		self.Fell = False	
		self.time = 0 #	Tiempo que lleva en la partida
		#self.timeAux = -1
		self.timeI = 0 #tiempo en que se quemó
		self.timeS = 0 #tiempo en que disparó
		self.cara = True
		self.v = 26
		self.m = 1
		self.factFall = 0.48
		self.limInf = 0
		#self.piso=1000
		#self.ataqueP = ataqueP()	
		self.ataqueP = [ataqueP(), ataqueP(), ataqueP()]
		self.vidas = 3
		self.puntos = 0
		self.state = "cayendo"		
		self.paredD = False
		self.paredI = False
		self.abismo = False
		self.partida = None
		self.contAnim = 0
		self.Mov = False
	
	
	def leerPartida(self,archivo):
	    with open(archivo) as json_data:
	        d = json.load(json_data)
	        data = json.dumps(d)
	        partida = json.loads(data)
	    return partida

	def cargaPartida(self, partida):
		self.partida = self.leerPartida(partida)
		self.vidas = self.partida["vidas"]
		if self.vidas<=0:
			self.vidas=3
		if self.partida['inicio']== 'inicio':
			self.posicion = self.rect.centerx/configPenguin.wbloque
		elif self.partida['inicio']=='checkpoint':
			#self.posicion = 31
			self.rect.centery = 0


             
	def enfria(self):

		if(self.state=="quemado" and self.time>=self.timeI+0.7):
			#print("Se recupero de quemadura yeeei")
			self.state='cayendo'
			if self.cara :
				self.image = graphics.load_image(configPenguin.sprites+"pingu2.gif")
			else:
				self.image = graphics.load_image(configPenguin.sprites+"pingu2L.gif")

		if (self.state=="golpeado" and self.time>=self.timeI+0.7):
			#print("Se recupero del golpe yeeei")
			self.state='cayendo'
			if self.cara :
				self.image = graphics.load_image(configPenguin.sprites+"pingu2.gif")
			else:
				self.image = graphics.load_image(configPenguin.sprites+"pingu2L.gif")		


		#	print("ya se enfrio")

	def Quemado(self):
		self.state = "quemado"
		self.timeI = self.time 
		if self.cara :
			self.image = graphics.load_image(configPenguin.sprites+"pingu2F.gif")
		else:
			self.image = graphics.load_image(configPenguin.sprites+"pingu2FL.gif")
				
		#print("Se quemo")

	def Golpeado(self):
		if(self.state!="golpeado"):
			#print("mientras me pagaron estaba...", self.state)
			#print("se supone que no estoy golpeado...")
			self.state="golpeado"
			self.timeI = self.time
			if self.cara:
				self.image = graphics.load_image(configPenguin.sprites+"pingu2_G.gif")
			else:
				self.image = graphics.load_image(configPenguin.sprites+"pingu2_G2.gif")

	def salto(self):
		if(self.v>21):
			self.v=21
		self.inAir = True
		self.state="saltando"

	def aterriza(self, top, x,y):				
		#print("aterrizando")
		#print("top", self.rect.top)
		#print("bottom", self.rect.bottom)
		#print("centery", self.rect.centery)
		#print("state", self.state)
		
		if(self.rect.top>0) and self.rect.centery>0 and self.rect.bottom>30:	
			self.v = 21
		#	if(top<=configPenguin.wbloque*3):
			#print("hishoiuhb")
		#		self.v+=top/configPenguin.hbloque+2
			self.inAir = False	
			
			#print("top", self.rect.top)
			#print("bottom", self.rect.bottom)
			#print("centery", self.rect.centery)
			self.rect.bottom=top+0.15*configPenguin.hbloque
			self.altura=top+0.15*configPenguin.hbloque + self.movVert_mapa-configPenguin.hbloque
			self.Fell = False	
		#print("bottom debería ser",top+2 )
		#print("bottom es", self.rect.bottom)
		

	def atackP(self):
		index=-1
		for atack in self.ataqueP:
			if(atack.cargado):
				index=self.ataqueP.index(atack)

		if(index>-1):
			self.ataqueP[index].atack(self)
			self.timeS=self.time
		
			#print("ataque")
	
	def Anima(self):
		if not self.cara:
			if(self.state=='quemado'):
				if(self.Mov):
					self.image = graphics.load_image(configPenguin.sprites+"pingu2FL.gif")
				else:
					self.image = graphics.load_image(configPenguin.sprites+"pingu2FL2.gif")
			elif self.state=="golpeado":
				if(self.Mov):
					self.image = graphics.load_image(configPenguin.sprites+"pingu2_G.gif")
				else:
					self.image = graphics.load_image(configPenguin.sprites+"pingu2_Inv2.gif")
		
			elif not(self.state=="quemado") and not(self.state=="golpeado"):
				if(self.Mov):
					self.image = graphics.load_image(configPenguin.sprites+"pingu2L.gif")
				else:
					self.image = graphics.load_image(configPenguin.sprites+"pingu2L2.gif")
		else:
			if(self.state=="quemado"):
				if(self.Mov):
					self.image = graphics.load_image(configPenguin.sprites+"pingu2F.gif")
				else:
					self.image = graphics.load_image(configPenguin.sprites+"pingu2F2.gif")
			elif self.state=="golpeado":
				if(self.Mov):
					self.image = graphics.load_image(configPenguin.sprites+"pingu2_G2.gif")
				else:
					self.image = graphics.load_image(configPenguin.sprites+"pingu2_Inv.gif")
			elif not(self.state=="quemado") and not(self.state=="golpeado"):
				if(self.Mov):
					self.image = graphics.load_image(configPenguin.sprites+"pingu2.gif")
				else:
					self.image = graphics.load_image(configPenguin.sprites+"pingu22.gif")
		self.contAnim+=0.05		
		if(self.state=="golpeado"):
			self.contAnim+=0.3

		if(self.contAnim>1.5 ):
			self.contAnim=0
			self.Mov=not(self.Mov)

	def camina(self, op):
		

		if(op==1) and not(self.paredI): #hacia la izquierda							

			if(self.state=='quemado'):
				if(self.Mov):
					self.image = graphics.load_image(configPenguin.sprites+"pingu2FL.gif")
				else:
					self.image = graphics.load_image(configPenguin.sprites+"pingu2FL2.gif")
			elif self.state=="golpeado":
				if(self.Mov):
					self.image = graphics.load_image(configPenguin.sprites+"pingu2_G.gif")
				else:
					self.image = graphics.load_image(configPenguin.sprites+"pingu2_Inv2.gif")
		
			elif not(self.state=="quemado") and not(self.state=="golpeado"):
				if(self.Mov):
					self.image = graphics.load_image(configPenguin.sprites+"pingu2L.gif")
				else:
					self.image = graphics.load_image(configPenguin.sprites+"pingu2L2.gif")
			if(self.posicion<=5):
				if self.rect.left >= 0.5:
					self.rect.centerx -= int(self.speed*self.factMov)
					#print("restando", int(self.speed*self.factMov))
					self.posicion -= int(self.speed*self.factMov)/(configPenguin.wbloque)
					self.cara=False
			else:
				if(self.rect.left>= 0.5):
					self.rect.centerx -= int(self.speed*self.factMov)
					#print("restando", int(self.speed*self.factMov))
					self.posicion -= int(self.speed*self.factMov)/(configPenguin.wbloque)
					self.cara=False
				
		if(op==2) and not(self.paredD): #hacia la derecha
			if(self.state=="quemado"):
				if(self.Mov):
					self.image = graphics.load_image(configPenguin.sprites+"pingu2F.gif")
				else:
					self.image = graphics.load_image(configPenguin.sprites+"pingu2F2.gif")
			elif self.state=="golpeado":
				if(self.Mov):
					self.image = graphics.load_image(configPenguin.sprites+"pingu2_G2.gif")
				else:
					self.image = graphics.load_image(configPenguin.sprites+"pingu2_Inv.gif")
			elif not(self.state=="quemado") and not(self.state=="golpeado"):
				if(self.Mov):
					self.image = graphics.load_image(configPenguin.sprites+"pingu2.gif")
				else:
					self.image = graphics.load_image(configPenguin.sprites+"pingu22.gif")
			if(self.posicion <= self.limMax-2):
				if self.posicion >= self.limMax-(self.limMax*0.75):
					self.rect.centerx += int(self.speed*self.factMov)
					#print("sumando", int(self.speed*self.factMov))
					self.posicion += int(self.speed*self.factMov)/(configPenguin.wbloque)
					self.cara=True				

				elif self.rect.right <= configPenguin.width*0.75:
					self.rect.centerx += int(self.speed*self.factMov)
					#print("sumando", int(self.speed*self.factMov))
					self.posicion += int(self.speed*self.factMov)/(configPenguin.wbloque)
					self.cara=True				
			#else:
			#	if(self.rect.right<=configPenguin.width-100):
			#		self.rect.centerx += int(self.speed*self.factMov)
					#print("sumando", int(self.speed*self.factMov))
			#		self.posicion += int(self.speed*self.factMov)/(configPenguin.wbloque)
			#		self.cara=True
		#Animando
		self.contAnim+=0.1		
		if(self.contAnim>1.5):
			self.contAnim=0
			self.Mov=not(self.Mov)




	def saltar(self):
		#print("self.inAir", self.inAir)		 
		if self.inAir:			
		#	print("v", self.v)
			#print("limT", self.limT)
			if self.v >0:
				f = 0.5*int(self.speed*self.m* self.v*self.v)				
				self.rect.bottom-=f #*self.factFall				
				self.altura-=f
				#self.rect.bottom-= 3.5*int(self.speed*self.m*self.factMov*self.factFall)
				#if(abs(self.v)>=5):
				self.v-=0.65 #self.factFall#1#self.factFall
				

				
			else:

				if(self.state!='quemado' and self.state!="Bloqueado_Ar" and self.state!='golpeado'):
					self.state="cayendo"
					#print("cambiando a: cayendo, por el salto")

					
	def cargaAtaque(self):
		#if self.ataques<2:#Si el numero de ataques es menor a dos, el jugador ya disparó
		for burbuja in self.ataqueP:
			if(not(burbuja.cargado)):
				if(self.time>=burbuja.timeShot+1.5):
					#self.ataques+=1
					burbuja.image = graphics.load_image("images/mini_atackP.gif")
					burbuja.cargado=True
					#print("disparo cargado")

		if(self.time>=self.timeS+0.05):
			self.timeS=0



	def cae(self):
		hits = pygame.sprite.spritecollide(self, self.plats, False)		
		
		#if self.inAir and self.state!="saltando":
			#self.v=10
		#print("hit ", hits)
		#print("type ", hits[0].type)
	#	print("estado ", self.state)				
	#	print("v", self.v)

		if(self.state=="Bloqueado_Ar" and self.time>=self.timeI+0.5):			
			self.state='cayendo'	
			self.rect.bottom+= 2.5*int(self.speed*self.m*self.factMov*self.factFall)

		#if(self.state=="levantado" and self.time>=self.timeI+0.5):			
		#	self.state='cayendo'		

		if(self.state=="Bloqueado_Ar" ):
			#print("Cayendo Bloqueado")
			if(hits) and self.rect.top>0:
				for h in hits:
					#print("tocando bloque mientras ando bloqueado")
					if(h.rect.bottom>=self.rect.bottom and h.type!="decor" and h.type!="checkpoint"):													
						self.aterriza(h.rect.top, h.rect.x, h.rect.y)
						#print("66")
					else:									
						f = -int(self.speed*self.m* self.v*self.v)		
						#self.rect.bottom-=f #*self.factFall				
						#self.rect.bottom-=f #*self.factFall				
						self.rect.bottom+= 2.5*int(self.speed*self.m*self.factMov*self.factFall)
						self.altura+= 2.5*int(self.speed*self.m*self.factMov*self.factFall)
						#if(abs(self.v)>=0):
						self.v-=self.factFall#0.5#1


			else:
				#self.state="cayendo"				
				f = -int(self.speed*self.m* self.v*self.v)		
				#self.rect.bottom-=f #*self.factFall				
				#self.rect.bottom-=f #*self.factFall				
				self.rect.bottom+= 2.5*int(self.speed*self.m*self.factMov*self.factFall)
				self.altura+= 2.5*int(self.speed*self.m*self.factMov*self.factFall)
				self.v-=self.factFall#1
				#if(abs(self.v)>=0):
				#	self.v-=self.factFall#1			
#				print("BLUUURR")


		if self.state=="cayendo" or self.state=="quemado" or self.state=='golpeado' or (self.state=="saltando" and not(self.inAir)) and self.rect.top>0:			

			if(not hits):
				#if(not self.inAir and self.v<0):
				#	self.v=22
					#self.inAir=True
				#print("caida libreee")	
				#if(self.rect.centery<=self.piso):
				f = -int(self.speed*self.m* self.v*self.v)		
				#self.rect.bottom-=f #*self.factFall				
				self.rect.bottom+= 2.5*int(self.speed*self.m*self.factMov*self.factFall)
				self.altura+= 2.5*int(self.speed*self.m*self.factMov*self.factFall)
				self.v-=self.factFall#0.5#1
				#if(abs(self.v)>=0):
				#	self.v-=self.factFall#1

			
			elif hits and self.rect.top>0:				
				for h in hits:
					#print(h)
					if(h.rect.top>=self.rect.centery and h.type!="movil"):								
						if(h.type!="comida" and h.type!="bonus" and h.type!="extraL" and h.type!="dorado" and h.type!="checkpoint"):
							#print("1")
							self.aterriza(h.rect.top, h.rect.x, h.rect.y)
			
					#Se queda atorado en el suelo
					elif(h.rect.top+16< self.rect.bottom) and self.rect.bottom< h.rect.bottom and h.type!="movil" and h.type!="checkpoint":												
						if(self.rect.centerx< h.rect.right) and self.rect.centerx>h.rect.left:
						#	print("2")
							self.aterriza(h.rect.top, h.rect.x, h.rect.y)						

					#Plataforma movil vertical									
					elif(h.type=="movil") and h.dir:								
						if(h.rect.top+16< self.rect.bottom) and self.rect.bottom< h.rect.bottom :
							if(self.rect.centerx< h.rect.right) and self.rect.centerx>h.rect.left:
								if(self.rect.centerx< h.rect.right) and self.rect.centerx>h.rect.left:
									#print("3")
									self.aterriza(h.rect.top, h.rect.x, h.rect.y)
									
								#print("moviendose con la plataforma")
						self.rect.centery+=h.factMov
						self.altura+= h.factMov
					
					#plataforma movil horizontal
					elif(h.type=="movil") and not h.dir and h.rect.top> self.rect.centery:						
						if(self.rect.centerx< h.rect.right) and self.rect.centerx>h.rect.left:							
							#print("4")
							self.aterriza(h.rect.top, h.rect.x, h.rect.y)
									

					if(h.type=='fuego') and self.state!='quemado' and self.state!="golpeado":
						#print("tocando fuegooo")
						#self.pingu.piso=h.rect.top-0.3*configPenguin.hbloque 
						if(self.rect.right> h.rect.left+5 or self.rect.left> h.rect.right-5):
							#self.pingu.salto()
							if(self.vidas>=0):
								self.vidas-=1
								self.Quemado()
					
					if h.type=="checkpoint":
						#print("este es el caso")
						self.state="cayendo"
						f = -int(self.speed*self.m* self.v*self.v)		
						#self.rect.bottom-=f #*self.factFall				
						self.rect.bottom+= 2.5*int(self.speed*self.m*self.factMov*self.factFall)
						self.altura+= 2.5*int(self.speed*self.m*self.factMov*self.factFall)
						self.v-=self.factFall#0.5#1
								
			
			elif hits:
				#print("abii")
				f = -int(self.speed*self.m* self.v*self.v)		
				#self.rect.bottom-=f #*self.factFall				
				self.rect.bottom+= 2.5*int(self.speed*self.m*self.factMov*self.factFall)
				self.altura+= 2.5*int(self.speed*self.m*self.factMov*self.factFall)
				self.v-=self.factFall#0.5#1


			if(self.altura>self.limInf+configPenguin.hbloque*1.5):
				self.vidas-=1
				self.abismo = True
				

		
 

	def draw(self, screen):
		if(self.vidas>=0):
			v_jug, v_jug_rect = texto("Vidas  "+str(self.vidas), configPenguin.width/9,40)
		else:
			v_jug, v_jug_rect = texto("Vidas  "+str(0), configPenguin.width/9,40)
		i=0;j=2
		noCarga = [ataqueP(),ataqueP(),ataqueP()]
		for carga in noCarga:
			carga.image=graphics.load_image("images/mini_atackP2.gif")

		for burbuja in self.ataqueP:
			if(burbuja.cargado):
				burbuja.rect.centerx = configPenguin.width/9+i
				burbuja.rect.centery = 120
				burbuja.draw(screen)	
				i+=80
			else:
				noCarga[j].rect.centerx = configPenguin.width/9+i
				noCarga[j].rect.centery = 120
				noCarga[j].draw(screen)	
				i+=80
				j-=1
			
		p_jug, p_jug_rect = texto("Puntos  "+str(self.puntos), configPenguin.width/9*2,40)
		screen.blit(p_jug, p_jug_rect)
		screen.blit(v_jug, v_jug_rect)
		screen.blit(self.image, self.rect)
		