# tcp_tunnel/__init__.py

from flask import Flask, request, render_template, jsonify
# from tcp_tunnel import create_exposed_app
import subprocess
import os
import signal

app = Flask(__name__)
# app = create_exposed_app()

servers = []

@app.route('/')
def home():
    return render_template('index.html', servers=servers)

@app.route('/start_tunnel_server', methods=['POST'])
def start_tunnel_server():
    ip = request.form.get('ip')
    port = request.form.get('port')
    password = request.form.get('password')
    memo = request.form.get('memo')

    # Start the tunnel server using the user's input
    command = f"python -m pytunnel --bind {ip}:{port} -e \"{password}\""
    process = subprocess.Popen(command, shell=True)

    # Save the server's information
    server = {'ip': ip, 'port': port, 'pid': process.pid, 'memo': memo}
    servers.append(server)

    return 'Tunnel server started successfully', 200

@app.route('/get_servers', methods=['GET'])
def get_servers():
    return jsonify(servers), 200

@app.route('/get_server_status', methods=['POST'])
def get_server_status():
    ip = request.form.get('ip')
    port = request.form.get('port')

    # Get the server's status
    command = f"python -m pytunnel --server {ip}:{port} -c \"status\""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output, error = process.communicate()

    return output, 200

@app.route('/restart_tunnel_server', methods=['POST'])
def restart_tunnel_server():
    port = request.form.get('port')

    # Restart the server using the saved PID
    server = next((s for s in servers if s['port'] == port), None)
    if server:
        os.kill(server['pid'], signal.SIGTERM)
        command = f"python -m pytunnel --bind {server['ip']}:{port} -e \"your_password\""
        process = subprocess.Popen(command, shell=True)
        server['pid'] = process.pid

    return 'Tunnel server restarted successfully', 200

@app.route('/stop_tunnel_server', methods=['POST'])
def stop_tunnel_server():
    port = request.form.get('port')

    # Stop the server using the saved PID
    server = next((s for s in servers if s['port'] == port), None)
    if server:
        os.kill(server['pid'], signal.SIGTERM)
        servers.remove(server)

    return 'Tunnel server stopped successfully', 200

@app.route('/update_memo', methods=['POST'])
def update_memo():
    port = request.form.get('port')
    memo = request.form.get('memo')

    # Update the server's memo
    server = next((s for s in servers if s['port'] == port), None)
    if server:
        server['memo'] = memo

    return 'Memo updated successfully', 200


if __name__ == '__main__':
    app.run(debug=True)