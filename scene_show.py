import pygame
import scene
import configPenguin
import graphics
import scene_intro
import scene_results
import scene_levels
from load_process import Mapa
import sys
import json
from pickle import dump, dumps, load, loads
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,200,0)

def error(objetivo, medido):
	return float((objetivo-medido)**2)

def texto(texto, posx, posy, color=(171,13,78), tam=40):
	fuente = pygame.font.Font("images/DroidSans.ttf",tam)
	salida = pygame.font.Font.render(fuente,texto,1, color)
	salida_rect=salida.get_rect()
	salida_rect.centerx = posx
	salida_rect.centery = posy
	return salida, salida_rect

class SceneShow(scene.Scene):
	"""docstring for SceneHome"""
	def __init__(self, director, level, info):
		scene.Scene.__init__(self,director)
		print("Mostrando proceso...\n\n")
		#pygame.mixer.music.load('/home/beto/Música/Musica/Vampire Killer.mp3')
		#pygame.mixer.music.play(-1)
		self.screen = pygame.display.set_mode((configPenguin.width, configPenguin.height))
		self.Dir = director
		self.level = level
		self.info = info
		self.all_sprites = pygame.sprite.Group()
		self.back = graphics.load_image(configPenguin.menus+"fondo1.png")
		#self.all_sprites.add(self.pingu)
		self.Map = Mapa(level, info)
		self.Map.load(0)
		self.counter=0
		self.finished= False
		self.textSurf, self.textRect = texto("Proceso de creacion de nivel terminado...", configPenguin.width/2,configPenguin.height/4, color=(255,255,255), tam=50 )
		self.textosEval=[]
		#print("filas:", self.Map.fil)
		#print("columnass:", self.Map.col)
		#print("Etiquetas de bloques", self.Map.labels)		
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
		if self.Map.chk_pnt !=None:	
			self.all_sprites.add(self.Map.chk_pnt)



	def on_update(self):
		#print("Numero de pasos totales:", len(self.Map.mapa))
		#print("paso:", self.counter)
		
		if not self.finished:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_INSERT] or keys[pygame.K_a] or keys[pygame.K_RIGHT]:
				self.textosEval = []
				self.all_sprites = pygame.sprite.Group()
				self.Map = Mapa(self.level,self.info)
				self.time = self.Dir.time
				self.Map.load(self.counter)
				#print("Evaluacion")
				#print(self.Map.evals[str(self.counter)])
				#print("Objetivos")
				txtSurf, txtRect = texto("Accion numero:"+str(self.counter), 
						configPenguin.width*(20/35), -(40)+configPenguin.height*(27/35), color=(255,255,255), tam=28)
				self.textosEval.append([txtSurf,txtRect])
				txtSurf, txtRect = texto("Accion elegida:"+str(self.Map.evals[str(self.counter)]["accion"]), 
						configPenguin.width*(26/35), -(40)+configPenguin.height*(27/35), color=(255,255,255), tam=28)
				self.textosEval.append([txtSurf,txtRect])
				objs=self.Map.evals["objetivo"]
				num=0
				for c in objs:
					cadena = str(c)
					#cadena+=":  error_ritmo = "+str(error(objs[str(c)]["ritmo"],self.Map.evals[str(self.counter)][c]["nFlucts"]))
					#cadena+=":  error_limInf = "+str(error(objs[str(c)]["limInf"],self.Map.evals[str(self.counter)][c]["minVal"]))
					#cadena+=":  error_limSup = "+str(error(objs[str(c)]["limSup"],self.Map.evals[str(self.counter)][c]["maxVal"]))
					cadena+=":  recompensa = "+str(self.Map.evals[str(self.counter)][c]["reward"])
					
					txtSurf, txtRect = texto( cadena, 
						configPenguin.width*(28/35), 40*num+configPenguin.height*(27/35), color=(255,255,255), tam=28 )
					self.textosEval.append([txtSurf,txtRect])
					num+=1
				txtSurf, txtRect = texto("Recompensa total: "+str(self.Map.evals[str(self.counter)]["Total"]), 
						configPenguin.width*(28/35), 40*num+configPenguin.height*(27/35), color=(255,255,255), tam=28 )
				self.textosEval.append([txtSurf,txtRect])
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
				if self.Map.chk_pnt !=None:	
					self.all_sprites.add(self.Map.chk_pnt)	
				#print("tiempo", self.time)
				self.counter+=1
				if self.counter>= len(self.Map.mapa):
					self.finished = True
					print("Proceso de creacion de nivel terminado...")
		else:		
			
			keys = pygame.key.get_pressed()
			for eventos in pygame.event.get():
				if eventos.type == pygame.QUIT:
					sys.exit(0)
			if keys[pygame.K_INSERT] or keys[pygame.K_a]:					
				self.Dir.change_scene(scene_levels.SceneLevels(self.Dir))
			

	def on_event(self):
		keys = pygame.key.get_pressed()

	def on_draw(self, screen):
		screen.blit(self.back, (0,0))
		self.all_sprites.draw(screen)
		self.Map.Start.draw(screen)	
		for par in self.textosEval:
			screen.blit(par[0], par[1])

		for parts in self.labels:
			screen.blit(parts[0],parts[1])

		for v in self.Map.decor:
			v.draw(screen)								

		if self.finished:
			#print("Insertando texto...")
			screen.blit(self.textSurf, self.textRect)
			for par in self.textosEval:
				screen.blit(par[0], par[1])

