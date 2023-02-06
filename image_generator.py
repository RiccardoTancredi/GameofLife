#Program to generate grid starting from an RGB image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import skimage.measure

def magnitude(v): #Converts coloured pixels to range: 0 black, 1 white
    norm = 0.3*v[0]+0.59*v[1]+0.11*v[2] #formula I found online which works nicely
    norm = norm/255 # To be removed in case the image is defined in range [0, 1] instead of [0, 255]
    return norm

def resizeImage(mbw,desiredDimension): # Resizes the image so that its height has more or less the value of desiredDimension (tat will be the pygame board dimension)
    mbw = np.array(mbw)
    ratio =  mbw.shape[0]//desiredDimension #horizontal axis
    output = skimage.measure.block_reduce(mbw, block_size=ratio, func=np.mean, cval=0, func_kwargs=None) 
    return output

def bit_to_rgb(mbw): #Converts matrix of 0s and 1s to [0,0,0] and [255,255,255] so that it can be drawn by pyplot. Only used it while coding to check
    mRGB = []
    for i in range(mbw.shape[0]):
        l = []
        for j in range(mbw.shape[1]):
            if mbw[i][j]==1:
                l.append([255,255,255])
            elif mbw[i][j]==0:
                l.append([0,0,0])
        mRGB.append(l)
    # plt.imshow(mRGB)
    # plt.show()
    return mRGB


def gridFromImage(imageName, resize=None, desiredDimension=None): #Function to convert image to a grid of 0s and 1s
    im = mpimg.imread(imageName)
    dims = im.shape #Image dimensions
    m = np.array(im) #Sees image as numpy array

    # Changes the image from colors to black and white
    mbw = [] #mbw: matrix whose values are in grayscale (from 0 to 1)
    for i in range(dims[0]): # rows
        l = []
        for j in range(dims[1]): # columns
            value = magnitude(m[i][j])
            l.append(value)
        mbw.append(l)

    if resize: 
        mbw = resizeImage(mbw, desiredDimension)
        dims = mbw.shape # image dimensions

    # Implements Floyd Steinberg Dithering 
    for i in range(dims[0]):
        for j in range(dims[1]): #approximates to the nearest color, keeping in mind the sums:
            if abs(mbw[i][j] - 1) < abs(mbw[i][j]): # If less than 0.5
                newValue = 1
            else:
                newValue = 0
            oldValue = mbw[i][j]
            mbw[i][j] = newValue
            #Spreads error to confining pixels
            errore = oldValue - newValue
            if j+1 < dims[1]-1:
                mbw[i][j+1] = mbw[i][j+1]+7/16*errore
            if i+1<dims[0]:
                if j+1 < dims[1]-1:
                    mbw[i+1][j+1] = mbw[i+1][j+1]+1/16*errore
                if j-1 >= 0:
                    mbw[i+1][j-1] = mbw[i+1][j-1]+3/16*errore
                mbw[i+1][j] = mbw[i+1][j]+5/16*errore

    mbw = np.array(mbw)
    mRGB = bit_to_rgb(mbw)

    return mbw

def printImage(imageName): # Prints the image to be confronted with the output
    foto = mpimg.imread(imageName)
    plt.imshow(foto)
    plt.show()

def main():
    immagine = "monna_lisa" 
    inputFile = "images/"+immagine+".jpg"
    nameOutputFile = "images_txt/"+immagine+".txt"
    matrix = gridFromImage(inputFile, resize=True, desiredDimension=20)
    outputFile =  open(nameOutputFile, "w")
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            outputFile.write(str(int(matrix[i][j])))
            if j!=matrix.shape[1]-1:
                outputFile.write(" ")
        outputFile.write("\n")
    outputFile.close()
    printImage(inputFile)

# main()