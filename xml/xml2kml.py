import xml.etree.ElementTree as ET
from pathlib import Path

def asignarColor(tipo):
    if tipo == "puerto":
        return "ff00ff00"
    elif tipo == "intermedio" or tipo=="bonificado":
        return "ffff0000"
    elif tipo == "meta" or tipo == "salida":
        return "ff0000ff"
    elif tipo == "anonimo":
        return "ff00ffff" 

class Kml(object):
    
    def __init__(self):
        
        self.raiz = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
        self.doc = ET.SubElement(self.raiz,'Document')

    def addPlacemark(self,nombre,long,lat,alt, color):
        """
        Añade un elemento <Placemark> con puntos <Point>
        """
        pm = ET.SubElement(self.doc,'Placemark')
        ET.SubElement(pm,'name').text = nombre

        st = ET.SubElement(pm, 'Style')
        icon_style = ET.SubElement(st, 'IconStyle')
        ET.SubElement(icon_style, 'scale').text = '1.0'
        ET.SubElement(icon_style, 'color').text = color

        punto = ET.SubElement(pm,'Point')
        ET.SubElement(punto,'coordinates').text = '{},{},{}'.format(long,lat,alt)

    def addLineString(self,nombre,extrude,tesela, listaCoordenadas, modoAltitud, color, ancho):
        """
        Añade un elemento <Placemark> con líneas <LineString>
        """
        ET.SubElement(self.doc,'name').text = nombre
        pm = ET.SubElement(self.doc,'Placemark')
        ls = ET.SubElement(pm, 'LineString')
        ET.SubElement(ls,'extrude').text = extrude
        ET.SubElement(ls,'tessellation').text = tesela
        ET.SubElement(ls,'coordinates').text = listaCoordenadas
        ET.SubElement(ls,'altitudeMode').text = modoAltitud 

        estilo = ET.SubElement(pm, 'Style')
        linea = ET.SubElement(estilo, 'LineStyle')
        ET.SubElement (linea, 'color').text = color
        ET.SubElement (linea, 'width').text = ancho

    def escribir(self,nombreArchivoKML):
        """
        Escribe el archivo KML con declaración y codificación
        """
        arbol = ET.ElementTree(self.raiz)
        """
        Introduce indentacióon y saltos de línea
        para generar XML en modo texto
        """
        ET.indent(arbol)
        arbol.write(nombreArchivoKML, encoding='utf-8', xml_declaration=True)
    

class Element:
    def __init__(self, longitud, latitud, altitud, distancia, tipo_de_elemento):
        self.longitud = longitud
        self.latitud = latitud
        self.altitud = altitud
        self.distancia = distancia
        self.tipo_de_elemento = tipo_de_elemento
        self.color = asignarColor(tipo_de_elemento)

        

def verXPath(archivoXML):
    
    try:
        
        arbol = ET.parse(archivoXML)
        
    except IOError:
        print('No se encuentra el archivo ', archivoXML)
        exit()
        
    except ET.ParseError:
        print("Error procesando en el archivo XML = ", archivoXML)
        exit()
       
    raiz = arbol.getroot()

    nombreKML = "etapa.kml"
        
    nuevoKML = Kml()

    coordenadasPaseo = ""
    elements = []

    # Recorrido de puntos anónimos
    for hijo in raiz.findall(".//{http://www.uniovi.es}punto_anonimo"): # Expresión XPath
        latitud = hijo.find("{http://www.uniovi.es}latitud").text.replace(",", ".")
        longitud = hijo.find("{http://www.uniovi.es}longitud").text.replace(",", ".")
        altitud = hijo.find("{http://www.uniovi.es}altitud").text
        distancia = float(hijo.get("distancia_salida").replace(",", "."))
        

        elements.append(Element(longitud, latitud, altitud, distancia, "anonimo"))
        #nuevoKML.addPlacemark("", longitud, latitud, altitud)
        #coordenadasPaseo += f"{longitud},{latitud},0.0\n"

    # Recorrido de hitos
    for hijo in raiz.findall(".//{http://www.uniovi.es}puerto_montaña"): # Expresión XPath
            latitud = hijo.find("{http://www.uniovi.es}latitud").text.replace(",", ".")
            longitud = hijo.find("{http://www.uniovi.es}longitud").text.replace(",", ".")
            altitud = hijo.find("{http://www.uniovi.es}altitud").text
            distancia = float(hijo.get("distancia_salida").replace(",", "."))
            tipo = "puerto"
            
            elements.append(Element(longitud, latitud, altitud, distancia, tipo))

    intermedio = raiz.find("{http://www.uniovi.es}sprint_intermedio")
    if intermedio is not None:
        latitud = intermedio.find("{http://www.uniovi.es}latitud").text.replace(",", ".")
        longitud = intermedio.find("{http://www.uniovi.es}longitud").text.replace(",", ".")
        altitud = intermedio.find("{http://www.uniovi.es}altitud").text
        distancia = float(hijo.get("distancia_salida").replace(",", "."))
        tipo = "intermedio"

        elements.append(Element(longitud, latitud, altitud, distancia, tipo))



    #Registrar salida y meta
    salida = raiz.find(".//{http://www.uniovi.es}posicion_inicio")
    elements.append(Element(salida.find("{http://www.uniovi.es}longitud").text.replace(",", "."), salida.find("{http://www.uniovi.es}latitud").text.replace(",", ".")
                            , salida.find("{http://www.uniovi.es}altitud").text, 0, "salida"))

    meta = raiz.find(".//{http://www.uniovi.es}posicion_fin")
    elements.append(Element(meta.find("{http://www.uniovi.es}longitud").text.replace(",", "."), meta.find("{http://www.uniovi.es}latitud").text.replace(",", ".")
                                , meta.find("{http://www.uniovi.es}altitud").text, 188, "meta"))

    elements.sort(key = lambda x: x.distancia)
    for element in elements:
        nuevoKML.addPlacemark("", element.longitud, element.latitud, element.altitud, element.color)
        # FOR TESTING print("Current element distance: ", element.distancia)
        coordenadasPaseo += f"{element.longitud},{element.latitud},0.0\n"

    nuevoKML.addLineString("Etapa 13","1","1",
                               coordenadasPaseo,'relativeToGround',
                               '#ff0000ff',"5")
    
    nuevoKML.escribir(nombreKML)
    print("Creado el archivo: ", nombreKML)
        

def main():

    ruta_xml = Path(__file__).parent / "etapaEsquema.xml"

    verXPath(ruta_xml) 

if __name__ == "__main__":
    main() 