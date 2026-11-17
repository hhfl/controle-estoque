from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.models import Movimentacao, Produto
from app.services import registrar_movimentacao

bp = Blueprint("movimentacoes", __name__, url_prefix="/movimentacoes")


@bp.route("/")
def historico():
    movs = Movimentacao.query.order_by(Movimentacao.data_hora.desc()).limit(200).all()
    return render_template("movimentacoes/lista.html", movimentacoes=movs)


@bp.route("/nova", methods=["GET", "POST"])
def nova():
    produtos = Produto.query.order_by(Produto.nome).all()
    if request.method == "POST":
        try:
            try:
                produto = db.session.get(Produto, int(request.form.get("produto_id", "")))
            except ValueError:
                produto = None
            if produto is None:
                raise ValueError("Selecione um produto válido.")
            try:
                quantidade = int(request.form.get("quantidade", ""))
            except ValueError:
                raise ValueError("A quantidade deve ser um número inteiro maior que zero.")
            registrar_movimentacao(produto, request.form.get("tipo", ""), quantidade,
                                   request.form.get("observacao", ""))
            flash("Movimentação registrada com sucesso!", "ok")
            return redirect(url_for("movimentacoes.historico"))
        except ValueError as erro:
            flash(str(erro), "erro")
    return render_template("movimentacoes/form.html", produtos=produtos, form=request.form)
