from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.models import Categoria, Produto
from app.services import validar_produto

bp = Blueprint("produtos", __name__, url_prefix="/produtos")


@bp.route("/")
def listar():
    busca = (request.args.get("q") or "").strip()
    consulta = Produto.query
    if busca:
        like = f"%{busca}%"
        consulta = consulta.filter(db.or_(Produto.nome.ilike(like), Produto.sku.ilike(like)))
    return render_template("produtos/lista.html",
                           produtos=consulta.order_by(Produto.nome).all(), busca=busca)


@bp.route("/novo", methods=["GET", "POST"])
def novo():
    categorias = Categoria.query.order_by(Categoria.nome).all()
    if not categorias:
        flash("Cadastre ao menos uma categoria antes de criar produtos.", "erro")
        return redirect(url_for("categorias.listar"))
    if request.method == "POST":
        dados, erros = validar_produto(request.form)
        if erros:
            for e in erros:
                flash(e, "erro")
            return render_template("produtos/form.html", produto=None,
                                   form=request.form, categorias=categorias)
        db.session.add(Produto(**dados))
        db.session.commit()
        flash("Produto cadastrado com sucesso!", "ok")
        return redirect(url_for("produtos.listar"))
    return render_template("produtos/form.html", produto=None, form={}, categorias=categorias)


@bp.route("/<int:produto_id>/editar", methods=["GET", "POST"])
def editar(produto_id):
    produto = db.get_or_404(Produto, produto_id)
    categorias = Categoria.query.order_by(Categoria.nome).all()
    if request.method == "POST":
        dados, erros = validar_produto(request.form, produto_id=produto.id)
        if erros:
            for e in erros:
                flash(e, "erro")
            return render_template("produtos/form.html", produto=produto,
                                   form=request.form, categorias=categorias)
        for campo, valor in dados.items():
            setattr(produto, campo, valor)
        db.session.commit()
        flash("Produto atualizado com sucesso!", "ok")
        return redirect(url_for("produtos.listar"))
    return render_template("produtos/form.html", produto=produto, form={}, categorias=categorias)


@bp.route("/<int:produto_id>/excluir", methods=["POST"])
def excluir(produto_id):
    produto = db.get_or_404(Produto, produto_id)
    db.session.delete(produto)
    db.session.commit()
    flash("Produto excluído.", "ok")
    return redirect(url_for("produtos.listar"))
