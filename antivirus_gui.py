import tkinter as tk
from tkinter import messagebox
import psutil
import requests

# GitHub raw URL for the suspicious process list
GITHUB_PROCESS_URL = "https://raw.githubusercontent.com/<your-username>/antivirus-signatures/main/processes.txt"

# Fetch the list of suspicious apps
def fetch_suspicious_apps():
    try:
        response = requests.get(GITHUB_PROCESS_URL)
        if response.status_code == 200:
            return [line.strip() for line in response.text.splitlines() if line.strip()]
        else:
            return []
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch suspicious apps: {e}")
        return []

# Find and stop suspicious apps
def scan_and_stop():
    suspicious_apps = fetch_suspicious_apps()
    if not suspicious_apps:
        messagebox.showinfo("Info", "No suspicious apps found in the list.")
        return

    log_text.delete("1.0", tk.END)  # Clear previous logs
    log_text.insert(tk.END, "Scanning running processes...\n")

    suspicious_found = False
    for process in psutil.process_iter(['pid', 'name']):
        try:
            process_name = process.info['name']
            process_pid = process.info['pid']
            if process_name in suspicious_apps:
                suspicious_found = True
                log_text.insert(tk.END, f"Suspicious app detected: {process_name} (PID: {process_pid})\n")
                process_instance = psutil.Process(process_pid)
                process_instance.terminate()
                log_text.insert(tk.END, f"Stopped: {process_name}\n")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if not suspicious_found:
        log_text.insert(tk.END, "No suspicious processes detected.\n")

# GUI setup
root = tk.Tk()
root.title("Antivirus Scanner")

# Window layout
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

# Label
label = tk.Label(frame, text="Antivirus Process Scanner", font=("Arial", 16))
label.pack(pady=10)

# Button to scan and stop suspicious processes
scan_button = tk.Button(frame, text="Scan and Stop Processes", command=scan_and_stop, font=("Arial", 12))
scan_button.pack(pady=5)

# Log output
log_label = tk.Label(frame, text="Logs:", font=("Arial", 12))
log_label.pack(anchor="w", pady=(10, 0))
log_text = tk.Text(frame, wrap=tk.WORD, height=15, width=50)
log_text.pack(fill=tk.BOTH, expand=True)

# Run the GUI
root.mainloop()
