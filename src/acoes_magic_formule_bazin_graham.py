# Esse bot está definido para obter dados das ações do site fundamentos e depois realizar um ranking dos melhorores
# baseados em indicadores


from utils import *

# Passo 1: importando as libs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import math
from selenium.webdriver.common.action_chains import ActionChains

ATIVO_COLUMN = 'Papel'
COTACAO_COLUMN = 'Cotação'
PVP_COLUMN = 'P/VP'
DY_COLUMN = 'Div.Yield'
ROIC_COLUMN = 'ROIC'
ROE_COLUMN = 'ROE'
PL_COLUMN = 'P/L'
PSR_COLUMN = 'PSR'
PATRIMONIO_LIQUIDO_COLUMN = 'Liq.2meses'
VPA_COLUMN = 'vpa'
LPA_COLUMN = 'lpa'
MARGEM_LIQ_COLUMN = 'Mrg. Líq.'
MARGEM_EBIT_COLUMN = 'Mrg Ebit'
LIQ_CORRENTE_COLUMN = 'Liq. Corr.'
DIV_BRUTA_PATRIM_COLUMN = 'Dív.Brut/ Patrim.'
CRESC_RECEITA_5A = 'Cresc. Rec.5a'
GRAHAM_COLUMN = 'valor_justo_graham'
BAZIN_COLUMN = 'preco_teto_bazin'
MARGEM_SEGURANCA_BAZIN = 'margem_seguranca_bazin'
POTENCIAL_GRAHAM_COLUMN = 'potencial_graham'
EV_EBIT_COLUMN = 'EV/EBIT'
EV_EBITDA_COLUMN = 'EV/EBITDA'
P_EBIT_COLUMN = 'P/EBIT'
SEGMENTO_COLUMN = 'segmento'
RANK_DY_COLUMN = 'rank_dy'
RANK_ROE_COLUMN = 'rank_roe'
RANK_ROIC_COLUMN = 'rank_roic'
RANK_POTENCIAL_GRAHAM_COLUMN = 'rank_potencial_graham'
RANK_MARGEM_SEGURANCA_BAZIN_COLUMN = 'rank_margem_seguranca_bazin'
RANK_PVP_COLUMN = 'rank_pvp'
RANK_PL_COLUMN = 'rank_pl'
RANK_MARGEM_LIQ = 'rank_margem_liq'
RANK_DIV_BRUTA_PATRIM = 'rank_div_bruta_patrim'
RANK_CRESC_RECEITA_5A = 'rank_cresc_receita_5a'
RANK_LIQ_CORRENTE = 'rank_liq_corrente'
RANK_MARGEM_EBIT = 'rank_margem_ebit'
RANK_EV_EBIT = 'rank_ev_ebit'
RANK_EV_EBITDA = 'rank_ev_ebitda'
RANK_P_EBIT = 'rank_p_ebit'
RANK_RESULT = 'RANK_RESULTADO'


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

    # Passo 3: clicar no botão empresas
    botao_empresas = navegador.find_element(
        'xpath', '/html/body/div[1]/div[1]/div[1]/span/a[1]')
    navegador.execute_script("arguments[0].click();", botao_empresas)

    # Passo 4: clicar no botão buscar
    botao_buscar = navegador.find_element(
        'xpath', '/html/body/div[1]/div[2]/form/input')
    navegador.execute_script("arguments[0].click();", botao_buscar)

    # Passo 5: lendo os dados do html
    tabela_elemento = navegador.find_element(
        'xpath', '/html/body/div[1]/div[2]/table')

    html_tabela = tabela_elemento.get_attribute('outerHTML')

    tabela = pd.read_html(str(html_tabela))[0]
    tabela[COTACAO_COLUMN] = tabela[COTACAO_COLUMN] / 100
    tabela[LIQ_CORRENTE_COLUMN] = tabela[LIQ_CORRENTE_COLUMN] / 100
    tabela[DIV_BRUTA_PATRIM_COLUMN] = tabela[DIV_BRUTA_PATRIM_COLUMN] / 100
    # tabela[EV_EBIT_COLUMN] = tabela[EV_EBIT_COLUMN]/ 100
    # tabela[EV_EBITDA_COLUMN] = tabela[EV_EBITDA_COLUMN]/ 100
    # tabela[P_EBIT_COLUMN] = tabela[P_EBIT_COLUMN]/ 100
    print(tabela)
    tabela_customizada = tabela[[ATIVO_COLUMN,
                                COTACAO_COLUMN,
                                PL_COLUMN,
                                DY_COLUMN,
                                PVP_COLUMN,
                                ROIC_COLUMN,
                                ROE_COLUMN,
                                PATRIMONIO_LIQUIDO_COLUMN,
                                PSR_COLUMN,
                                MARGEM_EBIT_COLUMN,
                                MARGEM_LIQ_COLUMN,
                                LIQ_CORRENTE_COLUMN,
                                DIV_BRUTA_PATRIM_COLUMN,
                                CRESC_RECEITA_5A,
                                EV_EBIT_COLUMN,
                                EV_EBITDA_COLUMN,
                                P_EBIT_COLUMN
                                 ]]

    tabela_customizada[VPA_COLUMN] = 0.0
    tabela_customizada[LPA_COLUMN] = 0.0
    tabela_customizada[GRAHAM_COLUMN] = 0.0
    tabela_customizada[BAZIN_COLUMN] = 0.0
    tabela_customizada[POTENCIAL_GRAHAM_COLUMN] = 0.0
    tabela_customizada[MARGEM_SEGURANCA_BAZIN] = 0.0
    tabela_customizada[RANK_DY_COLUMN] = 0.0
    tabela_customizada[RANK_ROE_COLUMN] = 0.0
    tabela_customizada[RANK_ROIC_COLUMN] = 0.0
    tabela_customizada[RANK_POTENCIAL_GRAHAM_COLUMN] = 0.0
    tabela_customizada[RANK_MARGEM_SEGURANCA_BAZIN_COLUMN] = 0.0
    tabela_customizada[RANK_PVP_COLUMN] = 0.0
    tabela_customizada[RANK_PL_COLUMN] = 0.0
    tabela_customizada[RANK_MARGEM_LIQ] = 0.0
    tabela_customizada[RANK_CRESC_RECEITA_5A] = 0.0
    tabela_customizada[RANK_DIV_BRUTA_PATRIM] = 0.0
    tabela_customizada[RANK_LIQ_CORRENTE] = 0.0
    tabela_customizada[RANK_MARGEM_EBIT] = 0.0
    tabela_customizada[RANK_EV_EBIT] = 0.0
    tabela_customizada[RANK_EV_EBITDA] = 0.0
    tabela_customizada[RANK_P_EBIT] = 0.0

    tabela_customizada[RANK_RESULT] = 0.0
    tabela_customizada[SEGMENTO_COLUMN] = ''

    tabela_customizada.set_index(ATIVO_COLUMN)
    # print(tabela_customizada)
