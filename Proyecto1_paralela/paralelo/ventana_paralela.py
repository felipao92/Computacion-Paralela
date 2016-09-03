#coding=utf-8
from Tkinter import *
from sys import argv
from PIL import Image, ImageTk , ImageOps,ImageEnhance,ImageChops,ImageFilter
from datetime import *
import PIL.ImageOps
from tkFileDialog import askopenfilename
import tkMessageBox
import numpy as np
import StringIO
from mpi4py import MPI
import secuencial

global imSerializable
global original
global ventana
global vaca
global va
global cosa
global cerdo
global ce
global iman
global imtk
global bri
global con

comm = MPI.COMM_WORLD  # comunicador entre dos procesadores #
rank = comm.rank     # id procesador actual #
size = comm.size     # tamano procesador #


def armarVentana():
    ventana = Tk()

    ventana.title("Filtro Imagenes")
    ventana.geometry("1280x760+0+0")
    global scale
    global scale1

    barramenu=Menu(ventana)
    menarch=Menu(barramenu)
    menarch.add_command(label='Abrir',command=abrir)
    menarch.add_command(label='Guardar',command=guardar)
    menarch.add_command(label='Salir' , command=exit)
    barramenu.add_cascade(label='Archivo',menu=menarch)

    menarche = Menu(barramenu)
    menarche.add_command(label='efectos')
    menarche.add_command(label='recorte')
    barramenu.add_cascade(label='Paralelo', menu=menarche)

    menarcho = Menu(barramenu)
    menarcho.add_command(label='bicubic x2 ',command=secuencial.bicubic2)
    menarcho.add_command(label='bicubic %2',command=secuencial.bicubic)
    menarcho.add_command(label='nearest x2',command=secuencial.nearest_neighbor)
    menarcho.add_command(label='nearest %2', command=secuencial.nearest_neighbor2)
    menarcho.add_command(label='bilineal x2',command=secuencial.bilineal)
    menarcho.add_command(label='bilineal %2',command=secuencial.bilineal2)
    barramenu.add_cascade(label='Redimensionar', menu=menarcho)

    menarcha = Menu(barramenu)
    menarcha.add_command(label='Multienfoque',command=enfoque)
    #menarcha.add_command(label='GRB',command=rara2)
    menarcha.add_command(label='RBG',command=rara)
    #menarcha.add_command(label='BGR', command=rara3)
    #menarcha.add_command(label='GBR', command=rara4)
    #menarcha.add_command(label='BRG', command=rara5)
    #menarcha.add_command(label='Panoramica',command=panora)
    #menarcha.add_command(label='movimiento',command=matrix)
    #barramenu.add_cascade(label='Especiales', menu=menarcha)
    ventana.config(menu=barramenu)



    b6 = Button(ventana, text='    Original    ', command=botonOriginal).place(x=10,y=60)
    b1 = Button(ventana, text='Escala Grises', command=botonGris).place(x=150,y=60 )
    b2 = Button(ventana, text='   Difusion     ', command=botonFiltroVecinos).place(x=150,y=100)
    b3 = Button(ventana, text='  Convolucion', command=botonConvolucion).place (x=150,y=140)
    b4 = Button(ventana, text='   Contraste   ',command=secuencial.contraste).place (x=380 , y=95)
    b5 = Button(ventana, text='      Sepia      ', command=secuencial.sepia).place(x=150 ,y=180)
    b7 = Button(ventana, text='      Rotar      ',command=botones).place(x=10,y=100)
    b8 = Button(ventana, text='      espejo     ' ,command=secuencial.espejo).place(x=10,y=140)
    b9 = Button(ventana, text='       brillo      ',command=secuencial.brillo2 ).place(x=380 ,y=35)
    b10 = Button(ventana, text='    Negativo   ' , command=negativo).place(x=150 , y=220)
    b11 = Button(ventana, text='     invertir     ',command=secuencial.invertirColores).place (x=150,y=260)
    b12 = Button(ventana, text='  RGB Rojo     ',command=secuencial.rgb_rojo).place(x=10,y=220)
    b30 = Button(ventana, text='    RGB verde ', command=secuencial.rgb_verde).place(x=10, y=260)
    b40 = Button(ventana, text='    RGB azul   ', command=secuencial.rgb_azul).place(x=10, y=300)
    #b13 = Button(ventana, text='  Panoramica  ').place(x=150,y=140)
    b14 = Button(ventana, text='        HDR      ',command=secuencial.bonito).place(x=150, y=300)
    b15 = Button(ventana, text='   De cabeza  ',command=secuencial.rotar2).place (x=10,y =180)
    #b16= Button(ventana, text='  Multienfoque').place(x=150 , y=60)
    #b17 = Button(ventana, text='  stopmotion  ').place(x=150, y=20)
    scale = Scale(ventana,label='Brillo', orient=HORIZONTAL, from_=0.5,to=1.7, resolution=0.1, width=20, length=200,command=secuencial.brolo)#.place(x=1100 , y=10)
    scale.set(1.1)
    scale.pack(side='top', padx=1, pady=1)
    scale1= Scale(ventana,label='Contraste' ,orient=HORIZONTAL, from_=0.7, to=1.5, resolution=0.001, width=20,length=200,command=secuencial.contraste2)  # .place(x=1100 , y=10)
    scale1.set(1.1)
    scale1.pack(side='top', padx=1, pady=10)
    return ventana

