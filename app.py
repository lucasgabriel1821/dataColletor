import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "http://www.detro.rj.gov.br/operacao/empresas-de-onibus-intermunicipais-1_1497903715&pag={}"
dataframes = []

for page in range(0, 100):
    url = base_url.format(page)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        div = soup.find('div', class_='card shadow')
        elements = div.find_all(['h5', 'li', 'strong']) if div else []
        data = [item.get_text(strip=True) for item in elements]
        df = pd.DataFrame({'data': data})
        dataframes.append(df)
    else:
        print(f"A solicitação para a página {page} falhou com o código de status {response.status_code}.")

result = pd.concat(dataframes)

result.to_excel('dados.xlsx', index=False)
print("Dados exportados para o arquivo 'dados.xlsx' com sucesso.")
