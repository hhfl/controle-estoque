from flask import Blueprint, render_template

from app.models import Produto

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    total = Produto.query.count()
    em_alerta = [p for p in Produto.query.order_by(Produto.nome).all() if p.estoque_baixo]
    return render_template("index.html", total=total, em_alerta=em_alerta)
