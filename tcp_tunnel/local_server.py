# tcp_tunnel/local_server.py

from flask import Flask, request, render_template, jsonify
import subprocess
import os
import signal

app = Flask(__name__)
# app = create_exposed_app()

servers = []

if __name__ == '__main__':
    app.run(debug=True)