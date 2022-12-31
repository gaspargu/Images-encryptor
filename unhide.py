import numpy as np
import skimage.io as io
import pai_io
import matplotlib.pyplot as plt
import sys
import math

imagenfile = sys.argv[1]

imagenA = pai_io.imread(imagenfile)

c = int(4) #bits menos significativos

def desoculta(imagenA,c):
    n = math.ceil(16/c)
    p = math.ceil(8/c)
    a = imagenA - ((imagenA >> c) << c)
    a = np.reshape(a, -1)
    b = np.zeros(2, dtype = np.uint16)
    d = a[1:1+2*n].astype(np.uint16)
    for i in range(n):                                            
        b += d[2*i:2*i+2] << c*i
    alto = b[0]
    ancho = b[1]
    r = 0
    if a[0] == 0:
        r = 1
    else:
        r = 3
    tamaño = int(alto)*int(ancho)*r

    imagenB = np.zeros(tamaño, dtype = np.uint8)
    
    for i in range(p):
        imagenB += a[(1+2*n+tamaño*i):(1+2*n+tamaño*i+tamaño)] << c*i
    if a[0] == 0:
        imagenB = np.reshape(imagenB, (alto, ancho))
    else:
        imagenB = np.reshape(imagenB, (alto, ancho, 3))
    
    return imagenB



plt.imshow (desoculta(imagenA,c), cmap = 'gray')
plt.axis('off')
plt.show()
