# tcp_tunnel/__init__.py
from .expoesed_server import app
from .local_server import app

def create_exposed_app():
    return app

def create_local_app():
    return app