import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import re
import os
import pyautogui

data = time.strftime("%d/%m/%Y")
# Criação de ano e mes
data_ano = time.strftime("%Y")
data_mes = time.strftime("%m")
# Criação de lista para o dicionário
meses_por_extenso = {
    "01": "1 - JANEIRO",
    "02": "2 - FEVEREIRO",
    "03": "3 - MARÇO",
    "04": "4 - ABRIL",
    "05": "5 - MAIO",
    "06": "6 - JUNHO",
    "07": "7 - JULHO",
    "08": "8 - AGOSTO",
    "09": "9 - SETEMBRO",
    "10": "10 - OUTUBRO",
    "11": "11 - NOVEMBRO",
    "12": "12 - DEZEMBRO"
}
# Laço que encontra o mês por extenso
data_mes = meses_por_extenso.get(data_mes, data_mes)

# Transformando data em string
data_str = str(data)

# Criação das opções do chromedriver
chrome_options = Options()

# Caminho para o Chrome instalado no PC
chrome_options.binary_location = r"C:\\Program Files\\Google\\Chrome\Application\\chrome.exe"

# download_dir = f"F://7. Sap Extratos//SAP - Extratos para a Contabilidade//BANCO DO BRASIL//ESSENCIA//{data_ano}//{data_mes}"
download_dir = 'C://projects//Request_marketing//dist'

chrome_prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "profile.default_content_setting_values.automatic_downloads": 1,  # Permitir múltiplos downloads
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("prefs", chrome_prefs)

# Caminho para o chromedriver
chrome_driver_path = r"C:\\Users\\matheus.carvalho\\OneDrive - Gentil Negócios\\Área de Trabalho\\Coisasuteis\\chromedriver-win64\\chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Caminho para o site
driver.get("https://gmtedi.bb.com.br/")

wait = WebDriverWait(driver, 20)

time.sleep(1)

# Definir o tamanho da janela do navegador
driver.maximize_window()

class ExtracaoBBNotasAPagar:
    """"
    Classe para extrair as notas a pagar do site do BB
    """
    def __init__(self, driver, download_dir):
        self.driver = driver
        self.download_dir = download_dir

    def execute(self):
        # Extraindo as contas
        self.extraindo_contas_a_pagar(data_str)

    def pegar_arquivos_em_diretorios(self):
        return set(os.listdir(self.download_dir))

    def esperar_download_concluir(self, timeout=30):
        arquivos_antes = self.pegar_arquivos_em_diretorios()
        tempo_fim = time.time() + timeout

        while time.time() < tempo_fim:
            arquivos_depois = self.pegar_arquivos_em_diretorios()
            novo_arquivo = arquivos_depois - arquivos_antes
            if novo_arquivo:
                return novo_arquivo.pop()
            time.sleep(1)
        return None

    def encontrar_elemento_autogui(self,botao_download):

        cordenadas = botao_download.location
        x = cordenadas['x']
        cordenadas = botao_download.location
        y = cordenadas['y']
        pyautogui.moveTo(x, y)

        pyautogui.click()

        return None

    def extraindo_contas_a_pagar(self, data_str):
        # Trecho relativo ao Login, se executado pelo método com Webdriver
        lista_credenciais = [
            '/html/body/app/div[1]/login/div/form/input[1]',
            '/html/body/app/div[1]/login/div/form/input[2]'
        ]
        # Loop que preenche as credenciais para login
        for index, credenciais in enumerate(lista_credenciais):
            campos = wait.until(EC.presence_of_element_located((By.XPATH, credenciais)))
            campos.click()
            time.sleep(1)
            campos.clear()
            time.sleep(1)
            if index == 0:
                user = 'BB_ESSENCIA_921468386'
                campos.send_keys(user)
            else:
                password = '12345678a'
                campos.send_keys(password)
        # Botão de login clicável para logar no site
        botao_login = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app/div[1]/login/div/form/button')))
        botao_login.click()
        time.sleep(2)
        # Botão para acessar a lista de extratos a pagar
        botao_download = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app/div[1]/home/div/div/div[2]/div/div[1]')))
        botao_download.click()
        time.sleep(2)
        # Ordenar extratos para o mais atual
        ordenar_extrato = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app/div[1]/download/div/table/thead/tr/th[3]/button')))
        ordenar_extrato.click()
        ordenar_extrato.click()

        # Corpo central da tabela
        tbody = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app/div[1]/download/div/table/tbody')))

        # Elementos a serem iterados
        linhas = tbody.find_elements(By.XPATH, './tr')

        # Lista de números procurados
        numeros_procurados = ['841505071', '841308803']
        contador_downloads = 0
        # Itera pelos números procurados
        for numero_procurado in numeros_procurados:
            contador = 0

            # iterar por todos os elementos da tabela para encontrar o número
            for linha in linhas:
                contador += 1
                # Armazena o texto do elemento para encontrar o número
                numero = linha.find_element(By.XPATH, './/td[@class="col-md-2 text-left"]').text
                # Armazena a data do elemento para procurar a data da nota
                data = linha.find_element(By.XPATH, './/td[@class="col-md-1 text-center"]').text
                texto_data = data
                match_data = re.search(r'(\d{2}/\d{2}/\d{4})', texto_data)
                if match_data:
                    texto_data = match_data.group(1)
                # Armazena o texto encontrado em uma variável
                texto_numero = numero
                match_numero = re.search(r'Contrato (\d+) -', texto_numero)
                if match_numero:
                    texto_numero = match_numero.group(1)
                # Compara o número encontrado para saber se é o mesmo procurado
                if numero_procurado == texto_numero and texto_data == data_str:
                    # Encontra o botão apra o donwlaod do arquivo
                    botao_download = wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/app/div[1]/download/div/table/tbody/tr[{contador}]/td[7]/button')))
                    # Scroll até o elemento
                    driver.execute_script("arguments[0].scrollIntoView();", botao_download)

                    # Clica no botão para baixar o arquivo
                    self.encontrar_elemento_autogui(botao_download)

                    arquivo_nome = self.esperar_download_concluir()
                    print('a')
                    if arquivo_nome is not None:
                        print(f'Arquivo baixado: {arquivo_nome}')
                    else:
                        print('Erro ao baixar o arquivo')
                    contador_downloads += 1
                    # Exibir o número de downloads
                    print(f'Quantidade de downloads: {contador_downloads}')
                    break

if __name__ == '__main__':
    extracao = ExtracaoBBNotasAPagar(driver, download_dir)
    extracao.execute()
