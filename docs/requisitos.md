# Requisitos do MVP — Controle de Materiais

## 1. Objetivo

Desenvolver uma aplicação web para auxiliar no controle de estoque e nas movimentações de materiais da JS Vilela Linhas e Cordas.

## 2. Requisitos funcionais

| Código | Descrição | Prioridade |
|---|---|---|
| RF01 | Permitir o cadastro de materiais. | Obrigatória |
| RF02 | Permitir o cadastro de setores. | Obrigatória |
| RF03 | Registrar entradas e saídas de materiais, identificando quantidade, setor e finalidade. | Obrigatória |
| RF04 | Consultar o saldo atual e o histórico de movimentações. | Obrigatória |
| RF05 | Registrar materiais utilizados e quantidades produzidas. | Desejável |

## 3. Requisitos não funcionais

- RNF01 — Segurança: disponibilizar autenticação e controle de acesso.
- RNF02 — Integridade: validar os dados e impedir saídas superiores ao estoque disponível.
- RNF03 — Compatibilidade: permitir acesso por navegadores modernos.
- RNF04 — Acessibilidade: utilizar textos legíveis, navegação por teclado e interface responsiva.

## 4. Regras de negócio

- Toda movimentação deve estar relacionada a um material e a um setor.
- A quantidade movimentada deve ser maior que zero.
- As saídas não podem ultrapassar o saldo disponível.
- A finalidade da movimentação deve ser informada, incluindo retiradas para amarrar redes.
- O saldo deve ser atualizado após cada movimentação válida.

## 5. Limites do MVP

A primeira versão não contemplará integração com máquinas ou balanças, controle financeiro, emissão de documentos fiscais ou aplicativo móvel nativo.