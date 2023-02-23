import sys
import openai
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import QPixmap, QImage

# Establecer la clave de API
openai.api_key = "tu api key"


# Clase principal de la aplicación
class GeneradorImagenes(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Crear widgets
        self.label = QLabel("Prompt:")
        self.lineedit = QLineEdit()
        self.boton = QPushButton("Crear")
        self.imagen = QLabel()

        # Crear layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.label)
        hbox.addWidget(self.lineedit)
        hbox.addWidget(self.boton)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.imagen)

        self.setLayout(vbox)

        # Conectar señal "clicked" del boton con el slot "crearImagen"
        self.boton.clicked.connect(self.crearImagen)

        # Configurar ventana principal
        self.setWindowTitle("Generador de imágenes")
        self.setGeometry(300, 300, 600, 400)

    # Slot que se ejecuta al hacer clic en el boton "Crear"
    def crearImagen(self):
        # Obtener el texto del prompt ingresado por el usuario
        prompt = self.lineedit.text()

        # Enviar solicitud a DALL-E y obtener la imagen generada
        response = openai.Image.create(
            prompt=prompt,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        
        # Descargar la imagen y convertirla a formato QImage
        response = requests.get(image_url)
        image = QImage.fromData(response.content)
        image_data = response.content

        # Guardar el contenido de la variable en un archivo en el disco
        with open("imagen.jpg", "wb") as f:
            f.write(image_data)

        # Mostrar la imagen en el lienzo
        pixmap = QPixmap.fromImage(image)
        self.imagen.setPixmap(pixmap)
        return image_url

   

# Funcion principal
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeneradorImagenes()
    window.show()
    sys.exit(app.exec_())

