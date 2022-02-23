import pygame
import scene
import configPenguin
import graphics
import scene_intro
import scene_results
from load_levels import Mapa
from sp_penguin import pingu
from sp_penguin import ataqueP as bubble
import sys
import monster

import json
from pickle import dump, dumps, load, loads

def texto(texto, posx, posy, color=(171,13,78), tam=40):
	fuente = pygame.font.Font("images/DroidSans.ttf",tam)
	salida = pygame.font.Font.render(fuente,texto,1, color)
	salida_rect=salida.get_rect()
	salida_rect.centerx = posx
	salida_rect.centery = posy
	return salida, salida_rect

class SceneHome(scene.Scene):
	"""docstring for SceneHome"""
	def __init__(self, director, level, partida):
		scene.Scene.__init__(self,director)
		print("Iniciando partida...\n\n")
		#pygame.mixer.music.load('/home/beto/Música/Musica/Vampire Killer.mp3')
		#pygame.mixer.music.play(-1)
		self.Dir = director
		self.partida = partida
		self.all_sprites = pygame.sprite.Group()
		self.back = graphics.load_image(configPenguin.menus+"fondo1.png")
		#self.all_sprites.add(self.pingu)
		self.Borde = configPenguin.width/configPenguin.wbloque
		self.Cima = configPenguin.height/configPenguin.hbloque
		self.on_plat =False
		self.sumaP = 0
		self.fact_plat = 1
		self.Map = Mapa(level)
		self.Map.load()
		#print("Etiquetas de bloques", self.Map.labels)		
		self.bounceT = 0
		self.bota = False
		self.altura_inicial = self.Map.Start.rect.centery 
		self.timeAux = 0
		pygame.time.wait(300)

		self.labels = []	
		for etiqueta in self.Map.labels:
			if self.Map.grafo[int(etiqueta)]["tipo"]!="meta" and self.Map.grafo[int(etiqueta)]["tipo"]!="inicio" and self.Map.grafo[int(etiqueta)]["tipo"]!="checkpoint":
				self.labels.append(texto(str(etiqueta), self.Map.labels[etiqueta][1]*(configPenguin.wbloque)+configPenguin.wbloque/2,self.Map.labels[etiqueta][0]*configPenguin.hbloque+configPenguin.hbloque/2, color=(0,127,0), tam=45 ))
			else:
				self.labels.append(texto(str(etiqueta), self.Map.labels[etiqueta][1]*(configPenguin.wbloque)+(configPenguin.wbloque*0.85),self.Map.labels[etiqueta][0]*configPenguin.hbloque+configPenguin.hbloque/3, color=(255,255,255), tam=45 ))

		for f in self.Map.fuego:
			self.all_sprites.add(f)
		
		for h in self.Map.hielo:
			self.all_sprites.add(h)
		
		for r in self.Map.rebota:
			self.all_sprites.add(r)

		for d in self.Map.Golds:
			self.all_sprites.add(d)

		for p in self.Map.roca: 
			self.all_sprites.add(p)

		for c in self.Map.comida:
			self.all_sprites.add(c)
		
		for m in self.Map.enemies:
			self.all_sprites.add(m)

		if self.Map.pinkP != None:
			self.all_sprites.add(self.Map.pinkP)

		self.all_sprites.add(self.Map.Goal)
		#self.all_sprites.add(self.Map.Start)

		if self.Map.xtraL !=None:
			self.all_sprites.add(self.Map.xtraL)

		if self.Map.chk_pnt:
			self.all_sprites.add(self.Map.chk_pnt)								
		self.limMax= self.Map.col
		self.pingu = pingu(self.all_sprites, self.limMax)

		for d in self.Map.Golds:
			self.pingu.TotalD+=1

		self.flagJP= 0
		self.time = 0
		self.limTmp = self.Map.tiempo #Opcion de tiempo segun longitud 1.5*self.limMax
		self.pingu.rect.bottom = self.Map.Start.rect.top+12
		self.pingu.cargaPartida(configPenguin.partidas+self.partida)

		#Cargamos las submisiones (peces dorados y pingüino rosa) completadas por el usuario anteriormente
		if(self.Map.record["dorados"]!=[]):
			self.pingu.Dorados=self.Map.record["dorados"]
		self.pingu.pinkPingu=self.Map.record["bonus"]

		self.pingu.limInf = self.Map.limInf+configPenguin.hbloque

		if self.pingu.partida["juego_anterior"]!=level:
			self.pingu.partida["inicio"]=="inicio"

		#Cargando la partida desde el checkpoint
		if(self.pingu.partida["inicio"]=="checkpoint") and self.pingu.partida["juego_anterior"]==level:
			self.Map.chk_pnt.image = graphics.load_image("spritesP/checkpoint2.gif")
			#self.pingu.rect.centerx = self.Map.chk_pnt.rect.centerx
			self.pingu.rect.centery = self.Map.chk_pnt.rect.centery

			i=0
			while(i< int(self.Map.chk_pnt.rect.right)):
				for plat in(self.all_sprites):
					plat.rect.centerx-= int(self.pingu.speed*self.pingu.factMov)
				self.Borde+= int(self.pingu.speed*self.pingu.factMov)/(configPenguin.wbloque) #1
				self.pingu.posicion += int(self.pingu.speed*self.pingu.factMov)/(configPenguin.wbloque)

				#for enemy in (self.Map.enemies):
					#enemy.rect.x-= int(self.pingu.speed*self.pingu.factMov)
				self.Map.Start.rect.centerx-= int(self.pingu.speed*self.pingu.factMov)				
				for v in (self.Map.decor):
					v.rect.centerx-=int(self.pingu.speed*self.pingu.factMov)				
				i+=0.8

			while(i< int(self.Map.chk_pnt.rect.bottom)):
				for plat in(self.all_sprites):
					plat.rect.centery+= int(self.pingu.speed*self.pingu.m*self.pingu.factMov*self.pingu.factFall)
				#self.+= int(self.pingu.speed*self.pingu.factMov)/(configPenguin.wbloque) #1
				#self.pingu.posicion += int(self.pingu.speed*self.pingu.factMov)/(configPenguin.wbloque)

				#for enemy in (self.Map.enemies):
					#enemy.rect.x-= int(self.pingu.speed*self.pingu.factMov)
				self.Map.Start.rect.centery+= int(self.pingu.speed*self.pingu.m*self.pingu.factMov*self.pingu.factFall)
				for v in (self.Map.decor):
					v.rect.centery+=int(self.pingu.speed*self.pingu.m*self.pingu.factMov*self.pingu.factFall)
				i+=78
				self.Cima+=0.275
				self.pingu.altura=0.8*(self.Map.chk_pnt.rect.centery)

		elif(self.Map.Start.rect.centery>configPenguin.height):
			i=0
			while(i< int(self.Map.Start.rect.bottom)):
				for plat in(self.all_sprites):
					plat.rect.centery+= int(self.pingu.speed*self.pingu.m*self.pingu.factMov*self.pingu.factFall)
				#self.+= int(self.pingu.speed*self.pingu.factMov)/(configPenguin.wbloque) #1
				#self.pingu.posicion += int(self.pingu.speed*self.pingu.factMov)/(configPenguin.wbloque)

				#for enemy in (self.Map.enemies):
					#enemy.rect.x-= int(self.pingu.speed*self.pingu.factMov)
				self.Map.Start.rect.centery+= int(self.pingu.speed*self.pingu.m*self.pingu.factMov*self.pingu.factFall)
				self.pingu.altura+=11.38*int(self.pingu.speed*self.pingu.m*self.pingu.factMov*self.pingu.factFall)
				for v in (self.Map.decor):
					v.rect.centery+=int(self.pingu.speed*self.pingu.m*self.pingu.factMov*self.pingu.factFall)

				i+=78
				self.Cima+=0.66
				#if(i%200==0):
					#print("moviendo...")


			self.pingu.posicion=0
			self.pingu.rect.centery=self.Map.Start.rect.centery-configPenguin.hbloque
			self.pingu.rect.centerx=self.Map.Start.rect.centerx-configPenguin.wbloque
		else:
			self.pingu.posicion=0
			self.pingu.rect.centery=self.Map.Start.rect.centery-configPenguin.hbloque
			self.pingu.rect.centerx=self.Map.Start.rect.centerx-configPenguin.wbloque

		self.Borde=int(self.Borde)	
		self.op=1
		self.end=0
		#print("limMax",self.limMax)
		#print("centerx", self.pingu.rect.centerx)
	
	def muevePantalla(self, space, dir1, dir2):
		if(dir1):
			#Moviendo hacia arriba
			if(dir2):
				self.pingu.rect.centery += space
				self.Cima+=space/configPenguin.hbloque
				for plat in(self.all_sprites):
					plat.rect.centery+= space
				for v in (self.Map.decor):
					v.rect.centery+=space
				for enemy in (self.Map.enemies):
					#enemy.rect.x-= int(self.pingu.speed*self.pingu.factMov)
					if(enemy.type=="troll"):
						if(enemy.ataque.existe):
							enemy.ataque.rect.centery+= space
				for burbuja in self.pingu.ataqueP:
					if(burbuja.existe):
						burbuja.rect.centery+=space
				self.Map.Start.rect.centery+= space
				for label in self.labels:
					label[1].centery+=space
				
				#				self.pingu.altura-=space

			#Moviendo hacia abajo
			else:
				self.pingu.rect.centery -= space
				self.Cima-=space/configPenguin.hbloque
				for plat in(self.all_sprites):
					plat.rect.centery-= space
				for v in (self.Map.decor):
					v.rect.centery-=space
				for enemy in (self.Map.enemies):
					#enemy.rect.x-= int(self.pingu.speed*self.pingu.factMov)
					if(enemy.type=="troll"):
						if(enemy.ataque.existe):
							enemy.ataque.rect.centery-= space
				for burbuja in self.pingu.ataqueP:
					if(burbuja.existe):
						burbuja.rect.centery-=space
				self.Map.Start.rect.centery-= space
				for label in self.labels:
					label[1].centery-=space
				#self.pingu.movVert_mapa -= space
