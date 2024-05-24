import pygame as pg, time as ti, random as ra, ctypes as ct
import serial as rs
from pygame.locals import *

nRes = (640,640); nt_WX = nt_HY = 32; nMAX_ROBOTS = 01; lGo = True
nMx = nMy = 0; nR_1 = 1154 ; nR_2 = 32

#----------------------------------------------------
#       Estructura Robots
#----------------------------------------------------
class eRobot(ct.Structure):
    __fields__ = [
        ('nF',ct.c_ushort), 
        ('nX',ct.c_ushort),
        ('nY',ct.c_ushort),
        ('nR',ct.c_ushort),
        ('nS',ct.c_ushort),
        ('dX',ct.c_ushort),
        ('dY',ct.c_ushort),
        ('nV',ct.c_ushort),
        ('nC',ct.c_ushort)
]
    
#----------------------------------------------------
#       Estructura Celda Inteligente Mapa
#----------------------------------------------------
class eCelda(ct.Structure):
    _fields_ = [
        ('nT',ct.c_ubyte), # Tipo de Tile/Baldosa
        ('nD',ct.c_ubyte), # Tile Disponible? 
        ('nS',ct.c_ubyte), # 0 : No se pinta - # 1 : Si se pinta
        ('nF',ct.c_ubyte), # Fila de Mapa
        ('nC',ct.c_ubyte), # Columna de Mapa 
        ('nR',ct.c_ubyte), # Recurso a Explotar:
                                # 1:Acero
                                # 2:Cobre
                                # 3:Litio
                                # 4:Butano
        ('nQ',ct.c_ubyte)  # Cantidad del Recurso
]   
    
#----------------------------------------------------
#       Funcion Carga de Imagenes
#---------------------------------------------------- 
def Load_Image(sFile,transp = False):
    try: image = pg.image.load(sFile)
    except pg.error,message:
        raise SystemExit,message
    image = image.convert()
    if transp:
       color = image.get_at((0,0))
       image.set_colorkey(color,RLEACCEL)
    return image

def init_Pygame():
    pg.init()
    pg.mouse.set_visible(False) 
    pg.display.set_caption('Mapa Inteligente | Proyecto P.R #2')
    return pg.display.set_mode(nRes)

#---------------------------------------------------------------------
# Inicilaiza parametros de los Robots
#---------------------------------------------------------------------
def init_Robot():
    for i in range(0,nMAX_ROBOTS):
        aBoe[i].nF = 1    # Robot Tipo 1
        aBoe[i].nX = 0    # (RA.randint(0,nRES[0] - nT_WX) / nT_WX) * nT_WX 
        aBoe[i].nY = 0    # (RA.randint(0,nRES[1] - nT_HY) / nT_HY) * nT_HY
        aBoe[i].nR = nR_1 # (RA.randint(0,nRES[0] - nT_WX) / nT_WX) * nT_WX
        aBoe[i].nS = 1    # Switch por defecto
        aBoe[i].dX = 1    # Por defecto robot Direccion Este.-
        aBoe[i].dY = 0 
        aBoe[i].nV = 1 
        aBoe[i].nC = 1 
    return

def Init_Fig():
    aImg = []
    aImg.append(Load_Image('T01.png',False )) # Tile Tierra, id = 0
    aImg.append(Load_Image('T02.png',False )) # Tile Roca,   id = 1
    aImg.append(Load_Image('Bo1.png',True  )) # Robot 1      id = 2
    aImg.append(Load_Image('Bo2.png',True  )) # Robot 2      id = 3
    aImg.append(Load_Image('Bo3.png',True  )) # Robot 3      id = 4
    aImg.append(Load_Image('Bo4.png',True  )) # Robot 4      id = 5
    aImg.append(Load_Image('Bo5.png',True  )) # Robot 5      id = 6
    aImg.append(Load_Image('Bo6.png',True  )) # Robot 6      id = 7
    aImg.append(Load_Image('Bo7.png',True  )) # Robot 7      id = 8
    aImg.append(Load_Image('Bo8.png',True  )) # Robot 8      id = 9
    aImg.append(Load_Image('Rat.png',True  )) # Mouse 9      id = 10
    return aImg

