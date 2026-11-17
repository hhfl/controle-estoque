# Plano de Testes (Verificação e Validação – Modelo V)

| Nível | O que valida | Como | Onde |
|---|---|---|---|
| Teste unitário | Regras de negócio (validações, entrada, saída, estoque baixo) | pytest | `tests/test_services.py` |
| Teste de integração | Rotas + views + banco (CRUD completo, mensagens de erro) | pytest + cliente de teste Flask | `tests/test_rotas.py` |
| Teste de sistema | Sistema completo no navegador | Roteiro manual | abaixo |
| Teste de aceitação | Usuários reais (5 colegas) | Formulário de teste | `formulario_de_teste.md` |

**Verificação:** revisão do código e comparação com os requisitos RF01–RF09 e RNF01–RNF06.

## Resultado dos testes automatizados
Execute `python -m pytest -v` e cole aqui o resultado (31 testes). Anexe também um print do terminal.

## Roteiro do teste de sistema (manual)
| # | Passo | Resultado esperado | Requisito |
|---|---|---|---|
| 1 | Criar categoria "Bebidas" | Mensagem de sucesso; aparece na lista | RF01 |
| 2 | Criar categoria "bebidas" | Erro "já existe" | RF01 |
| 3 | Criar produto com todos os campos válidos | Produto listado | RF02 |
| 4 | Criar produto com SKU repetido | Erro de SKU duplicado | RF03 |
| 5 | Criar produto com preço "abc" | Erro de preço | RNF03 |
| 6 | Registrar entrada de 5 unidades | Estoque soma 5 | RF04 |
| 7 | Registrar saída maior que o estoque | Erro "Estoque insuficiente" e estoque inalterado | RF05 |
| 8 | Consultar histórico | Movimentações listadas | RF06 |
| 9 | Reduzir estoque até o mínimo | Produto aparece no painel com ⚠️ | RF07 |
| 10 | Buscar produto por parte do nome | Lista filtrada | RF08 |
| 11 | Excluir categoria com produtos | Bloqueado com mensagem | RF09 |
| 12 | Abrir /rota-que-nao-existe | Página de erro 404 amigável | RNF03 |