#				self.pingu.altura+=space

		else:
			#Moviendo hacia la derecha
			if(dir2):
				self.pingu.rect.centerx -= space
				self.Borde+=space/(configPenguin.wbloque) #1
				for plat in(self.all_sprites):
					plat.rect.centerx-= space
				for v in (self.Map.decor):
					v.rect.centerx-=space
				for enemy in (self.Map.enemies):
					#enemy.rect.x-= int(self.pingu.speed*self.pingu.factMov)
					if(enemy.type=="troll"):
						if(enemy.ataque.existe):
							enemy.ataque.rect.centerx-= space
				for burbuja in self.pingu.ataqueP:
					if(burbuja.existe):
						burbuja.moverInv(self.pingu)
				self.Map.Start.rect.centerx-= space

				for label in self.labels:
					label[1].centerx-=space

			#Moviendo hacia la izquierda
			else:
				self.pingu.rect.centerx += space
				self.Borde-=space/(configPenguin.wbloque) #1
				for plat in(self.all_sprites):
					plat.rect.centerx+= space
				for v in (self.Map.decor):
					v.rect.centerx+=space
				for enemy in (self.Map.enemies):
					#enemy.rect.x+= int(self.pingu.speed*self.pingu.factMov)
					if(enemy.type=="troll"):
						if(enemy.ataque.existe):
							enemy.ataque.rect.centerx+= space
				for burbuja in self.pingu.ataqueP:
					if(burbuja.existe):
						burbuja.moverInv(self.pingu)
				self.Map.Start.rect.centerx+= space
				for label in self.labels:
					label[1].centerx+=space
		
	def on_update(self):
		#pygame.init()
		#self.pingu.rect.bottom = self.pingu.piso
		self.time =self.director.time
		self.limTmp-= self.time/1000
		self.pingu.saltar()
		self.pingu.cae()
		self.pingu.enfria()
		self.pingu.cargaAtaque()
		self.pingu.Anima()
		self.pingu.time += self.time/1000
		self.on_plat = False
		self.fact_plat = 1
		if(self.pingu.time<=0.05):
			self.pingu.altura = self.altura_inicial

		#self.pingu.altura = self.pingu.rect.bottom/configPenguin.hbloque-1
		#print("ataque ",self.pingu.ataques)
		#if(self.pingu.time>=self.timeAux+0.1):
		#	print("time ", self.pingu.time)
		#print("posicion ", self.pingu.posicion)

		#	print("centerx ", self.pingu.rect.centerx)
		#	self.timeAux+=0.1
		#print("altura inicial", self.altura_inicial)
		#print("limite ", self.limMax)
		#print("piso ",self.pingu.piso)
		#print("botom", self.pingu.rect.bottom)
		#print("estado ", self.pingu.state)	
		#print("v ", self.pingu.v)			
		#print("col ", self.pingu.posicion)
		#print("fila ", self.pingu.altura)
		#print("inAir", self.pingu.inAir)
		#print("borde", self.Borde)
		#print("cima", self.Cima)
		#print("altura", self.pingu.altura)
		#print("limite inferior", self.Map.limInf)

		if(self.altura_inicial !=self.Map.Start.rect.centery):
			if(self.Map.Start.rect.centery>self.altura_inicial):
				self.pingu.movVert_mapa = -(self.Map.Start.rect.centery - self.altura_inicial)

			else:
				self.pingu.movVert_mapa =(self.altura_inicial-self.Map.Start.rect.centery)
		#print("mov_vertical", self.pingu.movVert_mapa)
		
		self.pingu.limT=-0.5*configPenguin.hbloque
		if(self.pingu.vidas<0):
			#print("has muerto")
			self.end=1
			self.op=0

		if(self.limTmp<=0):
			self.end=1
			self.op=0

		if(self.pingu.abismo):
			self.end=1
			self.op=0

			
		while self.op==0:
			#print("GAME OVER")
			time = self.director.clock.tick(60)
			pygame.display.flip()	
			for eventos in pygame.event.get():
				if eventos.type == pygame.QUIT:
					sys.exit(0)
			if self.end==1:
				p_jug, p_jug_rect = texto("FIN DEL JUEGO ", configPenguin.width/2,configPenguin.height/2,color=(255,255,255), tam=50 )
				self.pingu.partida["juego_anterior"]= str(self.Map.name)#.replace(configPenguin.levelsP, "")
				#self.pingu.partida["juego_anterior"]=str(self.pingu.partida["juego_anterior"]).replace(".json","")
				self.director.screen.blit(p_jug, p_jug_rect)
				#Actualizamos el record del mapa
				self.Map.record["dorados"] =self.pingu.Dorados
				self.Map.record["bonus"] = self.pingu.pinkPingu
			
			if self.end==2:
				p_jug, p_jug_rect = texto("FELICITACIONES, HAS GANADO", configPenguin.width/2,configPenguin.height/2, color=(255,255,255), tam=50 )
				self.pingu.goal= True
				self.pingu.partida["inicio"]="inicio"
				#print("Siguiente nivel:", self.Map.next)
				if(not(self.Map.next in self.pingu.partida["desbloqueados"])):
					self.pingu.partida["desbloqueados"].append(self.Map.next)

				#Actualizamos el record del mapa
				self.Map.record["puntos"] = self.pingu.puntos
				self.Map.record["dorados"] =self.pingu.Dorados
				self.Map.record["bonus"] = self.pingu.pinkPingu
				self.Map.record["tiempo"] = self.pingu.time
				self.director.screen.blit(p_jug, p_jug_rect)
			
			#Actualizamos el mapa despues de la partida del jugador
			f_level = open(self.Map.name, "w")
			n= {"dificultad":"","tiempo":0,	"next_level":"","record": {"puntos":0, "dorados":[], "bonus":False, "tiempo":9999},"mapa":{}}
			data_string=json.dumps(n)
			decoded = json.loads(data_string)
			decoded["dificultad"] = self.Map.dificultad
			decoded["tiempo"] = self.Map.tiempo
			decoded["next_level"] = self.Map.next
			decoded["record"] =  self.Map.record
			decoded["mapa"] = self.Map.mapa
			nivel = json.dumps(decoded)
			f_level.write(nivel)	
			f_level.close()
			
			self.pingu.partida["vidas"]= self.pingu.vidas
			f = open(configPenguin.partidas+self.partida, "w")
			partida=json.dumps(self.pingu.partida)
			f.write(partida)	
			f.close()
			keys = pygame.key.get_pressed()
			if keys[pygame.K_INSERT] or keys[pygame.K_a]:
					self.op=1
					self.end=0
					self.Dir.change_scene(scene_results.SceneResults(self.Dir, self.pingu, self.partida))
					self.director.scene.results()
					#pygame.mixer.music.play(-1)

		#Animamos el pinguino rosa
		for plat in self.all_sprites:
			if(plat.type=="bonus"):				
				if(plat.T==0):
					plat.T = self.pingu.time
				elif(plat.T>0 and self.pingu.time>plat.T+0.15):
					plat.T = 0
					plat.saluda = not(plat.saluda)

				if(plat.saluda):
					plat.image = graphics.load_image("spritesP/pinguRosa2_2.gif")
				else:
					plat.image = graphics.load_image("spritesP/pinguRosa2.gif")

		#Animamos el bloque de rebote
		if(self.bounceT > 0):			
			for plat in self.all_sprites:
				if(plat.type=="rebota"):
					if(plat.activado and self.bota and self.pingu.time >=self.bounceT+0.95):
						self.bounceT=0
						self.bota = False
						plat.activado = False
						plat.rect.centery+=11
						plat.image = graphics.load_image("spritesP/bounce2.gif")

					elif(plat.activado and self.pingu.time>=self.bounceT+0.05 and not self.bota):								
						plat.rect.centery-=11
						plat.image =  graphics.load_image("spritesP/bouncing.gif")
						self.bota =True

		#Movemos los ataques del pinguino
		for burbuja in self.pingu.ataqueP:
			
			if(burbuja.existe):
				burbuja.mover(self.pingu)
				golpe=pygame.sprite.spritecollide(burbuja,self.all_sprites, False)
				if golpe:
					for g in golpe:
						if isinstance(g, monster.monster):
						#(g.type=="enemy" or g.type=="troll") :
							g.recibeGolpe(self.pingu.time)
							burbuja.existe=False
							if not(g.vivo):
								self.pingu.puntos+=g.puntos
						elif(g.type!="comida" and g.type!="bonus" and g.type!="dorado" and g.type!= "extraL" and g.type!="checkpoint"):
							burbuja.existe=False




		#Suma vida por conseguir 500 pts	
		if self.sumaP >=500:
				self.pingu.vidas+=1
				self.sumaP=0
		
		#Activando el movimiento automatico de los enemigos
		for enemy in self.Map.enemies:
			enemy.recupera(self.pingu.time)
			enemy.mover()
			
			#Activando el ataque automatico del enemigo
			#Solo si el enemigo esta frente al pinguino
			#print("centro del enemigo", enemy.rect.centerx)
			#print("limite a la izquierda", enemy.rect.centerx- 3*configPenguin.wbloque )
			#print("limite a la derecha", enemy.rect.centerx+ 3*configPenguin.wbloque )
			#print("centro del pinguino", self.pingu.rect.centerx)
			#print("enemy cara", enemy.cara)
			#print("enemy type", enemy.type)
			

			#el pinguino esta a la izquierda
			if(self.pingu.rect.centerx>= enemy.rect.centerx- enemy.distAttack*configPenguin.wbloque and self.pingu.rect.centerx< enemy.rect.centerx) and not (enemy.cara):
				enemy.atack(self.pingu.time)
				#print("enemy state", enemy.state)
				#print("atacando")

			#el pinguino esta a la derceha
			if(self.pingu.rect.centerx> enemy.rect.centerx and self.pingu.rect.centerx<= enemy.rect.centerx+ enemy.distAttack*configPenguin.wbloque) and enemy.cara:				
				enemy.atack(self.pingu.time)
				#print("enemy state", enemy.state)
				#print("atacando")

			#Movemos los ataques de los enemigos trol
			if(enemy.type=="troll"):
				if(enemy.ataque.existe):
					enemy.ataque.mover(enemy, self.pingu.time)
					golpe=pygame.sprite.collide_rect(enemy.ataque,self.pingu)					
					if golpe and self.pingu.state!="quemado":
						#print("Quemando al pinguino!!")
						self.pingu.vidas-=1
						self.pingu.Quemado()
						enemy.ataque.existe=False
						enemy.ataque.kill()
					#El fuego del enemigo se apaga al tocar la burbuja,
					#entonces eliminamos ambos objetos
					choque = pygame.sprite.spritecollide(enemy.ataque, self.all_sprites, False)
					if(choque):
						if(choque[0].type!="troll"):
							enemy.ataque.existe=False
							enemy.ataque.kill()

					for brubuja in self.pingu.ataqueP:
						golpeB = pygame.sprite.collide_rect(enemy.ataque, burbuja)
						if golpeB:
							enemy.ataque.existe=False
							enemy.ataque.kill()
							burbuja.existe=False
							burbuja.kill()



				
		#Colision de jugador con bloques en el suelo		
	
		#print(self.pingu.v)			
		hits = pygame.sprite.spritecollide(self.pingu, self.all_sprites, False)
		#print(hits)
		wallR = False
		wallL = False
		#print("pingu state", self.pingu.state)
		if hits and self.pingu.rect.top>0:
			#print("tocando algo")			   				
			
			#	print("pingu rect", self.pingu.rect)
			#	print("pingu top", self.pingu.rect.top)
		#		print("pingu bottom", self.pingu.rect.bottom)
			#	print("pingu centery", self.pingu.rect.centery)
			#	print("h rect", h.rect)
		#		print("h top", h.rect.top)
			#	print("h bottom", h.rect.bottom)
			for h in hits:


				if(self.pingu.rect.centery<h.rect.bottom and self.pingu.rect.centery>h.rect.top and self.pingu.rect.centerx>= h.rect.left and h.type!="decor" and h.type!="meta" and h.type!="comida" and h.type!="dorado" and h.type!="checkpoint"):

		#			print("Tocando pared por la izquierda")
					wallL=True
				if(h.type=="meta"):
						#self.pingu.piso=h.rect.top-0.3*configPenguin.hbloque 
						self.pingu.puntos+=int(10*self.limTmp)					
						self.op = 0
						self.end = 2

				#Golpeado por un enemigo
				if(isinstance(h, monster.monster)):					
					if(self.pingu.state!="quemado"):
						if(self.pingu.state!="golpeado"):
							self.pingu.Golpeado()
							#print(h)

							#print("golpeando enemigo")
							#print("Estado: ", self.pingu.state)
							self.pingu.vidas-=1	
							if(self.pingu.inAir):
								if(self.pingu.rect.centery>=h.rect.centery):
								#self.pingu.salto()
									h.contMov = 0
									h.cara = not(h.cara)
									#self.pingu.rect.centery+=20
									self.pingu.inAir=False
									self.pingu.v = 21
								else:
									h.contMov = 0
									h.cara = not(h.cara)
									self.pingu.rect.centery-=20
									self.pingu.v = 21
									#self.pingu.state="Bloqueado_Ar"
							else:
								if(self.pingu.rect.centerx < h.rect.centerx):
									self.pingu.rect.centerx-=12
								else:
									self.pingu.rect.centerx+=12

									#self.pingu.salto()

						#if(self.pingu.rect.centerx<h.rect.centerx) and self.pingu.state=="cayendo":
						#	self.pingu.rect.centerx-=configPenguin.wbloque	
						#elif self.pingu.state=="cayendo":
						#	self.pingu.rect.centerx+=configPenguin.wbloque	

							#self.pingu.rect.centery-=configPenguin.hbloque	
						
				if(h.type=="dorado" or h.type=="bonus" or h.type=="comida"):
					if(h.type=="dorado") and not(h.Num in self.pingu.Dorados):
						self.pingu.Dorados.append(h.Num)
					if(h.type=="bonus"):
						self.pingu.pinkPingu=True
					self.pingu.puntos+= h.points
					self.sumaP+=h.points
					p_jug, p_jug_rect = texto(str(h.points), self.pingu.rect.x,self.pingu.rect.top+100)
					self.director.screen.blit(p_jug, p_jug_rect)
					h.kill()
				
				if(h.type=="checkpoint"):
					h.image = graphics.load_image("spritesP/checkpoint2.gif")
					self.pingu.partida['inicio']='checkpoint'

					


				#else:
				#	print("Ya no hay pared por la izquierda")
				#	self.pingu.paredI=False

				#Caso 4- El jugador está a la izquierda y el bloque funciona como pared
				for h in hits:
					#el jugador es aplastado por una plataforma				

					if(self.pingu.rect.centery<h.rect.bottom and self.pingu.rect.centery>h.rect.top and self.pingu.rect.centerx<=h.rect.right and h.type!="decor" and h.type!="meta" and h.type!="comida" and h.type!="dorado" and h.type!="checkpoint"):
			#			print("Tocando pared por la derecha")
						wallR=True
					if(h.type=="meta"):
						#self.pingu.piso=h.rect.top-0.3*configPenguin.hbloque 
						self.pingu.puntos+=int(10*self.limTmp)					
						self.op = 0
						self.end = 2
				#else:
				#	print("Ya no hay pared por la derecha")
				#	self.pingu.paredD=False
				self.pingu.paredI = wallL
				self.pingu.paredD = wallR

				#Leve rebote con la pared
				if wallL:
					self.pingu.rect.centerx+=8
					self.pingu.posicion+= 8/(configPenguin.wbloque)
				if wallR:
					self.pingu.rect.centerx-=8
					self.pingu.posicion-= 8/(configPenguin.wbloque)

			
				#Caso 1 el bloque está abajo y funciona como piso
				if(self.pingu.rect.centery<=h.rect.top) :										

