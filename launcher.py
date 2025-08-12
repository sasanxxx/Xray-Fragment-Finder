"""
Project: Xray Fragment Tester
Author: github.com/sasanxxx
"""
import tkinter as tk
from tkinter import messagebox, font, filedialog
import json
import subprocess
import os
from core import generate_config

BEST_RESULT_FILENAME = "best_result.json"

# ## <-- CORRECTED: This dictionary was missing and has been added back.
DEFAULT_PARAMS = {
    "fragment_length": "5-10, 20-40",
    "fragment_interval": "10-20, 20-30",
    "server_name": "www.google.com, www.microsoft.com",
    "dns_server_url": "https://dns.google/dns-query, https://cloudflare-dns.com/dns-query",
    "websites_to_test": "https://www.google.com, https://www.youtube.com"
}

def get_params_from_gui(single_values=False):
    params = {}
    for key, entry in entries.items():
        value = entry.get().strip()
        if not value:
            raise ValueError(f"Field '{labels[key]}' cannot be empty.")
        if not single_values:
            params[key] = [s.strip() for s in value.split(',')]
        else:
            params[key] = value.split(',')[0].strip()
    return params

def start_test():
    try:
        params_to_save = get_params_from_gui()
        with open("params.json", "w", encoding='utf-8') as f:
            json.dump(params_to_save, f, indent=2)
        
        script_path = os.path.join(os.path.dirname(__file__), "A.py")
        if not os.path.exists(script_path):
            messagebox.showerror("Error", "Main script file 'A.py' not found.")
            return
            
        subprocess.Popen(f'cmd /k python "{script_path}"', creationflags=subprocess.CREATE_NEW_CONSOLE)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def generate_config_from_params(params: dict):
    try:
        base_config_filename = "Xray_Config (Fragment).json"
        with open(base_config_filename, "r", encoding='utf-8') as f:
            base_config = json.load(f)
            
        final_config = generate_config(base_config, params)
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Config As...",
            initialfile="generated_config.json"
        )
        
        if file_path:
            with open(file_path, "w", encoding='utf-8') as f:
                json.dump(final_config, f, indent=2)
            messagebox.showinfo("Success", f"Configuration file saved successfully to:\n{file_path}")
            
    except FileNotFoundError:
        messagebox.showerror("Error", f"Base config file '{base_config_filename}' not found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def generate_manual_config():
    try:
        params = get_params_from_gui(single_values=True)
        generate_config_from_params(params)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def generate_best_config():
    try:
        with open(BEST_RESULT_FILENAME, 'r', encoding='utf-8') as f:
            best_params = json.load(f)
        
        if "websites_to_test" not in best_params:
             best_params["websites_to_test"] = "https://www.google.com"
        
        generate_config_from_params(best_params)

    except FileNotFoundError:
        messagebox.showerror("Error", f"Best result file '{BEST_RESULT_FILENAME}' not found.\nPlease run a test first.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- GUI Setup ---
window = tk.Tk()
window.title("Xray Fragment Tester")
window.geometry("600x320")
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

try:
    with open(BEST_RESULT_FILENAME, 'r', encoding='utf-8') as f:
        best_params = json.load(f)
    
    if os.path.exists("params.json"):
        with open("params.json", 'r', encoding='utf-8') as f:
            last_params = json.load(f)
        best_params["websites_to_test"] = ", ".join(last_params["websites_to_test"])
    else:
        best_params["websites_to_test"] = DEFAULT_PARAMS["websites_to_test"]
except FileNotFoundError:
    best_params = None

for i, (key, text) in enumerate(labels.items()):
    label = tk.Label(form_frame, text=text, anchor="w")
    label.grid(row=i, column=0, sticky="w", padx=5, pady=5)
    
    entry = tk.Entry(form_frame, width=60)
    entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
    
    default_value = ""
    if best_params and key in best_params:
        default_value = best_params[key]
    elif key in DEFAULT_PARAMS:
        default_value = DEFAULT_PARAMS[key]
        
    entry.insert(0, default_value)
    entries[key] = entry

form_frame.grid_columnconfigure(1, weight=1)

button_frame = tk.Frame(window)
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Start Test", command=start_test, bg="#28a745", fg="white", font=("Arial", 10, "bold"), width=20)
start_button.pack(side="left", padx=5)

generate_manual_button = tk.Button(button_frame, text="Generate From Fields", command=generate_manual_config, bg="#007bff", fg="white", font=("Arial", 10, "bold"), width=20)
generate_manual_button.pack(side="left", padx=5)

generate_best_button = tk.Button(button_frame, text="Generate Best Config", command=generate_best_config, bg="#ffc107", fg="black", font=("Arial", 10, "bold"), width=20)
generate_best_button.pack(side="left", padx=5)

slogan_font = font.Font(family="Consolas", size=9, slant="italic")
slogan_label = tk.Label(window, text="...because we can!", font=slogan_font, fg="#555555")
slogan_label.pack(pady=5)

window.mainloop()