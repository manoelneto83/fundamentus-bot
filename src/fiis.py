# Esse bot está definido para obter dados dos fiis do site fundamentos e depois realizar um ranking dos melhorores
# baseados em indicadores

# import pyautogui
# import pyperclip
# import time
# import datetime
# import logging
# from selenium.webdriver.common.keys import Keys
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import random
# from selenium.common.exceptions import NoSuchElementException
from utils import *
# from os import environ, path, curdir
# from dotenv import load_dotenv

# Passo 1: importando as libs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

ATIVO_COLUMN = 'Papel'
SEGMENTO_COLUMN = 'Segmento'
COTACAO_COLUMN = 'Cotação'
DY_COLUMN = 'Dividend Yield'
PVP_COLUMN = 'P/VP'
LIQUIDEZ_COLUMN = 'Liquidez'
QTDE_IMOVEIS = 'Qtd de imóveis'

# SEGMENTOS
# Híbrido
# Lajes Corporativas
# Logística
# Outros
# Shoppings
# Títulos e Val. Mob.


# Passo 2: requisicoes web
# driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
navegador = openChrome()
navegador.get("https://www.fundamentus.com.br/")

# Passo 3: clicar no botão fii
botao_fii = navegador.find_element(
    'xpath', '/html/body/div[1]/div[1]/div[1]/span/a[2]')
navegador.execute_script("arguments[0].click();", botao_fii)

# Passo 4: clicar no botão buscar
botao_buscar = navegador.find_element(
    'xpath', '/html/body/div[1]/div[2]/form/input')
navegador.execute_script("arguments[0].click();", botao_buscar)

# Passo 5: lendo os dados do html
tabela_elemento = navegador.find_element(
    'xpath', '/html/body/div[1]/div[2]/table')

html_tabela = tabela_elemento.get_attribute('outerHTML')

tabela = pd.read_html(str(html_tabela))[0]
tabela[COTACAO_COLUMN] = tabela[COTACAO_COLUMN].str.replace(',', '').str.replace('.', '').astype(float) / 100

tabela_customizada = tabela[[ATIVO_COLUMN,
                             SEGMENTO_COLUMN,
                             COTACAO_COLUMN,
                             DY_COLUMN,
                             PVP_COLUMN,
                             LIQUIDEZ_COLUMN,
                             QTDE_IMOVEIS]]

tabela_customizada.set_index(ATIVO_COLUMN)
# print(tabela_customizada)  
# Primeiro, remova os pontos da coluna de liquidez e converta para float
tabela_customizada[LIQUIDEZ_COLUMN] = tabela_customizada[LIQUIDEZ_COLUMN].str.replace(
    '.', '').astype(float)
    
# print(tabela_customizada)
# Primeiro, substitua a virgula por ponto e remova o sinal de % e converta para float
tabela_customizada[DY_COLUMN] = tabela_customizada[DY_COLUMN].str.replace(
    ',', '.').str.replace('%', '').astype(float)

# print(tabela_customizada)
# Filtrando pela quantidade de imoveis superior ou igual a 5
# fiis_qtd_imoveis_maior_que_5 = tabela_customizada[ tabela_customizada['Qtd de imóveis'] >= 5]

# Filtrando pela liquidez superior ou igual a 500 mil
fiis_liquidez_maior_que_500_mil = tabela_customizada[tabela_customizada[LIQUIDEZ_COLUMN] >= 500000]

# Filtrando pela DY superior ou igual a 7%
# fiis_dy_maior_que_6_perc = fiis_liquidez_maior_que_500_mil[ (fiis_liquidez_maior_que_500_mil['Dividend Yield'] >= 7) & (fiis_liquidez_maior_que_500_mil['Segmento'] == 'Shoppings')]
fiis_dy_maior_que_6_perc = fiis_liquidez_maior_que_500_mil[(
    fiis_liquidez_maior_que_500_mil[DY_COLUMN] >= 7)]

fiis_dy_maior_que_6_perc_ordenado_dy = fiis_dy_maior_que_6_perc.sort_values(
    by=DY_COLUMN, ascending=False)


# tabela10 = tabela.head(10)
fiis_dy_maior_que_6_perc_ordenado_dy['rank_dy'] = fiis_dy_maior_que_6_perc_ordenado_dy[DY_COLUMN].rank(
    ascending=False)

fiis_dy_maior_que_6_perc_ordenado_pvp = fiis_dy_maior_que_6_perc_ordenado_dy.sort_values(
    by=PVP_COLUMN, ascending=True)

fiis_dy_maior_que_6_perc_ordenado_pvp['rank_pvp'] = fiis_dy_maior_que_6_perc_ordenado_pvp[PVP_COLUMN].rank(
)
# print(fiis_dy_maior_que_6_perc_ordenado_pvp)
fiis_dy_maior_que_6_perc_ordenado_pvp['metodo2em1'] = (
    fiis_dy_maior_que_6_perc_ordenado_pvp['rank_dy'] + fiis_dy_maior_que_6_perc_ordenado_pvp['rank_pvp'])

resultado = fiis_dy_maior_que_6_perc_ordenado_pvp.sort_values(
    by='metodo2em1', ascending=True)

nome_arquivo_csv = 'meu_dataframe.csv'

# Use o método to_csv para exportar o DataFrame para um arquivo CSV
resultado.to_csv(nome_arquivo_csv, index=False,  decimal=',')

# print(resultado)
print(f"rows: {resultado.shape[0]}")

# A formula magica no mercado de ações - Joel oWarnei yuld alterado
# Filtros

# 1 - Filtrar para remover os dy menor que 6%
# 2 - Filtrar para remover os fiis de pouca liquidez, menor de 500 mil cai fora.
# 3 - ordenar o dy do maior para o menor
# 4 - rank de dy - criar uma nova coluna que vai ser numerado para cada registro 1, 2, 3, 4 ...
# 5 - orderna o p/vp do menor para o maior
# 6 - rank de p/vp - criar uma nova coluna que vai ser numerado para cada registro 1, 2, 3, 4 ...
# 7 - soma dos 2 ranks
# 8 - ordernar pegar do menor para o maior
# 9 - Analisar por seguimento não pode comprar um segmento com outro.


# tabela_ordenada = tabela2.sort_values(by = "Cotação", ascending= True)

# tabela_ordenada['rank_cotacao'] = tabela_ordenada['Cotação'].rank()
# print(tabela_ordenada.head(10))
