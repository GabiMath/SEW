# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 14:17:40 2021

@author: Gabriela
"""


import xml.etree.ElementTree as ET

ID = ['Yo', 'Madre', 'Abuela Materna', 'Bisabuela Materna - Madre de Abuela', 
                 'Bisabuelo Materno - Padre de Abuela', 'Abuelo Materno', 
                 'Bisabuela Materna - Madre de Abuelo', 'Bisabuelo Materno - Padre de Abuelo',
                 'Padre', 'Abuela Paterna', 'Bisabuela Paterna - Madre de Abuela', 
                 'Bisabuelo Paterno - Padre de Abuela', 'Abuelo Paterno', 
                 'Bisabuela Paterna - Madre de Abuelo', 'Bisabuelo Paterno - Padre de Abuelo']


def datosXML(archivoXML):
    
    try:
        arbol = ET.parse(archivoXML)
        
    except IOError:
        print ('No se encuentra el archivo ', archivoXML)
        exit()
        
    except ET.ParseError:
        print("Error procesando en el archivo XML = ", archivoXML)
        exit()
       
    raiz = arbol.getroot()
    
    raiz = arbol.getroot()
    data=[]
    # Recorrido de los elementos del árbol
    
    for persona in raiz.iter('{http://www.uniovi.es}persona'):
        lugN = persona[0].find('{http://www.uniovi.es}lugarNacimiento').text
        fNac = persona[0].find('{http://www.uniovi.es}fechaNacimiento').text
        coorN = persona[0].find('{http://www.uniovi.es}coordenadasNacimiento')
        lugF = persona[0].find('{http://www.uniovi.es}lugarFallecimiento')
        fFac = persona[0].find('{http://www.uniovi.es}fechaFallecimiento')
        coorF = persona[0].find('{http://www.uniovi.es}coordenadasFallecimiento')
        desc = persona[0].find('{http://www.uniovi.es}comentario')
        foto = persona[0].find('{http://www.uniovi.es}fotografia').text
        video = persona[0].find('{http://www.uniovi.es}video')
        datos = persona.attrib
        datos['descripcion']=desc.text
        datos['foto']=foto
        if (coorN and lugN and fNac) is not None:
            latN, lonN, altN = coorN[0].text, coorN[1].text, coorN[2].text
            datos['lugN']=lugN
            datos['fNac']=fNac
            datos['latN']=latN
            datos['lonN']=lonN
            datos['altN']=altN
        if (coorF and lugF and fFac) is not None:
            latF, lonF, altF = coorF[0].text, coorF[1].text, coorF[2].text
            datos['lugF']=lugF.text
            datos['fFac']=fFac.text
            datos['latF']=latF
            datos['lonF']=lonF
            datos['altF']=altF
        else:
            datos['lugF']="NA"
            datos['fFac']="NA"
            datos['latF']="NA"
            datos['lonF']="NA"
            datos['altF']="NA"
        if video is not None:
            datos['video']=video.text
        else:
            datos['video']='NA'
        data.append(datos)
        
    return data
    
def prologoHTML(archivo, titulo):
    """ Escribe en el archivo de salida el prólogo del archivo KML"""

    archivo.write('<!DOCTYPE html>\n')
    archivo.write('<html lang="es">\n')
    archivo.write('<head>\n')
    archivo.write('<meta charset="UTF-8"/>\n')
    archivo.write('<title>'+titulo+'</title>\n')
    archivo.write('<meta name="autor" content="Dennis Gabriela Coy Calderón"/>\n')
    archivo.write('<meta name="viewport" content="width=device-width, initial-scale=1" />\n')
    archivo.write('<link rel="stylesheet" type="text/css" href="estilo.css" />\n')  
    archivo.write('</head>\n')
    archivo.write('<body>\n')
    archivo.write('<main>\n')
    archivo.write('<h1>'+titulo+'</h1>')

def contenidoHTML(archivo, datos, c):
    archivo.write("<h2>"+datos['nombre']+" ("+ID[c]+")</h2>\n")    
    archivo.write("<p>"+datos['descripcion'].replace('"', '')+"</p>\n")
    archivo.write("<h3>Datos</h3>\n")
    archivo.write("<p><strong>Lugar de Nacimiento:</strong> "+datos['lugN'].replace('"', '')+"</p>\n")
    archivo.write("<p><strong>Fecha Nacimiento:</strong> "+datos['fNac']+"</p>\n")
    archivo.write("<p><strong>Coordenadas Nacimiento:</strong>"+
                  datos['latN']+", "+datos['lonN']+datos['altN']+"</p>\n")
    if datos["lugF"]!="NA":
         archivo.write("<p><strong>Lugar de Fallecimiento:</strong> "+datos['lugF'].replace('"', '')+"</p>\n")
         archivo.write('<p><strong>Fecha Fallecimiento:</strong> '+datos['fFac']+'</p>\n')
         archivo.write("<p><strong>Coordenadas Fallecimiento:</strong> "+
                  datos['latF']+", "+datos['lonF']+datos['altF']+"</p>\n")
    archivo.write('<img src='+datos['foto']+' alt="Fotografia de '+datos['nombre']+'"/>\n')
    if datos['video']!="NA":
        archivo.write('<video controls preload="auto">')
        archivo.write('<source='+datos['video']+' type="video/mp4"/>\n')
        archivo.write('</video>')
    # Recorrido de los elementos del árbol
    
def añadirContenidoHTML(archivo, data):
    c = 0
    for datos in data:
        nombre = datos.get('nombre')+" "+datos.get('apellido')
        datos['nombre'] = nombre
        del datos['apellido']
        contenidoHTML(archivo, datos, c)
        c+=1

def epilogoHTML(archivo):
    """ Escribe en el archivo de salida el epílogo del archivo KML"""

    archivo.write("</body>\n")
    archivo.write('</main>\n')
    archivo.write("</html>\n") 

def main():
    
    archivo = input('Introduzca un archivo XML = ')
    
   # print(datosXML(archivo))
    
    nombreSalida  = input("Introduzca el nombre del archivo generado (*.html) = ")
    nombreHTML = input('Introduzca el nombre de la página = ')

    try:
        salida = open(nombreSalida + ".html",'w',encoding='utf-8')
    except IOError:
        print ('No se puede crear el archivo ', nombreSalida + ".html")
        exit()
    
    prologoHTML(salida, nombreHTML)
    añadirContenidoHTML(salida, datosXML(archivo))
    epilogoHTML(salida)
    salida.close()
    print('Documento '+nombreSalida+'.html creado exitosamente')

if __name__ == "__main__":
    main()   