import logging
import socket

class TCPLoggingHandler(logging.Handler):
    def __init__(self, host: str, port: int):
        super().__init__()
        self.host = host
        self.port = port

    def emit(self, record):
        log_entry = self.format(record)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.host, self.port))
                sock.sendall(log_entry.encode("utf-8"))
        except Exception as e:
            print(f"Logging error: {e}")

# Configure Logger
LOG_SERVER_HOST = "127.0.0.1"  # Change to remote server if needed
LOG_SERVER_PORT = 9080

logger = logging.getLogger("TCPLogger")
logger.setLevel(logging.INFO)

# Add TCP logging handler
tcp_handler = TCPLoggingHandler(LOG_SERVER_HOST, LOG_SERVER_PORT)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
tcp_handler.setFormatter(formatter)

logger.addHandler(tcp_handler)

