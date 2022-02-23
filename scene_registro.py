import pygame
import scene
import configPenguin
import graphics
import scene_select
import sys
import os, fnmatch
import pygame_textinput
import scene_carga
import json
from pickle import dump, dumps, load, loads

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

block_color = (53,115,255)

class boton(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = graphics.load_image(img)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y

def texto(texto, posx, posy, color=(255,255,255), tam=40):
	fuente = pygame.font.Font("images/DroidSans.ttf",tam)
	salida = pygame.font.Font.render(fuente,texto,1, color)
	salida_rect=salida.get_rect()
	salida_rect.centerx = posx
	salida_rect.centery = posy
	return salida, salida_rect

class SceneRegistro(scene.Scene):
	"""docstring for SceneHome"""
	def __init__(self, director):
		scene.Scene.__init__(self,director)
		pygame.init()
		self.screen = pygame.display.set_mode((configPenguin.width, configPenguin.height))		
		self.back = graphics.load_image(configPenguin.menus+"fondo2.png")		
		#self.all_sprites.add(self.pingu)
		self.time = 0
		self.Dir= director
		self.clock  = pygame.time.Clock()
		#pygame.mixer.music.load('/home/beto/Música/Musica/Soul Calibur III - Ephemeral Dream Setsuka.mp3')
		#pygame.mixer.music.play(-1)

	def text_objects(self,text, font):
		#print("text_objects")
		textSurface = font.render(text, True, black)
		return textSurface, textSurface.get_rect()

	def message_display(self,text):
		largeText = pygame.font.Font('freesansbold.ttf',115)
		TextSurf, TextRect = self.text_objects(text, largeText)
		TextRect.center = ((configPenguin.width/2),(configPenguin.height/2))
		self.screen.blit(TextSurf, TextRect)
		pygame.display.update()
		time.sleep(2)	

	def find(self, pattern, path):
		result = []
		for root, dirs, files in os.walk(path):
			for name in files:
				if fnmatch.fnmatch(name, pattern):
					result.append(name)
		return result

	def button(self, img1, img2,x,y,action=None, msg=""):
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		boton2 = boton(img2, x, y)			
		botonD = boton2		
		l = botonD.rect.left
		t = botonD.rect.top
		w = botonD.rect.right
		h = botonD.rect.bottom
		levels = self.find('*.json', configPenguin.partidas)
		valid = True
		if w > mouse[0] > l and h > mouse[1] > t:
			boton1 = boton(img1, x, y)			
			botonD = boton1
			if click[0] == 1 and action != None:			
				#for action in actions:
				#print("Ejecutando...")
				#print(action)
				if(action==self.Dir.loop):
					#self.Dir.change_scene(scene_home.SceneHome(self.Dir,"levelsP/levelDos.json"))
					self.Dir.change_scene(scene_select.SceneSelect(self.Dir))
					self.director.scene.level_selection()
					#self.Dir.clock = pygame.time.Clock()                
				if(action==2):
					self.Dir.change_scene(scene_carga.SceneCarga(self.Dir))
					self.director.scene.game_load()
				if(action==3):
					#Validacion de nombres de partidas...
					print("Validacion de nombre...", msg)
					for level in levels:
						if(msg==level):
							print("noooo")
							valid= False
							self.game_registro()
					if(valid):
						n= {"vidas":4,"desbloqueados":["levelDemo", "level1"],"inicio":"inicio","juego_anterior": "levelsP/levelDemo.json"}
						for i in range(2):
							f = open(configPenguin.partidas+"/"+msg,"w+")
							data = json.dumps(n)
							f.write(data)
						self.Dir.change_scene(scene_carga.SceneCarga(self.Dir))
						self.director.scene.game_load()		
				else:	
					action()         
				self.Dir.loop()
		else:

			boton2 = boton(img2, x, y)			
			botonD = boton2
		
		smallText = pygame.font.SysFont("comicsansms",20)
		#textSurf, textRect = self.text_objects(msg, smallText)
		#textRect.center = ( (x+(w/2)), (y+(h/2)) )
		#self.screen.blit(textSurf, textRect)
		self.screen.blit(botonD.image, botonD.rect)

	def game_registro(self):
		#sceneH = scene_home.SceneHome(dir)
		#self.Dir.change_scene(sceneH)
		intro = True
		textinput = pygame_textinput.TextInput(text_color=black, font_size=65)
		name = ""
		while intro:
			pygame.display.flip()
			self.on_draw(self.screen)
			#instructionLabel = makeLabel("Usa el teclado para escribir", int(configPenguin.width/6*2), int(configPenguin.height/11*1), 85, "white", "DroidSans")
			#showLabel(instructionLabel)
			t_levels, t_levels_rect = texto("Usa el teclado para escribir el nombre" , configPenguin.width/6*3, configPenguin.height/11*1,tam= 75) 
			t_levels2, t_levels_rect2 = texto("y la tecla enter para terminar" , configPenguin.width/6*2.8, configPenguin.height/11*2,tam= 75) 		
			self.screen.blit(t_levels, t_levels_rect)
			self.screen.blit(t_levels2, t_levels_rect2)
			events = pygame.event.get()
			for event in events:
				#print(event)
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
			
			 # Feed it with events every frame			
			if textinput.update(events):
				name+=str(textinput.get_text())
				print(name)
				print(textinput.get_text())
			
			self.button("spritesP/botonNiveles2.gif","spritesP/botonNiveles.gif",configPenguin.width/6*3, configPenguin.height/11*6, action=3, msg=name+".json")	    
			t_accept, t_accept_rect = texto("Aceptar" , configPenguin.width/6*3, configPenguin.height/11*6,tam= 45, color=black) 		
			self.screen.blit(t_accept, t_accept_rect)
			self.button("spritesP/nuevaPart.gif", "spritesP/nuevaPart.gif",configPenguin.width/6*3, configPenguin.height/11*4.3)
			self.screen.blit(textinput.get_surface(), (configPenguin.width/6*1.8, configPenguin.height/11*4))
								
			self.button("spritesP/returnF2.gif", "spritesP/returnF.gif",8/9*configPenguin.width, 10/12*configPenguin.height,action=2)		
			pygame.display.update()
			self.clock.tick(30)


	def on_update(self):
		self.time =self.Dir.time


	def on_event(self):
		keys = pygame.key.get_pressed()

	def on_draw(self, screen):
		screen.blit(self.back, (0,0))				



#def main():
#	pass

#if __name__== "__main__":
#	main()
