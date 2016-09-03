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
    menarcho.add_command(label='bicubic x2 ',command=bicubic2)
    menarcho.add_command(label='bicubic %2',command=bicubic)
    menarcho.add_command(label='nearest x2',command=nearest_neighbor)
    menarcho.add_command(label='nearest %2', command=nearest_neighbor2)
    menarcho.add_command(label='bilineal x2',command=bilineal)
    menarcho.add_command(label='bilineal %2',command=bilineal2)
    barramenu.add_cascade(label='Redimensionar', menu=menarcho)

    menarcha = Menu(barramenu)
    menarcha.add_command(label='Multienfoque',command=enfoque)
    menarcha.add_command(label='GRB',command=rara2)
    menarcha.add_command(label='RBG',command=rara)
    menarcha.add_command(label='BGR', command=rara3)
    menarcha.add_command(label='GBR', command=rara4)
    menarcha.add_command(label='BRG', command=rara5)
    menarcha.add_command(label='Panoramica',command=panora)
    menarcha.add_command(label='movimiento',command=matrix)
    barramenu.add_cascade(label='Especiales', menu=menarcha)
    ventana.config(menu=barramenu)



    b6 = Button(ventana, text='    Original    ', command=botonOriginal).place(x=10,y=60)
    b1 = Button(ventana, text='Escala Grises', command=botonGris).place(x=150,y=60 )
    b2 = Button(ventana, text='   Difusion     ', command=botonFiltroVecinos).place(x=150,y=100)
    b3 = Button(ventana, text='  Convolucion', command=botonConvolucion).place (x=150,y=140)
    b4 = Button(ventana, text='   Contraste   ',command=contraste).place (x=380 , y=95)
    b5 = Button(ventana, text='      Sepia      ', command=sepia).place(x=150 ,y=180)
    b7 = Button(ventana, text='      Rotar      ',command=botones).place(x=10,y=100)
    b8 = Button(ventana, text='      espejo     ' ,command=espejo).place(x=10,y=140)
    b9 = Button(ventana, text='       brillo      ',command=brillo2 ).place(x=380 ,y=35)
    b10 = Button(ventana, text='    Negativo   ' , command=negativo).place(x=150 , y=220)
    b11 = Button(ventana, text='     invertir     ',command=invertirColores).place (x=150,y=260)
    b12 = Button(ventana, text='  RGB Rojo     ',command=rgb_rojo).place(x=10,y=220)
    b30 = Button(ventana, text='    RGB verde ', command=rgb_verde).place(x=10, y=260)
    b40 = Button(ventana, text='    RGB azul   ', command=rgb_azul).place(x=10, y=300)
    #b13 = Button(ventana, text='  Panoramica  ').place(x=150,y=140)
    b14 = Button(ventana, text='        HDR      ',command=bonito).place(x=150, y=300)
    b15 = Button(ventana, text='   De cabeza  ',command=rotar2).place (x=10,y =180)
    #b16= Button(ventana, text='  Multienfoque').place(x=150 , y=60)
    #b17 = Button(ventana, text='  stopmotion  ').place(x=150, y=20)
    scale = Scale(ventana,label='Brillo', orient=HORIZONTAL, from_=0.5,to=1.7, resolution=0.1, width=20, length=200,command=brolo)#.place(x=1100 , y=10)
    scale.set(1.1)
    scale.pack(side='top', padx=1, pady=1)
    scale1= Scale(ventana,label='Contraste' ,orient=HORIZONTAL, from_=0.7, to=1.5, resolution=0.001, width=20,length=200,command=contraste2)  # .place(x=1100 , y=10)
    scale1.set(1.1)
    scale1.pack(side='top', padx=1, pady=10)
    return ventana


def nearest_neighbor():
    global imSerializable
    to=Toplevel()
    to.geometry("1290x1080+0+0")
    largo,ancho =imSerializable.size
    imagen_interpolada=imSerializable.filter(ImageFilter.BLUR)
    imagen_interpolada=imSerializable.resize((largo*2,ancho*2))
    imagen_interpolada.save("nearestgrande.jpg")
    imagen_interpolada=ImageTk.PhotoImage(imagen_interpolada)
    ce=Label(to,image=imagen_interpolada)
    ce.imSerializable=imagen_interpolada
    ce.pack()
    to.mainloop()
