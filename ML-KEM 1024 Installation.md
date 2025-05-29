# 🚀 Complete Guide: Installing liboqs + ML-KEM-1024 on macOS

This guide walks you through installing **Open Quantum Safe (OQS)** components for **ML-KEM-1024**, the NIST-standardized Kyber variant, along with Python bindings and a test for post-quantum key exchange.

> 🧪 For research, development, and secure application testing. Verified on macOS with Python 3.11+ and Apple Silicon/Intel.

---

## ✅ Step 1: Install Required Tools and Dependencies

Make sure [Homebrew](https://brew.sh) is installed.

```bash
brew update
brew install cmake ninja git python3 openssl
brew install open-quantum-safe/liboqs/liboqs
```

This installs the latest stable `liboqs` with support for ML-KEM.

---

## ✅ Step 2: (Optional) Clone and Build liboqs from Source

Skip this step if you're using Homebrew’s prebuilt `liboqs`.

```bash
git clone --recursive https://github.com/open-quantum-safe/liboqs.git
cd liboqs
mkdir build && cd build
cmake -GNinja ..
ninja
sudo ninja install
```

Verify it installed:

```bash
ls /usr/local/lib | grep oqs
ls /usr/local/include/oqs
```

You should see `liboqs.a` and `oqs.h`.

---

## ✅ Step 3: Install Python Bindings (`liboqs-python`)

Create and activate a Python virtual environment:

```bash
python3 -m venv pqcrypto_env
source pqcrypto_env/bin/activate
```

Clone and install Python bindings:

```bash
git clone --recursive https://github.com/open-quantum-safe/liboqs-python.git
cd liboqs-python

export LDFLAGS="-L/opt/homebrew/opt/liboqs/lib"
export CFLAGS="-I/opt/homebrew/opt/liboqs/include"

pip install --upgrade pip
pip install cmake ninja
pip install .
```

Verify the install:

```bash
python3 -c "import oqs; print(hasattr(oqs, 'KeyEncapsulation'))"
```

It should print `True`.

---

## ✅ Step 4: Test ML-KEM-1024 Key Exchange

Save the following code as `test_mlkem1024.py`:

```python
import oqs

def mlkem_1024_key_exchange():
    print("🚀 Performing ML-KEM-1024 Key Exchange...")

    alice_kem = oqs.KeyEncapsulation("ML-KEM-1024")
    alice_public = alice_kem.generate_keypair()

    bob_kem = oqs.KeyEncapsulation("ML-KEM-1024")
    ciphertext, shared_bob = bob_kem.encapsulate(alice_public)

    shared_alice = alice_kem.decapsulate(ciphertext)

    assert shared_bob == shared_alice, "❌ Key mismatch!"
    print("✅ ML-KEM-1024 Key Exchange Successful!")
    print(f"Shared Secret: {shared_alice.hex()}")

mlkem_1024_key_exchange()
```

Run the test:

```bash
python3 test_mlkem1024.py
```

Expected output:

```
✅ ML-KEM-1024 Key Exchange Successful!
Shared Secret: <hex string>
```

---

## ✅ Step 5: (Optional) Add Hybrid X25519 + ML-KEM-1024

Install NaCl for X25519:

```bash
pip install pynacl
```

### 🔒 Public Interface (Simplified Preview)

```python
class HybridKEMX25519MLKEM1024:
    def __init__(self): ...
    def encapsulate_for_peer(self, peer_mlkem_public_key, peer_x25519_public_key): ...
    def generate_shared_secret(self, peer_x25519_pub, peer_mlkem_ciphertext): ...
    def export_public(self): ...
    def export_private(self): ...
```

> 📌 Full source code is currently **private** and undergoing security review. This interface is shared for reference and integration planning.  
> It enables **hybrid key exchange** by combining X25519 and ML-KEM-1024 into a single, quantum-secure session key.

---

## ✅ Step 6: Re-enable SIP (If You Disabled It Earlier)

If you disabled SIP for installation:

1. Restart Mac and hold `Command + R` to enter Recovery Mode  
2. Open Terminal  
3. Run:

```bash
csrutil enable
```

4. Restart again and verify everything works

---

## 🧠 Notes

- Works with **Python 3.11+**
- Compatible with **Apple Silicon and Intel Macs**
- Secure by design for **post-quantum and hybrid key exchange**
- Based on final **NIST ML-KEM specification** (successor to Kyber)

---

## 🔐 You're Ready!

You now have a full Open Quantum Safe dev stack on macOS with:

- `liboqs` + `liboqs-python`
- ML-KEM-1024 support
- Verified encryption/decryption
- Optional hybrid mode with X25519
- Ready for integration into Darkelf Browser PQC Edition

---

> 📌 For research and educational use.  
> 🔐 Darkelf Browser PQC Edition is in active development.  
> 📅 Last Updated: 2025-05-29

