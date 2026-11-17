# Arquitetura

Padrão **MVC** (Model – View – Controller):

- **Model** (`app/models.py`): `Categoria`, `Produto`, `Movimentacao`.
- **View** (`app/templates/`): páginas HTML em Jinja2 com CSS.
- **Controller** (`app/controllers/`): rotas que recebem a requisição HTTP, chamam as regras de negócio e escolhem a view.
- **Service** (`app/services.py`): validações e regras (separadas dos controllers para facilitar os testes).

Fluxo: Usuário → Rota (Controller) → Service/Model (banco) → View (HTML) → Usuário.

**Decisões:** Python/Flask por ser simples e legível; MySQL por ser um SGBD popular; SQLite apenas para desenvolvimento e testes; modo de codificação **tradicional**.
