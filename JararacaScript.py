from bs4 import BeautifulSoup as bs
from requests import get
import pandas as pd
from os import replace


def dados_orientador(url, id=0):
    """Função que retorna os dados do orientador"""
    page = get(url)
    soup = bs(page.text, "html.parser")
    nome = soup.find("h2", attrs={"itemprop": "name"}).text
    tabela = soup.find("table", attrs={"id": "table-profile-ascendants"})
    linhas = tabela.findAll("tr")
    valores = [id, nome]
    anos = ""
    for l in linhas[1:]:
        dado = l.findAll("td")
        linha = [tr.text for tr in dado]
        linha[1] = limpa_nome(linha[1])
        linha[2] = limpa_nome(linha[2])
        anos += linha[2]
    for i in limpa_ano(anos):
        valores.append(i)
    divs = soup.findAll("div", attrs={"class": "has-extra-margin-bottom"})
    infos = divs[2].findAll("li", attrs={"class": "is-size-5"})
    lista = []
    for info in infos[:-1]:
        dado = info.text
        lista.append(limpa_nome(dado))
    for dado in lista:
        valor = ""
        for i in dado:
            if i.isdigit():
                valor += i
        valores.append(int(valor))
    return valores


def criar_arquivos(url):
    """Função que cria o arquivo csv com os cabeçalhos"""
    nodes = pd.DataFrame(
        columns=["Id", "Nome", "Tipo", "Ano", "Ds", "IG", "Fc", "Ft", "G", "R", "Pr"]
    )
    dados = dados_orientador(url)
    nome = dados[1]
    nodes.loc[len(nodes)] = dados
    nodes.to_csv("nodes.csv", index=False)
    edges = pd.DataFrame(columns=["Source", "Target"])
    edges.to_csv("edges.csv", index=False)
    with open("links.txt", "w") as file:
        file.write(url)
    return nome


def nomear_arquivos(nome, nodes="nodes.csv", edges="edges.csv", links="links.txt"):
    replace(nodes, f"{nome}_nodes.csv")
    replace(edges, f"{nome}_edges.csv")
    replace(links, f"{nome}_links.txt")


def criar_tabela(url, arquivo="nodes.csv", id=0):
    """Função que cria uma tabela com os dados dos orientados de um professor"""
    page = get(url)
    soup = bs(page.text, "html.parser")
    tabela = soup.find("table", attrs={"id": "table-profile-descendants"})
    plan = pd.DataFrame(
        columns=["Id", "Nome", "Tipo", "Ano", "Ds", "IG", "Fc", "Ft", "G", "R", "Pr"]
    )
    linhas = tabela.findAll("tr")
    links = []
    txt = []
    i = 1
    for l in linhas[1:]:
        dado = l.findAll("td")
        linha = [tr.text for tr in dado]
        linha[1] = limpa_nome(linha[1])
        linha[2] = limpa_nome(linha[2])
        linha[0] = int(linha[0])
        linha[3] = int(linha[3])
        orientacao = limpa_ano(linha[2])
        linha.insert(3, orientacao[1])
        linha[2] = orientacao[0]
        linha[0] = i + len(pd.read_csv(arquivo)) - 1
        html = l.find("a", attrs={"itemtype": "http://schema.org/Person"})
        link = "https://plataforma-acacia.org" + html["href"]
        if not duplicado(link):
            plan.loc[len(plan)] = linha  # Adiciona a linha na tabela
            i += 1
            txt.append(link)
            if linha[4] > 0 and not duplicado(
                link
            ):  # Verifica se o orientado tem orientados
                links.append([link, int(linha[0])])
    print(f"Baixando dados de: {linha[1]}")
    plan.to_csv(arquivo, mode="a", header=False, index=False)
    define_edges(plan, id)  # Chama a função para definir as arestas
    """Ver a ordenação"""
    for link in txt:
        adicionar_cache(link)
    for link in links:
        criar_tabela(link[0], "nodes.csv", link[1])  # Recursão


def adicionar_cache(link):
    with open("links.txt", "a") as myfile:
        myfile.write("\n" + link)


def duplicado(link):
    with open("links.txt") as file:
        lines = [line.rstrip() for line in file]
    if link in lines:
        return True
    else:
        return False


def limpa_nome(nome):
    """Função que limpa o nome dos orientados"""
    nome = nome.replace("\n", "")
    nome = nome.replace("  ", "")
    return nome


def limpa_ano(str):
    """Função que limpa o ano dos orientados"""
    if len(str) > 5:  # Tratamento para o caso de ter dois anos
        ano1 = int(str[1:5])
        ano2 = int(str[6:10])
        if ano1 <= ano2:
            ano = ano1
            tipo = str[0]
        else:
            ano = ano2
            tipo = str[5]
    else:
        ano = int(str[1:5])
        tipo = str[0]
    return tipo, ano


def define_edges(plan, id):
    """Função que define as arestas"""
    tabela = pd.DataFrame(columns=["Source", "Target"])
    final = len(pd.read_csv("edges.csv"))
    for i in range(len(plan)):
        tabela.loc[len(plan)] = [id, final + i + 1]
        tabela.to_csv("edges.csv", mode="a", header=False, index=False)


def limpa_arquivo(arquivo="nodes.csv"):
    """Função que limpa o arquivo para ficar apenas com os dados necessários"""
    plan = pd.read_csv(arquivo)
    plan.drop(["IG", "Fc", "Ft", "G", "R", "Pr"], axis=1, inplace=True)
    plan.to_csv(arquivo, index=False)


def add_ano_ord(arquivo="nodes.csv"):
    plan = pd.read_csv(arquivo)
    ano_i = int(plan["Ano"][0])
    ano_ord = []
    for ano in plan["Ano"]:
        ano_ord.append(int(ano) - ano_i + 1)
    plan["Ano_Ord"] = ano_ord
    plan.to_csv(arquivo, index=False)


def main():
    print("\nBem-vindo ao JararacaScript!")
    print(
        "\nEste programa irá baixar os dados de orientação de um professor por meio da Plataforma Acácia"
    )
    url = input("\nPor favor, insira a URL do professor que deseja baixar os dados: ")
    # url = "https://plataforma-acacia.org/profile/tereza-maria-de-azevedo-pires-serio/"
    # url = "https://plataforma-acacia.org/profile/isaias-pessotti/"
    # url = "https://plataforma-acacia.org/profile/silvia-tatiana-maurer-lane/"
    # url = "https://plataforma-acacia.org/profile/carolina-martuscelli-bori/"
    # url = "https://plataforma-acacia.org/profile/maria-do-carmo-guedes/"
    nome = criar_arquivos(url)
    print(f"\nBaixando dados de orientação de: {nome}\n")
    criar_tabela(url)
    limpa_arquivo()  # Limpa o arquivo para ficar apenas com os dados necessários
    add_ano_ord()
    nomear_arquivos(nome)
    print("\nOs dados foram baixados com sucesso!")
    print("\nOs arquivos gerados foram:")
    print(f"{nome}_nodes.csv")
    print(f"{nome}_edges.csv")
    print(f"{nome}_links.txt")
    print("\nObrigado por usar o JararacaScript!")


main()
