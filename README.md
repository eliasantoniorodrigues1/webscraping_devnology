## Devnology - Webscraping Beautifulsoup :snake:

### Coleta dados do Notebook Lenovo:

#### Bibliotecas utilizadas:

- Beautifulsoup

- Operator

- Requests

- Os

- Json

- RE

  

O objetivo inicial é coletar as informações em background sem a necessidade de abertura do browser.

Gerar um objeto contendo todos os produtos da página de **Laptops** e percorrer esse objeto coletando:

- Título do produto
- Descrição
- Preço
- Análises
- Link para acesso direto a página

Foram criadas algumas funções para facilitar a manutenção do processo e simplificar o código

##### Funções:

**obtem_dados**: Gera um objeto soup a partir de uma url recebida.

**remove_sinais_monetarios**: Essa função foi criada para facilitar a conversão do preço dos produtos no tipo float, para que dessa forma fosse ordenado de forma correta os produtos do menor preço para o maior.

**Parâmetros**: Recebe uma string e retorna um flooat

**gera_json**: Função para gerar um arquivo json da coleta realizada no site [webscraper.io] ( https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops ) no diretório base do projeto, para facilitar o consumo dos dados por uma REST API Ful.

**Parâmetros**: Recebe o caminho completo do arquivo, um dicionário, inteiro para definir a quantidade de indentação do json.



