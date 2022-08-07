# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 18:09:31 2021

@author: Luis Tomé, 48341
"""

from imageio import imread, imwrite
from matplotlib import use
import matplotlib.pyplot as plt
import numpy as np
from skimage.transform import rescale

#use('TkAgg')

#Constantes
fundoDir = ''; fantasDir = ''
bgImg = imread(fundoDir+"sky01.tif")
gImg = imread(fantasDir+"fantasma_bc.tif")
a = 0.6

#diminuir tamanho de imagem do fantasma
sGhost = rescale(gImg, 0.15 ,anti_aliasing=True)
gHeight, gWidth = sGhost.shape[:2]

#conversao de cada pixel da imagem do fantasma
    #   para num intervalo de valores de 0 a 255 
    #   e aumento de intensidade de cada pixel da imagem
for i in range(len(sGhost)):
    for j in range(len(sGhost[i])):
        sGhost[i][j] = int((((sGhost[i][j] - 0) * 255) / 1) + 0)*5

#Escolha de Posições
plt.figure();plt.imshow(bgImg);plt.axis('off')
vetores=plt.ginput(-1, show_clicks=True, mouse_pop=3, mouse_stop=2)
plt.close()

def copyFromOriginal(ori, cp):
    for c in range(3):
        cp[:,:,c] = ori[:,:,c]
    return cp

def separarPorBandas(img):
    rbgLst = []
    for banda in range(3):
        rbgLst.append(img[:,:,banda])
        
    return rbgLst

#copiar as bandas RGB da imagem de fundo para sobreposicao
sobposImg = copyFromOriginal(bgImg, np.ones_like(bgImg))

#copiar as bandas RGB da imagem de fundo para blending
blendImg = copyFromOriginal(bgImg, np.ones_like(bgImg))

def prjSobreBlend(alpha):
    """
    Criação das imagens de sobreposição e Blending
    Demonstração dos metodos de processamento de imagem.

    Parameters
    ----------
    alpha : float
        Grau de transparencia para blending.
        Valor compreendido entre 0.0 e 1.0

    Returns
    -------
    None.

    """
    
    h, r = np.histogram(sGhost, bins=256, range=(0, 255))
    pa = np.cumsum(np.cumsum(h)/float(gHeight*gWidth))
    #Limiarização pela média
    sGhostMask = sGhost >= (sum(pa))/len(pa)
    
    if alpha <= 0.0 and alpha >= 1.0:
        print("Grau de transparencia invalido: ", alpha)
        print("Grau de transparencia mudado para o valor intermédio: ", 0.5)
        alpha = 0.5
    
    for p in range(len(vetores)):
        
        x = int(vetores[p][0])
        y = int(vetores[p][1])
        
        sobre = [np.ones_like(sGhost),np.ones_like(sGhost),np.ones_like(sGhost)]
        blend = [np.ones_like(sGhost),np.ones_like(sGhost),np.ones_like(sGhost)]
        
        rgbS = separarPorBandas(sobposImg[y : y+gHeight, x : x+gWidth])
        rgbB = separarPorBandas(bgImg[y : y+gHeight, x : x+gWidth])
        
        for lst in range(len(sGhost)):
            for val in range(len(sGhost[lst])):
                if sGhostMask[lst][val] == False:
                    for b in range(3):
                        sobre[b][lst][val] = rgbS[b][lst][val]
                        blend[b][lst][val] = blendImg[y : y+gHeight, x : x+gWidth, b][lst][val]
                    
                else:
                    for b in range(3):
                        sobre[b][lst][val] = sGhost[lst][val]
                        blend[b][lst][val] = (sGhost[lst][val] + alpha * ( rgbB[b][lst][val] - sGhost[lst][val]))
                    
        for c in range(3):
            sobposImg[y : y+gHeight, x : x+gWidth,c] = sobre[c]
            blendImg[y : y+gHeight, x : x+gWidth,c] = blend[c]
                        
    imwrite('SkyPhantom_Sobreposicao.tif', sobposImg)
    imwrite('SkyPhantom_Blending.tif', blendImg)
    
    plt.figure()
    plt.subplot(131); plt.imshow(bgImg); plt.axis('off'); plt.title('Original')
    plt.subplot(132); plt.imshow(sobposImg); plt.axis('off'); plt.title('Sobreposição')
    plt.subplot(133); plt.imshow(blendImg); plt.axis('off'); plt.title('Blending')
    
a = 0.6
print("Grau de transparencia [0.0, 1.0]: ", a)
prjSobreBlend(a)