def Init_Mapa():
    for nF in range(0,nRes[1] / nt_HY):
        for nC in range(0,nRes[0] / nt_WX):   
            aMap[nF][nC].nT = ra.randint(0,4)  # 0: Baldosa sin Recursos
                                         # 1: Baldosa con Acero
                                         # 2: Baldosa con Cobre
                                         # 3: Baldosa con Litio
                                         # 4: Baldosa con Gas Butano
            aMap[nF][nC].nD = 1  # 1: Disponible - 0: No Disponible
            aMap[nF][nC].nS = 0 # No se pinta por Defecto
            aMap[nF][nC].nF = nF # Fila de la Celda
            aMap[nF][nC].nC = nC # Colu de la Celda
            aMap[nF][nC].nR = aMap[nF][nC].nT
            aMap[nF][nC].nQ = ra.randint(100,1000) # Unidades de RR
    return 

def Pinta_Mapa():
    for nF in range(0,nRes[1] / nt_HY):
        for nC in range(0,nRes[0] / nt_WX):
            if aMap[nF][nC].nT == 0: # Baldosa sin recursos
                sWin.blit(aFig[00],(aMap[nF][nC].nC*nt_HY,aMap[nF][nC].nF*nt_WX)) # Baldosa sin RR

            if aMap[nF][nC].nT == 1: # Baldosa con Recurso -> Acero
                if aMap[nF][nC].nS == 1: sWin.blit(aFig[13],(aMap[nF][nC].nC*nt_HY,aMap[nF][nC].nF*nt_WX)) # Baldosa con Acero
                else: sWin.blit(aFig[00],(aMap[nF][nC].nC*nt_HY,aMap[nF][nC].nF*nt_WX)) # Baldosa sin RR

            if aMap[nF][nC].nT == 2:  # Baldosa con Recurso -> Cobre
                if aMap[nF][nC].nS == 1: sWin.blit(aFig[14],(aMap[nF][nC].nC*nt_HY,aMap[nF][nC].nF*nt_WX)) # Baldosa con Cobre
                else: sWin.blit(aFig[00],(aMap[nF][nC].nC*nt_HY,aMap[nF][nC].nF*nt_WX)) # Baldosa sin RR

            if aMap[nF][nC].nT == 3:  # Baldosa con Recurso -> Litio
                if aMap[nF][nC].nS == 1: sWin.blit(aFig[15],(aMap[nF][nC].nC*nt_HY,aMap[nF][nC].nF*nt_WX)) # Baldosa con Litio
                else: sWin.blit(aFig[00],(aMap[nF][nC].nC*nt_HY,aMap[nF][nC].nF*nt_WX)) # Baldosa sin RR

            if aMap[nF][nC].nT == 4:  # Baldosa con Recurso -> Gas Butano
                if aMap[nF][nC].nS == 1: sWin.blit(aFig[16],(aMap[nF][nC].nC*nt_HY,aMap[nF][nC].nF*nt_WX)) # Baldosa con Gas Butano
                else: sWin.blit(aFig[00],(aMap[nF][nC].nC*nt_HY,aMap[nF][nC].nF*nt_WX)) # Baldosa sin RR

    return

