import socket
import os

FOLDER = 'server_files'
os.makedirs(FOLDER, exist_ok=True)

print("Server running on port 5000")
print("Working directory:", os.getcwd())
print(f"Saving files to: {FOLDER}")

server_socket = socket.socket()
server_socket.bind(('localhost', 5000))
server_socket.listen(3)

while True:
    client, _ = server_socket.accept()
    action = client.recv(1024).decode()

    if action == "UPLOAD":
        client.send(b"Send file path")
        filename = client.recv(1024).decode()
        save_path = os.path.join(FOLDER, filename)
        print(f"Receiving file: {filename} → {save_path}")

        with open(save_path, 'wb') as file:
            while True:
                data = client.recv(4096)
                if not data:
                    break
                file.write(data)

        print(f"Uploaded '{filename}' successfully")

    elif action.startswith("DOWNLOAD"):
        parts = action.split(maxsplit=1)
        if len(parts) < 2:
            client.send(b"ERROR: No filename")
        else:
            filename = parts[1]
            filepath = os.path.join(FOLDER, filename)
            if not os.path.exists(filepath):
                client.send(b"ERROR: File not found")
            else:
                filesize = os.path.getsize(filepath)
                client.send(f"READY {filesize}".encode())
                with open(filepath, 'rb') as file:
                    while True:
                        data = file.read(4096)
                        if not data:
                            break
                        client.sendall(data)
                print(f"Sent '{filename}'")

    else:
        client.send(b"ERROR: Unknown command")

    client.close()
