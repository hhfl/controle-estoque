# 1. Escopo e Requisitos

## 1.1 Ideia
Pequenos comércios costumam controlar o estoque em cadernos ou planilhas, o que gera erros, perdas e falta de produtos. O **Controle de Estoque** é uma aplicação web simples que registra produtos, categorias e movimentações, e avisa quando um produto está com estoque baixo.

## 1.2 Escopo
**Dentro do escopo:** cadastro de categorias; CRUD de produtos; registro de entradas e saídas; histórico; painel com alerta de estoque baixo; busca por nome/código.
**Fora do escopo (versões futuras):** login e perfis de usuário, emissão de notas fiscais, relatórios em PDF, integração com PDV, aplicativo mobile.

## 1.3 Público-alvo
Donos e funcionários de pequenas lojas, com pouca familiaridade com tecnologia.

## 1.4 Requisitos Funcionais
| ID | Requisito |
|----|-----------|
| RF01 | O sistema deve permitir cadastrar, listar e excluir categorias. |
| RF02 | O sistema deve permitir cadastrar, listar, editar e excluir produtos. |
| RF03 | O sistema deve impedir códigos (SKU) duplicados. |
| RF04 | O sistema deve registrar entradas e saídas de estoque. |
| RF05 | O sistema deve impedir saída maior que o estoque disponível. |
| RF06 | O sistema deve manter o histórico de movimentações. |
| RF07 | O sistema deve alertar produtos com estoque igual ou abaixo do mínimo. |
| RF08 | O sistema deve permitir buscar produtos por nome ou código. |
| RF09 | O sistema deve impedir excluir categoria que possua produtos. |

## 1.5 Requisitos Não Funcionais
| ID | Requisito |
|----|-----------|
| RNF01 | Usabilidade: interface clara, simples e consistente (princípios de IHC). |
| RNF02 | Desempenho: telas respondem em menos de 2 segundos em uso normal. |
| RNF03 | Confiabilidade: entradas inválidas exibem mensagem de erro sem quebrar o sistema. |
| RNF04 | Portabilidade: funciona nos principais navegadores e em telas de celular. |
| RNF05 | Manutenibilidade: código em camadas (MVC) e coberto por testes automatizados. |
| RNF06 | Integridade: banco relacional com chaves estrangeiras e restrições de domínio. |

## 1.6 Regras de Negócio
- RN01: preço, quantidade e estoque mínimo não podem ser negativos.
- RN02: quantidade de movimentação deve ser inteira e maior que zero.
- RN03: estoque baixo = quantidade atual ≤ estoque mínimo.
- RN04: o SKU é salvo em letras maiúsculas.