#################################################################################################################
    # tratando dados
#################################################################################################################
    tabela_customizada[PATRIMONIO_LIQUIDO_COLUMN] = formatar_valor(
        tabela_customizada[PATRIMONIO_LIQUIDO_COLUMN])
    tabela_customizada[PL_COLUMN] = formatar_valor(
        tabela_customizada[PL_COLUMN])
    tabela_customizada[PSR_COLUMN] = formatar_valor(
        tabela_customizada[PSR_COLUMN])
    tabela_customizada[EV_EBIT_COLUMN] = formatar_valor(
        tabela_customizada[EV_EBIT_COLUMN])
    tabela_customizada[EV_EBITDA_COLUMN] = formatar_valor(
        tabela_customizada[EV_EBITDA_COLUMN])
    tabela_customizada[P_EBIT_COLUMN] = formatar_valor(
        tabela_customizada[P_EBIT_COLUMN])
    # print(tabela_customizada)
    # Primeiro, substitua a virgula por ponto e remova o sinal de % e converta para float
    tabela_customizada[DY_COLUMN] = formatar_valor_percent(
        tabela_customizada[DY_COLUMN])
    tabela_customizada[ROIC_COLUMN] = formatar_valor_percent(
        tabela_customizada[ROIC_COLUMN])
    tabela_customizada[ROE_COLUMN] = formatar_valor_percent(
        tabela_customizada[ROE_COLUMN])
    tabela_customizada[MARGEM_EBIT_COLUMN] = formatar_valor_percent(
        tabela_customizada[MARGEM_EBIT_COLUMN])
    tabela_customizada[MARGEM_LIQ_COLUMN] = formatar_valor_percent(
        tabela_customizada[MARGEM_LIQ_COLUMN])
    tabela_customizada[CRESC_RECEITA_5A] = formatar_valor_percent(
        tabela_customizada[CRESC_RECEITA_5A])