def negativo():
    global imSerializable
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    label.destroy()
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable = PIL.ImageOps.invert(imSerializable)
        refresca(imSerializable)
    else:
        imSerializable = PIL.ImageOps.invert(imSerializable)
        refresca(grande)
        tkMessageBox.showinfo("¡ Mensaje !","Imagen Editada Correctamente\n\n * Puede Seguir Editando\n\n *Para ver los resultados vaya a su carpeta contendora")


def botones():
    box= Tk()
    box.title="medidas"
    box.geometry("180x200+10+200")
    b1 = Button(box, text='      Rotar 90       ', command=secuencial.rotar).place(x=10, y=10)
    b2 = Button(box, text='      Rotar 270     ', command=secuencial.rotar1).place(x=10, y=50)
    b3 = Button(box, text='      Rotar 180     ', command=secuencial.rotar2).place(x=10, y=90)
    b4 = Button(box, text='      Original        ', command=botonOriginal).place(x=10 ,y=130)

def botonGris():
    global imSerializable
    label.destroy()
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable = secuencial.filtroGrisesPromedio(imSerializable)
        refresca(imSerializable)
    else:
        imSerializable = secuencial.filtroGrisesPromedio(imSerializable)    
        refresca(grande)
        tkMessageBox.showinfo("¡ Mensaje !","Imagen Editada Correctamente\n\n * Puede Seguir Editando\n\n *Para ver los resultados vaya a su carpeta contendora")

def botonOriginal():
    global imSerializable
    global original
    global scale
    label.destroy()
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable = original
        label.destroy()
        scale.set(1.1)
        scale1.set(1.1)
        refresca(imSerializable)
    else:
        imSerializable = original
        label.destroy()
        scale.set(1.1)
        scale1.set(1.1)
        refresca(grande)
        tkMessageBox.showinfo("¡ Mensaje !","Imagen Editada Correctamente\n\n * Puede Seguir Editando\n\n *Para ver los resultados vaya a su carpeta contendora")

def botonFiltroVecinos():
    global imSerializable
    label.destroy()
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable = secuencial.filtroPromedio(imSerializable)
        refresca(imSerializable)
    else:
        imSerializable = secuencial.filtroPromedio(imSerializable)   
        refresca(grande)
        tkMessageBox.showinfo("¡ Mensaje !","Imagen Editada Correctamente\n\n * Puede Seguir Editando\n\n *Para ver los resultados vaya a su carpeta contendora")

def botonConvolucion():
    print "inicio ejecucion: %s"%(datetime.today())
    global imSerializable
    label.destroy()
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable = secuencial.convolucion(imSerializable)
        refresca(imSerializable)
        print "final ejecucion: %s"%(datetime.today())
    else:
        imSerializable = secuencial.convolucion(imSerializable)    
        refresca(grande)
        tkMessageBox.showinfo("¡ Mensaje !","Imagen Editada Correctamente\n\n * Puede Seguir Editando\n\n *Para ver los resultados vaya a su carpeta contendora")

def botonBinarizacion():
    global imSerializable, grande
    label.destroy()
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable = secuencial.filtroBinarizacion(imSerializable,int(argv[2]))
        refresca(imSerializable)
    else:
        imSerializable = secuencial.filtroBinarizacion(imSerializable,int(argv[2]))   
        refresca(grande)
        tkMessageBox.showinfo("¡ Mensaje !","Imagen Editada Correctamente\n\n * Puede Seguir Editando\n\n *Para ver los resultados vaya a su carpeta contendora")
    
def abrir():
    global original, imSerializable
    imSerializable = askopenfilename(filetypes=[("PNG", "*.png"), \
                                          ("JPEG", "*.jpeg"), \
                                          ("GIF", "*.gif"), \
                                          ("JPEG", "*.jpg")])
    
    label.destroy()
    imSerializable=Image.open(imSerializable)
    largo, ancho =imSerializable.size
    
    if largo>800 or ancho >800:
        respuesta=tkMessageBox.askquestion("¡ IMPORTANTE !", "Su fotografia acaba de superar el limite permitido y no cabe en la pantalla \n\n 1) Puede reducir el tamaño de ella para poder editarla (perdera calidad y pixeles) \n\n2) Trabajar con la imagen real, pero no podra ver los retoques hasta haberla guardado\n\n SI -> REDUCIR\n\n NO-> MANTENER TAMAÑO REAL " )
        if respuesta=="yes":
            recortada=imSerializable.resize((640,480))
            original=recortada
            imSerializable=recortada
            refresca(recortada)
            tkMessageBox.showinfo("Mensaje","Imagen Reducida Correctamente")
        else:
            muyGrande=Image.open("grande.jpeg")
            muyGrande=muyGrande.resize((640,353))
            original=imSerializable
            refresca(muyGrande)
    else:
        original=imSerializable
        refresca(imSerializable)


