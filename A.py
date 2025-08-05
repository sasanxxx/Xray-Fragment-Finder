"""
Project: Xray Fragment Tester
Author: github.com/sasanxxx
"""
import subprocess
import os
import time
import json
import itertools
import requests
import platform
import csv
from core import generate_config

XRAY_PATH = "xray.exe"
TEMP_CONFIG_FILE = "temp_config.json"
BASE_CONFIG_FILENAME = "Xray_Config (Fragment).json"
PARAMS_FILENAME = "params.json"
RESULTS_FILENAME = "results.csv"
xray_process = None

COMMON_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

def start_xray(config_content: dict):
    global xray_process
    stop_xray()
    try:
        with open(TEMP_CONFIG_FILE, "w", encoding='utf-8') as f: json.dump(config_content, f, indent=2)
    except Exception as e:
        print(f"  [FAIL] Error saving config: {e}"); return False
    
    try:
        creationflags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
        xray_process = subprocess.Popen([XRAY_PATH, "-c", TEMP_CONFIG_FILE], creationflags=creationflags, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
        if xray_process.poll() is not None:
            print(f"  [FAIL] Xray exited immediately."); return False
        return True
    except Exception as e:
        print(f"  [FAIL] Error starting Xray: {e}"); return False

def stop_xray():
    global xray_process
    if xray_process and xray_process.poll() is None:
        try: xray_process.kill()
        except Exception: pass
    if platform.system() == "Windows": subprocess.run(["taskkill", "/F", "/IM", "xray.exe"], capture_output=True, check=False)
    else: subprocess.run(["killall", "-9", "xray"], capture_output=True, check=False)

def test_accessibility(proxy_url: str | None, websites: list) -> bool:
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    for site in websites:
        try:
            response = requests.get(site, proxies=proxies, timeout=30, headers=COMMON_HEADERS)
            if response.status_code != 200: return False
        except requests.exceptions.RequestException: return False
    return True

def measure_speed_and_latency(proxy_url: str | None) -> tuple[float | None, float | None]:
    speed, latency = None, None
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    try:
        lat_res = requests.get("https://www.google.com", proxies=proxies, timeout=30, headers=COMMON_HEADERS)
        if lat_res.status_code == 200: latency = lat_res.elapsed.total_seconds() * 1000
        
        speed_res = requests.get("https://cachefly.cachefly.net/10mb.test", proxies=proxies, headers=COMMON_HEADERS, timeout=90, stream=True)
        speed_res.raise_for_status()
        start_time = time.time()
        total_size_bytes = sum(len(chunk) for chunk in speed_res.iter_content(chunk_size=8192))
        duration_seconds = time.time() - start_time
        if duration_seconds > 0: speed = (total_size_bytes * 8) / duration_seconds / 1_000_000
    except requests.exceptions.RequestException: pass
    return speed, latency

if __name__ == "__main__":
    try:
        if os.path.exists(PARAMS_FILENAME):
            print(f"Loading parameters from '{PARAMS_FILENAME}'...")
            with open(PARAMS_FILENAME, 'r', encoding='utf-8') as f:
                params_from_gui = json.load(f)
            PARAMETER_GRID = {k: v for k, v in params_from_gui.items() if k != "websites_to_test"}
            WEBSITES_TO_TEST = params_from_gui["websites_to_test"]
        else:
            print("No params.json found, using default parameters...")
            PARAMETER_GRID = {"fragment_length": ["5-10", "20-40"],"fragment_interval": ["10-20", "20-30"],"server_name": ["www.google.com", "www.microsoft.com"],"dns_server_url": ["https://dns.google/dns-query", "https://cloudflare-dns.com/dns-query"]}
            WEBSITES_TO_TEST = ["https://www.google.com", "https://www.youtube.com"]

        with open(BASE_CONFIG_FILENAME, "r", encoding='utf-8') as f:
            BASE_CONFIG_TEMPLATE = json.load(f)
        print(f"Successfully loaded base config from '{BASE_CONFIG_FILENAME}'")
        
        keys, values = zip(*PARAMETER_GRID.items())
        all_combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]
        
        file_exists = os.path.isfile(RESULTS_FILENAME)
        with open(RESULTS_FILENAME, 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            if not file_exists:
                csv_writer.writerow(['Timestamp', 'Fragment Length', 'Fragment Interval', 'Server Name', 'DNS Server', 'Accessibility', 'Speed (Mbps)', 'Latency (ms)'])

            print("\n--- Starting Grid Search ---")
            
            for i, params in enumerate(all_combinations):
                print(f"\n[TEST {i+1}/{len(all_combinations)}] with {params}")
                baseline_speed, baseline_latency = measure_speed_and_latency(proxy_url=None)
                if baseline_speed: print(f"  -> Baseline: Speed={baseline_speed:.2f} Mbps | Latency={baseline_latency:.2f} ms")
                else: print("  -> Warning: Could not establish a stable baseline connection.")

                config = generate_config(BASE_CONFIG_TEMPLATE, params)
                if start_xray(config):
                    proxy_url = "socks5h://127.0.0.1:10808"
                    is_accessible = test_accessibility(proxy_url=proxy_url, websites=WEBSITES_TO_TEST)
                    
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    if is_accessible:
                        print("  -> Accessibility: SUCCESS")
                        proxy_speed, proxy_latency = measure_speed_and_latency(proxy_url=proxy_url)
                        if proxy_speed and proxy_latency:
                            usage_str = f"({(proxy_speed/baseline_speed)*100:.1f}%)" if baseline_speed else ""
                            print(f"  -> Metrics: Speed={proxy_speed:.2f} Mbps {usage_str}, Latency={proxy_latency:.2f} ms")
                            csv_writer.writerow([timestamp, params['fragment_length'], params['fragment_interval'], params['server_name'], params['dns_server_url'], 'Success', f"{proxy_speed:.2f}", f"{proxy_latency:.2f}"])
                        else:
                            print("  -> Metrics Test: FAILED")
                            csv_writer.writerow([timestamp, params['fragment_length'], params['fragment_interval'], params['server_name'], params['dns_server_url'], 'Success (Metrics Failed)', 'N/A', 'N/A'])
                    else:
                        print("  -> Accessibility: FAILED")
                        csv_writer.writerow([timestamp, params['fragment_length'], params['fragment_interval'], params['server_name'], params['dns_server_url'], 'Failed', 'N/A', 'N/A'])
        
        print("\n--- Grid Search Finished ---")
        print(f"Results have been saved to '{RESULTS_FILENAME}'")

    except FileNotFoundError as e:
        print(f"\nFATAL ERROR: A required file was not found: {e}. Make sure xray.exe and {BASE_CONFIG_FILENAME} are in the same folder as the script.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        print("-> Final cleanup: Ensuring Xray is stopped.")
        stop_xray()
        input("Press Enter to exit...")