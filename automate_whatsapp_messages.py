from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def sendText(text):
    msg_box = driver.find_element(By.XPATH, "//div[@contenteditable='true' and @data-tab='10']")
    for line in text.split('\n'):
        msg_box.send_keys(line)
        msg_box.send_keys(Keys.SHIFT + Keys.ENTER)
    msg_box.send_keys(Keys.ENTER)
    # Pausar entre mensajes
    time.sleep(1)

# Configuración de Selenium
service = Service(executable_path='C:/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get("https://web.whatsapp.com")

# Pausa para escanear el código QR manualmente
input("Presiona Enter después de escanear el código QR y que se cargue WhatsApp Web completamente...")

# Buscar el chat de la persona una vez y seleccionarlo
search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
search_box.clear()
search_box.send_keys("Tia Yorlen")
time.sleep(2)  # Pausa para que se cargue la búsqueda

contact = driver.find_element(By.XPATH, f"//span[@title='Tia Yorlen']")
contact.click()

# Esperar a que se abra el chat
time.sleep(2)

# Leer el archivo de texto con los mensajes
with open('C:/Users/dago/Documents/ChatWhatsApp/Chat.txt', 'r', encoding='utf-8') as file:
    mensajes = file.readlines()

text_to_sent = ""
# Recorre cada mensaje y envíalo
for mensaje in mensajes:
    mensaje = mensaje.strip()  # Elimina espacios en blanco y saltos de línea
    print(mensaje)
    if not mensaje:  # Si la línea está vacía, omitirla
        continue
    
    if "(archivo adjunto)" in mensaje:
        # Vaciar mensaje previo antes de enviar la imagen
        if text_to_sent:
            sendText(text_to_sent)
            text_to_sent = ""

        image_path = "C:/Users/dago/Documents/ChatWhatsApp/" + mensaje[mensaje.find("IMG"):mensaje.find(" (archivo adjunto)")]

        attachment_box = driver.find_element(By.XPATH, "//div[@title='Attach']")
        attachment_box.click()
        time.sleep(1)
        
        file_input = driver.find_element(By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']")
        file_input.send_keys(image_path)
        time.sleep(1.2)

        send_button = driver.find_element(By.XPATH, "//span[@data-icon='send']")
        send_button.click()
        time.sleep(2)
        continue
    elif "Yorlen Audrey Ramirez" in mensaje:
        if text_to_sent:
            # Vaciar mensaje previo antes de llenar el nuevo mensaje
            sendText(text_to_sent)
            time.sleep(0.8)
        text_to_sent = mensaje[:mensaje.find(" - ")] + "\n"
        text_to_sent += mensaje[mensaje.find("Ramirez:")+8:] + "\n"
    else:
        text_to_sent += mensaje + "\n"

if text_to_sent:
    sendText(text_to_sent)
    text_to_sent = ""

# Cerrar el navegador
driver.quit()