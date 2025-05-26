# Darkelf Browser (Compiled Release)

Darkelf is a stealth-optimized, privacy-hardened browser built with PySide6 and cryptographic safeguards.  
This release ships with the core logic compiled into `.so` binaries using Cython to protect source code.
Please make to place both .so files with launch.py file into the same folder on the desktop. - Name: darkelf_build or darkelf_core

---

## 🚀 How to Launch

> ✅ Works on **Apple M1, M2, M3, M4 (ARM64)** running **macOS**  
> ⚠️ Requires **Python 3.11** specifically (due to compiled binary)

---

### 1. Clone the Repo and Set Up

```bash
git clone https://github.com/Darkelf2024/Darkelf-Browser.git
cd Darkelf-Browser
```

---

### 2. Install Dependencies

Install all required packages using the included `requirements.txt`:

```bash
pip install -r requirements.txt
```

Or manually, if needed:

```bash
pip install PySide6 cryptography adblockparser httpx dnspython stem psutil Pillow piexif PyPDF2
```

---

### 3. Run the Browser

Run one of the compiled builds:

```bash
python3 launch_darkelf.py extreme
# or
python3 launch_darkelf.py osint
```

---

## 🧱 Files Included

| File                                              | Purpose                          |
|---------------------------------------------------|----------------------------------|
| [`darkelf_extreme.cpython-311-darwin.so`](https://github.com/Darkelf2024/Darkelf-Browser/blob/main/darkelf_extreme.cpython-311-darwin.so)       | Compiled main browser engine     |
| [`darkelf_osint_stealth.cpython-311-darwin.so`](https://github.com/Darkelf2024/Darkelf-Browser/blob/main/darkelf_osint_stealth.cpython-311-darwin.so) | OSINT-focused stealth module     |
| [`launch_darkelf.py`](https://github.com/Darkelf2024/Darkelf-Browser/blob/main/launch_darkelf.py)                       | Launches either mode             |
| [`requirements.txt`](https://github.com/Darkelf2024/Darkelf-Browser/blob/main/requirements.txt)                         | Dependency list                  |
| `README.md`                                       | You're reading it                |

---

## ⚠️ System Requirements

- ✅ macOS (M1–M4, ARM64)
- ✅ Python **3.11** installed
- ✅ QtWebEngine (via `PySide6`)
- ✅ `tor` (`brew install tor`) for anonymized routing

---

## 🛡️ Security Notes

- 🔒 Core logic is obfuscated and Cython-compiled
- 🧅 Optional Tor SOCKS proxy support (127.0.0.1:9052)
- 🧬 Encrypted logs, secure cookies, and anti-forensics logic
- 💻 Runtime RAM-wipe and forensic tool detection included

---

## 🧠 Want the Source?

> Source `.py` files are also available in the repo for transparency and community contributions.  
You can use either `.py` or `.so` depending on your needs.

---

## 📜 License

Darkelf is licensed under **LGPL** — feel free to use, fork, and contribute.

---

## 💬 Support

For questions, submit an issue or visit:  
[https://github.com/Darkelf2024/Darkelf-Browser](https://github.com/Darkelf2024/Darkelf-Browser)