def nearest_neighbor2():
    global imSerializable
    to=Toplevel()
    to.geometry("1290x1080+0+0")
    largo,ancho =imSerializable.size
    imagen_interpolada=imSerializable.filter(ImageFilter.BLUR)
    imagen_interpolada=imSerializable.resize((largo/2,ancho/2))
    imagen_interpolada.save("nearestchica.jpg")
    imagen_interpolada=ImageTk.PhotoImage(imagen_interpolada)
    ce=Label(to,image=imagen_interpolada)
    ce.imSerializable=imagen_interpolada
    ce.pack()
    to.mainloop()

def bicubic():
    global imSerializable
    ta = Toplevel()
    ta.geometry("1290x1080+0+0")
    largo, ancho = imSerializable.size
    imagen_interpolada = imSerializable.resize((largo/2, ancho/2), Image.ANTIALIAS)
    imagen_interpolada.save("bicubicchica.jpg")
    imagen_interpolada = ImageTk.PhotoImage(imagen_interpolada)
    ce = Label(ta, image=imagen_interpolada)
    ce.imSerializable = imagen_interpolada
    ce.pack()
    ta.mainloop()

def bicubic2():
    global imSerializable
    ta=Toplevel()
    ta.geometry("1290x1080+0+0")
    largo,ancho=imSerializable.size
    imagen_interpolada=imSerializable.resize((largo*2,ancho*2),Image.ANTIALIAS)
    imagen_interpolada.save("bicubicgrande.jpg")
    imagen_interpolada=ImageTk.PhotoImage(imagen_interpolada)
    ce=Label(ta,image=imagen_interpolada)
    ce.imSerializable=imagen_interpolada
    ce.pack()
    ta.mainloop()

def bilineal():
    global imSerializable
    te=Toplevel()
    te.geometry("1290x1080+0+0")
    largo,ancho=imSerializable.size
    imagen_interpolada=imSerializable.resize((largo*2,ancho*2))
    imagen_interpolada.save("bilinealgrande.jpg")
    imagen_interpolada=ImageTk.PhotoImage(imagen_interpolada)
    ce = Label(te, image=imagen_interpolada)
    ce.imSerializable = imagen_interpolada
    ce.pack()
    te.mainloop()


def bilineal2():
    global imSerializable
    te = Toplevel()
    te.geometry("1290x1080+0+0")
    largo, ancho = imSerializable.size
    imagen_interpolada = imSerializable.resize((largo/2, ancho/2))
    imagen_interpolada.save("bilinealchica.jpg")
    imagen_interpolada = ImageTk.PhotoImage(imagen_interpolada)
    ce = Label(te, image=imagen_interpolada)
    ce.imSerializable = imagen_interpolada
    ce.pack()
    te.mainloop()

def panora():
    global ti
    global muestra
    ti=Toplevel()
    ti.geometry("1290x1080+0+0")
    tu = Toplevel()
    tu.geometry("120x250+0+0")
    tu.title("panoramica")
    b6 = Button(tu, text='   izquierda ',command=der).place(x=10, y=10)
    b1 = Button(tu, text='   derecha   ',command=izq).place(x=10, y=50)
    b2 = Button(tu, text='    centro    ',command=cent).place(x=10, y=90)
    b3 = Button(tu, text='Panoramica',command=final).place(x=10, y=130)
    b6 = Button(tu, text='    mezcla   ', command=final2).place(x=10, y=170)
    b7 = Button(tu, text='    mezcla2  ', command=final3).place(x=10, y=210)
    muestra=Image.open("panoramica.jpg")
    refresca4(muestra)
    ti.mainloop()


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

def filtroGrisesPromedio(imagen):
    x, y = imagen.size
    px = imagen.load()
    imagenGrises = Image.new('RGB',(x,y))
    for i in range(x):
        for j in range(y):
            pixeles = px[i,j]
            prom = sum(pixeles) / 3
            imagenGrises.putpixel((i,j),(prom,prom,prom))
    return imagenGrises

