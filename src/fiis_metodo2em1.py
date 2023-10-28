from utils import *

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
def execute():
    # Marca o tempo de início
    inicioTempo = time.time()

    # Passo 2: requisicoes web
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
    tabela[COTACAO_COLUMN] = tabela[COTACAO_COLUMN].str.replace(
        ',', '').str.replace('.', '').astype(float) / 100

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
    # Filtrando pela quantidade de imoveis superior ou igual a 5, fundos de papeis não tem imoveis
    # fiis_qtd_imoveis_maior_que_5 = tabela_customizada[tabela_customizada[QTDE_IMOVEIS] >= 3]

    # Filtrando pela liquidez superior ou igual a 500 mil
    fiis_liquidez_maior_que_500_mil = tabela_customizada[
        tabela_customizada[LIQUIDEZ_COLUMN] >= 500000]

    # Filtrando pela DY superior ou igual a 7%
    # fiis_dy_maior_que_6_perc = fiis_liquidez_maior_que_500_mil[ (fiis_liquidez_maior_que_500_mil['Dividend Yield'] >= 7) & (fiis_liquidez_maior_que_500_mil['Segmento'] == 'Shoppings')]
    fiis_dy_maior_que_6_perc = fiis_liquidez_maior_que_500_mil[(
        fiis_liquidez_maior_que_500_mil[DY_COLUMN] >= 6)]

    fiis_dy_maior_que_6_perc_ordenado_dy = fiis_dy_maior_que_6_perc.sort_values(
        by=DY_COLUMN, ascending=False)


    # tabela10 = tabela.head(10)
    fiis_dy_maior_que_6_perc_ordenado_dy['rank_dy'] = fiis_dy_maior_que_6_perc_ordenado_dy[DY_COLUMN].rank(
        ascending=False)

    df_resultado = fiis_dy_maior_que_6_perc_ordenado_dy.sort_values(
        by=PVP_COLUMN, ascending=True)

    df_resultado['rank_pvp'] = df_resultado[PVP_COLUMN].rank()
    # print(df_resultado)
    df_resultado['metodo2em1'] = (
        df_resultado['rank_dy'] + df_resultado['rank_pvp'])

    resultado = df_resultado.sort_values(by='metodo2em1', ascending=True)

    df_resultado['rank_posicao'] = df_resultado['metodo2em1'].rank()

    nome_arquivo = 'fiis.xlsx'

    # Use o método to_csv para exportar o DataFrame para um arquivo CSV
    # resultado.to_csv(nome_arquivo_csv, index=False,  decimal=',')

    with pd.ExcelWriter(nome_arquivo) as writer:
        df_resultado.to_excel(writer, sheet_name='Geral', index=False)

    # Remover repetições na coluna 'segmento'
    list_segmentos = df_resultado[SEGMENTO_COLUMN].unique()
    # Remove os itens vazios da lista
    list_segmentos = list(filter(None, list_segmentos))
    print(f'list_segmentos: {list_segmentos}')
    # Percorrer os segmentos e cria uma abas com os dados do segmento corrente.
    for segmento in list_segmentos:
        print(f'segmento corrente: {segmento}')
        df_by_segmento = df_resultado[df_resultado[SEGMENTO_COLUMN] == segmento]
        print(df_by_segmento)
        if not (df_by_segmento.empty):
            with pd.ExcelWriter(nome_arquivo, mode='a') as writer:
                df_by_segmento.to_excel(
                    writer, sheet_name=segmento[:30], index=False)

    print(df_resultado)
    print(f"rows: {df_resultado.shape[0]}")

    # Marca o tempo de término
    fimTempo = time.time()

    # Calcula o tempo decorrido
    tempo_decorrido = fimTempo - inicioTempo
    print(f"Tempo decorrido: {format2decimal(tempo_decorrido)} segundos")

    # print(resultado)
    print(f"rows: {resultado.shape[0]}")

def format2decimal(valor):
    return float("{:.2f}".format(valor))

execute()
# A formula magica no mercado de ações - Joel oWarnei yuld alterado
# Filtros