# Ponto de entrada para hospedagem (PythonAnywhere / gunicorn)
from app import create_app

application = create_app()
app = application
