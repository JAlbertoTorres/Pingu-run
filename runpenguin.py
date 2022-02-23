"""runpenguin.py"""
import pygame
import director
import scene_home
import scene_intro
import scene_registro
import scene_carga

def main():
	dir = director.Director()
	sceneI = scene_carga.SceneCarga(dir)
	dir.change_scene(sceneI)
	sceneI.game_load()
	#dir.loop()

if __name__=='__main__':
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	main()
#	pygame.init()
