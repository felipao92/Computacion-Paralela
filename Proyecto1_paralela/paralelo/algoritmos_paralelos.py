#coding=utf-8
from mpi4py import MPI
import numpy as np
from PIL import Image,ImageChops, ImageEnhance, ImageOps, ImageFilter
import StringIO
import PIL.ImageOps 
from time import time

comm = MPI.COMM_WORLD  # comunicador entre dos procesadores #
rank = comm.rank     # id procesador actual #
size = comm.size     # tamano procesador #

def sepia(arrImg):
    final=Image.fromarray(arrImg)
    width, height = final.size

    for w in range(width):
        for h in range(height):
            r, g, b = final.getpixel((w, h))
            gray = (r+g+b)/3
            r = gray + (25 * 2)
            g = gray + 25
            b = gray - 25
            if r > 255:
                r = 255
            if g > 255:
                g = 255
            if b < 0:
                b = 0
            final.putpixel((w, h), (r, g, b))
    arrImg=convertirImgMatrixRGB(final)
    return arrImg

def mezclarRGB(img,r,g,b):
    arrImg=convertirImgMatrixRGB(img)
    for i in range(img.size[1]):
        for j in range(img.size[0]):
            arrImg[i][j][0] = (arrImg[i][j][0]+r)/2
            arrImg[i][j][1] = (arrImg[i][j][1]+g)/2
            arrImg[i][j][2] = (arrImg[i][j][2]+b)/2
    imgRGB=Image.fromarray(arrImg)
    return imgRGB

def rgb_rojo(arrImg):
    final=Image.fromarray(arrImg)
    r=255
    g=0
    b=0
    imgRGB=mezclarRGB(final,r,g,b)
    arrImg=convertirImgMatrixRGB(final)
    return imgRGB

def rgb_verde(arrImg): #entra la imagen a modificar como parametro
    final=Image.fromarray(arrImg)
    r=0
    g=255
    b=0
    imgRGB=mezclarRGB(final,r,g,b)
    arrImg=convertirImgMatrixRGB(final)
    return imgRGB # retorna la imagen en rgb 

def rgb_azul(arrImg): #entra la imagen a modificar como parametro
    final=Image.fromarray(arrImg)
    r=0
    g=0
    b=255
    imgRGB=mezclarRGB(final,r,g,b)
    arrImg=convertirImgMatrixRGB(final)
    return imgRGB # retorna la imagen en rgb     
   

def brillo(arrImg):
    final=Image.fromarray(arrImg)
    new_image = ImageEnhance.Brightness(final).enhance(-3)
    arrImg=convertirImgMatrixRGB(new_image)
    return arrImg

def contraste(arrImg):
    final=Image.fromarray(arrImg)   
    new_image = ImageEnhance.Contrast(final).enhance(2)
    arrImg=convertirImgMatrixRGB(new_image)
    return arrImg
   

def convertirImgMatrixRGB(img):
    return np.array(img.convert("RGB"))

#recibe un arreglo RGB de la imagen,lo convierte en negativo y retorna el arreglo negativo
def convertirImgNegativo(arrImg):
    for i in range(len(arrImg)): #largo
        for j in range(len(arrImg[0])):  #ancho
            arrImg[i][j] = 255-arrImg[i][j]
    return arrImg

def escalaDeGrises(arrImg):
	final=Image.fromarray(arrImg)
	new_image = ImageOps.grayscale(final)
	arrImg=convertirImgMatrixRGB(new_image)
	return arrImg
	
def reflejo(arrImg): 
    final=Image.fromarray(arrImg) 
    new_image = ImageOps.mirror(final)
    arrImg=convertirImgMatrixRGB(new_image)
    return arrImg

def rotar(arrImg): 
    final=Image.fromarray(arrImg) 
    new_image = ImageOps.mirror(final)
    arrImg=convertirImgMatrixRGB(new_image)
    return arrImg    
    
   
def convolucion(arrImg):
	imagen=Image.fromarray(arrImg)
	x,y = imagen.size
	px = imagen.load()
	#MX = [[-1,0,1],[-1,0,1],[-1,0,1]] #mascara lineas horizontales
	MX = [[-1,0,1],[-2,0,2],[-1,0,1]]
	#MY = [[1,1,1],[0,0,0],[-1,-1,-1]] #mascara lineas verticales
	MY = [[1,2,1],[0,0,0],[-1,-2,-1]]

	imagenNuevaX = Image.new('RGB',(x,y))
	imagenNuevaY = Image.new('RGB',(x,y))
	imn = Image.new('RGB',(x,y))
	for j in range(y):
		for i in range(x):
			sumatoria = 0
			sumatoriay = 0
			for mj in range(-1,2):
				for mx in range(-1,2):
					try:
						sumatoria += MX[mj+1][mx+1]*px[i+mx,j+mj][1]
						sumatoriay += MY[mj+1][mx+1]*px[i+mx,j+mj][1] 
					except:
						sumatoria += 0
						sumatoriay += 0
			punto1 = sumatoria
			punto2 = sumatoriay
			#Normalizar
			if(punto1 < 0):
				punto1 = 0
			if(punto1 > 255):
				punto1 = 255
			if(punto2 < 0):
				punto2 = 0
			if(punto2 > 255):
				punto2 = 255
			imagenNuevaX.putpixel((i,j),(punto1,punto1,punto1))
			imagenNuevaY.putpixel((i,j),(punto2,punto2,punto2))
	px1 = imagenNuevaX.load()
	px2 = imagenNuevaY.load()
	#Mezclar las mascaras
	for i in range(x):
		for j in range(y):
			p1 = px1[i,j]
			p2 = px2[i,j]
			r = ( p1[0] + p2[0] ) / 2
			g = ( p1[1] + p2[1] ) / 2
			b = ( p1[2] + p2[2] ) / 2
			imn.putpixel((i,j),(r,g,b))
	arrImg=convertirImgMatrixRGB(imn)
	return arrImg	

