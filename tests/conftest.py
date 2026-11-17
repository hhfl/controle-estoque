import pytest

from app import create_app, db
from app.models import Categoria, Produto


@pytest.fixture
def app():
    app = create_app("config.TestConfig")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def produto(app):
    cat = Categoria(nome="Bebidas")
    db.session.add(cat)
    db.session.commit()
    p = Produto(nome="Suco de Laranja", sku="SUC-001", preco=7.5,
                quantidade=10, estoque_minimo=3, categoria_id=cat.id)
    db.session.add(p)
    db.session.commit()
    return p
