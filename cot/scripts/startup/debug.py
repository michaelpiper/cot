import socket

HOST = "0.0.0.0"  # Listen on all available interfaces
PORT = 9080       # Choose a port
def debug():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Listening for logs on {HOST}:{PORT}...")
        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(f"{data.decode('utf-8', errors="ignore")}")


# Run the Flask app
if __name__ == "__main__":
    debug()