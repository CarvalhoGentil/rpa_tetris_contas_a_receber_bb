import requests, json
import datetime
from datetime import datetime
import re
from util import HEADER_GMTEDI_BB,HEADER_EXTRATOS,HEADER_DOWNLOAD_EXTRATO
class ExtrairContasAReceber:
    """
        Essa classe tem por finalidade:
        1. Realizar o login no site Banco do Brasil - contas a pagar
        2. Navegar até a página com todos os extratos
        3. Clicar no extrato do dia de hoje
        4. Clicar em baixar
    """
    def execute(self):
        """ Realiza o fluxo de atividades da classe """
        formatted_date = self.encontrando_data()

        self.realizando_login(formatted_date)

    def encontrando_data(self):
        # Obtém a data do dia de hoje
        today = datetime.today()

        # Formata a data no formato desejado YYYYMMDD
        formatted_date = today.strftime('%Y%m%d')

        return formatted_date
    def realizando_login(self,formatted_date):
        """
        Método responsável por realizar o login no site loja digital
        """
        # Criando uma sessão requests
        session = requests.Session()
        # Obtendo o token de autenticação para logar no site
        payload = {
            'username': 'bb_essencia_921468386',
            'password': '12345678a',
            'scope':'sia:usuario GMTAUT01 GMTAUT02 GMTAUT03 GMTAUT04 GMTAUT05 GMTAUT06 GMTAUT07 GMTPTL00 GMTPTL01 GMTPTL02 GMTPTL03 GMTMON01 GMTMON02 GMTMON03 GMTMON04 GMTCAT02 GMTCAT03 GMTCAT04 GMTCAT05 GMTCAT06 GMTCAT07 GMTCAT08 GMTCAT09 GMTCAT10 GMTCAT17 GMTCAT18 GMTCAT19 GMTSIA01 GMTSIA02 GMTSIA03 catalogo:engine',
            'grant_type':'password'
        }
        url ='https://gmtedi.bb.com.br/gmt-autorizador-api/autoriza'

        response = session.post(url,headers=HEADER_GMTEDI_BB, data=payload)

        acces_token = response.text.split('"access_token":"')[1].split('"')[0]
        refresh_token = response.text.split('"refresh_token":"')[1].split('"')[0]

        # Acessando lista de extratos
        url_extratos = 'https://gmtedi.bb.com.br/gmt-sia-api/921468386/retorno/v2'

        HEADER_EXTRATOS['Authorization'] =f'Bearer {acces_token}'

        response = session.get(url_extratos,headers=HEADER_EXTRATOS)

        data = json.loads(response.text)

        data = data['arquivos']

        lista_extratos = ['841308803','841505071']
        
        HEADER_DOWNLOAD_EXTRATO['Cookie']=f'usuarioCadastro=%7B%22access_token%22%3A%22i{acces_token}%22%2C%22token_type%22%3A%22Bearer%22%2C%22expires_in%22%3A1800%2C%22refresh_token%22%3A%227293d{refresh_token}%22%2C%22scope%22%3A%22sia%3Ausuario%22%2C%22userData%22%3A%7B%22tipoUsuario%22%3A2%2C%22userAplicacao%22%3Anull%2C%22userExterno%22%3A%7B%22username%22%3A%22BB_ESSENCIA_921468386%22%2C%22mci%22%3A921468386%2C%22userImpessoal%22%3Atrue%7D%2C%22userInterno%22%3Anull%7D%2C%22data_expiracao%22%3A%222024-05-28T11%3A06%3A35.996-03%3A00%22%2C%22isUserAdmin%22%3A%22N%22%7D'


        for arquivos in data:
            nome = arquivos['nome']
            nome =str(nome)
            id = arquivos['id']
            # Regex para capturar as variáveis
            pattern = r'CNAB240\.C(\d{6,9})\.(\d{8})\d{8}\.\d{6}\.RET'
            # Encontrar as variáveis usando o regex
            match = re.match(pattern, nome)
            nome_regex = None
            data_regex = None
            if match:
                nome_regex = match.group(1)  # Captura C841308803
                data_regex = match.group(2)  # Captura 20240524

                print(f"\n nome: {nome_regex}")
                print(f'nome_comparadtivo: {lista_extratos[0]}, nome_comparativo: {lista_extratos[1]}')
                print('==========================================')
                print(f"data: {data_regex}")
                print(f"data_comparativa: {formatted_date}")

            if nome_regex == lista_extratos[0] and data_regex == formatted_date:
                url_baixar_extrato = f'https://gmtedi.bb.com.br/gmt-sia-api/921468386/retorno/57343267/{nome}'
                response = session.get(url_baixar_extrato,headers=HEADER_DOWNLOAD_EXTRATO)
            elif nome_regex == lista_extratos[1] and data_regex == formatted_date:
                url_baixar_extrato = f'https://gmtedi.bb.com.br/gmt-sia-api/921468386/retorno/57341871/{nome}'
                response = session.get(url_baixar_extrato,headers=HEADER_DOWNLOAD_EXTRATO)
executando = ExtrairContasAReceber().execute()