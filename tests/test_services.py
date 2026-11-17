"""Testes unitários das regras de negócio (camada de serviço)."""
import pytest

from app import db
from app.models import Movimentacao
from app.services import registrar_movimentacao, validar_produto


def form_valido(produto, **extra):
    dados = {"nome": "Água", "sku": "agu-1", "preco": "3,50", "quantidade": "5",
             "estoque_minimo": "2", "categoria_id": str(produto.categoria_id)}
    dados.update(extra)
    return dados


def test_validar_produto_valido(produto):
    dados, erros = validar_produto(form_valido(produto))
    assert erros == []
    assert dados["sku"] == "AGU-1"          # SKU em maiúsculas
    assert str(dados["preco"]) == "3.50"    # vírgula aceita


@pytest.mark.parametrize("campo,valor", [
    ("nome", ""), ("nome", "A"), ("sku", ""), ("preco", "abc"), ("preco", "-1"),
    ("quantidade", "-5"), ("quantidade", "x"), ("estoque_minimo", "-1"),
    ("categoria_id", "999"), ("categoria_id", ""),
])
def test_validar_produto_rejeita_dados_invalidos(produto, campo, valor):
    _, erros = validar_produto(form_valido(produto, **{campo: valor}))
    assert erros


def test_sku_duplicado_rejeitado(produto):
    _, erros = validar_produto(form_valido(produto, sku="suc-001"))
    assert any("Já existe" in e for e in erros)


def test_sku_do_proprio_produto_na_edicao_e_permitido(produto):
    _, erros = validar_produto(form_valido(produto, sku="SUC-001"), produto_id=produto.id)
    assert erros == []


def test_entrada_aumenta_estoque(produto):
    registrar_movimentacao(produto, "ENTRADA", 5)
    assert produto.quantidade == 15
    assert Movimentacao.query.count() == 1


def test_saida_diminui_estoque(produto):
    registrar_movimentacao(produto, "SAIDA", 4, "venda balcão")
    assert produto.quantidade == 6


def test_saida_maior_que_estoque_e_bloqueada(produto):
    with pytest.raises(ValueError, match="Estoque insuficiente"):
        registrar_movimentacao(produto, "SAIDA", 11)
    assert produto.quantidade == 10
    assert Movimentacao.query.count() == 0


@pytest.mark.parametrize("tipo,qtd", [("OUTRO", 1), ("ENTRADA", 0), ("ENTRADA", -3)])
def test_movimentacao_invalida(produto, tipo, qtd):
    with pytest.raises(ValueError):
        registrar_movimentacao(produto, tipo, qtd)


def test_estoque_baixo(produto):
    assert not produto.estoque_baixo
    registrar_movimentacao(produto, "SAIDA", 7)  # 3 <= mínimo 3
    assert produto.estoque_baixo
