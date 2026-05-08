# XSLT-Transformer

### 🖥️ OS Support & Download

| Platform | Recommended (One-click) | Advanced (Source Code) |
|---|---|---|
| **Windows** | [Download XSLT-Transformer.exe](XSLT-Transformer.exe) | [See Source Code section](#-installation--source-code) |
| **Linux / macOS** | — | [See Source Code section](#-installation--source-code) |

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Quick Start

1. **Download**: Click on `XSLT-Transformer.exe` in the file list above and click the "Download" button.
2. **Run**: Double-click the file. 
   * *Note: If Windows shows a "Windows protected your PC" warning, click "More info" and then "Run anyway".*
3. **Use**: Select your XML and XSL files, then click **⚡ Transform**.

- **Python 3.8+** → [Download Python](https://www.python.org/downloads/)

---

## 🛠️ Installation / Source Code

This method works for **Windows, Linux, and macOS**. Open your terminal (**PowerShell**, **CMD**, or **Bash**) inside the project folder and run:

```powershell
pip install lxml customtkinter
```

| Package | Purpose |
|---|---|
| `lxml` | High-performance XML/XSLT processing engine |
| `customtkinter` | Modern, themeable Tkinter widget library |

---

## Running the Application

```powershell
python .\transformar.py
```

The GUI window will open immediately.

---

## Usage

1. Click **Browse** next to *XML File* and select your source `.xml` file.
2. Click **Browse** next to *XSL Stylesheet* and select your `.xsl` or `.xslt` file.
3. Optionally click **Browse** next to *Output File* to choose where to save the result (defaults to `~/resultado.html`).
4. Click **⚡ Transform**.
5. Once complete, open the generated file in your browser or any text editor.

> **Tip:** If the transformation fails, an error dialog will appear with the exact XSLT error message from `lxml` to help you debug your stylesheet.

---

## 🐧 Linux / 🍎 macOS Specifics

If you are on Linux or macOS, follow the installation steps above. If you don't have Python installed yet:
2. **Install Python** (if not installed):
   - **Linux**: `sudo apt update && sudo apt install python3 python3-pip`
   - **macOS**: `brew install python`
3. **Install Dependencies**:
   ```bash
   pip install lxml customtkinter
   ```
4. **Run**:
   ```bash
   python transformar.py
   ```

---

## License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute it.
