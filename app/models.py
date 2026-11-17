"""MODEL (MVC): entidades e regras de armazenamento."""
from datetime import datetime

from app import db


class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), unique=True, nullable=False)

    produtos = db.relationship("Produto", back_populates="categoria")


class Produto(db.Model):
    __tablename__ = "produto"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(30), unique=True, nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    estoque_minimo = db.Column(db.Integer, nullable=False, default=0)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)

    categoria = db.relationship("Categoria", back_populates="produtos")
    movimentacoes = db.relationship("Movimentacao", back_populates="produto",
                                    cascade="all, delete-orphan")

    @property
    def estoque_baixo(self):
        return self.quantidade <= self.estoque_minimo


class Movimentacao(db.Model):
    __tablename__ = "movimentacao"

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    tipo = db.Column(db.String(7), nullable=False)  # ENTRADA ou SAIDA
    quantidade = db.Column(db.Integer, nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.now)
    observacao = db.Column(db.String(200))

    produto = db.relationship("Produto", back_populates="movimentacoes")
