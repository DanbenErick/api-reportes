# import mysql.connector
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import requests

def generar_pdf_service(inicio, fin, area, pdf):

    url = f"https://api-zszn.onrender.com/input-controls/obtener-padron-estudiantes/{inicio}/{fin}/{area}"
    # url = f"http://localhost:3500/input-controls/obtener-padron-estudiantes/{inicio}/{fin}/{area}"

    print("PRINT UTILLLLLLL =====================>",url)

    response = requests.get(url)

    if response.status_code == 200:
        # La petición fue exitosa
        # Acceder a los datos de la respuesta
        
        datos = response.json()
        # print(datos)
    else:
        # La petición falló
        print(f"Error: {response.status_code}")


    c = canvas.Canvas(f"{pdf}.pdf", pagesize=A4)
    width, height = A4

    # print("Datao DNI", datos[0]['DNI'])

    for i, data in enumerate(datos):
        # http_imagen = f'http:localhost:3500/{data['DNI']}/{data['DNI']}.jpg'
        

        c.setFont("Helvetica-Bold", 12) #tAMAÑO DE LA FUENTE Y TIPO DE LETRA
        c.drawString(30, height - 30, "UNIVERSIDAD NACIONAL DANIEL ALCIDES CARRION")  # Añadir texto al encabezado
        c.drawString(30, height - 50, "DIRECCION DE ADMISION")
        c.drawString(30, height - 70, "CEPRE III - 2024")
        c.drawString(30, height - 90, "PADRON DE POSTULANTES")
        c.drawString(30, height - 110, f"AREA {area}")
        #Tamaño y espaciado de las fuentes
        c.setFont("Helvetica", 10) 
        c.setFont("Helvetica-Bold", 10)
        c.drawString(33, height - 140 - ((i % 4) * 150), f"CODIGO/DNI: {data['DNI']}")  # Ajustar la posición de los datos
        c.drawString(160, height - 170 - ((i % 4) * 150), f"APELLIDO PATERNO: {data['AP_PATERNO']}")
        c.drawString(160, height - 190 - ((i % 4) * 150), f"APELLIDO MATERNO: {data['AP_MATERNO']}")
        c.drawString(160, height - 210 - ((i % 4) * 150), f"NOMBRES: {data['NOMBRES']}")
        c.setFont("Helvetica-Bold", 8) 
        c.drawString(160, height - 230 - ((i % 4) * 150), f"ESCUELA: {data['ESCUELA_COMPLETA']}")
        c.drawString(160, height - 250 - ((i % 4) * 150), f"MODALIDAD: {data['NOMBRE_MODALIDAD']}")

        # Dibujar un rectángulo a la izquierda para la foto
        c.rect(30, height - 270 - ((i % 4) * 150), 120, 120)   

        # Dibujar un rectángulo para la huella digital
        c.rect(480, height - 220 - ((i % 4) * 150), 70, 70)
        c.drawString(500, height - 270 - ((i % 4) * 150), 'FIRMA')
        c.rect(480, height - 258 - ((i % 4) * 150), 70, 1, stroke=1)
        c.line(50, height - 279 - ((i % 4) * 150), width - 50, height - 279 - ((i % 4) * 150))

        # Agregar pie de página
        c.setFont("Helvetica", 8)
        c.drawString(30, 30, datetime.now().strftime("%d/%m/%Y"))  # Fecha
        c.drawCentredString(width / 2, 30, "ADMISION")  # Texto centrado "ADMISION"
        c.drawString(width - 100, 30, f"Página {i + 1}")  # Número de página

        # Crear una nueva página cada 4 resultados
        if (i + 1) % 4 == 0 and i != 0:
            c.showPage()#Persona por pagina

    # Guardar el PDF
    c.save()
    return f"{pdf}.pdf"
    

    