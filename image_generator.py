from PIL import Image
import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

imageName = "images/amogus.jpg"

def magnitude(v): #Converts coloured pixels to range: 0 black, 1 white
    norm = 0.3*v[0]+0.59*v[1]+0.11*v[2] #formula I found online which works nicely
    norm = norm/255
    return norm

def gridFromImage(imageName):
    im = mpimg.imread(imageName)
    dims = im.shape #dimensioni dell'immagine
    m = np.array(im) #vedi la foto come un array su numpy
    mbw = [] #mbw: matrice con i valori su scala di grigio

    # size = (100, 100)
    # im = im.resize(size)

    # Cambia l'immagine da colorata ad in bianco e nero
    for i in range(dims[0]): #righe
        l = []
        for j in range(dims[1]): #colonne
            value = magnitude(m[i][j])
            l.append(value)
        mbw.append(l)

    # Funzione di Floyd da definizione
    for i in range(dims[0]):
        for j in range(dims[1]): #approssimala al colore più vicino, tenendo conto delle somme:
            if abs(mbw[i][j] - 1) < abs(mbw[i][j]): # If less than 0.5
                newValue = 1
            else:
                newValue = 0
            oldValue = mbw[i][j]
            mbw[i][j] = newValue
            #distribuisci l'errore sugli altri pixel
            errore = oldValue - newValue
            if j+1 < dims[1]-1:
                mbw[i][j+1] = mbw[i][j+1]+7/16*errore
            if i+1<dims[0]:
                if j+1 < dims[1]-1:
                    mbw[i+1][j+1] = mbw[i+1][j+1]+1/16*errore
                if j-1 >= 0:
                    mbw[i+1][j-1] = mbw[i+1][j-1]+3/16*errore
                mbw[i+1][j] = mbw[i+1][j]+5/16*errore

    mRGB = []
    for i in range(dims[0]):
        l = []
        for j in range(dims[1]):
            if mbw[i][j]==1:
                l.append([255,255,255])
            elif mbw[i][j]==0:
                l.append([0,0,0])
        mRGB.append(l)
    plt.imshow(mRGB)
    plt.show()
    return mbw


    # new_im = np.zeros(im.size)
    # for i in im.size[0]:
    #     for j in im.size[1]: #per ogni pixel vai al più vicino tra zero e uno e propaga errore
        
    #         if (im[i][j] > 0.5)
    #             new_im[i][j] = 1
    #         else:
    #             new_im[i][j] = 0
    # return new_im

# def Floyd(imageName):
#     im = mpimg.imread(imageName)
#     new_im = np.zeros(im.size)
#     for i in im.size[0]:
#         for j in im.size[1]:
#             if (im[i][j] > 0.5):
#                 new_im[i][j] = 1
#             else:
#                 new_im[i][j] = 0
#     return new_im
    

def printImage(imageName):
    # foto=imageio.imread(imageName, )
    foto = mpimg.imread(imageName)
    plt.imshow(foto)
    plt.show()

def main():
    gridFromImage(imageName)

main()