import os

# Obtém o diretório do script
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Lista todos os arquivos no diretório
arquivos_no_diretorio = os.listdir(diretorio_atual)

# Remove arquivos executáveis
for arquivo in arquivos_no_diretorio:
    if arquivo.endswith(".exe"):
        caminho_arquivo = os.path.join(diretorio_atual, arquivo)
        try:
            os.remove(caminho_arquivo)
            print(f"Arquivo removido com sucesso: {caminho_arquivo}")
        except Exception as e:
            print(f"Erro ao remover o arquivo {caminho_arquivo}: {e}")
