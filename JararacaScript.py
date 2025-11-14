import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs
from time import sleep, time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
}


def get_ascendants_data(url):
    global matrix
    values = [
        len(matrix),
        bs(get(url, headers=headers).text, "html.parser")
        .find("h2", attrs={"itemprop": "name"})
        .text,
    ]
    tags = bs(get(url, headers=headers).text, "html.parser").find_all(
        "div", attrs={"class": "tags has-addons"}
    )
    for tag in tags[1]:
        if tag != "\n":
            values.append(tag.text.strip().replace("\n", ""))
    values.append(False)
    table = (
        bs(get(url, headers=headers).text, "html.parser")
        .find("div", attrs={"class": "columns is-gapless"})
        .find_all("div", attrs={"class": "column is-narrow"})
    )
    for div in table:
        div_data = div.find_all("td", attrs={"class": "has-text-right"})
        values += [data.text for data in div_data]
    values = [int(i) if type(i) == str and i.isdigit() else i for i in values]
    matrix.append(values)


def get_table_data(url: str) -> list:
    """Fetch data from the table in the given URL."""
    current_try = 1
    timeout = 2
    max_tries = 5
    while current_try <= max_tries:
        try:
            table = (
                bs(get(url, headers=headers).text, "html.parser")
                .find("table", attrs={"id": "table-profile-descendants"})
                .find_all("tr")
            )
            break
        except AttributeError:
            wait_time = timeout**current_try
            print(
                f"Tentativa {current_try} falhou. Tentando novamente em {wait_time} segundos..."
            )
            sleep(wait_time)
            current_try += 1
    return table


def get_descendants_data(url: str, id: int = 0):
    """Fetch profile data from the given URL."""
    global matrix
    global cache
    table_rows = get_table_data(url)
    links = []
    for row in table_rows[1:]:
        link = (
            "https://plataforma-acacia.org"
            + row.find("a", attrs={"itemtype": "http://schema.org/Person"})["href"]
        )
        if link in cache:
            continue
        table_data = row.find_all("td")
        data = [td.text.strip().replace("\n", "") for td in table_data]
        data[0] = len(matrix)
        orientation = choose_orientation(data[2])
        data.pop(2)
        data[2:2] = orientation
        print(f"\nSalvando dados de: {data[1]}")
        data = [int(i) if type (i) == str and i.isdigit() else i for i in data]
        matrix.append(data)
        print(f"O processo está {progress():.2f}% completo")
        edges.append((id, len(matrix) - 1))
        cache.append(link)
        if data[5] > 0:
            links.append((link, len(matrix) - 1))
    for link in links:
        get_descendants_data(link[0], link[1])


def get_columns_from_table(url: str) -> list:
    """Extract column names from the table in the given URL."""
    table_rows = get_table_data(url)
    columns = [column.text.strip() for column in table_rows[0].find_all("th")]
    columns[0] = "ID"
    columns[2] = "Tipo"
    columns.insert(3, "Ano")
    columns.insert(4, "Coorientação")
    return columns


def choose_orientation(
    orientations: str,
) -> list:
    """Choose the first orientation or coorientation from the given string."""
    orientations = orientations.replace(" ", "")
    if len(orientations) == 5:
        return [orientations[0], orientations[1:5], False]
    elif len(orientations) == 7:
        return [orientations[0], orientations[1:5], True]

    def parse_orientation(str_orientations: str) -> list:
        """Parse the orientation string into a list of orientations."""
        list_of_orientations = []
        for i in range(len(str_orientations)):
            if str_orientations[i] in "MDP":
                type = str_orientations[i]
                year = str_orientations[i + 1 : i + 5]
                orientation = [type, year, False]
                list_of_orientations.append(orientation)
            elif str_orientations[i] in "C":
                orientation[2] = True
        return list_of_orientations

    choosed_orientation = None
    orientations = parse_orientation(orientations)
    for orientation in orientations:
        if not orientation[2]:
            choosed_orientation = orientation
            return choosed_orientation
    if choosed_orientation is None:
        return orientations[0]

def progress() -> float:
    """Calculate the progress percentage based on the number of nodes."""
    total_nodes = len(matrix)
    total = matrix[0][5] + 1
    return (total_nodes / total) * 100

start_time = time()
matrix = []
edges = []
cache = []
print("\nBem-vindo ao JararacaScript!")
print(
        "\nEste programa irá baixar os dados de orientação de um professor por meio da Plataforma Acácia"
    )
url = input("\nPor favor, insira a URL do professor que deseja baixar os dados: ")
# Example URL:
# url = "https://plataforma-acacia.org/profile/tereza-maria-de-azevedo-pires-serio/"
get_ascendants_data(url)
name = matrix[0][1]
print(f"\nOrientador: {name}")
get_descendants_data(url)

df_nodes = pd.DataFrame(matrix, columns=get_columns_from_table(url))
df_nodes.drop(columns=["IG", "Fc", "Ft", "G", "R", "Pr"], axis=1, inplace=True) # Remove unnecessary columns
df_nodes["Polygon"] = df_nodes["Coorientação"].apply(lambda x: 3 if x else 0)
df_nodes["Ano_Ord"] = df_nodes["Ano"] - df_nodes["Ano"][0] + 1
df_edges = pd.DataFrame(edges, columns=["Source", "Target"])
print("\nOs dados foram baixados com sucesso!")
df_nodes.to_csv(f"{name}_nodes.csv", index=False)
df_edges.to_csv(f"{name}_edges.csv", index=False)
print("\nOs arquivos gerados foram:")
print(f"{name}_nodes.csv")
print(f"{name}_edges.csv")
print("\nObrigado por usar o JararacaScript!")
print("\nDesenvolvido por Guilherme Xavier Souza - github.com/guixavs")
print(f"\nTempo de execução: {time() - start_time:.2f} segundos")
