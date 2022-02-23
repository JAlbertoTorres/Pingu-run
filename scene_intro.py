import pygame
import scene
import configPenguin
import graphics
#from load_levels import Mapa
#from sp_penguin import pingu
#import scene_home
import scene_carga
import scene_select
import sys

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

class SceneIntro(scene.Scene):
	"""docstring for SceneHome"""
	def __init__(self, director, partida):
		scene.Scene.__init__(self,director)
		pygame.init()
		self.partida = partida
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

	def button(self, img1, img2,x,y,action=None):
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		boton2 = boton(img2, x, y)			
		botonD = boton2		
		l = botonD.rect.left
		t = botonD.rect.top
		w = botonD.rect.right
		h = botonD.rect.bottom

		if w > mouse[0] > l and h > mouse[1] > t:
			boton1 = boton(img1, x, y)			
			botonD = boton1
			if click[0] == 1 and action != None:			
				#for action in actions:
				#print("Ejecutando...")
				#print(action)
				if(action==self.Dir.loop):
					#self.Dir.change_scene(scene_home.SceneHome(self.Dir,"levelsP/levelDos.json"))
					self.Dir.change_scene(scene_select.SceneSelect(self.Dir, self.partida))
					self.Dir.scene.level_selection()
					#self.Dir.clock = pygame.time.Clock()                
				else:
					self.Dir.change_scene(scene_carga.SceneCarga(self.Dir))
					self.Dir.scene.game_load()
				self.Dir.loop()
		else:

			boton2 = boton(img2, x, y)			
			botonD = boton2
		
		smallText = pygame.font.SysFont("comicsansms",20)
		#textSurf, textRect = self.text_objects(msg, smallText)
		#textRect.center = ( (x+(w/2)), (y+(h/2)) )
		#self.screen.blit(textSurf, textRect)
		self.screen.blit(botonD.image, botonD.rect)

	def game_intro(self):
		#sceneH = scene_home.SceneHome(dir)
		#self.Dir.change_scene(sceneH)
		intro = True
		while intro:
			self.on_draw(self.screen)
			for event in pygame.event.get():
				#print(event)
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
			#self.screen.fill(white)
			largeText = pygame.font.SysFont("comicsansms",115)			

			
			self.button("spritesP/BotonEmpezar2.gif","spritesP/BotonEmpezar.gif",1/2*configPenguin.width, 4/11*configPenguin.height,self.Dir.loop)
			self.button("spritesP/returnF2.gif", "spritesP/returnF.gif",10/11*configPenguin.width, 7.6/9*configPenguin.height,self.Dir.quit)		
			pygame.display.update()
			self.clock.tick(15)


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
