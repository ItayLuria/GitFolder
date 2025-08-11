import socket
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

SERVER_HOST = 'localhost'
SERVER_PORT = 5000
BUF = 4096

FOLDER = 'client_files'
os.makedirs(FOLDER, exist_ok=True)

def uploadfile():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    filename = os.path.basename(filepath)
    try:
        connection = socket.socket()
        connection.connect((SERVER_HOST, SERVER_PORT))
        connection.send(b"UPLOAD")
        if connection.recv(1024).decode() != "Send file path":
            messagebox.showerror("Error", "Server did not ask for file path.")
            connection.close()
            return
        connection.send(filename.encode())
        with open(filepath, 'rb') as file:
            while True:
                data = file.read(BUF)
                if not data:
                    break
                connection.sendall(data)
        connection.close()
        messagebox.showinfo("Success", f"Uploaded '{filename}'")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def downloadfile():
    name = simpledialog.askstring("Input", "Filename to download:")
    if not name:
        return
    savepath = os.path.join(FOLDER, name)
    try:
        connection = socket.socket()
        connection.connect((SERVER_HOST, SERVER_PORT))
        connection.send(f"DOWNLOAD {name}".encode())
        response = connection.recv(1024).decode()
        if not response.startswith("READY"):
            messagebox.showerror("Error", response)
            connection.close()
            return
        _, filesize_str = response.split()
        filesize = int(filesize_str)
        received = 0
        with open(savepath, 'wb') as file:
            while received < filesize:
                data = connection.recv(BUF)
                if not data:
                    break
                file.write(data)
                received += len(data)
        connection.close()
        messagebox.showinfo("Success", f"Downloaded '{name}'")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("File Upload/Download System")
tk.Button(root, text="Upload", command=uploadfile).pack(padx=180, pady=10)
tk.Button(root, text="Download", command=downloadfile).pack(padx=10, pady=10)
root.mainloop()
