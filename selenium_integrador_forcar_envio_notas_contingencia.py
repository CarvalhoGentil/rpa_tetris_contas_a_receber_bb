import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode
# chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
# chrome_options.add_argument("--window-size=1920,1200")  # Set the window size
driver = webdriver.Chrome()

driver.get("https://blue-flower-038511b0f.2.azurestaticapps.net/login")

wait = WebDriverWait(driver, 20)
login = 'marcos'
senha = 'integragn@production'

# Defina o caminho para o arquivo JSON
file_path = r'C:\Users\matheus.carvalho\OneDrive - Gentil Negócios\Área de Trabalho\integracao_contingencia\response.json'

# Verifique se o arquivo existe
if os.path.exists(file_path):
    # Abra e leia o arquivo JSON
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    # Crie uma lista para armazenar as chaves
    keys_list = list(data.keys())

    # Filtre a lista para incluir apenas chaves numéricas
    numeric_keys_list = [key for key in keys_list if key.isdigit()]

    print(numeric_keys_list)

# informações para lohar no loja digital
#TODO: passar isso para config
lista_credenciais =['/html/body/app-root/sb-login/sb-layout-auth/div/div[1]/main/div/div/div/div/div[2]/form/div[1]/input','/html/body/app-root/sb-login/sb-layout-auth/div/div[1]/main/div/div/div/div/div[2]/form/div[2]/input']
# Loop que preenche as credenciais para login
for index, credenciais in enumerate(lista_credenciais):
    campos = wait.until(EC.presence_of_element_located((By.XPATH, credenciais)))
    campos.click()
    time.sleep(1)
    campos.clear()
    time.sleep(1)
    if index == 0:
        user = 'marcos'
        campos.send_keys(user)
    else:
        password = 'integragn@production'
        campos.send_keys(password)
print('logado com sucesso')

botao_login = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/sb-login/sb-layout-auth/div/div[1]/main/div/div/div/div/div[2]/form/div[3]/button')))