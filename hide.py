import numpy as np
import skimage.io as io
import pai_io
import matplotlib.pyplot as plt
import sys
import math

imagenAfile = sys.argv[1]
imagenBfile = sys.argv[2]

imagenA = pai_io.imread(imagenAfile)
imagenB = pai_io.imread(imagenBfile)

c = int(4) #bits menos significativos

"""
Verifica si imagenA puede guardar imagenB 
"""

def soportaImagen(imagenA, imagenB, c):
    if 1 + 2*math.ceil(16/c) + imagenB.size*math.ceil(8/c) > imagenA.size:
        return False
    else:
        return True

def oculta(imagenA, imagenB, c):
    if not soportaImagen(imagenA,imagenB, c):
        print("Espacio insuficiente")
    else:
        print(1 + 2*math.ceil(16/c) + imagenB.size*math.ceil(8/c))
        print(imagenA.size)
        n = math.ceil(16/c)
        p = math.ceil(8/c)
        t = 1 + 2*n + imagenB.size*p                                                      #cantidad de pixeles necesarios para guardar pixeles de imagenB
        a = np.reshape(imagenA, -1)
        b = np.reshape(imagenB, -1)       
        a[0:t] = (a[0:t] >> c) << c                                                          #elimina cifra menos significativa de imagenA

        if len(imagenB.shape) == 2:                                                                      #detecta si la imagenB es gris o rgb             
            a[0] += 0
        else:
            a[0] += 1

        
        dim = np.array([imagenB.shape[0],imagenB.shape[1]], dtype= np.uint16)
        for i in range(n):                                                                              #guarda el valor del largo y ancho de la imagenB en los primeros pixeles
            a[(2*i+1):(2*i+1+2)] += dim - ((dim >> c) << c)
            dim = dim >> c
            

        
        for i in range(p):                                                                               #guarda la imagenB
            a[(1+2*n+b.size*i):(1+2*n+b.size*i+b.size)] += b - ((b >> c) << c)
            b = b >> c
        
        if len(imagenA.shape) == 2:
            a = np.reshape(a, (imagenA.shape[0],imagenA.shape[1]))
        else:
            a = np.reshape(a, (imagenA.shape[0],imagenA.shape[1], 3))

        x = imagenAfile.rsplit(".")
        io.imsave(x[0]+'_hide.png',a)

oculta(imagenA, imagenB, c)
