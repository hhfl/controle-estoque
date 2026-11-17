"""Testes de integração: fluxo completo pelas rotas (controllers + views + model)."""
from app import db
from app.models import Categoria, Produto


def test_paginas_principais_abrem(client, produto):
    for url in ("/", "/produtos/", "/categorias/", "/movimentacoes/", "/movimentacoes/nova",
                "/produtos/novo", f"/produtos/{produto.id}/editar"):
        assert client.get(url).status_code == 200


def test_pagina_inexistente_retorna_404_amigavel(client):
    r = client.get("/nao-existe")
    assert r.status_code == 404
    assert "não encontrado" in r.get_data(as_text=True)


def test_produto_inexistente_retorna_404(client):
    assert client.get("/produtos/999/editar").status_code == 404


def test_criar_categoria_e_duplicada(client):
    client.post("/categorias/nova", data={"nome": "Limpeza"})
    r = client.post("/categorias/nova", data={"nome": "limpeza"}, follow_redirects=True)
    assert "já existe" in r.get_data(as_text=True)
    assert Categoria.query.count() == 1


def test_excluir_categoria_com_produtos_e_bloqueado(client, produto):
    r = client.post(f"/categorias/{produto.categoria_id}/excluir", follow_redirects=True)
    assert "Não é possível excluir" in r.get_data(as_text=True)
    assert Categoria.query.count() == 1


def test_crud_produto(client, produto):
    cid = produto.categoria_id
    # Create
    r = client.post("/produtos/novo", data={"nome": "Café", "sku": "caf-1", "preco": "12,90",
                    "quantidade": "20", "estoque_minimo": "5", "categoria_id": cid},
                    follow_redirects=True)
    assert "cadastrado com sucesso" in r.get_data(as_text=True)
    novo = Produto.query.filter_by(sku="CAF-1").one()
    # Read / busca
    assert "Café" in client.get("/produtos/?q=caf").get_data(as_text=True)
    # Update
    client.post(f"/produtos/{novo.id}/editar", data={"nome": "Café Premium", "sku": "CAF-1",
                "preco": "15", "quantidade": "20", "estoque_minimo": "5", "categoria_id": cid})
    assert db.session.get(Produto, novo.id).nome == "Café Premium"
    # Delete
    client.post(f"/produtos/{novo.id}/excluir")
    assert db.session.get(Produto, novo.id) is None


def test_produto_invalido_mostra_erro_e_nao_salva(client, produto):
    r = client.post("/produtos/novo", data={"nome": "", "sku": "", "preco": "x",
                    "quantidade": "-1", "estoque_minimo": "0",
                    "categoria_id": produto.categoria_id})
    html = r.get_data(as_text=True)
    assert "obrigatório" in html and "preço" in html
    assert Produto.query.count() == 1


def test_movimentacao_pela_tela(client, produto):
    r = client.post("/movimentacoes/nova", data={"produto_id": produto.id, "tipo": "SAIDA",
                    "quantidade": "4"}, follow_redirects=True)
    assert "registrada com sucesso" in r.get_data(as_text=True)
    assert db.session.get(Produto, produto.id).quantidade == 6


def test_saida_acima_do_estoque_mostra_erro(client, produto):
    r = client.post("/movimentacoes/nova", data={"produto_id": produto.id, "tipo": "SAIDA",
                    "quantidade": "99"})
    assert "Estoque insuficiente" in r.get_data(as_text=True)
    assert db.session.get(Produto, produto.id).quantidade == 10


def test_movimentacao_com_entradas_invalidas_nao_quebra(client, produto):
    for dados in ({"produto_id": "", "tipo": "ENTRADA", "quantidade": "1"},
                  {"produto_id": produto.id, "tipo": "ENTRADA", "quantidade": "abc"},
                  {"produto_id": produto.id, "tipo": "ENTRADA", "quantidade": "0"}):
        assert client.post("/movimentacoes/nova", data=dados).status_code == 200


def test_painel_lista_estoque_baixo(client, produto):
    produto.quantidade = 1
    db.session.commit()
    assert "Suco de Laranja" in client.get("/").get_data(as_text=True)