def Pinta_Robot():
    for i in range(0,nMAX_ROBOTS): # Iteramos las 8 Figuras del Robot
        if aBoe[i].nF == 1: sWin.blit(aFig[3] ,(aBoe[i].nX,aBoe[i].nY))
        if aBoe[i].nF == 2: sWin.blit(aFig[4] ,(aBoe[i].nX,aBoe[i].nY))
        if aBoe[i].nF == 3: sWin.blit(aFig[5] ,(aBoe[i].nX,aBoe[i].nY))
        if aBoe[i].nF == 4: sWin.blit(aFig[6] ,(aBoe[i].nX,aBoe[i].nY))     
        if aBoe[i].nF == 5: sWin.blit(aFig[7] ,(aBoe[i].nX,aBoe[i].nY))
        if aBoe[i].nF == 6: sWin.blit(aFig[8] ,(aBoe[i].nX,aBoe[i].nY))
        if aBoe[i].nF == 7: sWin.blit(aFig[9] ,(aBoe[i].nX,aBoe[i].nY))
        if aBoe[i].nF == 8: sWin.blit(aFig[10],(aBoe[i].nX,aBoe[i].nY))
    return

#---------------------------------------------------------------------
# Actualiza la estructura de datos de cada uno de los robots dentro del
# Mapa sMapa.
#---------------------------------------------------------------------
def Mueve_Robot():
    for i in range(0,nMAX_ROBOTS): # Recorrimos todos los Robots
        aBoe[i].nR -= 1      # Decrementamos en 1 el Rango del Robot
        if aBoe[i].nR <= 0:   # Robot termino sus pasos? 
            if aBoe[i].nS == 1:
                aBoe[i].nS = 2  # Cambio de estado
                aBoe[i].nR = nR_2 # Robot baja nR_2 pasos
                aBoe[i].dX = 0 ; aBoe[i].dY = 1
            elif aBoe[i].nS == 2:
                aBoe[i].nS = 3  # Cambio de estado
                aBoe[i].nR = nR_1 # Robot OEste nR_1 pasos
                aBoe[i].dX = -1 ; aBoe[i].dY = 0
            elif aBoe[i].nS == 3:
                aBoe[i].nS = 4  # Cambio de estado
                aBoe[i].nR = nR_2 # Robot baja nR_2 pasos
                aBoe[i].dX = 0 ; aBoe[i].dY = 1
            else:
                aBoe[i].nS = 1  # Cambio de estado
                aBoe[i].nR = nR_1 # Robot Este nR_1 pasos
                aBoe[i].dX = 1 ; aBoe[i].dY = 0
     #Actualizamos (Xs,Ys) de los Sprites en el Mapa 2D
     #--------------------------------------------------
    aBoe[i].nX += aBoe[i].dX*aBoe[i].nV # Posicion Robot[i] en eje X
    aBoe[i].nY += aBoe[i].dY*aBoe[i].nV # Posicion Robot[i] en eje Y
    aBoe[i].nC += 1
    if aBoe[i].nC >= 20:
        aBoe[i].nC = 1
        aBoe[i].nF += 1
        if aBoe[i].nF == 9:
           aBoe[i].nF = 1
        if aBoe[i].nX < 1 and aBoe[i].nY == 544: init_Robot()
    return

def Pinta_Mouse():
    sWin.blit(aFig[10],(nMx,nMy))
    return 

def Pausa():
    while 1:
        e = pg.event.wait()
        if e.type in (pg.QUIT, pg.KEYDOWN):
            return


sWin = init_Pygame() ; aFig = Init_Fig() 

aMap = [[eCelda() for nC in range(nRes[0]/nt_WX)] for nF in range(nRes[1]/nt_HY)]
aBoe = [ eRobot() for i in range(0,nMAX_ROBOTS) ] ; init_Robot(); Init_Mapa() 

while lGo:
    cKey = pg.key.get_pressed()
    if cKey[pg.K_ESCAPE] : lGo = ('A' > 'B')
 
    if cKey[pg.K_p]  : Pausa() 
    if cKey[pg.K_s]  : pg.image.save(sWin,'mapinte.png') 
     
    ev = pg.event.get()
    for e in ev:
        if e.type == QUIT           : lGo = (2 > 3)
        if e.type == pg.MOUSEMOTION : nMx,nMy = e.pos
 
    Pinta_Mapa() 
    Pinta_Robot()
    Mueve_Robot() 
    Pinta_Mouse()
    pg.display.flip()
 #aClk[0].tick(100)

pg.quit

