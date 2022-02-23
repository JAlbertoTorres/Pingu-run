import pygame
import scene
import configPenguin
import graphics
from load_levels import Mapa
from load_levels import leerMapa
from sp_penguin import pingu
import scene_show
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

class SceneLevels(scene.Scene):
	"""docstring for SceneHome"""
	def __init__(self, director):
		scene.Scene.__init__(self,director)
		self.screen = pygame.display.set_mode((configPenguin.width, configPenguin.height))
		self.back = graphics.load_image(configPenguin.menus+"fondo2.png")
		#self.all_sprites.add(self.pingu)
		self.time = 0
		self.Dir= director
		self.clock  = pygame.time.Clock()
		self.level_selection()
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


	def button(self, img1, img2,x,y, msg=None, msg2=None, action=None):
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
					self.Dir.change_scene(scene_show.SceneShow(self.Dir,configPenguin.procesos+msg,configPenguin.procesos+msg2 ))
					self.Dir.clock = pygame.time.Clock() 
				else:
					action()               
				        
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
		pygame.init()
		while True:
			#print("desbloqueados", self.desbloqueados)
			#print("Mostrando niveles")
			levels = self.find('*.npy', configPenguin.procesos)
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
				name = str(level).replace(".npy", "")
				info = str(level).replace(".npy", "")				
				partes = info.split('n')
				
				name = partes[1]
				info= partes[0]+'nINFO'
				for p in partes[1:]:
					info+=p
				
				nombres.append(name)
				botones.append(self.button("spritesP/botonNiveles2.gif","spritesP/botonNiveles.gif",configPenguin.width/6*(i), configPenguin.height/4*(j), str(level), str(info),self.Dir.loop))				
				i+=1
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
			returnF = self.button("spritesP/quit2.gif", "spritesP/quit.gif",8/9*configPenguin.width, 10/12*configPenguin.height,action=self.Dir.quit)		
			self.screen.blit(returnF.image, returnF.rect)
		#pygame.display.update()
	

		
	def on_update(self):
		self.time =self.Dir.time

	def on_event(self):
		pygame.init()
		keys = pygame.key.get_pressed()

	def on_draw(self, screen):
		#self.level_selection()
		screen.blit(self.back, (0,0))				



#def main():
#	pass

#if __name__== "__main__":
#	main()
