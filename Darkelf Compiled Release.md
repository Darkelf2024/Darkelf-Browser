# Darkelf Browser (Compiled Release)

Darkelf is a stealth-optimized, privacy-hardened browser built with PySide6 and cryptographic safeguards.  
This version ships with the core logic compiled to a `.so` binary using Cython to protect source code.

---

## 🚀 How to Launch

> Make sure you have **Python 3.11** installed (required to match the compiled binary).

### 1. Install Dependencies

Install the required libraries (preferably in a virtual environment):

```bash
pip install PySide6 cryptography adblockparser httpx dnspython stem psutil Pillow piexif
```

> Optional (for PDFs):
```bash
pip install PyPDF2
```

---

### 2. Run the Browser

From the project directory, run:

```bash
python3 launch_darkelf.py
```

This script:
- Loads the compiled logic from `darkelf_extreme.cpython-311-darwin.so`
- Launches the full Darkelf GUI

---

## 🧱 Files Included

| File                                | Purpose                          |
|-------------------------------------|----------------------------------|
| `darkelf_extreme.cpython-311-darwin.so` | Cython-compiled browser logic    |
| `launch_darkelf.py`                 | Entry point to run the browser   |
| `README.md`                         | You're reading it                |

---

## ⚠️ Requirements

- macOS (Darwin) ARM64 (M1/M2)
- Python **3.11**
- QtWebEngine (via PySide6)
- Optional: Tor installed (`brew install tor`) for anonymized network support

---

## 🛡️ Security Notes

- Core logic is obfuscated and compiled
- Tor SOCKS proxy support (127.0.0.1:9052) is integrated
- Encrypted logs, cookie protection, and anti-forensics mechanisms included

---

## 💬 Support

For questions, submit an issue or visit:  
[https://github.com/Darkelf2024/Darkelf-Browser](https://github.com/Darkelf2024/Darkelf-Browser)
