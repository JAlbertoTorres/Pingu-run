" Configuracion general del proyecto"

# Nombre
name = "Run Penguin" 

# Resolucion
width= 1848
height = 1026

#Tamaño de los bloques (64*64)
#wbloque = int(width/11)
#hbloque = int(height/9)

wbloque = int(width/29)
hbloque = int(height/16)
#print(hbloque)
# Directorios
sprites = "spritesP/"
backs = "backgroundsP/"
menus = "menusP/"
partidas = "partidasP/"
#fonts = fontsP/
music =  "/home/beto/Música/Musica/"
#sounds = soundsP/
levelsP = "levelsFunc/"
#procesos = "bestlevelSimpleV4_2_2070/"
maxValP = 9999 
 #La estructura es {"TipoDeBloque": [[limites de huella i-esima]],[[limites de trayectoria i-esima]]}
limites={"T1":[[[-2, 0, -2, 0]],[[-2, 0, -2, 5]]],  #Troll con movimiento a la derecha
         "A":[[[-1, 0, -2, 0]],[[-1, 9, -2, 0]]],  #Aguila con movimiento hacia abajo 
         "O":[[[-2, 0, -3, 0]],[[-2, 0, -3, 6]]],  #Oso con movimiento hacia la derecha
         "T":[[[-2, 0, -2, 0]],[[-2, 0, -7, 0]]], #Troll con movimiento a la izquierda
         "A1":[[[-1, 0, -2, 0]],[[-10, 0, -2, 0]]], #Aguila con movimiento hacia arriba
         "O1":[[[-2, 0, -3, 0]],[[-2, 0, -9, 0]]], #Oso con movimiento hacia la izquierda
         "rv":[[[0, 0, 0, 1]],[[0, 5, 0, 1]]], #Plataforma movil con movimiento hacia abajo
         "rv1":[[[0, 0, 0, 1]],[[0, -5, 0, 1]]], #Plataforma movil con movimiento hacia arriba
         "rh":[[[0, 0, 0, 1]],[[0, 0, 0, 5]]], #Plataforma movil con movimiento hacia la derecha
         "rh1":[[[0, 0, 0, 1]],[[0, 0, -5, 1]]], #Plataforma movil con movimiento hacia la izquierda                                                                        
         "d": [[[0,0, 0, 1]]], #Pez dorado - equivalente a comida
         "p": [[[-1, 0, -1,0]]], #Pingüino rosa
         "c": [[[0,1, 0, 1]]], #Checkpoint
         "G": [[[-1, 0, 0, 1]]] #Meta
                    }