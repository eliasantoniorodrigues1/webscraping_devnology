from bs4 import BeautifulSoup
from operator import itemgetter
import requests
import os
import re
import json


def obtem_dados(url):
    """
        param: url
        Recebe uma url e retorna um objeto soup para coleta das informações 
        no site.
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    return soup


def remove_sinais_monetarios(string):
    """
        Recebe uma string e retorna um float
        param: string
        return: float
    """

    # Essa expressão regular remove os caracteres que não são digitos
    # Espaços, R$
    string = re.sub(r'[^0-9.,]', '', string)
    try:
        valor = float(string)
    except Exception:
        valor = float(string.replace(',', '.'))

    return valor


def gera_json(fullpathfile, dicionario, indent):
    """
        Recebe o caminho completo do arquivo, um dicionário e
        a indentação desejada no arquivo.
        param: fullpathfile
        param: dicionario
        param: ident
    """
    with open(fullpathfile, 'a+', encoding='utf-8') as file:
        json.dump(dicionario, file, indent=indent)


if __name__ == '__main__':

    # Diretório padrão do projeto
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Link base:
    url = 'https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops'
    soup = obtem_dados(url)

    # Pesquisar notebook:
    marca = 'lenovo'

    # Classe base do css contendo todo o conteúdo dos produtos => (thumbnail):
    resultados = soup.find_all('div', {'class': 'thumbnail'})

    # Consolidação das informações coletadas:
    total_produtos = []
    for item in resultados:
        # Testa se o título do produto é igual a marca pesquisada:
        marca_prod_pesquisado = item.find('a', {'class': 'title'}).text
        if marca in marca_prod_pesquisado.lower():
            # Dicionário contendo as informações do produto:
            produto = {
                'Title': item.find('a', {'class': 'title'}).text.replace('...', '').strip(),
                'Description': item.find('p', {'class': 'description'}).text.strip(),
                # Trata os preços dos produtos de string para float:
                'Price': remove_sinais_monetarios(
                    item.find('h4',
                              {'class': 'pull-right price'}).text),
                'Reviews': item.find('p', {'class': 'pull-right'}).text.strip(),
                'Link': 'https://webscraper.io' + item.find('a').get('href')
            }

            total_produtos.append(produto.copy())
            produto.clear()

    # lista_ordenada:
    lista_ordenada = sorted(
        total_produtos, key=itemgetter('Price'), reverse=False)
    for produto in lista_ordenada:
        gera_json(os.path.join(BASE_DIR, 'dados_produtos.json'), produto, 4)
