# Esse bot está definido para se integrar com o rocket web chat

import pyautogui
import pyperclip
import time
import datetime
import logging
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from selenium.common.exceptions import NoSuchElementException
from utils import *
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

"""App configuration."""


# Find .env file
basedir = path.abspath(curdir)
load_dotenv(path.join(basedir, '.env'))

# configura o tempo de forma global
pyautogui.PAUSE = 0.5
login_user_redmine = environ.get('LOGIN_USER_REDMINE')
login_password_redmine = environ.get('LOGIN_PASSWORD_REDMINE')
login_user_rocket = environ.get('LOGIN_USER_ROCKET')
login_password_rocket = environ.get('LOGIN_PASSWORD_ROCKET')

path_img = "./src/img/"
path_web_driver = environ.get('PATH_WEB_DRIVER')
horasAlvo = 6
# configurando os logs
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(message)s',
                    filename=f"./logs/{datetime.datetime.now().strftime('%Y-%m-%d %Hh%Mm%Ss')}-cotacaoAcoes.log",
                    filemode="w")


ativos = [
    # "TASA4", //bloqueado na phoebus
    "POSI3",
    "USIM5",
    "BBAS3",
    "TAEE11",
    "SAPR11",
    "TRPL4",
    "VIVT3",
    "VALE3",
    "PETR4",
    "TECN3",
    "KLBN4",
    "RANI3",
    "BMGB4",
    "MRFG3",
    "CMIG4",
    "CBAV3",
    "CMIN3",
    "ITSA4",
    "CPLE3",
    "ITUB4",
    "GOAU4",
    "KEPL3",
    "SANB11",
    "BBSE3",
    "AESB3",
    "UNIP6",
    "BRKM5",

]

celulas = [
    # "D25", #tauros bloqueado na phoebus
    "D18",
    "D19",
    "D20",
    "D21",
    "D22",
    "D23",
    "D24",
    "D25",
    "D26",
    "D37",
    "D38",
    "D39",
    "D40",
    "D41",
    "D42",
    "D43",
    "D44",
    "D45",
    "D46",
    "D30",
    "D31",
    "D32",
    "D47",
    "D48",
    "D49",
    "D50",
    "D51",


]

celulas_p_vp = [
    "I18",
    "I19",
    "I20",
    "I21",
    "I22",
    "I23",
    "I24",
    "I25",
    "I26",
    "I37",
    "I38",
    "I39",
    "I40",
    "I41",
    "I42",
    "I43",
    "I44",
    "I45",
    "I46",
    "I30",
    "I31",
    "I32",
    "I47",
    "I48",
    "I49",
    "I50",
    "I51",


]

links = [
    # "https://investidor10.com.br/acoes/{}/", //taurus bloqueado na phoebus
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",
    "https://investidor10.com.br/acoes/{}/",

]


def execute():
    for i in range(len(ativos)):
        try:
            imprimir(f"Iniciando o fluxo para o ativo: {ativos[i]}")
            time.sleep(5)
            imprimir("Abrindo o navegador chrome...")
            # openAndMaximizedApp("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", 0)
            navegador = openChrome()

            linkAtual = links[i].format(ativos[i])
            pyperclip.copy(linkAtual)
            url = pyperclip.paste()
            navegador.get(url)

            cotacao_atual = navegador.find_element(
                'xpath', '//*[@id="cards-ticker"]/div[1]/div[2]/div/span').text
            cotacao_atual = cotacao_atual.replace("R$ ", "")

            p_vp = navegador.find_element(
                'xpath', '//*[@id="cards-ticker"]/div[3]/div[2]/span').text

            imprimir(f"cotacao atual {cotacao_atual}")
            imprimir(f"p_vp atual {p_vp}")

            openAndMaximizedApp(
                "https://docs.google.com/spreadsheets/d/1ND_kM4sd0P3joJg4OSjFw4-6pYz4xL04aEpmZAkIn04/edit#gid=271190194", 5)

            # so pra tirar o mouse de cima da imagem
            pyautogui.moveTo(100, 100)

            time.sleep(5)
            click(f"{path_img}input_celula.png", 25)
            time.sleep(1)

            imprimir(f"selecionando celula {celulas[i]}")
            pyautogui.write(celulas[i])
            pyautogui.press("enter")
            imprimir(f"escrevendo cotação atual")
            pyautogui.write(cotacao_atual)
            pyautogui.press("enter")
            # so pra tirar o mouse de cima da imagem
            pyautogui.moveTo(100, 100)

            # escrevendo o p/vp
            time.sleep(1)
            click(f"{path_img}input_celula.png", 25)
            time.sleep(0.5)

            imprimir(f"selecionando celula {celulas_p_vp[i]}")
            pyautogui.write(celulas_p_vp[i])
            pyautogui.press("enter")
            imprimir(f"escrevendo p/vp atual {p_vp}")
            pyautogui.write(p_vp)
            pyautogui.press("enter")
            # so pra tirar o mouse de cima da imagem
            pyautogui.moveTo(100, 100)

            imprimir("fechando navegador...")
            navegador.quit()

        except Exception as err:
            imprimir(f"Ocorreu um erro: {err}")
            raise

    imprimir("fim Acoes")


execute()
