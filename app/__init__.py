from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)

    from app.controllers import main, produtos, categorias, movimentacoes

    for modulo in (main, produtos, categorias, movimentacoes):
        app.register_blueprint(modulo.bp)

    @app.errorhandler(404)
    def nao_encontrado(_erro):
        return render_template("erro.html", codigo=404,
                               mensagem="Página ou registro não encontrado."), 404

    @app.errorhandler(500)
    def erro_interno(_erro):
        db.session.rollback()
        return render_template("erro.html", codigo=500,
                               mensagem="Ocorreu um erro inesperado. Tente novamente."), 500

    with app.app_context():
        db.create_all()

    return app
