import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "http://www.detro.rj.gov.br/operacao/empresas-de-onibus-intermunicipais-1_1497903715&pag={}"
headers = {'Agent-User': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
dataframes = []

for page in range(0, 100):
    url = base_url.format(page)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        site = BeautifulSoup(response.content, 'html.parser')
        div = site.find('div', class_='card shadow')
        elements = div.find_all(['h5', 'li', 'strong', 'p']) if div else []
        data = [item.get_text(strip=True) for item in elements]
        df = pd.DataFrame({'dados': data})
        dataframes.append(df)
    else:
        print(f"A solicitação para a página {page} falhou com o código de status {response.status_code}.")

result = pd.concat(dataframes)

result.to_excel('infos.xlsx', index=False)
print("Dados exportados para o arquivo 'infos.xlsx' com sucesso! Verifique na pasta de destino.")
