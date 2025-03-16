# JararacaPy
Um script para criar grafos de Genealogia Acadêmica com dados da [Plataforma Acácia](https://plataforma-acacia.org/)

## Plataforma Acácia
De acordo com o site da Plataforma Acácia (2022), o projeto surgiu com o objetivo de _"documentar as relações formais de orientação no contexto dos programas de pós graduação brasileiros"_ por meio dos dados do **Currículo Lattes**. 

A partir do link do perfil de um orientador na Plataforma Acácia, o script JararacaPy gera arquivos _csv_. Com esses arquivos e o software [Gephi](https://gephi.org/), é possível criar grafos de Genealogia Acadêmica.


## Pré-requisitos
O projeto foi desenvolvido em [Python 3.13](https://www.python.org/) e utiliza as seguintes bibliotecas:
* [BeatifulSoup 4.13](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#)
```bash
pip install beautifulsoup4
```
* [Pandas 2.2](https://pandas.pydata.org/)
```bash
pip install pandas
```

Para gerar a visualização em forma de grafo de Genealogia Acadêmica, é utilzado o software [Gephi 0.10](https://gephi.org/) com os seguintes plugins:
* Ordered Graph Layout
* Lineage

## Instruções
1. Execute o arquivo JararacaPy fornecendo o link do orientador desejado.

2. Aguarde a execução do script e confira se na pasta do projeto foram gerados 3 novos arquivos:
   - _NomeDoOrientador_edges.csv_
   - _NomeDoOrientador_links.txt_
   - _NomeDoOrientador_nodes.csv_

### Gephi
1. Importe o arquivo _"NomeDoOrientador_nodes.csv"_ na aba **Nodes** do **Data Laboratory** pelo comando **Import Spreadshit**
	* Selecione a opção **Append to existing workspace**

2. Importe o arquivo _"NomeDoOrientador_edges.csv"_ na aba **Edges** do **Data Laboratory** pelo comando **Import Spreadshit**
	* Selecione a opção **Append to existing workspace**

3.

## Nome

## Referências