def filtroPromedio(imagen):
    x,y = imagen.size
    pixeles = imagen.load()
    imagenFiltrada = Image.new('RGB',(x,y))
    c = 1
    for i in range(x):
        for j in range(y):
            px = pixeles[i,j]
            try:
                p1 = pixeles[i+1,j]
                c += 1
            except:
                p1 = (0,0,0)
            try:
                p2 = pixeles[i-1,j]
                c += 1
            except:
                p2 = (0,0,0)
            try:
                p3 = pixeles[i,j+1]
                c += 1
            except:
                p3 = (0,0,0)
            try:
                p4 = pixeles[i,j-1]
                c += 1
            except:
                p4 = (0,0,0)

            if(c > 4):
                c = 4
            r = p1[0] + p2[0] + p3[0] + p4[0]
            g = p1[0] + p2[0] + p3[0] + p4[0]
            b = p1[0] + p2[0] + p3[0] + p4[0]

            imagenFiltrada.putpixel((i,j),(r/c,g/c,b/c))
            c = 0
    return imagenFiltrada


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

def rgb_rojo(): #entra la imagen a modificar como parametro
    global imSerializable
    label.destroy()
    r=255
    g=0
    b=0
    imgRGB=mezclarRGB(imSerializable,r,g,b)
    imgRGB.save("Efecto_RGB_rojo.png")    #guarda la imagen RGB
    refresca(imgRGB) # retorna la imagen en rgb

def rgb_verde(): #entra la imagen a modificar como parametro
    global imSerializable
    label.destroy()
    r=0
    g=255
    b=0
    imgRGB=mezclarRGB(imSerializable,r,g,b)
    imgRGB.save("Efecto_RGB_verde.png")   #guarda la imagen RGB
    refresca(imgRGB) # retorna la imagen en rgb
def rgb_azul(): #entra la imagen a modificar como parametro
    global imSerializable
    label.destroy()
    r=0
    g=0
    b=255
    imgRGB=mezclarRGB(imSerializable,r,g,b)
    imgRGB.save("Efecto_RGB_azul.png")   #guarda la imagen RGB
    refresca(imgRGB) # retorna la imagen en rgb

def rara():
    global imSerializable
    label.destroy()
    r,g,b=imSerializable.split()
    imSerializable=Image.merge('RGB',(r,b,g))
    imSerializable.save("rbg.png")
    refresca(imSerializable)

def rara2():
    global imSerializable
    label.destroy()
    r,g,b=imSerializable.split()
    imSerializable=Image.merge('RGB',(g,r,b))
    imSerializable.save("grb.png")
    refresca(imSerializable)
def rara3():
    global imSerializable
    label.destroy()
    r,g,b=imSerializable.split()
    imSerializable=Image.merge('RGB',(b,g,r))
    imSerializable.save("bgr.png")
    refresca(imSerializable)
def rara4():
    global imSerializable
    label.destroy()
    r,g,b=imSerializable.split()
    imSerializable=Image.merge('RGB',(g,b,r))
    imSerializable.save("gbr.png")
    refresca(imSerializable)
def rara5():
    global imSerializable
    label.destroy()
    r,g,b=imSerializable.split()
    imSerializable=Image.merge('RGB',(b,r,g))
    imSerializable.save("brg.png")
    refresca(imSerializable)

def matrix():
    global cerdo
    global iman
    global imtk
    cerdo=Toplevel()
    cerdo.title("matrix")
    cerdo.geometry("800x680+0+0")
    scale1 = Scale(cerdo, label='movimiento', orient=HORIZONTAL, from_=1, to=30, resolution=1, width=20,
                   length=200, command=nana)  # .place(x=1100 , y=10)
    scale1.set(1)
    scale1.pack(side='top', padx=1, pady=10)
    iman = Image.open("1.jpg")
    iman = iman.resize((500, 500))
    iman = iman.rotate(270)
    imtk = ImageTk.PhotoImage('RGBA', iman.size)
    ce = Label(cerdo, image=imtk)
    ce.iman = imtk
    ce.pack()

    imtk.paste(iman)
    cerdo.mainloop()

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


def filtroConvolucion(imagen):
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
    
    return imn


def filtroBinarizacion(imagen, umbral):
    x,y = imagen.size
    px = imagen.load()
    imagenBinarizada = Image.new('RGB',(x,y))
    for i in range(x):
        for j in range(y):
            vRGB = px[i,j][1]
            if (vRGB > umbral):
                imagenBinarizada.putpixel((i,j), (255,255,255))
            else:
                imagenBinarizada.putpixel((i,j), (0,0,0))
    return imagenBinarizada



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



