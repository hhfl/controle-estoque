from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.models import Categoria

bp = Blueprint("categorias", __name__, url_prefix="/categorias")


@bp.route("/")
def listar():
    return render_template("categorias/lista.html",
                           categorias=Categoria.query.order_by(Categoria.nome).all())


@bp.route("/nova", methods=["POST"])
def nova():
    nome = (request.form.get("nome") or "").strip()
    if len(nome) < 2 or len(nome) > 60:
        flash("O nome da categoria deve ter entre 2 e 60 caracteres.", "erro")
    elif Categoria.query.filter(db.func.lower(Categoria.nome) == nome.lower()).first():
        flash("Essa categoria já existe.", "erro")
    else:
        db.session.add(Categoria(nome=nome))
        db.session.commit()
        flash("Categoria cadastrada!", "ok")
    return redirect(url_for("categorias.listar"))


@bp.route("/<int:categoria_id>/excluir", methods=["POST"])
def excluir(categoria_id):
    categoria = db.get_or_404(Categoria, categoria_id)
    if categoria.produtos:
        flash("Não é possível excluir: há produtos nesta categoria.", "erro")
    else:
        db.session.delete(categoria)
        db.session.commit()
        flash("Categoria excluída.", "ok")
    return redirect(url_for("categorias.listar"))
