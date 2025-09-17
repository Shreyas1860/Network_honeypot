# Advanced Interactive Honeypot 🍯

An advanced, containerized honeypot written in Python. This tool mimics several common services to attract and log connection attempts, providing valuable insight into automated attacks and network reconnaissance.

The honeypot is designed to be interactive, featuring a fake shell to keep attackers engaged and gather more detailed intelligence on their methods. All interactions are logged with timestamps and IP geolocation data.



---

## ✨ Features

* **Multi-Service Decoy**: Emulates FTP, SSH, Telnet, and HTTP services on their standard ports.
* **Interactive Fake Shell**: Keeps attackers engaged by responding to basic commands (`ls`, `whoami`, `uname`).
* **IP Geolocation**: Automatically enriches logs with the attacker's geographical location and ISP information.
* **Secure Deployment**: Runs inside a Docker container to isolate it from the host system, ensuring security.
* **Real-time Logging**: All connection attempts and commands are logged to the console and a persistent file.

---

## 🛠️ Setup & Deployment

This project is designed to be run as a Docker container for maximum security and ease of setup.

### Prerequisites
* [Docker](https://www.docker.com/) or [Podman](https://podman.io/) installed.
* An understanding of the security risks of running a honeypot. **Only run this in a controlled, isolated environment.**

### Deployment Steps

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your_username/your_repository.git](https://github.com/your_username/your_repository.git)
    cd your_repository
    ```

2.  **Build the Docker image:**
    ```bash
    docker build -t advanced-honeypot .
    ```

3.  **Run the container:**
    This command starts the honeypot in the background and maps the necessary ports.
    ```bash
    docker run -d --name honeypot-container \
      -p 21:21 \
      -p 22:22 \
      -p 23:23 \
      -p 80:80 \
      advanced-honeypot
    ```
    *Note: On some systems, you may need to configure the system to allow rootless containers to bind to privileged ports (< 1024).*

---

##  usage

Once the container is running, all interactions are logged automatically.

* **View Live Logs:**
    To see the honeypot's activity in real-time, follow the container's logs:
    ```bash
    docker logs -f honeypot-container
    ```

* **Access the Log File:**
    A persistent log file named `honeypot.log` will be created inside the container. You can copy it to your host machine for analysis:
    ```bash
    docker cp honeypot-container:/app/honeypot.log .
    ```

* **Testing a Connection:**
    From another terminal, you can test the honeypot's services:
    ```bash
    telnet <your_docker_host_ip> 23
    ```
