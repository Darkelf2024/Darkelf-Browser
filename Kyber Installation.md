
# 🚀 Complete Guide: Installing liboqs and Running Kyber768 Key Exchange on macOS

This guide provides a **step-by-step installation process** for setting up **Open Quantum Safe (OQS)**, `liboqs`, and its Python bindings, allowing you to run **Kyber768** key exchange on macOS.

---

## ✅ Step 1: Install Required Dependencies

Before installing `liboqs`, ensure you have the required tools:

### 🔹 macOS (Homebrew)
```sh
brew update
brew install cmake ninja git python3 openssl
brew install open-quantum-safe/liboqs/liboqs
brew install pqcrypto
```

---

## ✅ Step 2: Clone and Build `liboqs` (OQS Library)

The `liboqs` library contains implementations of **Kyber768** and other post-quantum cryptography (PQC) algorithms.

### 1️⃣ Clone the Open Quantum Safe (OQS) Library
```sh
git clone --recursive https://github.com/open-quantum-safe/liboqs.git
cd liboqs
```

### 2️⃣ Build `liboqs`
```sh
mkdir build && cd build
cmake -GNinja ..
ninja
sudo ninja install
```

### 3️⃣ Verify Installation
```sh
ls /usr/local/lib | grep oqs
ls /usr/local/include/oqs
```
If files like `liboqs.a` and `oqs.h` appear, the installation was successful! 🎉

---

## ✅ Step 3: Install Python Bindings (`liboqs-python`)

Now, install the **Python wrapper** for `liboqs`.

### 1️⃣ Create a Virtual Environment (Recommended)
```sh
python3 -m venv pqcrypto_env
source pqcrypto_env/bin/activate  # Activate the environment
```

### 2️⃣ Clone and Install `liboqs-python`
```sh
git clone --recursive https://github.com/open-quantum-safe/liboqs-python.git
cd liboqs-python
pip install --upgrade pip
pip install cmake ninja
pip install .
```

### 3️⃣ Test Python Installation
```sh
python3 -c "import oqs; print(dir(oqs))"
```
If `KeyEncapsulation` appears in the list, everything is set up correctly! ✅

---

## ✅ Step 4: Run a Kyber768 Key Exchange Test

Now, test **Kyber768** encryption and decryption.

### 🔹 Save this as `test_kyber.py`
```python
import oqs

def kyber768_key_exchange():
    print("🚀 Performing Kyber768 Key Exchange...")

    # Alice (Key Generation)
    alice_kem = oqs.KeyEncapsulation("Kyber768")
    alice_public_key = alice_kem.generate_keypair()
    
    # Bob (Encapsulate Secret)
    bob_kem = oqs.KeyEncapsulation("Kyber768")
    ciphertext, shared_secret_bob = bob_kem.encap_secret(alice_public_key)

    # Alice (Decapsulate Secret)
    shared_secret_alice = alice_kem.decap_secret(ciphertext)

    assert shared_secret_alice == shared_secret_bob, "❌ Key exchange failed!"
    
    print("✅ Kyber768 Key Exchange Successful!")
    print(f"Shared Secret: {shared_secret_alice.hex()}")

kyber768_key_exchange()
```

### 🔹 Run the test
```sh
python3 test_kyber.py
```

If the output includes `"✅ Kyber768 Key Exchange Successful!"`, everything is working! 🚀🎉  

---

## ✅ Step 5: Re-enable SIP on macOS (If Disabled)

If you disabled **System Integrity Protection (SIP)** to fix permission errors, you should re-enable it:

1. Restart your Mac **in Recovery Mode** (`Command + R` while booting).
2. Open **Terminal** in Recovery Mode.
3. Run:
   ```sh
   csrutil enable
   ```
4. Restart and verify everything still works.

Note: Works with Python3.11

---

## 🚀 You're Ready!

You have successfully installed **Open Quantum Safe (OQS)**, `liboqs`, and `liboqs-python`, and **tested Kyber768 encryption** on macOS! 🔥  

Let me know if you need help! 🚀
```
- The information provided is for research and educational purposes
- Darkelf Browser Kyber768 Edition is in testing phases - Release in the future 
