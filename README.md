# COM231_GitHub_API

Trabalho Final da matéria de Banco de Dados II do curso de Bacharelado em Ciência da Computação na Universidade Federal de Itajubá (Unifei)

O trabalho é dividido em duas partes:
- Script para consumir dados da API do GitHub e popular um banco PostgreSQL (diretório `script_github_api`)
- Aplicação Ad-hoc baseada no banco previamente populado (diretório `aplicacao_adhoc`)

## Banco PostgreSQL

O Modelo Entidade Relacionamento modelado para o banco está apresentado na imagem `MER_GITHUB_API.png`. O SQL referente a criação das tabelas está descrito no arquivo `github_api.sql`, junto com algumas requisições que utilizei durante a criação do banco.

> NOTA: Os dados da API do GitHub são salvos no padrão de um banco orientado à documentos, fiz o tratamento dos dados para que condizesse com o modelo entidade relacionamento.

## Funcionamento do script

O script de coleta foi escrito em inteiramente em Javascript e utiliza as bibliotecas:
- `pkg`: Responsável por fazer a conexão com o banco PostgreSQL
- `moment`: Usado para converter as datas da API para o formato aceito pelo PostgreSQL
- `fetch`: Para consumir os dados da API
- `fs`: Para criar e atualizar um arquivo de histórico de IDs de repositório já adicionados ao banco

Esse script inicia a busca por repositórios criados dentro de um período definido de tempo e, partindo dos dados desse repositório, coleta os dados de usuário, pull requests, issues e commits a ele relacionado.

Para consumir os dados da API do GitHub é necessário ter um token de autenticação (gerado gratuitamente na conta pessoal do GitHub). O token deve ser colocado na variável `accessToken`.

Para aumentar a variedade de dados são dados os seguintes parâmetros à requisição:
- `page`: Seleciona a página de resposta da API (no máximo 10)
- `per_page`: Seleciona a quantidade de resultados que deve retornar em cada página (no máximo 100)
- `startDate` e `endDate`: Informa o período da data de criação dos repositórios a serem consumidos (string no formato `YYYY-MM-DD`)
- O parâmetro `is:public` é adicionado diretamente a query de requisição para garantir que todos os repositórios coletados serão públicos

## Funcionamento da Aplicação Ad-hoc

A aplicação adhoc é uma aplicação ORM DAO e pode ser inicializada pelo arquivo `controller.py`. O backend foi todo escrito em Python e o frontend em Flask.

Para utilizar a aplicação, é preciso atualizar as informações descritas no arquivo `config.py` para condizer com as informações do banco PostgreSQL.

A aplicação é dividida em:
- Controller: o núcleo principal da aplicação e por onde ela é inicializada
- Model: realiza o tratamento dos dados e conecta o controller com o DAO
- DAO: responsável por todas as operações no banco
- View: a view é dividida em várias rotas HTML com ajuda do Flask
- Forms: definições dos formulários usados no HTML

O login da aplicação é feita com base no usuário e senha do próprio banco. Além disso, é usada uma chave csrf para simular uma proteção a mais de acesso a aplicação.
