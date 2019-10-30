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
    return (int(rect_x), int(rect_y), int(rect_width), int(rect_height))


#borrar imágenes sin etiqueta


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
            dict_imagen = {'nombre': nombre_imagen_archivo, 'annotations': arreglo_caras, 'size':{'height':img_height,'width': img_width}}
            arreglo_de_images.append(dict_imagen)
            renglon = renglon + numero_caras + 1

        objeto_imagen = arreglo_de_images[0]
#         fig,ax = plt.subplots(1)
        img = mpimg.imread(os.path.join("dataset",objeto_imagen['nombre']))
#         ax.imshow(img)
#         for rectangle in objeto_imagen['annotations']:
#             rect = patches.Rectangle((rectangle[2],rectangle[3]),rectangle[0],rectangle[1],linewidth=1,edgecolor='r',facecolor='none')
#             ax.add_patch(rect)
#         plt.show()
        return pd.DataFrame(arreglo_de_images)

#Borrar todas las imagenes que no están en nuestro dataframe
def eraseImagesNotInDataframe(dataframe, columnname):
  #1. Conseguir un arreglo de todas las imagenes en /"imagefolder"
  arreglo_de_imagenes = glob.glob('./dataset/*.jpg')

  #2. Hacer un loop por cada nombre de imagen en el arreglo
    #2.a Checar si esta en el dataframe
  	#2.b Borrar esa imagen del imageFolder

  count = 0
  for nombre_en_dataframe in dataframe[columnname]:
      print(nombre_en_dataframe)
  for nombre_imagen in arreglo_de_imagenes:
    nombre_imagen_sin_dataset = nombre_imagen.replace("./dataset/", "")
    print("Nombre de imagen en folder: " + nombre_imagen_sin_dataset)
    if nombre_imagen_sin_dataset not in dataframe[columnname]:
        count = count + 1
  print(count)

def createXMLForImage(dataframe, imageName):
    print("Hello")
  #1. Conseguir datos de la imagen (nombre, anotaciones, etc...)

  #2. Utilizar la funcion del profe para guardarlo en /dataset


#Generar dataframe de todos los labels
all_images_dataframe=generateLabelDataArray(labels_files[0])
for n in range (1,len(labels_files)):
    new_arr= generateLabelDataArray(labels_files[n])
    all_images_dataframe = pd.concat([all_images_dataframe,new_arr])

lista_nombre = all_images_dataframe["nombre"].tolist()
arreglo_de_imagenes = [os.path.basename(path) for path in glob.glob('./dataset/*.jpg')]
cnt = 0
for img in arreglo_de_imagenes:
    if img not in lista_nombre:
        cnt = cnt + 1
        os.remove("./dataset/{}".format(img))

def pdToXml(name, coordinates, size, img_folder):
    xml = ['<annotation>']
    xml.append("    <folder>{}</folder>".format(img_folder))
    xml.append("    <filename>{}</filename>".format(name))
    xml.append("    <source>")
    xml.append("        <database>Unknown</database>")
    xml.append("    </source>")
    xml.append("    <size>")
    xml.append("        <width>{}</width>".format(size["width"]))
    xml.append("        <height>{}</height>".format(size["height"]))
    xml.append("        <depth>3</depth>".format())
    xml.append("    </size>")
    xml.append("    <segmented>0</segmented>")

    for field in coordinates:
        print
        print(field)
        xmin, ymin = max(0,field[0]), max(0,field[1])
        xmax = min(size["width"], field[0]+field[2])
        ymax = min(size["height"], field[1]+field[3])

        xml.append("    <object>")
        xml.append("        <name>Face</name>")
        xml.append("        <pose>Unspecified</pose>")
        xml.append("        <truncated>0</truncated>")
        xml.append("        <difficult>0</difficult>")
        xml.append("        <bndbox>")
        xml.append("            <xmin>{}</xmin>".format(int(xmin)))
        xml.append("            <ymin>{}</ymin>".format(int(ymin)))
        xml.append("            <xmax>{}</xmax>".format(int(xmax)))
        xml.append("            <ymax>{}</ymax>".format(int(ymax)))
        xml.append("        </bndbox>")
        xml.append("    </object>")
    xml.append('</annotation>')
    return '\n'.join(xml)


#eraseImagesNotInDataframe(all_images_dataframe, "nombre")

#iterar por cada imagen y llamar createXMLForImage
xmls = []
for index, imagen in all_images_dataframe.iterrows():
    nombre_imagen = imagen['nombre']
    coordenadas = imagen["annotations"]
    size = imagen["size"]
    xml = pdToXml(nombre_imagen, coordenadas, size, 'dataset')
    xmls.append(xml)
    archivo = open("./dataset/" + nombre_imagen.replace('.jpg', '.xml'), "w")
    archivo.write(xml)
