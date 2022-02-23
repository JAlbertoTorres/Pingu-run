import pygame, sys, random
from pygame.locals import *
import configPenguin
from pathlib import Path
import os
import numpy as np
#import enemies
import graphics
import json
import copy
import troll
import oso
import aguila

class FirePlat(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)        
        self.image = graphics.load_image("spritesP/lil_lava.gif")
        self.type = "fuego"
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class simpleFirePlat(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)        
        self.image = graphics.load_image("spritesP/lil_lavaS.gif")
        self.type = "fuego"
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class BouncePlat(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.id = "b_"+str(x)+str(y)
        self.image = graphics.load_image("spritesP/bounce2.gif")
        self.rect = self.image.get_rect()
        self.type = "rebota"
        self.rect.x = x-15
        self.rect.y = y-0.2*configPenguin.hbloque
        self.activado = False


class IcePlat(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = graphics.load_image("spritesP/lil_ice.gif")
        self.rect = self.image.get_rect()
        self.type = "piso"
        self.rect.x = x
        self.rect.y = y

class simpleIce(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = graphics.load_image("spritesP/ice2.gif")
        self.rect = self.image.get_rect()
        self.type = "piso"
        self.rect.x = x
        self.rect.y = y

class RockPlat(pygame.sprite.Sprite):
    def __init__(self,x,y,mov, direction,cara=True):
        pygame.sprite.Sprite.__init__(self)
        self.image = graphics.load_image("spritesP/roca.gif")
        self.rect = self.image.get_rect()
        self.type = "movil"
        self.dir = direction #El True significa que la plataforma va de arriba a abajo, y el false de izquierda a derecha     
        self.cara = cara #Movimiento inicial, si dir==True, ira hacia abajo, sino, ira hacia la derecha
        self.movSpace = mov #Cuantos bloques se moverá
        self.factMov = 3
        self.contMov = 0
        self.rect.x = float(x)
        self.rect.y = float(y)

class StartPoint(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = graphics.load_image("spritesP/lil_Start.gif")
        self.rect = self.image.get_rect()
        self.type = "decor"
        self.rect.x = x
        self.rect.y = y-configPenguin.hbloque*0.35

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Goal(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = graphics.load_image("spritesP/goal.gif")
        self.rect = self.image.get_rect()
        self.type = "meta"
        self.rect.x = x
        self.rect.y = y-configPenguin.hbloque*0.35

class redFish(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = graphics.load_image("spritesP/pezR.gif")
        self.rect = self.image.get_rect()
        self.type = "comida"
        self.points = 50
        self.rect.x = x
        self.rect.y = y#+35

class blueFish(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = graphics.load_image("spritesP/pezA.gif")
        self.rect = self.image.get_rect()
        self.type = "comida"
        self.points = 10
        self.rect.x = x
        self.rect.y = y#+35

class pinkSquid(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = graphics.load_image("spritesP/calamarP.gif")
        self.rect = self.image.get_rect()
        self.type = "comida"
        self.points = 30
        self.rect.x = x
        self.rect.y = y#+20

class whiteSquid(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = graphics.load_image("spritesP/calamarB.gif")
        self.rect = self.image.get_rect()
        self.type = "comida"
        self.points = 15
        self.rect.x = x
        self.rect.y = y#+20

class goldenFish(pygame.sprite.Sprite):
    def __init__(self,x,y,label):
        pygame.sprite.Sprite.__init__(self)
        self.image = graphics.load_image("spritesP/GoldFish.gif")
        self.rect = self.image.get_rect()
        self.type = "dorado"
        self.points = 100
        self.Num = label
        self.rect.x = x
        self.rect.y = y#+10  

class PinkPingu(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = graphics.load_image("spritesP/pinguRosa2.gif")
        self.rect = self.image.get_rect()
        self.type = "bonus"
        self.points = 200
        self.saluda = False
        self.T = 0
        self.rect.x = x
        self.rect.y = y-configPenguin.hbloque*0.3

class lifeBlock(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = graphics.load_image("spritesP/lil_xtra.gif")
        self.rect = self.image.get_rect()
        self.type = "extraL"    
        self.rect.x = x
        self.rect.y = y

class checkpoint(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = graphics.load_image("spritesP/checkpoint1.gif")
        self.rect = self.image.get_rect()
        self.type = "checkpoint"    
        self.rect.x = x
        self.rect.y = y


class ClockBlock(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = graphics.load_image("spritesP/time.gif")
        self.rect = self.image.get_rect()
        self.type = "decor"    
        self.rect.x = x
        self.rect.y = y

class voidBlock(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = graphics.load_image("spritesP/void.gif")
        self.rect = self.image.get_rect()
        self.type = "decor"    
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Mapa():
    def __init__(self, archivo, info):
        #pygame.sprite.Group.__init__(self)
         
        self.fuego = []                
        self.rebota = []         
        self.hielo = []
        self.roca = []
        self.Start = None
        self.Goal = None
        self.pinkP = None
        self.xtraL = None
        self.chk_pnt = None
        self.decor = []
        self.Golds = []
        self.comida = []
        self.enemies = []        
        #self.plats = pygame.sprite.Group()
        self.widthB = configPenguin.wbloque
        self.heightB = configPenguin.hbloque
        self.name = archivo 
        self.mapa = leerMapa(archivo)
        self.evals = leerMapaJSON(info)
        self.fil = len(self.mapa[0])
        self.col = len(self.mapa[0][0])

#        grafName = "evaluado_"+archivo.split("/")[1]
 #       self.grafo = leerMapa(grafName)
        self.labels = {}

         
    def load(self, i):
        
        paso= self.mapa[i]
        if type(paso[0])== np.int64:
            paso = stateToMap(paso,self.fil,self.col)
        contDor=0
        for f in range(self.fil):
            for c in range(self.col):               
                #Bloque de hielo 
                if paso[f][c] == 'i':
                    self.hielo.append(IcePlat((c)*self.widthB, (f)*self.heightB))
                #Bloque de hielo simple
                if paso[f][c] == 'iS':
                   # print("PISOOOO en ", (c)*self.widthB, (f)*self.heightB)
                    self.hielo.append(simpleIce((c)*self.widthB, (f)*self.heightB))                   
                #Bloque de fuego
                if paso[f][c] == 'f': 
                    self.fuego.append(FirePlat((c)*self.widthB, (f)*self.heightB))
                #Bloque de fuego simple
                if paso[f][c] == 'fS': 
                    self.fuego.append(simpleFirePlat((c)*self.widthB, (f)*self.heightB))
                #Bloque de rebote
                if paso[f][c] == 'b':
                    self.rebota.append(BouncePlat((c)*self.widthB, (f)*self.heightB))
                #Bloque de roca movil vertical
                if paso[f][c] == 'rv':
                    self.roca.append(RockPlat(float((c)*self.widthB), float((f)*self.heightB),1, True))
                if paso[f][c] == 'rv1':
                    self.roca.append(RockPlat(float((c)*self.widthB), float((f)*self.heightB),1, True, cara=False))
                #Bloque de roca movil horizontal    
                if paso[f][c] == 'rh':
                    self.roca.append(RockPlat(float((c)*self.widthB), float((f)*self.heightB),1, False))
                if paso[f][c] == 'rh1':
                    self.roca.append(RockPlat(float((c)*self.widthB), float((f)*self.heightB),1, False,cara=False))
                #Bloque de inicio
                if paso[f][c] == 'S':
                    self.Start = StartPoint((c)*self.widthB, (f)*self.heightB)
                #Bloque Checkpoint                    
                if paso[f][c] == 'c':
                    self.chk_pnt = checkpoint((c)*self.widthB, (f)*self.heightB)                    
                #Bloque de fin/meta
                if paso[f][c] == 'G':
                    self.Goal = Goal((c)*self.widthB, (f)*self.heightB)
                #Bloque de pez rojo
                if paso[f][c] == 'rf':
                    self.comida.append(redFish((c)*self.widthB, (f)*self.heightB))
                #Bloque de pez azul
                if paso[f][c] == 'bf':
                    self.comida.append(blueFish((c)*self.widthB, (f)*self.heightB))
                #Bloque de calamar blanco
                if paso[f][c] == 'ws':
                    self.comida.append(whiteSquid((c)*self.widthB, (f)*self.heightB))
                #Bloque de calamar rosa
                if paso[f][c] == 'ps':
                    self.comida.append(pinkSquid((c)*self.widthB, (f)*self.heightB))
                #Bloque de pez dorado
                if paso[f][c] == 'd':
                    self.Golds.append(goldenFish((c)*self.widthB, (f)*self.heightB, contDor))
                    contDor+=1
                #Bloque de pinguino rosa
                if paso[f][c] == 'p':
                    self.pinkP = PinkPingu((c)*self.widthB, (f)*self.heightB)
                #Bloque de vida extra
                if paso[f][c] == 'l':
                    self.xtraL = lifeBlock((c)*self.widthB, (f)*self.heightB)
                #Bloque de enemigo Troll
                if paso[f][c] == 'T':
                    self.enemies.append(troll.troll((c)*self.widthB, (f)*self.heightB-0.65*configPenguin.hbloque))
                #Bloque de enemigo Troll_en direccion inversa
                if paso[f][c] == 'T1':
                    self.enemies.append(troll.troll((c)*self.widthB, (f)*self.heightB-0.65*configPenguin.hbloque, cara=False))
                #Bloque de enemigo Oso
                if paso[f][c] == 'O1':
                    self.enemies.append(oso.oso((c)*self.widthB, (f)*self.heightB-0.55*configPenguin.hbloque))
                #Bloque de enemigo Oso con direccion inversa
                if paso[f][c] == 'O':
                    self.enemies.append(oso.oso((c)*self.widthB, (f)*self.heightB-0.55*configPenguin.hbloque, cara=False))
                #Bloque de enemigo Aguila
                if paso[f][c] == 'A':
                    self.enemies.append(aguila.aguila((c)*self.widthB-0.5*configPenguin.wbloque, (f)*self.heightB))
                #Bloque de enemigo Aguila con direccion inversa
                if paso[f][c] == 'A1':
                    self.enemies.append(aguila.aguila((c)*self.widthB-0.5*configPenguin.wbloque, (f)*self.heightB, cara=False))
                    #Bloque vacio, se dibuja una cuadricula en pantalla
                  #  if(paso[f][c])=="x":
                   #     self.decor.append(voidBlock((c)*self.widthB, (f)*self.heightB))

            #Cargamos las etiquetas de los bloques
            #for nodo in self.grafo:
             #   self.labels[nodo["id"]]= nodo["p_inicio"]
        #print("Las etiquetas del json son las siguientes:")     
        #for label in self.mapa:
         #   print(label)

def stateToMap(state, filas, columnas):
    mapa = []
    translate ={'0':'x', '1':'i', '2':'f', '3':'b', '4':'rh', '5':'rh1', '6':'rv', '7':'rv1',
                '8':'ws', '9':'ps', '10':'rf', '11':'bf', '12':'d', '13':'p', '14':'l',
                '15':'T', '16':'T1', '17':'O', '18':'O1', '19':'A', '20':'A1',
                '21':'c', '22':'S', '23':'G'}
    
    #print("Translating map to state...")
    fila=0
    #print(state.shape)
    while fila <filas:
        mapa.append([])
        columna=0
        while columna<columnas:
            mapa[-1].append(translate[str(state[fila*filas+columna])])
        #print("adding:", self.map[fila][columna],"->", translate[self.map[fila][columna]])
            columna+=1
        fila+=1

    return mapa

def leerMapaJSON(archivo):
    with open(archivo+".json") as json_data:
        d = json.load(json_data)
        data = json.dumps(d)
        mapa = json.loads(data)
    return mapa

def leerMapa(archivo):
    #print("cargando archivo: \n",archivo)
    p = Path(archivo)
    with p.open('rb') as f:
        fsz = os.fstat(f.fileno()).st_size
        out = np.load(f, allow_pickle=True)
        while f.tell() < fsz:
            out = np.vstack((out, np.load(f,allow_pickle=True)))
    #print()
    return out

#def leerGrafo(archivo):
