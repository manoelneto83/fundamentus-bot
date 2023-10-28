import pyautogui
import pyperclip
import time
import datetime

from io import BytesIO
import win32clipboard
from PIL import Image
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from os import environ, path, curdir
from dotenv import load_dotenv
# pyautogui.click -> clicar
# pyautogui.press -> apertar 1 tecla
# pyautogui.hotkey -> conjunto de teclas
# pyautogui.write -> escrever um texto

# Pre-Requisitos:
# Esse Robô assume que na máquina tenha o chorme instalado
# o webdriver para uso do selemium
# o rocket.chat para enviar a mensagem para cada integrante do time.

# [ok] 1 -  abrir no navegador
# [ok] 2 - abrir o redmine
# [ok] 3 - fazer login
# [ok] 4 - abrir a visão de horas
# [ok] 5 - realizar consulta
# [ok] 6 - fazer printscreen da tela
# [ok] 7 - enviar no rocket para cada usuário.
# [ok] 8 - melhorar os logs com data e hora formatada
# [ok] 9 - salvar os logs
# capturar erros
# enviar logs de execução por email.
# melhorar funcao de wait para esperar por algumas tentativas.

# configurando os logs
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(message)s',
#                     filename=f"./logs/{datetime.datetime.now().strftime('%Y-%m-%d %Hh%Mm%Ss')}-xerife.logs",
#                     filemode="w")

# imprimi uma mensagem na ela


def imprimir(mensagem):
    # logging.debug("====================================")
    # logging.debug(mensagem)
    print("====================================")
    print(mensagem)
    # print("====================================")

# função faz o click na imagem passada no parametro


def click(image, left=0):
    wait(image)
    pos = pyautogui.locateOnScreen(image, confidence=0.9)
    print(f"posicao image {pos}")
    # print(pos)

    if (pos != None):
        x, y = pyautogui.center(pos)
        x = x - left
        pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)
        time.sleep(1)
        pyautogui.click(x, y)
        imprimir("fiz o click em x e y")

# aguarda ate a imagem passada aparecer na tela.


def wait(image):
    while not pyautogui.locateOnScreen(image, confidence=0.9):
        time.sleep(1)
        imprimir("esperando 1s...")


def openAndMaximizedApp(pathApp, secondsToMaximized):
    pyautogui.hotkey("win", "r")
    time.sleep(0.3)
    # pyautogui.write(pathApp)
    # time.sleep(0.5)
    pyperclip.copy(pathApp)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.3)
    pyautogui.press("enter")
    time.sleep(secondsToMaximized)

    # imprimir("Maximizando a aplicacao...")
    # pyautogui.hotkey("alt", "space")
    # time.sleep(0.5)
    # pyautogui.press("x")
    # time.sleep(1)


def send_to_clipboard(filePath):
    image = Image.open(filePath)
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()


def openChrome():
    # Find .env file
    basedir = path.abspath(curdir)
    load_dotenv(path.join(basedir, '.env'))

    path_web_driver = environ.get('PATH_WEB_DRIVER')

    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    navegador = webdriver.Chrome(executable_path=path_web_driver, chrome_options=options, service=Service(
        ChromeDriverManager().install()))  # openChrome()
    time.sleep(0.5)
    navegador.maximize_window()
    return navegador
