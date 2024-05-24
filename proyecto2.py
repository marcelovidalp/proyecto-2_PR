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

def

aBoe = [ eRobot() for i in range(0,nMAX_ROBOTS) ] ; Init_Robot(); Init_Mapa() 