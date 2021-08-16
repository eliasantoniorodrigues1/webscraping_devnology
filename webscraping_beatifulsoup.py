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
                # Por não estar conseguindo capturar os atributos de dados do elemento
                # 'p', optei por dar um find_all em todos os elementos span que continham
                # as classificações dos produtos e retornar um len da lista.
                'Rating': len(item.find_all('span', {'class': 'glyphicon glyphicon-star'})),
                'Link': 'https://webscraper.io' + item.find('a').get('href')
            }
            
            print(len(item.find_all('span', {'class': 'glyphicon glyphicon-star'})))
            total_produtos.append(produto.copy())
            produto.clear()

    # lista_ordenada pelo menor preço:
    lista_ordenada = sorted(
        total_produtos, key=itemgetter('Price'), reverse=False)

    # Gera json no diretório do projeto:
    with open('dados_produtos.json', 'w') as file:
        file.write(json.dumps(lista_ordenada, indent=4))