def imgcontruc(imagen): 
	rotada = imagen.rotate(90)
	return rotada

def divisionTareaImagen(ruta):
    img=Image.open(ruta)
    imgSize=img.size
    largo=imgSize[1]
    ancho=imgSize[0]
    tamanoParte=largo/(size-1)  #(size-1) es para no incluir el procesador cero
    xInicio=0
    yInicio=0
    tamPar=tamanoParte
    for i in range(1,size):
        parteImgEnvio=img.crop((xInicio,yInicio,ancho,tamPar))
        tamPar=tamPar+tamanoParte
        yInicio=yInicio+tamanoParte
        rutaSalida="photoCut"+str(i)+".jpg"
        parteImgEnvio.save(rutaSalida)
        arrImg=convertirImgMatrixRGB(parteImgEnvio)
        comm.send(arrImg,dest=i)



#----------------------------------------------------------------------------------------------------------------------------
#DE AQUI PARA ABAJO SON LAS FUNCIONES QUE UTLIZAMOS PARA EDITAR UNA IMAGEN EN PARALELO 



def rgb_rojo_paralelo():
    
    if rank==0:
        ruta="perro.jpg"
        divisionTareaImagen(ruta)
    if rank!=0:
        arrTrabajo=comm.recv(source=0)    #cada procesador recibe un arreglo RGB que contiene un trozo horizontal de la imagen
        arrImgSalida=rgb_rojo(arrTrabajo)
        comm.send(arrImgSalida,dest=0)
    if rank==0 :       #recibe los arreglos y los junta uno abajo del otro
        for i in range(1,size):
            if i > 1:
                construcImg = np.concatenate((construcImg,comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal=Image.fromarray(construcImg)
        imgContrucFinal.save("RGB_ROJO_PARALELO.jpg")

def rgb_verde_paralelo():
    
    if rank==0:
        ruta="perro.jpg"
        divisionTareaImagen(ruta)
    if rank!=0:
        arrTrabajo=comm.recv(source=0)    #cada procesador recibe un arreglo RGB que contiene un trozo horizontal de la imagen
        arrImgSalida=rgb_verde(arrTrabajo)
        comm.send(arrImgSalida,dest=0)
    if rank==0 :       #recibe los arreglos y los junta uno abajo del otro
        for i in range(1,size):
            if i > 1:
                construcImg = np.concatenate((construcImg,comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal=Image.fromarray(construcImg)
        imgContrucFinal.save("RGB_VERDE_PARALELO.jpg")

def escala_de_grises_paralelo():
    
    if rank==0:
        ruta="15mb.jpg"
        divisionTareaImagen(ruta)
    if rank!=0:
        arrTrabajo=comm.recv(source=0)    #cada procesador recibe un arreglo RGB que contiene un trozo horizontal de la imagen
        arrImgSalida=escalaDeGrises(arrTrabajo)
        comm.send(arrImgSalida,dest=0)
    if rank==0 :       #recibe los arreglos y los junta uno abajo del otro
        for i in range(1,size):
            if i > 1:
                construcImg = np.concatenate((construcImg,comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal=Image.fromarray(construcImg)
        imgContrucFinal.save("RGB_BLANCO_Y_NEGRO.jpg")

def rgb_azul_paralelo():
    
    if rank==0:
        ruta="perro.jpg"
        divisionTareaImagen(ruta)
    if rank!=0:
        arrTrabajo=comm.recv(source=0)    #cada procesador recibe un arreglo RGB que contiene un trozo horizontal de la imagen
        arrImgSalida=rgb_azul(arrTrabajo)
        comm.send(arrImgSalida,dest=0)
    if rank==0 :       #recibe los arreglos y los junta uno abajo del otro
        for i in range(1,size):
            if i > 1:
                construcImg = np.concatenate((construcImg,comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal=Image.fromarray(construcImg)
        imgContrucFinal.save("RGB_AZUL_PARALELO.jpg")        

def sepia_paralelo():
    if rank==0:
        ruta="perro.jpg"
        divisionTareaImagen(ruta)
    if rank!=0:
        arrTrabajo=comm.recv(source=0)    #cada procesador recibe un arreglo RGB que contiene un trozo horizontal de la imagen
        arrImgSalida=sepia(arrTrabajo)
        #arrImgSalida=convertirImgNegativo(arrTrabajo)    #enviar el arreglo RGB a transformarlo en arreglo negativo de la imagen
        comm.send(arrImgSalida,dest=0)
    if rank==0 :       #recibe los arreglos y los junta uno abajo del otro
        for i in range(1,size):
            if i > 1:
                construcImg = np.concatenate((construcImg,comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal=Image.fromarray(construcImg)
        imgContrucFinal.save("SEPIA_PARALELO.jpg")	


def brillo_paralelo():
    if rank==0:
        ruta="15mb.jpg"
        divisionTareaImagen(ruta)
    if rank!=0:
        arrTrabajo=comm.recv(source=0)    #cada procesador recibe un arreglo RGB que contiene un trozo horizontal de la imagen
        arrImgSalida=brillo(arrTrabajo)
        comm.send(arrImgSalida,dest=0)
    if rank==0 :       #recibe los arreglos y los junta uno abajo del otro
        for i in range(1,size):
            if i > 1:
                construcImg = np.concatenate((construcImg,comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal=Image.fromarray(construcImg)
        imgContrucFinal.save("BRILLO_PARALELO.jpg")


def contraste_paralelo():
    if rank==0:
        ruta="15mb.jpg"
        divisionTareaImagen(ruta)
    if rank!=0:
        arrTrabajo=comm.recv(source=0)    #cada procesador recibe un arreglo RGB que contiene un trozo horizontal de la imagen
        arrImgSalida=contraste(arrTrabajo)
        comm.send(arrImgSalida,dest=0)
    if rank==0 :       #recibe los arreglos y los junta uno abajo del otro
        for i in range(1,size):
            if i > 1:
                construcImg = np.concatenate((construcImg,comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal=Image.fromarray(construcImg)
        imgContrucFinal.save("CONTRASTE_PARALELO.jpg")

def espejo_paralelo():
    
    if rank==0:
        ruta="15mb.jpg"
        divisionTareaImagen(ruta)
    if rank!=0:
        arrTrabajo=comm.recv(source=0)    #cada procesador recibe un arreglo RGB que contiene un trozo horizontal de la imagen
        arrImgSalida=reflejo(arrTrabajo)
        comm.send(arrImgSalida,dest=0)
    if rank==0 :       #recibe los arreglos y los junta uno abajo del otro
        for i in range(1,size):
            if i > 1:
                construcImg = np.concatenate((construcImg,comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal=Image.fromarray(construcImg)
        imgContrucFinal.save("ESPEJO_PARALELO.jpg")	


def negativo_paralelo():
    
    if rank==0:
        ruta="15mb.jpg"
        divisionTareaImagen(ruta)
    if rank!=0:
        arrTrabajo=comm.recv(source=0)    #cada procesador recibe un arreglo RGB que contiene un trozo horizontal de la imagen
        arrImgSalida=convertirImgNegativo(arrTrabajo)    #enviar el arreglo RGB a transformarlo en arreglo negativo de la imagen
        comm.send(arrImgSalida,dest=0)
    if rank==0 :       #recibe los arreglos y los junta uno abajo del otro
        for i in range(1,size):
            if i > 1:
                construcImg = np.concatenate((construcImg,comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal=Image.fromarray(construcImg)
        imgContrucFinal.save("NEGATIVO_PARALELO.jpg")

def convolucion_paralelo():
    
    if rank==0:
        ruta="perro.jpg"
        divisionTareaImagen(ruta)
    if rank!=0:
        arrTrabajo=comm.recv(source=0)    #cada procesador recibe un arreglo RGB que contiene un trozo horizontal de la imagen
        arrImgSalida=convolucion(arrTrabajo)    #enviar el arreglo RGB a transformarlo en arreglo negativo de la imagen
        comm.send(arrImgSalida,dest=0)
    if rank==0 :       #recibe los arreglos y los junta uno abajo del otro
        for i in range(1,size):
            if i > 1:
                construcImg = np.concatenate((construcImg,comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal=Image.fromarray(construcImg)
        imgContrucFinal.save("CONVOLUCION_PARALELO.jpg")        	

def rotar_paralelo():
    if rank==0:
        ruta="15mb.jpg"
        ruta2=Image.open("15mb.jpg")
        divisionTareaImagen(ruta)
    if rank!=0:
        arrTrabajo=comm.recv(source=0)    #cada procesador recibe un arreglo RGB que contiene un trozo horizontal de la imagen
        arrImgSalida=rotar(arrTrabajo)    #enviar el arreglo RGB a transformarlo en arreglo negativo de la imagen
        comm.send(arrImgSalida,dest=0)
    if rank==0 :       #recibe los arreglos y los junta uno abajo del otro
        for i in range(1,size):
            if i > 1:
                construcImg = np.concatenate((construcImg,comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal=Image.fromarray(construcImg)
        imgcontruF=imgcontruc(ruta2)
        imgcontruF.save("ROTAR_PARALELO.jpg")        	



tiempo_inicial = time() 
rotar_paralelo()
tiempo_final = time() 
tiempo_ejecucion = tiempo_final - tiempo_inicial
print("el tiempo en segundos fue de") , tiempo_ejecucion