#################################################################################################################
    # Filtros
#################################################################################################################
    tabela_filtro = tabela_customizada[tabela_customizada[PATRIMONIO_LIQUIDO_COLUMN] >= 1000000]
    # tabela_filtro = tabela_filtro[tabela_filtro[PVP_COLUMN] <= 900]
    # tabela_filtro_roe = tabela_filtro_pvp[tabela_filtro_pvp[ROE_COLUMN] >= 13]
    tabela_filtro = tabela_filtro[tabela_filtro[ROIC_COLUMN] >= 0]

    # ALGUNS SETORES COMO O BANCARIO TEM O PSR = 0
    # tabela_filtro_psr = tabela_filtro_roic[tabela_filtro_roic[PSR_COLUMN] >= 0]
    # tabela_filtro_dy = tabela_filtro_roic[tabela_filtro_roic[DY_COLUMN] >= 4]

    # ALGUNS SETORES COMO BANCARIOS E SEGUROS TEM ESSE INDICADOR = 0
    # tabela_filtro_margem_liq = tabela_filtro_psr[tabela_filtro_psr[MARGEM_LIQ_COLUMN] >= 0]
    # tabela_filtro_margem_ebit = tabela_filtro_margem_liq[
    #     tabela_filtro_margem_liq[MARGEM_EBIT_COLUMN] >= 0]
    # tabela_filtro_p_ebit = tabela_filtro_margem_ebit[tabela_filtro_margem_ebit[P_EBIT_COLUMN] <= 10]

    tabela_filtro_dy = tabela_filtro[tabela_filtro[DY_COLUMN] >= 4]

    # tabela_filtro_dy = tabela_filtro_dy.head(10)

    tabela_filtro_dy = remove_tasa(tabela_filtro_dy)

    tabela_filtro_dy = tabela_filtro_dy.sort_values(
        by=ROIC_COLUMN, ascending=False)
    tabela_filtro_dy[RANK_ROIC_COLUMN] = tabela_filtro_dy[ROIC_COLUMN].rank(
        ascending=False)

    tabela_filtro_dy = tabela_filtro_dy.sort_values(
        by=EV_EBIT_COLUMN, ascending=True)
    tabela_filtro_dy[RANK_EV_EBIT] = tabela_filtro_dy[EV_EBIT_COLUMN].rank(
        ascending=True)

    tabela_filtro_dy['RANK_MAGIC_FORMULE'] = tabela_filtro_dy[RANK_ROIC_COLUMN] + tabela_filtro_dy[RANK_EV_EBIT]

    tabela_filtro_dy = tabela_filtro_dy.sort_values(
        by='RANK_MAGIC_FORMULE', ascending=True)

    #FILTRANDO PELAS 50 MELHORES ACOES COLOCADAS
    tabela_filtro_dy = tabela_filtro_dy.head(50)

    for index, row in tabela_filtro_dy.iterrows():
        ativo = row[ATIVO_COLUMN]
        print(ativo)
        baseUrl = "https://statusinvest.com.br/acoes/{}"
        baseurl = baseUrl.format(ativo)
        print(baseurl)
        navegador.get(baseurl)
        try:
            preco_justo = float(preco_justo_graham(
                navegador, index, tabela_filtro_dy))
            tabela_filtro_dy.at[index,
                                SEGMENTO_COLUMN] = getSegmentoEmpresa(navegador)
            tabela_filtro_dy.at[index, GRAHAM_COLUMN] = preco_justo
            potencial = ((preco_justo/row[COTACAO_COLUMN])*100)-100
            tabela_filtro_dy.at[index, POTENCIAL_GRAHAM_COLUMN] = format2decimal(
                potencial)
            teto_bazin = format2decimal(preco_teto_bazim(navegador))
            print(f"bazin preco teto -> {teto_bazin}")
            tabela_filtro_dy.at[index, BAZIN_COLUMN] = teto_bazin
            tabela_filtro_dy.at[index,
                                MARGEM_SEGURANCA_BAZIN] = teto_bazin - row[COTACAO_COLUMN]
            print(f"mergem bazin -> {teto_bazin - row[COTACAO_COLUMN]}")

        except Exception as err:
            imprimir(f"Ocorreu um erro: {err}")
            tabela_filtro_dy.at[index, GRAHAM_COLUMN] = 0
            tabela_filtro_dy.at[index, POTENCIAL_GRAHAM_COLUMN] = 0

    #FAZER O RANK DE BAZIN E GHARAM
    tabela_filtro_dy = tabela_filtro_dy.sort_values(
        by=POTENCIAL_GRAHAM_COLUMN, ascending=False)
    tabela_filtro_dy[RANK_POTENCIAL_GRAHAM_COLUMN] = tabela_filtro_dy[POTENCIAL_GRAHAM_COLUMN].rank(
        ascending=False)

    tabela_filtro_dy = tabela_filtro_dy.sort_values(
        by=MARGEM_SEGURANCA_BAZIN, ascending=False)
    tabela_filtro_dy[RANK_MARGEM_SEGURANCA_BAZIN_COLUMN] = tabela_filtro_dy[MARGEM_SEGURANCA_BAZIN].rank(
        ascending=False)


    tabela_filtro_dy[RANK_RESULT] = tabela_filtro_dy[RANK_ROIC_COLUMN] + tabela_filtro_dy[RANK_EV_EBIT] + tabela_filtro_dy[RANK_POTENCIAL_GRAHAM_COLUMN] + tabela_filtro_dy[RANK_EV_EBIT] + tabela_filtro_dy[RANK_MARGEM_SEGURANCA_BAZIN_COLUMN]

    tabela_filtro_dy = tabela_filtro_dy.sort_values(
        by=RANK_RESULT, ascending=True)
    tabela_filtro_dy["RANK_POSICAO"] = tabela_filtro_dy[RANK_RESULT].rank(
        ascending=True)

    # # # Use o método to_csv para exportar o DataFrame para um arquivo CSV
    # nome_arquivo_csv = 'acoes.csv'
    # tabela_filtro_dy.to_csv(nome_arquivo_csv, index=False,  decimal=',')
    # Crie um arquivo Excel e adicione os DataFrames em abas separadas
    nome_arquivo = 'acoes_magic_formule_bazin_graham.xlsx'
    with pd.ExcelWriter(nome_arquivo) as writer:
        tabela_filtro_dy.to_excel(writer, sheet_name='Geral', index=False)

    # Remover repetições na coluna 'segmento'
    list_segmentos = tabela_filtro_dy[SEGMENTO_COLUMN].unique()
    # Remove os itens vazios da lista
    list_segmentos = list(filter(None, list_segmentos))
    print(f'list_segmentos: {list_segmentos}')
    # Percorrer os segmentos e cria uma abas com os dados do segmento corrente.
    for segmento in list_segmentos:
        print(f'segmento corrente: {segmento}')
        df_by_segmento = tabela_filtro_dy[tabela_filtro_dy[SEGMENTO_COLUMN] == segmento]
        print(df_by_segmento)
        with pd.ExcelWriter(nome_arquivo, mode='a') as writer:
            df_by_segmento.to_excel(
                writer, sheet_name=segmento[:30], index=False)

    print(tabela_filtro_dy)
    print(f"rows: {tabela_filtro_dy.shape[0]}")

    # Marca o tempo de término
    fimTempo = time.time()

    # Calcula o tempo decorrido
    tempo_decorrido = fimTempo - inicioTempo
    print(f"Tempo decorrido: {tempo_decorrido} segundos")


