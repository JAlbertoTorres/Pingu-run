import pygame
import scene
import configPenguin
import graphics
from load_levels import Mapa
import scene_home
import scene_intro
import load_levels
import sys


black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

block_color = (53,115,255)

def horas(t,s,m,h):
	if(t>=24*60*60):
		h = 24
	else:
		h = int(t/60)
		m = int((t-h*60)/60)
		s = int((t-h*60)%60)

	return s,m,h

def minutos(t, s, m, h):
	if(t<60*60):
		m = int(t/60)
		s = int((t-m*60))
	else:
		s,m,h = horas(t,s,m,h)
	return s,m,h

def segundos(t, s, m, h):
	if(t<60):
		s = t
	else:		
		s,m,h = minutos(t, s, m, h)		
	return s,m,h

def tiempo(tiempo):
	#print("tiempo", tiempo)
	hrs = 0
	mins = 0
	seg = 0
	seg, mins, hrs = segundos(tiempo, seg,mins,hrs)	
	return str(str(format(hrs, '.2f')) +":"+str(format(mins,'.2f'))+":"+str(format(seg, '.2f')))


def texto(texto, posx, posy, color=(255,255,128), tam=45):
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

class SceneResults(scene.Scene):
	"""docstring for SceneHome"""
	def __init__(self, director, pingu, partida):
		scene.Scene.__init__(self,director)
		pygame.init()
		self.all_sprites = pygame.sprite.Group()
		self.screen = pygame.display.set_mode((configPenguin.width, configPenguin.height))
		self.back = graphics.load_image(configPenguin.menus+"backgroundResults.gif")
		self.time = 0
		self.Horas = 0
		self.Mins = 0
		self.Seg = 0
		self.Dir = director
		self.player = pingu
		self.partida = partida
		self.Reloj = load_levels.ClockBlock(1/8*configPenguin.width ,2/9*configPenguin.height)
		self.PinguR = load_levels.PinkPingu(1/8*configPenguin.width ,4/9*configPenguin.height)
		self.Dorado = load_levels.goldenFish(1/8*configPenguin.width ,6/9*configPenguin.height,1)	
		self.all_sprites.add(self.Dorado)
		self.all_sprites.add(self.PinguR)
		self.all_sprites.add(self.Reloj)

		

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
					self.Dir.change_scene(scene_intro.SceneIntro(self.Dir, self.partida))
					self.Dir.clock = pygame.time.Clock()           
					self.Dir.scene.game_intro()              
				
		else:

			boton2 = boton(img2, x, y)			
			botonD = boton2
		
		smallText = pygame.font.SysFont("comicsansms",20)
		#textSurf, textRect = self.text_objects(msg, smallText)
		#textRect.center = ( (x+(w/2)), (y+(h/2)) )
		#self.screen.blit(textSurf, textRect)
		self.screen.blit(botonD.image, botonD.rect)

	def results(self):
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
			#Reporte de tiempo
			if(self.player.goal):
				if(self.player.pinkPingu):
					t_jug, t_jug_rect = texto(str(str(tiempo(self.player.time))+" = "+str(self.player.puntos-self.PinguR.points -len(self.player.Dorados)*self.Dorado.points)+" puntos"), 1/2*configPenguin.width ,self.Reloj.rect.y+configPenguin.hbloque*0.75, color=black, tam=70)
					self.screen.blit(t_jug, t_jug_rect)
				else:
					t_jug, t_jug_rect = texto(str(str(tiempo(self.player.time))+" = "+str(self.player.puntos-len(self.player.Dorados)*self.Dorado.points)+" puntos"), 1/2*configPenguin.width ,self.Reloj.rect.y+configPenguin.hbloque*0.75, color=black, tam=70)
					self.screen.blit(t_jug, t_jug_rect)
			else:
				t_jug, t_jug_rect = texto("0 puntos", 1/2*configPenguin.width ,self.Reloj.rect.y+configPenguin.hbloque*0.75, color=black, tam=70)
				self.screen.blit(t_jug, t_jug_rect)
			if(self.player.pinkPingu):
				pp_jug, pp_jug_rect = texto("Encontrada :D = "+str(self.PinguR.points)+" puntos", 1/2*configPenguin.width ,self.PinguR.rect.y+configPenguin.hbloque*0.75, color=black, tam=70)
				self.screen.blit(pp_jug, pp_jug_rect)
			else:
				pp_jug, pp_jug_rect = texto("No encontrada :( = 0 puntos", 1/2*configPenguin.width ,self.PinguR.rect.y+configPenguin.hbloque*0.75, color=black, tam=70)
				self.screen.blit(pp_jug, pp_jug_rect)
			g_jug, g_jug_rect = texto(str(str(len(self.player.Dorados))+"/"+str(self.player.TotalD))+"="+str(len(self.player.Dorados)*self.Dorado.points)+" puntos", 1/2*configPenguin.width ,self.Dorado.rect.y+configPenguin.hbloque*0.75, color=black, tam=70)
			self.screen.blit(g_jug, g_jug_rect)
			

			self.button("spritesP/continue2.gif","spritesP/continue.gif",8/9*configPenguin.width, 10/12*configPenguin.height,self.Dir.loop)
			pygame.display.update()
			

	def on_update(self):
		self.time =self.Dir.time


	def on_event(self):
		keys = pygame.key.get_pressed()


	def on_draw(self, screen):
		screen.blit(self.back, (0,0))				
		self.all_sprites.draw(screen)
			


#def main():
#	pass

#if __name__== "__main__":
#	main()
