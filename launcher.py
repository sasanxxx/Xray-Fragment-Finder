"""
Project: Xray Fragment Tester
Author: github.com/sasanxxx
"""
import tkinter as tk
from tkinter import messagebox
from tkinter import font
import json
import subprocess
import os

DEFAULT_PARAMS = {
    "fragment_length": "5-10, 20-40",
    "fragment_interval": "10-20, 20-30",
    "server_name": "www.google.com, www.microsoft.com",
    "dns_server_url": "https://dns.google/dns-query, https://cloudflare-dns.com/dns-query",
    "websites_to_test": "https://www.google.com, https://www.youtube.com"
}

def start_test():
    try:
        params_to_save = {
            "fragment_length": [s.strip() for s in entries["fragment_length"].get().split(',')],
            "fragment_interval": [s.strip() for s in entries["fragment_interval"].get().split(',')],
            "server_name": [s.strip() for s in entries["server_name"].get().split(',')],
            "dns_server_url": [s.strip() for s in entries["dns_server_url"].get().split(',')],
            "websites_to_test": [s.strip() for s in entries["websites_to_test"].get().split(',')]
        }
        
        with open("params.json", "w", encoding='utf-8') as f:
            json.dump(params_to_save, f, indent=2)
        
        script_path = os.path.join(os.path.dirname(__file__), "A.py")
        if not os.path.exists(script_path):
            messagebox.showerror("Error", f"Main script file 'A.py' not found.")
            return
            
        subprocess.Popen(f'cmd /k python "{script_path}"', creationflags=subprocess.CREATE_NEW_CONSOLE)
        
    except Exception as e:
        messagebox.showerror("Script Execution Error", str(e))

window = tk.Tk()
window.title("Xray Fragment Tester Launcher")
window.geometry("600x280") # کمی ارتفاع پنجره را بیشتر کردم
window.resizable(False, False)

form_frame = tk.Frame(window, padx=10, pady=10)
form_frame.pack(fill="x", expand=True)

entries = {}
labels = {
    "fragment_length": "Fragment Length",
    "fragment_interval": "Fragment Interval",
    "server_name": "Server Name",
    "dns_server_url": "DNS Server URL",
    "websites_to_test": "Websites to Test"
}

for i, (key, text) in enumerate(labels.items()):
    label = tk.Label(form_frame, text=text, anchor="w")
    label.grid(row=i, column=0, sticky="w", padx=5, pady=5)
    
    entry = tk.Entry(form_frame, width=60)
    entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
    entry.insert(0, DEFAULT_PARAMS[key])
    entries[key] = entry

form_frame.grid_columnconfigure(1, weight=1)

start_button = tk.Button(window, text="Start Test", command=start_test, bg="green", fg="white", font=("Arial", 10, "bold"))
start_button.pack(pady=10)

# --- [تغییر] اضافه کردن لیبل شعار ---
slogan_font = font.Font(family="Consolas", size=9, slant="italic")
slogan_label = tk.Label(window, text="...because we can!", font=slogan_font, fg="#555555")
slogan_label.pack(pady=5)

window.mainloop()