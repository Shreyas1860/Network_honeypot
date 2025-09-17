import socket
import threading
import datetime
import requests

LOG_FILE = 'honeypot_final.log'
SERVICES = {
    21: {"name": "FTP", "banner": b"220 ProFTPD 1.3.5 Server\n"},
    22: {"name": "SSH", "banner": b"SSH-2.0-OpenSSH_8.2p1\n"},
    23: {"name": "Telnet", "banner": b"\nWelcome to the Admin Console\n\nlogin: "},
    80: {"name": "HTTP", "banner": b"HTTP/1.1 404 Not Found\nServer: Apache/2.4.41\n\n"},
}
FAKE_COMMANDS = {
    "ls -l": b"total 0\n-rw-r--r-- 1 root root 0 Sep 17 14:00 important.dat\n",
    "whoami": b"root\n",
    "uname -a": b"Linux debian 5.10.0-18-amd64 #1 SMP Debian 5.10.140-1 (2022-09-02) x86_64 GNU/Linux\n",
    "help": b"Available commands: ls, whoami, uname, help, exit\n"
}

def log_event(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_message = f"[{timestamp}] {message}"
    print(full_message, flush=True)
    with open(LOG_FILE, 'a') as f:
        f.write(full_message + '\n')

def get_geolocation(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return f"{data.get('city', 'N/A')}, {data.get('regionName', 'N/A')}, {data.get('country', 'N/A')} (ISP: {data.get('isp', 'N/A')})"
        return "Geolocation lookup failed."
    except Exception:
        return "Geolocation lookup error."

def handle_client(client_socket, client_address, port, banner):
    geo_info = get_geolocation(client_address[0])
    log_event(f"Connection to port {port} from: {client_address[0]} ({geo_info})")
    
    try:
        client_socket.sendall(banner)
        
        while True:
            if port in [22, 23]:
                client_socket.sendall(b"root@debian:~# ")
            
            data = client_socket.recv(1024).decode('utf-8', errors='ignore').strip()
            
            if not data:
                break
            
            log_event(f"CMD on port {port} from {client_address[0]}: {data}")
            
            response = FAKE_COMMANDS.get(data.lower(), b"bash: command not found\n")
            client_socket.sendall(response)
            
            if data.lower() == 'exit':
                break

    except Exception as e:
        log_event(f"Error with client {client_address[0]} on port {port}: {e}")
    
    finally:
        log_event(f"Closing connection from {client_address[0]} on port {port}")
        client_socket.close()

def start_listener(port, service_info):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(5)
        log_event(f"Honeypot for {service_info['name']} listening on port {port}...")

        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address, port, service_info['banner']))
            thread.start()
    except PermissionError:
        log_event(f"Error: Permission denied to bind to port {port}. Try running with 'sudo'.")
    except Exception as e:
        log_event(f"Listener error on port {port}: {e}")
    finally:
        server_socket.close()

def main():
    log_event("Starting Advanced Honeypot...")
    threads = []
    for port, service_info in SERVICES.items():
        thread = threading.Thread(target=start_listener, args=(port, service_info))
        threads.append(thread)
        thread.start()

if __name__ == "__main__":
    main()