def refresca4(imagen):
    im = ImageTk.PhotoImage(imagen)
    global li
    li = Label(ti,image=im)
    li.imagen = im
    li.pack()

def der():
    global muestra
    li.destroy()
    cad=muestra.crop((0,0,400,600))
    cad.save("derecha.jpg")
    refresca4(cad)
def cent():
    global muestra
    li.destroy()
    cad=muestra.crop((400,0,800,600))
    cad.save("centro.jpg")
    refresca4(cad)
def izq():
    global muestra
    li.destroy()
    cad=muestra.crop((800,0,1200,600))
    cad.save("izquierda.jpg")
    refresca4(cad)
def final():
    li.destroy()
    fina=Image.new("RGB",(1200,600),"black")
    na=Image.open("derecha.jpg")
    ne=Image.open("izquierda.jpg")
    ni=Image.open("centro.jpg")
    fina.paste(na, (0, 0))
    fina.paste(ni, (400, 0))
    fina.paste(ne, (800, 0))
    fina.save("panoramica_final.jpg")
    refresca4(fina)

def final2():
    li.destroy()
    fina=Image.new("RGB",(1200,600),"black")
    na=Image.open("derecha.jpg")
    ne=Image.open("izquierda.jpg")
    ni=Image.open("centro.jpg")
    fina.paste(ne, (0, 0))
    fina.paste(ni, (400, 0))
    fina.paste(na, (800, 0))
    fina.save("panoramica_final.jpg")
    refresca4(fina)

def final3():
    li.destroy()
    fina=Image.new("RGB",(1200,600),"black")
    na=Image.open("derecha.jpg")
    ne=Image.open("izquierda.jpg")
    ni=Image.open("centro.jpg")
    fina.paste(ni, (0, 0))
    fina.paste(na, (400, 0))
    fina.paste(ne, (800, 0))
    fina.save("panoramica_final.jpg")
    refresca4(fina)



def convertirImgMatrixRGB(img):
    return np.array(img.convert("RGB"))

def mezclarRGB(img,r,g,b):
    arrImg=convertirImgMatrixRGB(img)
    for i in range(img.size[1]):
        for j in range(img.size[0]):
            arrImg[i][j][0] = (arrImg[i][j][0]+r)/2
            arrImg[i][j][1] = (arrImg[i][j][1]+g)/2
            arrImg[i][j][2] = (arrImg[i][j][2]+b)/2
    imgRGB=Image.fromarray(arrImg)
    return imgRGB


def rara():
    global imSerializable
    label.destroy()
    r,g,b=imSerializable.split()
    imSerializable=Image.merge('RGB',(r,b,g))
    imSerializable.save("rbg.png")
    refresca(imSerializable)


def nana(value):
    global cerdo
    global iman
    global imtk
    #iman=Image.open("1.jpg")
    iman = Image.open(str(int(value)) + ".jpg")
    iman = iman.resize((500, 500))
    iman = iman.rotate(270)
    imtk.paste(iman)


def enfoque():
    global vaca
    global cosa
    vaca=Toplevel()
    vaca.title("enfoque")
    vaca.geometry("800x680+0+0")
    b6 = Button(vaca, text='    cerca    ', command=cambiar).place(x=10, y=60)
    b7 = Button(vaca, text='    lejos      ', command=cambiar1).place(x=10, y=100)
    cosa=Image.open("enfoque_reducido1.jpg")
    refresca2(cosa)
    vaca.mainloop()

def cambiar():
    global cosa
    va.destroy()
    cosa = Image.open("enfoque_reducido1.jpg")
    refresca2(cosa)


def cambiar1():
    global cosa
    va.destroy()
    cosa = Image.open("enfoque_reducido2.jpg")
    refresca2(cosa)

def refresca2(imagen):
    im = ImageTk.PhotoImage(imagen)
    global va
    va = Label(vaca,image=im)
    va.imagen = im
    va.pack()


def refresca(imagen):
    im = ImageTk.PhotoImage(imagen)
   # global imSerializable
    global label
    #imSerializable=Image.open(imagen)
    label = Label(image=im)
    label.imagen = im
    label.pack()

def guardar():
    global imSerializable
    imSerializable.save("Imagen_Guardada.jpg")
    tkMessageBox.showinfo("Mensaje","Imagen Guardada Correctamente")

 

#*******************************************************************************************************************
# ****************************** ALGORITMOS PARALELOS **************************************************************
#*******************************************************************************************************************

def divisionTareaImagen(img):
    
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


def convolucion_paralelo(imagen):
    
    if rank==0:
        divisionTareaImagen(imagen)
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


def main():
    global imSerializable
    global original
    imSerializable = Image.open("perro.jpg")
    original = imSerializable
    v = armarVentana()
    refresca(imSerializable)
    v.mainloop()
    
main()