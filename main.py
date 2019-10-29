import glob
import pandas as pd
import re
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import numpy as np
import os
import math

#Obtener nombres de imágenes
resultado = glob.glob('./dataset/*.jpg')
imagenes = pd.Series(resultado)

#Obtener nombres de archivos con labels
labels_files = glob.glob('./labels/*ellipseList.txt')

#funcion para convertir coordenadas de ovalo a rectangular
def transformCoordinates(coordinates, width, height):
    major_axis_radius = coordinates[0]
    minor_axis_radius = coordinates[1]
    angle = coordinates[2]
    x = coordinates[3]
    y = coordinates[4]
    hypotenuse = (major_axis_radius * 2)
    rect_width = minor_axis_radius*2
    rect_height = abs(hypotenuse * math.sin(angle))
    rect_x = x - rect_width / 2
    rect_y = y - rect_height / 2
    if rect_x <= 0:
        rect_width -= abs(rect_x)
        rect_x = 0
    elif rect_y <= 0:
        rect_height -= abs(rect_y)
        rect_y = 0
    if rect_x + rect_width >= width:
        rect_width -= (rect_x + rect_width) - width
    if rect_y + rect_height >= height:
        rect_height -= (rect_y + rect_height) - height

    #print("Coordenadas rectangulo: ", (rect_width, rect_height, rect_x, rect_y))
    return (int(rect_width), int(rect_height), int(rect_x), int(rect_y))

#Funcion para obtener un arreglo con cada linea del archivo
def generateLabelDataArray(file):
    objetos = []
    with open(file) as f:
        #Leer todos los datos del archivo
        datos = f.read().splitlines()
        renglon = 0
        arreglo_de_images = []
        while renglon < len(datos):
            nombre_imagen = datos[renglon]
            nombre_imagen_archivo = "{}.jpg".format(nombre_imagen)
            #Verificar que si leimos un nombre de imagen
            rg = re.compile("\d{4}_\d{2}_\d{2}_.*_.*_(\d)")
            mtch = rg.match(nombre_imagen)
            if mtch:
                something = None
            else:
                renglon = renglon + 1
                continue
            #Verificar que existe archivo de la imagen
            img_width = 0
            img_height = 0
            current_image = None
            try:
                img = mpimg.imread(os.path.join("dataset",nombre_imagen_archivo))
                #(img_width, img_height, _) = img.size()
                current_image = img
            except:
                renglon = renglon + 1
                continue
            #Termino de verificacion
            img_height = current_image.shape[0]
            img_width = current_image.shape[1]
            renglon = renglon + 1
            numero_caras = int(datos[renglon])
            arreglo_caras = []
            #Leer coordenadas de las caras
            for c in range(1, numero_caras+1):
                coordenada_cara = datos[renglon+c]
                #arreglo_caras.append(coordenada_cara)
                arr_strings = coordenada_cara.split(" ")
                #["321","132","12","213","321","","1"]
                arr_strings.pop(5)
                arr_floats = [float(x) for x in arr_strings]
                arreglo_caras.append(transformCoordinates(arr_floats, img_width, img_height))
            dict_imagen = {'nombre': nombre_imagen_archivo, 'annotations': arreglo_caras}
            arreglo_de_images.append(dict_imagen)
            renglon = renglon + numero_caras + 1

        objeto_imagen = arreglo_de_images[0]
        fig,ax = plt.subplots(1)
        img = mpimg.imread(os.path.join("dataset",objeto_imagen['nombre']))
        ax.imshow(img)
        for rectangle in objeto_imagen['annotations']:
            rect = patches.Rectangle((rectangle[2],rectangle[3]),rectangle[0],rectangle[1],linewidth=1,edgecolor='r',facecolor='none')
            ax.add_patch(rect)
        plt.show()
        return arreglo_de_images



arr = generateLabelDataArray(labels_files[0])
print(arr)
