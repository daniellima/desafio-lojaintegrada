# Desafio Loja Integrada
Repositório criado para o desafio do Processo Seletivo da Loja Integrada

O objetivo é a criação de uma API de Carrinho que poderia ser usada normalmente em um E-commerce.

## Instalação

Só é necessário ter Docker e Docker-Compose instalados para fazer o projeto funcionar.

## Usando

```bash
# Para iniciar a API execute:
docker-compose up --build -d

# A API deve estar ouvindo a porta 8080. Para testar:
curl localhost:8080
```

## Roadmap

...

## Contribuindo

Esse projeto é feito para um processo seletivo em específico, então não faz muito sentido contribuir, mas deixo aqui as instruções, até para o caso de eu precisar lembrar:

Esse projeto usa [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)

Em termos de stack:
- Uso de Docker para o ambiente de desenvolvimento
- Python 3.9
- Poetry para gerenciar dependências
- pytest para testes
- aiohttp como framework web

### Rodando testes

```bash
# A primeira coisa a fazer é rodar os testes e ver se está tudo certo:
docker-compose run web poetry run python -m pytest 

# Se precisar atualizar alguma dependência do projeto:
docker-compose run web poetry update

# Lembre que o update só vai atualizar o lock file em um container efêmero. 
# Para efetivamente instalar na imagem da aplicação, refaça o build:
docker-compose build # ou docker-compose up --build -d
```

## Autores

Daniel Lima (daniellima.pessoal at gmail dot com)

## Status

Não pretendo continuar a evoluir o projeto, já que ele é um desafio específico de um PS.

