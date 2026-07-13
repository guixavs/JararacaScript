import re
import time
from urllib.parse import urljoin

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests


class AcaciaScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            }
        )
        self.base_url = "https://plataforma-acacia.org"
        self.nodes = []
        self.edges = []
        self.visited_links = set()
        self.total_expected = 0

    def get_soup(self, url, retries=3):
        """Faz a requisição com delay (educação) e retentativas (resiliência)."""
        for attempt in range(retries):
            try:
                time.sleep(0.1)
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return bs(response.text, "html.parser")

            except (
                requests.exceptions.RequestException,
                requests.exceptions.HTTPError,
            ) as e:
                if attempt < retries - 1:
                    print(
                        f"\n[Aviso] Falha de conexão. Tentando novamente em 3 segundos... (Tentativa {attempt + 1} de {retries})"
                    )
                    time.sleep(3)
                else:
                    print(
                        f"\n[Erro fatal] Não foi possível acessar a página após {retries} tentativas: {e}"
                    )
                    raise

    def scrape_profile(self, url):
        print("\nAcessando o perfil raiz...")
        self.visited_links.add(url)
        soup = self.get_soup(url)

        name = soup.find("h1", attrs={"itemprop": "name"}).get_text(strip=True)
        orientations = "".join(
            [o.get_text(strip=True) for o in soup.select("td[data-label='Formações']")]
        )
        metrics = [
            m.get_text(strip=True)
            for m in soup.find_all(
                "td", attrs={"class": "has-text-weight-bold has-text-right"}
            )
        ]

        root_id = 0
        root_data = [root_id, name, orientations] + metrics
        self.nodes.append(root_data)

        self.total_expected = int(root_data[3])

        print(f"Orientador: {name}")
        print(f"Descendentes mapeados: {self.total_expected}\n")

        if self.total_expected > 0:
            self._get_descendants(url, root_id)

        return name

    def _get_descendants(self, url, parent_id):
        soup = self.get_soup(url)

        current_name = self.nodes[parent_id][1]
        progress = (len(self.nodes) / max(self.total_expected, 1)) * 100
        print(
            f"\rBaixando dados de {current_name[:35]:<35} | Progresso: {progress:>6.2f}%",
            end="",
            flush=True,
        )

        for tr in soup.select("#table-profile-descendants tbody tr"):
            a_tag = tr.find("a")
            if not a_tag:
                continue

            link = urljoin(self.base_url, a_tag["href"])

            if link not in self.visited_links:
                self.visited_links.add(link)

                node_id = len(self.nodes)
                self.edges.append([parent_id, node_id])

                tds = tr.find_all("td")
                data = [td.get_text(strip=True) for td in tds]
                data[0] = node_id

                self.nodes.append(data)

                if int(data[3]) > 0:
                    self._get_descendants(link, node_id)


def clear_orientations(record_str):
    pattern = re.compile(r"([PMD])(\d{4})(Co)?")
    records = [
        (degree_type, int(year), bool(is_co_advised))
        for degree_type, year, is_co_advised in pattern.findall(record_str)
    ]

    if not records:
        return None, None, False

    non_co_records = [r for r in records if not r[2]]
    candidates = non_co_records if non_co_records else records

    degree_type, year, is_co_advised = min(candidates, key=lambda r: r[1])
    return degree_type, year, is_co_advised


def nodes_treatment(df):
    columns_to_drop = ["IG", "Fc", "Ft", "G", "R", "Pr"]
    df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

    df["Tipo"], df["Ano"], df["Co"] = zip(*df["Orientações"].apply(clear_orientations))

    df.drop(columns=["Orientações"], inplace=True)
    return df[["Id", "Nome", "Tipo", "Ano", "Ds", "Co"]]


def main():
    print("\nBem-vindo ao JararacaScript!")
    print(
        "Este programa irá baixar os dados de orientação de um professor por meio da Plataforma Acácia\n"
    )

    url = input("Por favor, insira a URL do professor que deseja baixar os dados: ")

    time_start = time.time()
    scraper = AcaciaScraper()

    try:
        name = scraper.scrape_profile(url)
    except Exception as e:
        print(f"\n\nO processo foi interrompido devido a um erro: {e}")
        return

    print("\n\nOs dados foram baixados com sucesso!")
    print("O processo está 100% completo. Tratando dados...\n")

    col_names = ["Id", "Nome", "Orientações", "Ds", "IG", "Fc", "Ft", "G", "R", "Pr"]
    df_nodes = pd.DataFrame(scraper.nodes, columns=col_names)
    df_nodes = nodes_treatment(df_nodes)

    df_nodes["Polygon"] = df_nodes["Co"].apply(lambda x: 3 if x else 0)
    min_year = df_nodes["Ano"].min()
    df_nodes["Ano_Ord"] = df_nodes["Ano"] - min_year + 1

    nodes_filename = f"{name}_nodes.csv"
    edges_filename = f"{name}_edges.csv"

    df_nodes.to_csv(nodes_filename, index=False, header=True)
    pd.DataFrame(scraper.edges, columns=["Source", "Target"]).to_csv(
        edges_filename, index=False, header=True
    )

    print("Os arquivos gerados foram:")
    print(f"- {nodes_filename}")
    print(f"- {edges_filename}")
    print("\nObrigado por usar o JararacaScript!")
    print(f"Tempo de execução: {time.time() - time_start:.2f} segundos")


if __name__ == "__main__":
    main()