#					print("caso 1 ")	
					#op=1
					self.pingu.limT=-0.5*configPenguin.hbloque
					#if(h.type!="decor" and h.type!="dorado" and h.type!="bonus" and h.type!="comida" and h.type!="extraL"):
					#	self.pingu.aterriza(h.rect.top)
						#op=0
					#	print("tocando piso")


					if(h.type=='rebota') and self.pingu.state!='quemado' and self.pingu.state!="golpeado":
				#		print("Tocando el bloque de rebota")
						if(not h.activado):
							#print("No, no esta activado")
							#self.pingu.piso=h.rect.top-0.3*configPenguin.hbloque 
							#print(self.pingu.state)
							#print("inAir", self.pingu.inAir)
							#if(self.pingu.rect.centery< h.rect.right-5 and self.pingu.rect.centery> h.rect.left+5): 
							self.pingu.salto()
							self.pingu.rect.centery-=22
							if(self.pingu.inAir):
								self.bounceT = self.pingu.time
								h.activado = True
				#		else:
				#			print("activadooo")																					
												
					#El pinguino está en una plataforma movil
					if(h.type=="movil"):
						self.fact_plat = h.factMov
						self.on_plat = True 

					#Moviendo al pinguino con el piso movil			
					if(h.type=="movil") and h.dir:						
						#if not(h.dir):
						#	if(h.cara):
						#		self.pingu.rect.centerx+=h.factMov
						
						#	else:
						#		self.pingu.rect.centerx-=h.factMov
						#if h.dir:

						if (h.cara):
							self.pingu.state = "cayendo"
							self.pingu.inAir = False
							self.pingu.aterriza(h.rect.top, h.rect.x,h.rect.y)

						else:
							if(self.pingu.state != "golpeado"):
								self.pingu.state = "levantado"
							self.pingu.rect.centery -= h.factMov
							self.pingu.altura -= h.factMov
							self.pingu.aterriza(h.rect.top, h.rect.x,h.rect.y)


					
								#self.piso = h.rect.top-0.3*configPenguin.hbloque 


					#Llega a la meta :D			
					if(h.type=="meta"):
						#self.pingu.piso=h.rect.top-0.3*configPenguin.hbloque 
						self.pingu.puntos+=int(10*self.limTmp)					
						self.op = 0
						self.end = 2			

					#Toco una vida extra
					if(h.type=="extraL"):
						self.pingu.vidas+=1
						h.kill()
		
				

				#Caso 2- El jugador está abajo y el bloque funciona como techo
				elif(self.pingu.rect.top <=h.rect.bottom) and (self.pingu.rect.centery>h.rect.top) and self.pingu.inAir:
				#	print("caso 2 ")

					#Golpeado por un enemigo
					#if(h.type=="enemy" and self.pingu.state!="quemado"):
					#	self.pingu.vidas-=1
					#	self.pingu.Quemado()								

					if(h.type!="dorado" and h.type!="bonus" and h.type!="comida" and h.type!="decor" and h.type!="extraL" and h.type!="checkpoint" and not(isinstance(h, monster.monster)) and self.pingu.state!="Bloqueado_Ar") and self.pingu.state!="golpeado":
						self.pingu.limT = h.rect.bottom
						self.pingu.state = "Bloqueado_Ar"
						self.pingu.timeI = self.pingu.time
						self.pingu.rect.centery+= configPenguin.hbloque*0.2
						#self.pingu.rect.posicion+= 12/(configPenguin.wbloque)
						#print("Aqui esta el piso??")

				#	print("limT ", self.pingu.limT)
				#	print("pingu.top", self.pingu.rect.top)

					if(h.type=='fuego') and self.pingu.state!='quemado' and self.pingu.state!="golpeado" and self.pingu.state!='Bloqueado_Ar':
						#self.pingu.piso=h.rect.top-0.3*configPenguin.hbloque 
						if(self.pingu.rect.centerx> h.rect.x-38 and self.pingu.rect.centerx> h.rect.x-38):
							#self.pingu.salto()
							if(self.pingu.vidas>=0):
								self.pingu.vidas-=1
								self.pingu.Quemado()

					#Llega a la meta :D			
					if(h.type=="meta"):
						#self.pingu.piso=h.rect.top-0.3*configPenguin.hbloque 
						self.pingu.puntos+=int(10*self.limTmp)					
						self.op = 0
						self.end = 2

					#Toco una vida extra
					if(h.type=="extraL"):
						self.pingu.vidas+=1
						h.kill()
				
				#Caso 2_2- El jugador está abajo y el bloque funciona como techo pero esta atorado
				elif (self.pingu.rect.centery>h.rect.top) and (self.pingu.rect.top<=h.rect.bottom):	
					if(h.type!="dorado" and h.type!="bonus" and h.type!="comida" and h.type!="decor" and h.type!="extraL" and h.type!="checkpoint" and not(isinstance(h, monster.monster)) and self.pingu.state!="Bloqueado_Ar") and self.pingu.state!="golpeado":
						self.pingu.limT = h.rect.bottom
						self.pingu.state = "Bloqueado_Ar"
						self.pingu.timeI = self.pingu.time
						self.pingu.rect.centery+= configPenguin.hbloque*0.2		
			
			#Caso 3- El jugador está a la derecha y el bloque funciona como pared		
			

			#El jugador sera movido por una pared
			for h in hits:
				if(h.type=="movil" and not h.dir):				
					if(h.cara and not(self.pingu.paredD)):
						self.pingu.rect.centerx+=h.factMov
						self.pingu.posicion += int(h.factMov)/(configPenguin.wbloque)
					if not h.cara and not(self.pingu.paredI):
						self.pingu.rect.centerx-=h.factMov
						self.pingu.posicion -= int(h.factMov)/(configPenguin.wbloque)
				#El jugador es aplastado
				if(not wallR) and (not wallL) and not(h.type=="dorado" or h.type=="bonus" or h.type=="comida" or h.type=="meta" or h.type=="checkpoint"):		
					if not(self.pingu.inAir) and h.rect.top<self.pingu.rect.top and h.rect.bottom>self.pingu.rect.top and self.pingu.state!="golpeado" and self.pingu.state!="quemado" and not self.pingu.Fell:
						if(self.pingu.rect.right>(h.rect.left+25)) or (self.pingu.rect.left<h.rect.right-25	) : 
						
							#print("APLASTADOOO")
							#print("h", h)
							self.pingu.vidas-=1
							self.pingu.Golpeado()

		else:
			if(self.pingu.state!="saltando" and self.pingu.state!="Bloqueado_Ar" and self.pingu.state!="golpeado" and self.pingu.state!="quemado"):
				self.pingu.state="cayendo"
				self.pingu.Fell = True
				#self.pingu.cae()
				#print("NO ESTA TOCANDO NADA")

		#Activando las plataformas moviles
		for plat in (self.all_sprites):
			if(plat.type=="movil"):
				#Moviendo la plataforma de arriba a abajo
				if plat.dir:
			#		print("contador",plat.contMov)
			#		print("movLimite", plat.movSpace)
					#Bajando			
					if plat.cara:		
			#			print("bajando")
						plat.rect.centery+=plat.factMov
						plat.contMov+=0.01
						if(plat.contMov>=plat.movSpace):
							plat.cara=not(plat.cara)
							plat.contMov=0
					#subiendo
					else:			
			#			print("subiendo")

						plat.rect.centery-=plat.factMov
						plat.contMov+=0.01
						if(plat.contMov>=plat.movSpace):
							plat.cara=not(plat.cara)
							plat.contMov=0						
		
				
				#Moviendo la plataforma de izquierda a derecha	
				else: 
				#	print("contador",plat.contMov)
			#		print("movLimite", plat.movSpace)
					#Bajando			
					if plat.cara:		
			#			print("bajando")			
						plat.rect.centerx+=plat.factMov
						plat.contMov+=0.01
						if(plat.contMov>=plat.movSpace):
							plat.cara=not(plat.cara)
							plat.contMov=0
					#subiendo
					else:			
			#			print("subiendo")			
						plat.rect.centerx-=plat.factMov
						plat.contMov+=0.01
						if(plat.contMov>=plat.movSpace):
							plat.cara=not(plat.cara)
							plat.contMov=0

		

		#Habra que mover la pantalla a la derecha		
		if(self.pingu.rect.right >= configPenguin.width*0.55 and self.Borde <= self.limMax-0.5):
			if(self.on_plat):
				self.muevePantalla(self.fact_plat, False, True)
			else:
				self.muevePantalla(int(self.pingu.speed*self.pingu.factMov), False, True)
		
		#Habra que mover la pantalla a la izquierda	
		if(self.Borde>(configPenguin.width/configPenguin.wbloque)and self.pingu.rect.left <= configPenguin.width*0.45 and self.pingu.posicion >5.6):
			if(self.on_plat):
				self.muevePantalla(self.fact_plat, False, False)
			else:				
				self.muevePantalla(int(self.pingu.speed*self.pingu.factMov), False, False)
		
		#Habra que mover la pantalla hacia arriba
		if(self.pingu.rect.top <= configPenguin.height*0.15):
			if(self.on_plat):
				self.muevePantalla(self.fact_plat, True, True)
			else:				
				self.muevePantalla(int(self.pingu.speed*self.pingu.factMov), True, True)
			
		#Habra que mover la pantalla hacia abajo
		if(self.pingu.rect.bottom > 0.9*configPenguin.height) and (self.pingu.altura < self.pingu.limInf-2.5*configPenguin.hbloque): 
			#print(self.pingu.altura," <= ", self.pingu.limInf-4*configPenguin.hbloque)
		
			#print(self.Cima," > ", (configPenguin.height/configPenguin.hbloque)-1)
			if(self.on_plat):
				self.muevePantalla(self.fact_plat, True, False)
			else:				
				self.muevePantalla(int(self.pingu.speed*self.pingu.factMov), True, False)
			
		#Colisiones entre enemigos y el entorno
		for enemy in self.Map.enemies:
			enem_hits = pygame.sprite.spritecollide(enemy, self.all_sprites, False)
			#if (enemy.type=="vertical"):
			#	print(enem_hits)
			if (enem_hits):				
				for en_h in enem_hits:

					#los enemigos evitan la lava
					if(en_h.type=="fuego" and enemy.rect.centerx<en_h.rect.centerx) and enemy.type!="vertical":
						enemy.cara = not enemy.cara
						enemy.contMov = 0
						enemy.rect.centerx -= configPenguin.wbloque*0.5
						#print("Tocando lavaaa")
					
					elif(en_h.type=="fuego" and enemy.rect.centerx>en_h.rect.centerx)and enemy.type!="vertical":
						enemy.cara = not enemy.cara
						enemy.contMov = 0
						enemy.rect.centerx += configPenguin.wbloque*0.5
						#print("Tocando lavaaa")

					#Los enemigos verticales chocan con los pisos o techos
					if(en_h.type!="comida" and en_h.type!="bonus" and en_h.type!="dorado" and en_h.type!= "extraL" and en_h.type!="checkpoint") and (en_h.rect.top> enemy.rect.centery) and enemy.type=="vertical":
						if(enemy.state!="girando") and not isinstance(en_h, monster.monster):
							enemy.cara = not(enemy.cara)
							enemy.contMov = 0
							enemy.rect.centery-= configPenguin.wbloque*0.3
							enemy.state="girando"
							enemy.timeG=self.pingu.time
						######print(en_h.type)
					#	print("Tocando piso")

					if(en_h.type!="comida" and en_h.type!="bonus" and en_h.type!="dorado" and en_h.type!= "extraL" and en_h.type!="checkpoint") and (en_h.rect.bottom< enemy.rect.centery) and enemy.type=="vertical":
						if(enemy.state!="girando") and not isinstance(en_h, monster.monster):
							enemy.cara = not(enemy.cara)
							enemy.contMov = 0
							enemy.rect.centery+= configPenguin.wbloque*0.3
							enemy.state="girando"
							enemy.timeG=self.pingu.time
					#	print("Tocando techo")

					#Los enemigos horizontales chocan con las paredes
					if(en_h.type=="piso" or en_h.type=="movil" ) and en_h.rect.centery< enemy.rect.bottom and en_h.rect.centerx>enemy.rect.centerx:
						if(enemy.type!="vertical"):
							if(en_h.type=="piso"):
								enemy.cara = not enemy.cara
								enemy.contMov = 0
						
							enemy.rect.centerx-= configPenguin.wbloque*0.25

						#else:
						#	enemy.rect.centery-=12
						

						#print("chocando con pared a la derecha")

					if(en_h.type=="piso" or en_h.type=="movil") and en_h.rect.centery< enemy.rect.bottom and en_h.rect.centerx<enemy.rect.centerx:
						if(enemy.type!="vertical"):							
							if en_h.type=="piso": 
								enemy.cara = not enemy.cara
								enemy.contMov = 0#enemy.movSpace
							enemy.rect.centerx+= configPenguin.wbloque*0.25							
							
					
					#Los enemigos horizontales chocan entre sí

					'''if(isinstance(en_h,monster.monster))  and en_h.rect.centerx<enemy.rect.centerx:						
						enemy.cara = not enemy.cara
						en_h.cara = not enemy.cara
						enemy.contMov = 0
						en_h.contMov = 0					
						enemy.rect.centerx+= configPenguin.wbloque*0.2
						en_h.rect.centerx-= configPenguin.wbloque*0.2

					if(isinstance(en_h,monster.monster))  and en_h.rect.centerx>enemy.rect.centerx:						
						enemy.cara = not enemy.cara
						en_h.cara = not enemy.cara
						enemy.contMov = 0
						en_h.contMov = 0					
						enemy.rect.centerx-= configPenguin.wbloque*0.2			
						en_h.rect.centerx+= configPenguin.wbloque*0.2'''

							
	def on_event(self):
		pygame.init()
		keys = pygame.key.get_pressed()

		if (keys[pygame.K_UP]) and (self.pingu.state!='quemado') and (self.pingu.state!="Bloqueado_Ar") and (self.pingu.state!="golpeado") and not self.pingu.Fell:
			self.pingu.salto()
		#	print("forzando saltando")
		
		if(keys[pygame.K_RIGHT]):
			self.pingu.camina(2)
		
		if(keys[pygame.K_LEFT]):
			self.pingu.camina(1)	

		if(keys[pygame.K_SPACE]):
			self.pingu.atackP()


	def on_draw(self, screen):
		screen.blit(self.back, (0,0))
					
		self.all_sprites.draw(screen)
		self.Map.Start.draw(screen)	

		t_jug, t_jug_rect = texto("Tiempo  "+str(int(self.limTmp)), configPenguin.width/9*4,40)
		screen.blit(t_jug, t_jug_rect)

		for parts in self.labels:
			screen.blit(parts[0],parts[1])

		#for enemy in self.Map.enemies:
		#	enemy.draw(screen)
		for burbuja in self.pingu.ataqueP:
			if(burbuja.existe):
				burbuja.draw(screen)

		for enemy in self.Map.enemies:
			if(enemy.type=="troll"):
				if(enemy.ataque.existe):
					enemy.ataque.draw(screen)

		for v in self.Map.decor:
			v.draw(screen)						

		self.pingu.draw(screen)		


#def main():
#	pass

#if __name__== "__main__":
#	main()
