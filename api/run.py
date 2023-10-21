import io
import os
import zipfile
import socket
from functools import wraps

from flask import Flask, send_file, request, jsonify

app = Flask(__name__)

CLIENT_DIR = '../cli/client/'
ZIP_NAME = 'bytecode-client.zip'
ACCEPTABLE_HOSTS_PATH = 'valid_hosts'

def get_acceptable_ips():
    with open(ACCEPTABLE_HOSTS_PATH, 'r') as f:
        return [get_ip_from_hostname(line.strip()) for line in f if line.strip()] + ['127.0.0.1']

def restrict_ip_access():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            allowed_ips = get_acceptable_ips()
            client_ip = request.remote_addr

            if client_ip not in allowed_ips:
                response = jsonify(error="Sod off")
                response.status_code = 403

                return response
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/download_client', methods=['GET'])
@restrict_ip_access()
def download_client():
    memory_file = io.BytesIO()

    with zipfile.ZipFile(memory_file, 'w') as zf:
        for root, _, files in os.walk(CLIENT_DIR):
            for file in files:
                full_path = os.path.join(root, file)
                zf.write(full_path, arcname=os.path.relpath(full_path, CLIENT_DIR))
    
    memory_file.seek(0)
    return send_file(memory_file, download_name=ZIP_NAME, as_attachment=True)

def get_ip_from_hostname(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaterror:
        return None

if __name__ == '__main__':
    app.run(debug=True)