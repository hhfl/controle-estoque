# 5. Dicionário de Dados

## Tabela `categoria`
| Campo | Tipo | Nulo | Chave | Descrição / Domínio |
|---|---|---|---|---|
| id | INT AUTO_INCREMENT | Não | PK | Identificador da categoria |
| nome | VARCHAR(60) | Não | UNIQUE | Nome da categoria (2 a 60 caracteres) |

## Tabela `produto`
| Campo | Tipo | Nulo | Chave | Descrição / Domínio |
|---|---|---|---|---|
| id | INT AUTO_INCREMENT | Não | PK | Identificador do produto |
| nome | VARCHAR(100) | Não | — | Nome do produto (2 a 100 caracteres) |
| sku | VARCHAR(30) | Não | UNIQUE | Código do produto, em maiúsculas |
| preco | DECIMAL(10,2) | Não | — | Preço unitário em reais, ≥ 0 |
| quantidade | INT | Não | — | Quantidade atual em estoque, ≥ 0 (padrão 0) |
| estoque_minimo | INT | Não | — | Limite para alerta de estoque baixo, ≥ 0 (padrão 0) |
| categoria_id | INT | Não | FK → categoria.id | Categoria do produto |

## Tabela `movimentacao`
| Campo | Tipo | Nulo | Chave | Descrição / Domínio |
|---|---|---|---|---|
| id | INT AUTO_INCREMENT | Não | PK | Identificador da movimentação |
| produto_id | INT | Não | FK → produto.id | Produto movimentado (exclusão em cascata) |
| tipo | VARCHAR(7) | Não | — | `ENTRADA` ou `SAIDA` |
| quantidade | INT | Não | — | Unidades movimentadas, > 0 |
| data_hora | DATETIME | Não | — | Momento do registro (padrão: agora) |
| observacao | VARCHAR(200) | Sim | — | Texto livre opcional |
