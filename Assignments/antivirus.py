import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import time
import os
import threading

API_KEY = "870b51e07a9e76516a37de0232c9bb60cb1d2371f1388ea05140a25b9c2edfde"
VT_UPLOAD_URL = "https://www.virustotal.com/api/v3/files"
headers = {"x-apikey": API_KEY}

def browse_file():
    path = filedialog.askopenfilename()
    if path:
        file_path_var.set(path)
        result_var.set("")

def scan_file():
    filepath = file_path_var.get()
    if not filepath:
        messagebox.showwarning("No file selected", "Please select a file to scan.")
        return

    scan_button.config(state="disabled")
    result_var.set("Uploading... please wait.")
    root.update_idletasks()

    def worker():
        try:
            filepath_norm = os.path.normpath(filepath)
            with open(filepath_norm, "rb") as f:
                files = {"file": (os.path.basename(filepath_norm), f)}
                response = requests.post(VT_UPLOAD_URL, headers=headers, files=files)

            if response.status_code not in (200, 201):
                update_result(f"Upload failed: {response.status_code}")
                enable_scan()
                return

            analysis_id = response.json()["data"]["id"]
            analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"

            for _ in range(12):
                analysis_response = requests.get(analysis_url, headers=headers)
                data = analysis_response.json()
                status = data["data"]["attributes"]["status"]
                if status == "completed":
                    break
                update_result("Scan in progress...")
                time.sleep(3)
            else:
                update_result("Scan did not complete within 1 minute.")
                enable_scan()
                return

            stats = data["data"]["attributes"]["stats"]
            malicious_count = stats.get("malicious", 0)

            if malicious_count > 0:
                update_result(f"File is NOT SAFE! {malicious_count} suspicious attributes were found...")
            else:
                update_result("This file appears to be clean.")
        except Exception as e:
            update_result(f"Error: {str(e)}")

        enable_scan()

    threading.Thread(target=worker, daemon=True).start()

def update_result(text):
    root.after(0, lambda: result_var.set(text))

def enable_scan():
    root.after(0, lambda: scan_button.config(state="normal"))

root = tk.Tk()
root.title("Antivirus Scanner")
root.geometry("500x180")

file_path_var = tk.StringVar()
result_var = tk.StringVar()

tk.Label(root, text="Select file to scan:").pack(pady=5)
tk.Entry(root, textvariable=file_path_var, width=60).pack(pady=5)
tk.Button(root, text="Browse", command=browse_file).pack(pady=5)
scan_button = tk.Button(root, text="Scan", command=scan_file)
scan_button.pack(pady=10)
tk.Label(root, textvariable=result_var, wraplength=450, fg="blue").pack(pady=10)

root.mainloop()