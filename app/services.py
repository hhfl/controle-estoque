"""Regras de negócio e validação (usadas pelos controllers)."""
from decimal import Decimal, InvalidOperation

from app import db
from app.models import Categoria, Movimentacao, Produto


def _inteiro_nao_negativo(valor, rotulo, erros):
    try:
        numero = int(valor)
        if numero < 0:
            raise ValueError
        return numero
    except (TypeError, ValueError):
        erros.append(f"{rotulo} deve ser um número inteiro maior ou igual a zero.")
        return None


def validar_produto(form, produto_id=None):
    """Retorna (dados, erros). Se erros estiver vazio, os dados são válidos."""
    erros = []
    nome = (form.get("nome") or "").strip()
    sku = (form.get("sku") or "").strip().upper()

    if len(nome) < 2:
        erros.append("O nome é obrigatório (mínimo de 2 caracteres).")
    if len(nome) > 100:
        erros.append("O nome pode ter no máximo 100 caracteres.")
    if not sku:
        erros.append("O código (SKU) é obrigatório.")
    elif len(sku) > 30:
        erros.append("O código (SKU) pode ter no máximo 30 caracteres.")
    else:
        existente = Produto.query.filter_by(sku=sku).first()
        if existente and existente.id != produto_id:
            erros.append(f"Já existe um produto com o código {sku}.")

    preco = None
    try:
        preco = Decimal((form.get("preco") or "").replace(",", "."))
        if preco < 0 or not preco.is_finite():
            raise InvalidOperation
        preco = preco.quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        preco = None
        erros.append("O preço deve ser um número maior ou igual a zero (ex.: 12,50).")

    quantidade = _inteiro_nao_negativo(form.get("quantidade", "0"), "A quantidade", erros)
    minimo = _inteiro_nao_negativo(form.get("estoque_minimo", "0"), "O estoque mínimo", erros)

    categoria = None
    try:
        categoria = db.session.get(Categoria, int(form.get("categoria_id", "")))
    except (TypeError, ValueError):
        pass
    if categoria is None:
        erros.append("Selecione uma categoria válida.")

    dados = dict(nome=nome, sku=sku, preco=preco, quantidade=quantidade,
                 estoque_minimo=minimo, categoria_id=categoria.id if categoria else None)
    return dados, erros


def registrar_movimentacao(produto, tipo, quantidade, observacao=""):
    """Atualiza o estoque. Levanta ValueError se a operação for inválida."""
    if tipo not in ("ENTRADA", "SAIDA"):
        raise ValueError("Tipo de movimentação inválido.")
    if not isinstance(quantidade, int) or quantidade <= 0:
        raise ValueError("A quantidade deve ser um número inteiro maior que zero.")
    if tipo == "SAIDA" and quantidade > produto.quantidade:
        raise ValueError(
            f"Estoque insuficiente: {produto.nome} possui apenas {produto.quantidade} unidade(s).")

    produto.quantidade += quantidade if tipo == "ENTRADA" else -quantidade
    mov = Movimentacao(produto=produto, tipo=tipo, quantidade=quantidade,
                       observacao=(observacao or "").strip()[:200])
    db.session.add(mov)
    db.session.commit()
    return mov
