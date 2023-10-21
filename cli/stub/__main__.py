import zipfile
import urllib.request
import io
import os
import sys
import shutil
import tempfile
import subprocess

SERVER_API = 'http://127.0.0.1:5000/download_client'
TEMP_DIR = tempfile.mkdtemp()
MODULES_PATH = os.path.join(TEMP_DIR, 'temp_switchboard')
VERSION_FILE_PATH = os.path.join(MODULES_PATH, 'VERSION')
REQUIREMENTS_PATH = os.path.join(MODULES_PATH, 'requirements.txt')

print(f'Temp dir at {TEMP_DIR}')

def download_client_code():
    try:
        with urllib.request.urlopen(SERVER_API) as response:
            memory_zip = io.BytesIO(response.read())
            z = zipfile.ZipFile(memory_zip)
            z.extractall(MODULES_PATH)
    
    except urllib.error.HTTPError as e:
        print(f'Issue connecting to the server {e.code}')
        sys.exit(1)
    
    except urllib.error.URLError as e:
        print(f'Failed to connect: {e.reason}')
        sys.exit(1)

def install_requirements():
    try:
        result = subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--target', TEMP_DIR, '-r', REQUIREMENTS_PATH],
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print('Non-zero when pip installing - something is wrong.')
        cleanup()
        sys.exit(1)
    

def run_client():
    with open(VERSION_FILE_PATH, 'r') as version_file:
        print(f'Version: {version_file.read().strip()}')
    
    sys.path.insert(0, TEMP_DIR)

    print('From temp_switchboard')

    from temp_switchboard import main
    main.main()

def cleanup():
    shutil.rmtree(TEMP_DIR)

if __name__ == '__main__':
    print('CLIENT CODE!')
    download_client_code()
    install_requirements()
    run_client()
    cleanup()