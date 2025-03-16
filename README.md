# JararacaScript
Um script para criar grafos de Genealogia Acadêmica com dados da [Plataforma Acácia](https://plataforma-acacia.org/)

## Plataforma Acácia
De acordo com a página inicial da Plataforma Acácia, o site surgiu com o objetivo de _"documentar as relações formais de orientação no contexto dos programas de pós graduação brasileiros"_ por meio dos dados do **Currículo Lattes**. 

A partir do link do perfil de um orientador na Plataforma Acácia, o script JararacaPy gera arquivos _csv_. Com esses arquivos e o software [Gephi](https://gephi.org/), é possível criar grafos de Genealogia Acadêmica.


## Pré-requisitos
O projeto foi desenvolvido em [Python 3.13](https://www.python.org/) e utiliza as seguintes bibliotecas:
* [BeatifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#)
```bash
pip install beautifulsoup4
```
* [Pandas](https://pandas.pydata.org/)
```bash
pip install pandas
```

Para gerar a visualização em forma de grafo de Genealogia Acadêmica, é utilzado o software [Gephi 0.10](https://gephi.org/) com os seguintes plugins:
* Ordered Graph Layout
* Lineage

## Instruções
1. Execute o arquivo JararacaPy fornecendo o link do orientador desejado.

2. Aguarde a execução do script e confira se na pasta do projeto foram gerados 3 novos arquivos:
   * _NomeDoOrientador_edges.csv_
   * _NomeDoOrientador_links.txt_
   * _NomeDoOrientador_nodes.csv_

### Gephi
1. Importe o arquivo _"NomeDoOrientador_nodes.csv"_ na aba **Nodes** do **Data Laboratory** pelo comando **Import Spreadshit**
	* Selecione a opção **Append to existing workspace**

2. Importe o arquivo _"NomeDoOrientador_edges.csv"_ na aba **Edges** do **Data Laboratory** pelo comando **Import Spreadshit**
	* Selecione a opção **Append to existing workspace**

3. Na seção **Layout** do **Overview**, aplique o _Ordered Graph Layout_ com as seguintes configurações:

	![image](https://github.com/user-attachments/assets/d9264dd1-b36e-4f73-8b4d-3544fd8dab0c)

4. Em **Preview**, aplique as seguintes configurações para renderizar a visualização do grafo:

	![image](https://github.com/user-attachments/assets/d05d9a1e-725e-45a4-a3af-79c3fa9d882e)


#### Observações
* As configurações acima foram fornecidas por Rafael J. Pezzuto Damaceno, responsável pela Plataforma Acácia.
* Cada parâmetro pode ser alterado dependendo do objetivo e do tamanho do grafo.
* Por meio da seção **Appearence** do **Overview**, podem ser aplicadas cores e tamanhos diferentes de acordo com parâmetros dos orientandos. Exemplos:
	* Definir a cor a parir do tipo de orientação (Partition → Choose an attribute → Tipo → Apply)
 	* Definir o tamanho a partir do número de descendentes acadêmicos (Ranking → Choose an attribute → ds → Apply)
	* Definir a cor a parir da geração (Usar a Statistics _Lineage_)
 * Para eixo e legenda, exporte o arquivo no **Preview** e adicione-os em software separado (ex. Photoshop, GIMP etc.).

## Exemplos
* Por tipo de orientação:

	![IP](https://github.com/user-attachments/assets/e7d02652-56c2-4560-8b32-0311e64c23a3)
	Orientador: [Isaias Pessotti](https://plataforma-acacia.org/profile/isaias-pessotti/)
  	
* Usando a Statistics _Lineage_:

	![Sério](https://github.com/user-attachments/assets/d7a298f7-a1ad-4eed-a764-a6c865d38f41)
	Orientadora: [Tereza Maria de Azevedo Pires Sério](https://plataforma-acacia.org/profile/tereza-maria-de-azevedo-pires-serio/)

* Com adição de informações:

	![image](https://github.com/user-attachments/assets/74e85038-0f94-4135-98f6-64da1728238c)
	Orientadora: [Maria do Carmo Guedes](https://plataforma-acacia.org/profile/maria-do-carmo-guedes/) (+dados de Iniciações Científicas)
 	

## Nome
De acordo com a página Sobre da Plataforma Acácia:
> O termo Acácia é uma inspiração da árvore Acácia, uma espécie nativa do sudeste Australiano. O formato da copa desta espécie assemelha-se com os grafos de genealogia acadêmica identificados no contexto brasileiro, ou seja, são compactos em termos de altura, indicando que no Brasil a Ciência é jovem (possui poucas gerações de doutores e mestres), mas largos, em termos de comprimento.
Assim como uma Jararaca - a qual pode coexistir no mesmo habitat da Acácia no Brasil -, o script explora os galhos da árvore Ciência brasileira. (Além do programa ser escrito em Python).

### Mais informações
ROSSI, L.; DAMACENO, R.; MENA-CHALCO, J. [Genealogia acadêmica: Um novo olhar sobre impacto acadêmico de pesquisadores](https://www.cgee.org.br/documents/10195/3952601/184920.pdf). Revista Parcerias Estratégicas, v. 23, p. 197–212, 1 dez. 2018.

Contato: guilhermexaviersouza.0@gmail.com

