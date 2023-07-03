# tcp_tunnel/__init__.py
from .expoesed_server import app as exposed_app
from .local_server import app as local_app

def create_exposed_app():
    return exposed_app

def create_local_app():
    return local_app