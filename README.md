# Controle de Estoque

Aplicação web acadêmica para apoiar pequenas lojas no cadastro de produtos e categorias e no controle de entradas e saídas de estoque, com aviso de estoque baixo.

Projeto Integrador Transdisciplinar em Engenharia de Software II.

Projeto desenvolvido como atividade acadêmica; identificadores pessoais foram omitidos desta cópia pública.

## Tecnologias

- Python, Flask e Flask-SQLAlchemy
- MySQL para produção e SQLite para desenvolvimento e testes
- HTML, CSS, JavaScript e templates Jinja2
- pytest

## Estrutura

```text
app/models.py                       entidades
app/services.py                     regras de negócio e validações
app/controllers/                    rotas e controladores
app/templates/                      páginas da aplicação
tests/                              testes automatizados
database/schema.sql                 esquema MySQL
docs/situacao1_planejamento/        requisitos e modelagem
docs/situacao2_desenvolvimento/     arquitetura e manual de uso
docs/situacao3_testes/              plano, formulário e laudo de qualidade
```

## Executar localmente

```bash
python -m venv .venv
```

Ative o ambiente virtual e instale as dependências:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS ou Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Inicie a aplicação:

```bash
python run.py
```

Abra `http://127.0.0.1:5000` no navegador. Sem `DATABASE_URL`, a aplicação usa um banco SQLite local.

Para configurar MySQL, defina `DATABASE_URL` no ambiente. Exemplo com valores ilustrativos:

```text
mysql+pymysql://usuario:senha@host/estoque
```

Não grave senhas ou chaves reais no código nem no repositório.

## Testes automatizados

Execute a suíte incluída no projeto com:

```bash
python -m pytest -v
```

O resultado deve ser registrado após a execução. O laudo em `docs/situacao3_testes/laudo_de_qualidade.md` também deve ser preenchido com avaliações reais; os campos em branco não representam testes realizados.