def invertirColores():
    global imSerializable
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    label.destroy()
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable = ImageChops.invert(imSerializable)
        refresca(imSerializable)
    else:
        imSerializable = ImageChops.invert(imSerializable)
        refresca(grande)
        tkMessageBox.showinfo("¡ Mensaje !","Imagen Editada Correctamente\n\n * Puede Seguir Editando\n\n *Para ver los resultados vaya a su carpeta contendora")
        
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
        
def sepia():
    global imSerializable
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    label.destroy()
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        width, height = imSerializable.size

        for w in range(width):
            for h in range(height):
                r, g, b = imSerializable.getpixel((w, h))
                gray = (r + g + b) / 3
                r = gray + (25 * 2)
                g = gray + 25
                b = gray - 25
                if r > 255:
                    r = 255
                if g > 255:
                    g = 255
                if b < 0:
                    b = 0
                imSerializable.putpixel((w, h), (r, g, b))
        refresca(imSerializable)
    else:
        width, height = imSerializable.size
        for w in range(width):
            for h in range(height):
                r, g, b = imSerializable.getpixel((w, h))
                gray = (r + g + b) / 3
                r = gray + (25 * 2)
                g = gray + 25
                b = gray - 25
                if r > 255:
                    r = 255
                if g > 255:
                    g = 255
                if b < 0:
                    b = 0
                imSerializable.putpixel((w, h), (r, g, b))
        refresca(grande)
        tkMessageBox.showinfo("¡ Mensaje !","Imagen Editada Correctamente\n\n * Puede Seguir Editando\n\n *Para ver los resultados vaya a su carpeta contendora")



def espejo():

    global imSerializable
    label.destroy()
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable= ImageOps.mirror(imSerializable)
        refresca(imSerializable)
    else:
        imSerializable= ImageOps.mirror(imSerializable)
        refresca(grande)   
        tkMessageBox.showinfo("¡ Mensaje !","Imagen Editada Correctamente\n\n * Puede Seguir Editando\n\n *Para ver los resultados vaya a su carpeta contendora") 

def contraste():
    global imSerializable
    label.destroy()
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable=ImageEnhance.Contrast(imSerializable)
        imSerializable=imSerializable.enhance(4)
        refresca(imSerializable)
    else:
        imSerializable=ImageEnhance.Contrast(imSerializable)
        imSerializable=imSerializable.enhance(4)
        refresca(grande)
        tkMessageBox.showinfo("¡ Mensaje !","Imagen Editada Correctamente\n\n * Puede Seguir Editando\n\n *Para ver los resultados vaya a su carpeta contendora")    


def contraste2(value):
    global imSerializable
    label.destroy()
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable = ImageEnhance.Contrast(imSerializable)
        imSerializable = imSerializable.enhance(float(value))
        refresca(imSerializable)
    else:
        imSerializable = ImageEnhance.Contrast(imSerializable)
        imSerializable = imSerializable.enhance(float(value))
        refresca(grande)    


def girar(value):
    global imSerializable
    label.destroy()
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable = imSerializable.rotate(float(value))
        refresca(imSerializable)
    else:
        imSerializable = imSerializable.rotate(float(value))
        refresca(grande)    
        tkMessageBox.showinfo("¡ Mensaje !","Imagen Editada Correctamente\n\n * Puede Seguir Editando\n\n *Para ver los resultados vaya a su carpeta contendora")

def brillo2():
    global imSerializable
    label.destroy()
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable = ImageEnhance.Brightness(imSerializable)
        imSerializable = imSerializable.enhance(1.5)
        refresca(imSerializable)
    else:
        imSerializable = ImageEnhance.Brightness(imSerializable)
        imSerializable = imSerializable.enhance(1.5)
        refresca(grande)
        tkMessageBox.showinfo("¡ Mensaje !","Imagen Editada Correctamente\n\n * Puede Seguir Editando\n\n *Para ver los resultados vaya a su carpeta contendora")    

