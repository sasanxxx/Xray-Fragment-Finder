# Xray Fragment Finder

Automatically discover the optimal Xray `fragment` configuration for your network.

## 📝 Overview

This project is a Python-based tool with a simple GUI designed to automate the process of finding the best Xray `fragment` parameters. It performs a comprehensive grid search over various settings, tests connectivity to user-defined websites, measures performance metrics like speed and latency, and saves all results to a CSV file for easy analysis.

This tool is intended to help users in regions with heavy internet filtering find a working configuration to restore access and identify the most performant connection settings.

---

## ✨ Features

* **Simple GUI Launcher:** An easy-to-use Tkinter interface (`launcher.py`) to input your test parameters.
* **Automated Grid Search:** Tests all combinations of `fragment length`, `interval`, `server_name`, and `dns_server_url`.
* **Accessibility Testing:** Verifies that a configuration can successfully connect to multiple user-defined websites (e.g., Google, YouTube).
* **Performance Measurement:** Measures real-world download speed (Mbps) and connection latency (ms) for each successful configuration.
* **Baseline Comparison:** Automatically tests your direct internet connection before each proxy test to provide a clear performance benchmark.
* **Persistent Results:** All test results are incrementally saved to a `results.csv` file, so no data is lost if the script is interrupted.
* **One-Click Setup:** Includes a `setup.bat` script to automatically download the latest version of Xray-core and install all required Python libraries.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8 or newer.
* Windows operating system (the `setup.bat` script is designed for Windows).

### Quick Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/sasanxxx/Xray-Fragment-Finder.git
    ```

2.  **Navigate into the project directory:**
    ```bash
    cd Xray-Fragment-Finder
    ```

3.  **Run the setup script:**
    ```bash
    setup.bat
    ```
    This script will handle everything: it installs the necessary Python libraries and downloads the latest `xray.exe` into the project folder.

---

## 💻 How to Use

1.  **(Optional) Edit the Base Config:** You can modify the `Xray_Config (Fragment).json` file if you need to change fundamental settings like the inbound port.
2.  **Run the Launcher:**
    ```bash
    python launcher.py
    ```
3.  **Enter Parameters:** Fill in the comma-separated values you want to test in the GUI window.
4.  **Start the Test:** Click the **"Start Test"** button.
5.  **Monitor Progress:** A new console window will appear, showing the live progress of each test.
6.  **Check Results:** When the script is finished, open the `results.csv` file with any spreadsheet program (like Excel or Google Sheets) to view and sort all the successful configurations.

---

### Project Files

* `launcher.py`: The graphical user interface used to start the tests.
* `A.py`: The main script containing the core testing logic.
* `Xray_Config (Fragment).json`: The base Xray configuration file used as a template.
* `setup.bat`: The automated installer for dependencies and Xray-core.
* `requirements.txt`: A list of Python libraries needed for the project.
