import xml.etree.ElementTree as ET
from pathlib import Path

WIDTH = 1500  
HEIGHT = 700

def mapear(valor, in_min, in_max, out_min, out_max):
    if in_max == in_min:
        return (out_min + out_max) / 2
    return (valor - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Svg(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.raiz = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="2.0", width = str(self.width), height = str(self.height))
        
    def addLine(self,x1,y1,x2,y2,stroke,strokeWith):
        """
        Añade un elemento line
        """
        ET.SubElement(self.raiz,'line',
                      x1=x1,
                      y1=y1,
                      x2=x2,
                      y2=y2,
                      stroke=stroke,
                      strokeWith=strokeWith)

    def addPolyline(self,points,stroke,strokeWith,fill):
        """
        Añade un elemento polyline
        """
        ET.SubElement(self.raiz,'polyline',
                      points=points,
                      stroke=stroke,
                      strokeWith=strokeWith,
                      fill=fill)
        
    def addText(self,texto,x,y,fontFamily,fontSize,style):
        """
        Añade un elemento texto
        """
        ET.SubElement(self.raiz,'text',
                      x=x,
                      y=y,
                      fontFamily=fontFamily,
                      fontSize=fontSize,
                      style=style).text=texto

    def escribir(self,nombreArchivoSVG):
        """ de
        Escribe el archivo SVG con declaración y codificación
        """
        arbol = ET.ElementTree(self.raiz)
        
        """
        Introduce indentacióon y saltos de línea
        para generar XML en modo texto
        """
        ET.indent(arbol)
        
        arbol.write(nombreArchivoSVG, 
                    encoding='utf-8', 
                    xml_declaration=True
                    )

class Element:
    def __init__(self, altitud, distancia, texto):
        self.altitud = altitud
        self.distancia = distancia
        if texto is not None:
            self.nombre = texto
        else:
            self.nombre = ""

def crearSvg(archivoXML):
    try:
            
        arbol = ET.parse(archivoXML)
            
    except IOError:
        print('No se encuentra el archivo ', archivoXML)
        exit()
            
    except ET.ParseError:
        print("Error procesando en el archivo XML = ", archivoXML)
        exit()
           
    raiz = arbol.getroot()

    nombreSVG = "altimetria.svg"
    nuevoSVG = Svg(WIDTH, HEIGHT)

    coordenadas = ""
    elements = []

    # # Recorrido de puntos anónimos
    # for hijo in raiz.findall(".//{http://www.uniovi.es}punto-anon"): # Expresión XPath
    #     altitud = hijo.find("{http://www.uniovi.es}altitud").text
    #     distancia = float(hijo.find("{http://www.uniovi.es}distancia").text)
    #     nombre = hijo.get("nombre")
        
    #     elements.append(Element(altitud, distancia, nombre))

    # # Recorrido de hitos
    # for hijo in raiz.findall(".//{http://www.uniovi.es}hito"): # Expresión XPath
    #         altitud = hijo.find("{http://www.uniovi.es}altitud").text
    #         distancia = float(hijo.find("{http://www.uniovi.es}distancia").text)
    #         nombre = ""

    #         if hijo.find("{http://www.uniovi.es}puerto") is not None:
    #             puerto = hijo.find("{http://www.uniovi.es}puerto")
    #             nombre = puerto.find("{http://www.uniovi.es}nombre").text
    #         elif hijo.find("{http://www.uniovi.es}sprint-intermedio") is not None:
    #             nombre = hijo.find("{http://www.uniovi.es}sprint-intermedio").text
    #         else:
    #             nombre = hijo.find("{http://www.uniovi.es}sprint-bonificado").text
            
    #         elements.append(Element(altitud, distancia, nombre))

    # #Registrar salida y meta
    # salida = raiz.find(".//{http://www.uniovi.es}lugar-salida")
    # elements.append(Element(salida.find("{http://www.uniovi.es}altitud").text, 0, "Inicio"))

    # meta = raiz.find(".//{http://www.uniovi.es}lugar-meta")
    # elements.append(Element(meta.find("{http://www.uniovi.es}altitud").text, 192.8, "Final"))

    # Recorrido de puntos anónimos
    for hijo in raiz.findall(".//{http://www.uniovi.es}punto_anonimo"): # Expresión XPath
        altitud = hijo.find("{http://www.uniovi.es}altitud").text
        distancia = float(hijo.get("distancia_salida").replace(",", "."))
        nombre = hijo.get("nombre")

        elements.append(Element(altitud, distancia, nombre))

    # Recorrido de hitos
    for hijo in raiz.findall(".//{http://www.uniovi.es}puerto_montaña"): # Expresión XPath
        altitud = hijo.find("{http://www.uniovi.es}altitud").text
        distancia = float(hijo.get("distancia_salida").replace(",", "."))
        nombre = ""

        elements.append(Element(altitud, distancia, nombre))

    intermedio = raiz.find("{http://www.uniovi.es}sprint_intermedio")
    if intermedio is not None:
        altitud = intermedio.find("{http://www.uniovi.es}altitud").text
        distancia = float(hijo.get("distancia_salida").replace(",", "."))
        nombre = ""

        elements.append(Element(altitud, distancia, nombre))



    #Registrar salida y meta
    salida = raiz.find(".//{http://www.uniovi.es}posicion_inicio")
    elements.append(Element(salida.find("{http://www.uniovi.es}altitud").text, 0, "Inicio"))

    meta = raiz.find(".//{http://www.uniovi.es}posicion_fin")
    elements.append(Element(meta.find("{http://www.uniovi.es}altitud").text, 188, "Final"))    

    elements.sort(key = lambda x: x.distancia)

    for element in elements:
            #x = (float(element.distancia))+40
            x = (WIDTH-100)/188*float(element.distancia)+50
            #y = (HEIGHT-float(element.altitud))/6
            y = HEIGHT-(float(element.altitud))/3
            coordenadas += f"{x},{y} "
            if element.nombre != "":
                nuevoSVG.addText(element.nombre,str(x),str(y+20),'Verdana','55', "writing-mode: tb; glyph-orientation-vertical: 0;")
            
    
    nuevoSVG.addPolyline(coordenadas,'red','4','none') 
    """Creación del archivo en formato SVG"""
    nuevoSVG.escribir(nombreSVG)
    print("Creado el archivo: ", nombreSVG)
    

def main():
    
    print(Svg.__doc__)

    

    ruta_xml = Path(__file__).parent / "etapaEsquema.xml"

    crearSvg(ruta_xml)
    

    #nuevoSVG.addText('texto vertical','220','25','Verdana','55', "writing-mode: tb; glyph-orientation-vertical: 0;")
    
    
if __name__ == "__main__":
    main() 