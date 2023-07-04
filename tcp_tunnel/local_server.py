# tcp_tunnel/local_server.py

from flask import Flask, request, render_template, jsonify
import subprocess
import os
import signal

app = Flask(__name__)

servers = []

@app.route('/')
def home():
    return render_template('index.html', servers=servers)

@app.route('/start_local_server', methods=['POST'])
def start_local_server():
    target_ip = request.form.get('target_ip')
    target_port = request.form.get('target_port')
    server_ip = request.form.get('server_ip')
    server_port = request.form.get('server_port')
    bind_port = request.form.get('bind_port')
    password = request.form.get('password')
    memo = request.form.get('memo')

    # Start the local server using the user's input
    command = f"python -m pytunnel --port {bind_port} --target {target_ip}:{target_port} --server {server_ip}:{server_port} -e \"{password}\""
    process = subprocess.Popen(command, shell=True)

    # Save the server's information
    server = {'target_ip': target_ip, 'target_port': target_port, 'server_ip': server_ip, 'server_port': server_port, 'bind_port': bind_port, 'pid': process.pid, 'memo': memo}
    servers.append(server)

    return 'Local server started successfully', 200

@app.route('/get_local_servers', methods=['GET'])
def get_local_servers():
    return jsonify(servers), 200

@app.route('/restart_local_server', methods=['POST'])
def restart_local_server():
    server_port = request.form.get('server_port')

    # Restart the server using the saved PID
    server = next((s for s in servers if s['server_port'] == server_port), None)
    if server:
        os.kill(server['pid'], signal.SIGTERM)
        command = f"python -m pytunnel --port {server['server_port']} --target {server['target_ip']}:{server['target_port']} --server {server['server_ip']}:{server['server_port']} -e \"your_password\""
        process = subprocess.Popen(command, shell=True)
        server['pid'] = process.pid

    return 'Local server restarted successfully', 200

@app.route('/stop_local_server', methods=['POST'])
def stop_local_server():
    server_port = request.form.get('server_port')

    # Stop the server using the saved PID
    server = next((s for s in servers if s['server_port'] == server_port), None)
    if server:
        os.kill(server['pid'], signal.SIGTERM)
        servers.remove(server)

    return 'Local server stopped successfully', 200

@app.route('/update_memo', methods=['POST'])
def update_memo():
    server_port = request.form.get('server_port')
    memo = request.form.get('memo')

    # Update the server's memo
    server = next((s for s in servers if s['server_port'] == server_port),None)
    if server:
        server['memo'] = memo

    return 'Memo updated successfully', 200

if __name__ == '__main__':
    app.run(debug=True)