def bonito():
    global imSerializable
    label.destroy()
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable = ImageEnhance.Contrast(imSerializable)
        imSerializable = imSerializable.enhance(1.199)
        imSerializable = ImageEnhance.Brightness(imSerializable)
        imSerializable = imSerializable.enhance(1.187)
        refresca(imSerializable)
    else:
        imSerializable = ImageEnhance.Contrast(imSerializable)
        imSerializable = imSerializable.enhance(1.18)
        imSerializable = ImageEnhance.Brightness(imSerializable)
        imSerializable = imSerializable.enhance(1.18)    
        refresca(grande)
        tkMessageBox.showinfo("¡ Mensaje !","Imagen Editada Correctamente\n\n * Puede Seguir Editando\n\n *Para ver los resultados vaya a su carpeta contendora")

def botones():
    box= Tk()
    box.title="medidas"
    box.geometry("180x200+10+200")
    b1 = Button(box, text='      Rotar 90       ', command=rotar).place(x=10, y=10)
    b2 = Button(box, text='      Rotar 270     ', command=rotar1).place(x=10, y=50)
    b3 = Button(box, text='      Rotar 180     ', command=rotar2).place(x=10, y=90)
    b4 = Button(box, text='      Original        ', command=botonOriginal).place(x=10 ,y=130)


def brolo(value):
    global imSerializable
    label.destroy()
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable= ImageEnhance.Brightness(imSerializable)
        imSerializable= imSerializable.enhance(float(value))
        refresca(imSerializable)
    else:
        imSerializable= ImageEnhance.Brightness(imSerializable)
        imSerializable= imSerializable.enhance(float(value))    
        refresca(grande)

def rotar():
    global imSerializable
    global recortada
    label.destroy()
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353)) 
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable=imSerializable.rotate(90)
        refresca(imSerializable)
    
    else:
        imSerializable=imSerializable.rotate(90)    
        refresca(grande)
        tkMessageBox.showinfo("¡ Mensaje !","Imagen Editada Correctamente\n\n * Puede Seguir Editando\n\n *Para ver los resultados vaya a su carpeta contendora")

def rotar2():
    global imSerializable
    global recortada
    label.destroy()
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable=imSerializable.rotate(180)
        refresca(imSerializable)

    else:
        imSerializable=imSerializable.rotate(180)
        refresca(grande)
        tkMessageBox.showinfo("¡ Mensaje !","Imagen Editada Correctamente\n\n * Puede Seguir Editando\n\n *Para ver los resultados vaya a su carpeta contendora")
def rotar1():
    global imSerializable
    global recortada
    label.destroy()
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable=imSerializable.rotate(270)
        refresca(imSerializable)

    else:
        imSerializable=imSerializable.rotate(270)
        refresca(grande)
        tkMessageBox.showinfo("¡ Mensaje !","Imagen Editada Correctamente\n\n * Puede Seguir Editando\n\n *Para ver los resultados vaya a su carpeta contendora")

def botonGris():
    global imSerializable
    label.destroy()
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable = filtroGrisesPromedio(imSerializable)
        refresca(imSerializable)
    else:
        imSerializable = filtroGrisesPromedio(imSerializable)    
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
        imSerializable = filtroPromedio(imSerializable)
        refresca(imSerializable)
    else:
        imSerializable = filtroPromedio(imSerializable)   
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
        imSerializable = filtroConvolucion(imSerializable)
        refresca(imSerializable)
        print "final ejecucion: %s"%(datetime.today())
    else:
        imSerializable = filtroConvolucion(imSerializable)    
        refresca(grande)
        tkMessageBox.showinfo("¡ Mensaje !","Imagen Editada Correctamente\n\n * Puede Seguir Editando\n\n *Para ver los resultados vaya a su carpeta contendora")

def botonBinarizacion():
    global imSerializable, grande
    label.destroy()
    grande=Image.open("grande.jpeg")
    grande=grande.resize((640,353))
    largo, ancho =imSerializable.size
    if largo<800 or ancho <800:
        imSerializable = filtroBinarizacion(imSerializable,int(argv[2]))
        refresca(imSerializable)
    else:
        imSerializable = filtroBinarizacion(imSerializable,int(argv[2]))   
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


def main():
    global imSerializable
    global original
    imSerializable = Image.open("perro.jpg")
    original = imSerializable
    v = armarVentana()
    refresca(imSerializable)
    v.mainloop()

main()