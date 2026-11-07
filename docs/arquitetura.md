# Arquitetura do Sistema

## Arquitetura escolhida

O MVP utilizará uma arquitetura monolítica em camadas, separando a interface, as regras de negócio e a persistência dos dados.

## Tecnologias planejadas

- Python 3.12: linguagem principal.
- Django: framework para desenvolvimento web.
- HTML5 e CSS3: estrutura e apresentação das telas.
- Bootstrap: construção de interface responsiva.
- PostgreSQL: banco de dados relacional.

## Organização das camadas

1. Apresentação: telas, formulários e consultas realizadas pelos usuários.
2. Regras de negócio: validação das movimentações e atualização do estoque.
3. Persistência: armazenamento dos materiais, setores e movimentações no banco de dados.

## Objetivo

A arquitetura busca facilitar a organização, manutenção e evolução do sistema, permitindo que as funcionalidades sejam desenvolvidas de forma estruturada.