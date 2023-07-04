import os

import requests
from zipfile import ZipFile
from bs4 import BeautifulSoup


def download_file(link_arq:str, file_name:str) -> None:
    """Essa função baixa todos os arquivos de indicadores da sessão `Documentos`
    do site do Instituto Nacional da Propriedade Industrial
    (https://www.gov.br/inpi/pt-br/acesso-a-informacao/boletim-mensal/arquivos/documentos).
    """

    r = requests.get(link_arq)
    with open(file_name, 'wb') as f:
        f.write(r.content)


def unzip_file(file_name:str,)-> None:
    """Essa função faz a descompactação dos arquivos de indicadores baixados 
    da sessão `Documentos` do site do Instituto Nacional da Propriedade Industrial
    (https://www.gov.br/inpi/pt-br/acesso-a-informacao/boletim-mensal/arquivos/documentos) 
    """

    with ZipFile(file_name, 'r') as zip:
        zip.extractall(file_name.replace('.zip', ''))


def remove_file_zip(file_name:str)-> None:
    """Essa função remove os arquivos zipados.
    """

    if os.path.exists(file_name):
        os.remove(file_name)


def extract_data(delet_zip=True) -> None:
    """Essa função percorre as paginas da sessão `Documentos` do site do
    Instituto Nacional da Propriedade Industrial
    (https://www.gov.br/inpi/pt-br/acesso-a-informacao/boletim-mensal/arquivos/documentos)
    e extrai todos os arquivos de indicadores.
    """

    url = 'https://www.gov.br/inpi/pt-br/acesso-a-informacao/boletim-mensal/arquivos/documentos?b_start:int={}'
    num_page = 0

    while True:
        print(url.format(num_page))
        response = requests.get(url.format(num_page))
        site = BeautifulSoup(response.content, 'html.parser')
        
        # Obter tags dos arquivos:
        tag_geral = site.find('div', attrs={'class': 'entries'})
        tag_arquivo = tag_geral.find_all('a', attrs={'class': 'state-missing-value url'})

        for tag in tag_arquivo:

            if tag.text.endswith('.zip') and 'indicador' in tag.text.lower():
                file_name = tag.get_text()
                print('  ', file_name)
                
                file_page = tag.get('href')
                link_arq = f"{file_page.replace('/view', '')}/@@download/file/{file_name}"
                
                download_file(link_arq, file_name)

                unzip_file(file_name)
                
                if delet_zip == True:
                    remove_file_zip(file_name)

        num_page += 20

        # Checar tag de proxima pagina:
        tag_pages = site.find('ul', attrs={'class': 'paginacao listingBar'})
        page_end = tag_pages.find_all('span')[-1].get('class')
        stop = ['proximo', 'desabilitado']

        if (page_end == stop):
            break


if __name__=='__main__':
    extract_data()
