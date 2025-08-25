import requests
import pandas as pd
import bs4 as bs

def buscar_tramites(link):
    header = {'User-Agent':'andrezao'}

    try:
        print(link)
        res = requests.get(link, headers=header, timeout=30)
        res.encoding = response.apparent_encoding
        texto = res.text
        taquigrafica = bs.BeautifulSoup(texto, 'html.parser')
        
        return taquigrafica.text.replace("\r", "").replace("\t", "").replace("\n", "")
    except:
        print("burro")
        return -1;

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0",
}

params = {
    "txOrador": "",
    "txPartido": "",
    "txUF": "",
    "dtInicio": "",
    "dtFim": "",
    "txTexto": "Internet",
    "txSumario": "",
    "basePesq": "plenario",
    "CampoOrdenacao": "dtSessao",
    "PageSize": "50",
    "TipoOrdenacao": "DESC",
    "btnPesq": "Pesquisar",
}

response = requests.get(
    "https://www.camara.leg.br/internet/sitaqweb/resultadoPesquisaDiscursos.asp",
    params=params,
    headers=headers,
)

html = bs.BeautifulSoup(response.text, "html.parser")

tabela = html.find("table")
elementos = tabela.find_all("tr", {"class": "even"})
raspados = []

for celula in elementos:
    try:
        data = celula.find_all("td")[0].text
        sessao = celula.find_all("td")[1].text.strip()
        fase = celula.find_all("td")[2].text.strip()
        link = "https://www.camara.leg.br/internet/sitaqweb/" + elementos[0].find_all(
            "td"
        )[3].a["href"].replace("\r", "").replace("\t", "").replace("\n", "")
        nome = celula.find_all("td")[5].text.strip().replace(", -----", "")
        raspados.append(
            {"data": data, "sessao": sessao, "fase": fase, "link": link, "nome": nome}
        )
        raspados["text"] = buscar_tramites(raspados["link"])
    except:
        continue

# taquigrafia = buscar_tramites('https://www.camara.leg.br/internet/sitaqweb/TextoHTML.asp?etapa=5&nuSessao=155.2025&nuQuarto=4557408&nuOrador=1&nuInsercao=1&dtHorarioQuarto=22:48&sgFaseSessao=OD&Data=20/08/2025&txApelido=Gilson%20Marques&txFaseSessao=Ordem%20do%20Dia&txTipoSessao=Ordin%C3%A1ria%20-%20CD&dtHoraQuarto=22:48&txEtapa=')
frame = pd.DataFrame(raspados)
print(frame)