def formatar_valor(valor):
    # Remove todos os pontos e vírgulas da string
    valor_formatado = valor.str.replace(
        '.', '').str.replace(',', '').astype(float) / 100

    return valor_formatado


def formatar_valor_percent(valor):
    # Remove todos os pontos e vírgulas da string
    valor_formatado = valor.str.replace('.', '').str.replace(
        ',', '').str.replace('%', '').astype(float) / 100

    return valor_formatado


def preco_justo_graham(navegador, index, tabela_filtro_dy):
    print("[IN] - preco_justo_graham")

    vpa = navegador.find_element(
        'xpath', '/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[9]/div/div/strong').text

    vpa = vpa.replace(",", ".")

    vpa = float(vpa)
    print(f"vpa-> {vpa}")

    lpa = navegador.find_element(
        'xpath', '/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[11]/div/div/strong').text

    lpa = lpa.replace(",", ".")
    lpa = float(lpa)

    print(f"vpa-> {lpa}")

    tabela_filtro_dy.at[index, VPA_COLUMN] = vpa
    tabela_filtro_dy.at[index, LPA_COLUMN] = lpa

    num = 22.5 * lpa * vpa
    print(f"22.5 * lpa * vpa-> {num}")

    num_negativo = False
    if (num < 0):
        num = num * -1
        num_negativo = True

    raiz = math.sqrt(num)
    if (num_negativo):
        raiz = raiz * -1

    print(f"raiz-> {raiz}")
    valor_formatado = format2decimal(raiz)
    print(f"raiz valor_formatado -> {valor_formatado}")

    print("[OUT] - preco_justo_graham")
    return valor_formatado


