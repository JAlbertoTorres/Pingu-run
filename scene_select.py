import pygame
import scene
import configPenguin
import graphics
from load_levels import Mapa
from load_levels import leerMapa
from sp_penguin import pingu
import scene_home
import scene_intro
import sys
import os, fnmatch

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,200,0)



def texto(texto, posx, posy, color=(255,255,255), tam=40):
	fuente = pygame.font.Font("images/DroidSans.ttf",tam)
	salida = pygame.font.Font.render(fuente,texto,1, color)
	salida_rect=salida.get_rect()
	salida_rect.centerx = posx
	salida_rect.centery = posy
	return salida, salida_rect

class boton(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = graphics.load_image(img)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y

class SceneSelect(scene.Scene):
	"""docstring for SceneHome"""
	def __init__(self, director, partida):
		scene.Scene.__init__(self,director)
		pygame.init()
		self.partida= partida
		self.screen = pygame.display.set_mode((configPenguin.width, configPenguin.height))
		self.back = graphics.load_image(configPenguin.menus+"fondo2.png")
		#self.all_sprites.add(self.pingu)
		self.time = 0
		self.Dir= director
		self.clock  = pygame.time.Clock()
		self.desbloqueados = leerMapa(configPenguin.partidas+partida)["desbloqueados"]		
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


	def button(self, img1, img2,x,y, msg=None, action=None):
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
				if(action==2):
					self.Dir.change_scene(scene_intro.SceneIntro(self.Dir, self.partida))
					self.Dir.clock = pygame.time.Clock()           
					self.Dir.scene.game_intro() 
				if(action==self.Dir.loop):
					self.Dir.change_scene(scene_home.SceneHome(self.Dir,configPenguin.levelsP+msg, self.partida))
					self.Dir.clock = pygame.time.Clock()                
				        
				self.Dir.loop()
		else:

			boton2 = boton(img2, x, y)			
			botonD = boton2
			
		return botonD

	def draw_text(self,image,rect):
		self.screen.blit(image, rect)	

	def find(self, pattern, path):
		result = []
		for root, dirs, files in os.walk(path):
			for name in files:
				if fnmatch.fnmatch(name, pattern):
					result.append(name)
		return result


	def level_selection(self):
		while True:
			#print("desbloqueados", self.desbloqueados)
			levels = self.find('*.json', configPenguin.levelsP)
			pygame.display.flip()
			self.on_draw(self.screen)
			t_levels, t_levels_rect = texto("Selecciona un nivel", configPenguin.width/9*2, configPenguin.height/11*1,tam= 85) 
			self.screen.blit(t_levels, t_levels_rect)
			i=1;j=1
			#print(levels)
			for event in pygame.event.get():
				#print(event)
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
			botones =[]
			nombres=[]
			levels.sort()
			
			for level in levels:
				name = str(level).replace(".json", "")
				name = name.split('_')[-1]
				if 'all' in self.desbloqueados:
					nombres.append(name)	
					botones.append(self.button("spritesP/botonNiveles2.gif","spritesP/botonNiveles.gif",configPenguin.width/6*(i), configPenguin.height/4*(j), str(level),self.Dir.loop))
				else:
					nombres.append(name)
					if(name in self.desbloqueados):
						botones.append(self.button("spritesP/botonNiveles2.gif","spritesP/botonNiveles.gif",configPenguin.width/6*(i), configPenguin.height/4*(j), str(level),self.Dir.loop))
					else:
						botones.append(self.button("spritesP/botonNivelesBloq.gif","spritesP/botonNiveles2.gif",configPenguin.width/6*(i), configPenguin.height/4*(j), str(level)))
				i+=1
			#print(i)
				if(i==5):
					j+=1
					i=1
			i=1;j=1;k=0		
			nombres.sort
			for b in botones:				
				w = b.rect.centerx
				h = b.rect.centery
				self.screen.blit(b.image, b.rect)				
				textSurf, textRect = texto(nombres[k], w, h, white, tam=30)				
				self.draw_text(textSurf,textRect )
				#print(nombres[k])
				i+=1
				#print(i)
				if(i==4):
					j+=1
					i=1
				
				k+=1
			returnF = self.button("spritesP/returnF2.gif", "spritesP/returnF.gif",8/9*configPenguin.width, 10/12*configPenguin.height,action=2)		
			self.screen.blit(returnF.image, returnF.rect)
		#pygame.display.update()
	

		
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