def format2decimal(valor):
    return float("{:.2f}".format(valor))


def getSegmentoEmpresa(navegador):
    return navegador.find_element(
        'xpath', '/html/body/main/div[5]/div[1]/div/div[3]/div/div[3]/div/div/div/a/strong').text


def preco_teto_bazim(navegador):

    botao_5anos = navegador.find_element(
        'xpath', '/html/body/main/div[3]/div/div[1]/div/div[1]/div[2]/ul/li[2]/a')
    navegador.execute_script("arguments[0].scrollIntoView(true);", botao_5anos)
    time.sleep(1)

    navegador.execute_script("arguments[0].click();", botao_5anos)
    time.sleep(1)
    botao_agruparPorAno = navegador.find_element(
        'xpath', '/html/body/main/div[3]/div/div[1]/div/div[5]/label/span[2]')

    navegador.execute_script(
        "arguments[0].click();", botao_agruparPorAno)

    # Use ActionChains para mover o mouse sobre o elemento (hover)
    time.sleep(0.5)
    print(pyautogui.position())
    print(botao_agruparPorAno.location)
    x = 896
    y = 458
    # movendo o mouse para o grafico ano atual -1 e obtendo o devidendo desse ano
    pyautogui.moveTo(x, y, 0.5, pyautogui.easeOutQuad)

    dividendo_ano_menos_1 = navegador.find_element(
        'xpath', '/html/body/main/div[3]/div/div[1]/div/div[3]/div/div/div[2]/span[1]').text
    print(dividendo_ano_menos_1)

    # movendo o mouse para o grafico ano atual -2 e obtendo o devidendo desse ano
    pyautogui.moveTo(712, y, 0.5, pyautogui.easeOutQuad)
    time.sleep(0.5)
    dividendo_ano_menos_2 = navegador.find_element(
        'xpath', '/html/body/main/div[3]/div/div[1]/div/div[3]/div/div/div[2]/span[1]').text
    print(dividendo_ano_menos_2)

    # movendo o mouse para o grafico ano atual -3 e obtendo o devidendo desse ano
    pyautogui.moveTo(500, y, 0.5, pyautogui.easeOutQuad)
    time.sleep(0.5)
    dividendo_ano_menos_3 = navegador.find_element(
        'xpath', '/html/body/main/div[3]/div/div[1]/div/div[3]/div/div/div[2]/span[1]').text
    print(dividendo_ano_menos_3)

    # movendo o mouse para o grafico ano atual -4 e obtendo o devidendo desse ano
    pyautogui.moveTo(280, y, 0.5, pyautogui.easeOutQuad)
    time.sleep(0.5)
    dividendo_ano_menos_4 = navegador.find_element(
        'xpath', '/html/body/main/div[3]/div/div[1]/div/div[3]/div/div/div[2]/span[1]').text
    print(dividendo_ano_menos_4)
    time.sleep(0.5)
    dividendo_ano_menos_1 = dividendo_ano_menos_1.replace(
        "R$ ", "").replace(",", ".")
    dividendo_ano_menos_2 = dividendo_ano_menos_2.replace(
        "R$ ", "").replace(",", ".")
    dividendo_ano_menos_3 = dividendo_ano_menos_3.replace(
        "R$ ", "").replace(",", ".")
    dividendo_ano_menos_4 = dividendo_ano_menos_4.replace(
        "R$ ", "").replace(",", ".")

    dividendo_ano_menos_1 = float(dividendo_ano_menos_1 or 0)
    dividendo_ano_menos_2 = float(dividendo_ano_menos_2 or 0)
    dividendo_ano_menos_3 = float(dividendo_ano_menos_3 or 0)
    dividendo_ano_menos_4 = float(dividendo_ano_menos_4 or 0)

    print(dividendo_ano_menos_1)
    print(dividendo_ano_menos_2)
    print(dividendo_ano_menos_3)
    print(dividendo_ano_menos_4)

    soma_dividendos = (dividendo_ano_menos_1 + dividendo_ano_menos_2 +
                       dividendo_ano_menos_3 + dividendo_ano_menos_4)

    qtde_anos = 0
    if (dividendo_ano_menos_1 > 0):
        qtde_anos = qtde_anos + 1

    if (dividendo_ano_menos_2 > 0):
        qtde_anos = qtde_anos + 1

    if (dividendo_ano_menos_3 > 0):
        qtde_anos = qtde_anos + 1

    if (dividendo_ano_menos_4 > 0):
        qtde_anos = qtde_anos + 1

    print(f"qtde_anos-> {qtde_anos}")
    print(f"soma_dividendos-> {soma_dividendos}")
    media_dividendos = soma_dividendos / qtde_anos
    print(f"media_dividendos-> {media_dividendos}")

    metrica_barsi = 0.06

    preco_teto = media_dividendos / metrica_barsi
    # preco_teto = preco_teto.replace(".", ",")

    print(f"preco_teto-> {preco_teto}")

    return preco_teto


def remove_tasa(df):
    for index, row in df.iterrows():
        ativo = row[ATIVO_COLUMN]
        print(ativo)
        # removendo a tauros
        if ativo == 'TASA4':
            df = df.drop(index)
        if ativo == 'TASA3':
            df = df.drop(index)

    return df


execute()


# A formula magica no mercado de ações - Joel oWarnei yuld alterado
