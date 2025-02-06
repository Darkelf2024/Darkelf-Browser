# Encryption Features

The current implementation of Darkelf includes several layers of encryption and security features. Here's a detailed breakdown.

# Encryption Layers in Darkelf Browser

Darkelf Browser implements multiple layers of encryption to ensure **secure communication, data protection, and user privacy**. The encryption mechanisms include **ECDH for key exchange, AES-CBC for symmetric encryption, RSA-OAEP for asymmetric encryption, and a secure PRNG** for cryptographic operations.

---

## **1. ECDH (Elliptic Curve Diffie-Hellman) - Secure Key Exchange**
### **Purpose:**  
ECDH is used to establish a **shared secret** between parties over an untrusted channel.

### **Implementation:**  
- The browser's **Web Cryptography API** generates an **ECDH key pair**.
- Public keys are securely exchanged.
- A **shared secret** is derived from the exchanged public keys.
- This shared secret is used as an encryption key for **AES-GCM encryption**.

### **Security Benefits:**  
✅ Ensures **perfect forward secrecy (PFS)**.  
✅ Prevents third parties from decrypting exchanged data even if they intercept public keys.  

---

## **2. AES-CBC (Advanced Encryption Standard - Cipher Block Chaining) - Symmetric Encryption**
### **Purpose:**  
AES-CBC is used to encrypt and decrypt data securely with a **symmetric key**.

### **Implementation:**  
- A **256-bit AES key** is randomly generated.
- A **random 16-byte IV** (Initialization Vector) is generated for each encryption.
- The **plaintext is padded** to a multiple of 16 bytes before encryption.
- The **AES-CBC cipher** encrypts the padded plaintext.
- The **IV is prepended to the ciphertext** for decryption integrity.

### **Security Benefits:**  
✅ AES is **fast and efficient** for large data.  
✅ CBC mode ensures **data confidentiality**, but integrity must be verified separately.  

---

## **3. RSA-OAEP (Rivest-Shamir-Adleman with Optimal Asymmetric Encryption Padding) - Public Key Encryption**
### **Purpose:**  
RSA-OAEP is used for **securely encrypting and decrypting data** using public and private keys.

### **Implementation:**  
- A **4096-bit RSA key pair** is generated.
- The **RSA public key** encrypts data.
- The **RSA private key** decrypts encrypted data.
- OAEP padding is used for **increased security**.

### **Security Benefits:**  
✅ RSA ensures **confidentiality** for sensitive data.  
✅ OAEP padding **prevents common attacks** like chosen plaintext attacks.  

---

## **4. AES-GCM (Advanced Encryption Standard - Galois/Counter Mode) - Authenticated Encryption**
### **Purpose:**  
AES-GCM is used as an **authenticated encryption** method after the **ECDH key exchange**.

### **Implementation:**  
- The **shared secret** from ECDH is used as the AES-GCM encryption key.
- A **random 12-byte IV** is generated.
- AES-GCM encrypts the plaintext **and produces an authentication tag**.
- This tag ensures **data integrity and authenticity**.

### **Security Benefits:**  
✅ AES-GCM provides **both encryption and authentication**.  
✅ Protects against **man-in-the-middle (MITM) attacks**.  

---

## **5. Secure Pseudo-Random Number Generator (PRNG) - WebCrypto API**
### **Purpose:**  
Darkelf uses **cryptographically secure random number generation** to enhance security.

### **Implementation:**  
- The **WebCrypto API's getRandomValues()** function generates **random bytes**.
- The random bytes are used for **key generation, IVs, and cryptographic operations**.

### **Security Benefits:**  
✅ Ensures **high entropy** and **unpredictability** for encryption keys.  
✅ Prevents predictable values that could compromise security.  

---

## **Post-Quantum Encryption (Future Implementation - Placeholder)**
### **Purpose:**  
To protect against future quantum computing threats, Darkelf plans to integrate **post-quantum cryptography**.

### **Planned Implementation:**  
- Replace RSA with **NIST-standardized post-quantum cryptographic algorithms**.
- Use libraries like **Open Quantum Safe (liboqs)** for secure key exchange.
- Implement **quantum-resistant encryption schemes**.

---

## **Encryption Layers in Darkelf Browser (Step-by-Step Flow)**  

### **1. Secure Key Exchange (ECDH)**
✅ **Layer 1:** Generate an **ECDH key pair**.  
✅ **Layer 2:** Exchange **public keys** and derive a **shared secret** securely.  

### **2. Secure Data Encryption (AES-GCM & AES-CBC)**
✅ **Layer 3:** Use the **shared secret** as the **AES-GCM encryption key** for securing data.  
✅ **Layer 4:** AES-CBC is used for **local file encryption** to protect stored data.  

### **3. Public Key Encryption (RSA-OAEP)**
✅ **Layer 5:** Encrypt **sensitive data** (e.g., user credentials) using **RSA public key**.  
✅ **Layer 6:** Decrypt data securely with the **RSA private key**.  

### **4. Secure Randomness (WebCrypto PRNG)**
✅ **Layer 7:** Use **WebCrypto's secure PRNG** for cryptographic operations.  

---

## **Final Thoughts**
Darkelf Browser implements a **multi-layered encryption model** to ensure **data confidentiality, integrity, and secure communications**. With **future post-quantum enhancements**, it aims to remain secure against evolving cryptographic threats.

---

## **Key Notes**
1. **Post-Quantum Placeholder:** Post-quantum encryption is not currently implemented but is planned for future versions. Libraries such as liboqs provide a foundation for integrating post-quantum algorithms.  
2. **Standards Compliance:** Encryption methods used align with industry best practices, including AES-GCM for authenticated encryption and RSA-OAEP for asymmetric encryption. Future updates aim to adopt NIST-recommended post-quantum cryptography standards.  
3. **Layer Dependencies:** Layers build on each other logically:
   - Layers 1–2 establish the shared secret (ECDH).
   - Layer 3 uses the shared secret for symmetric encryption (AES-GCM).
   - Layers 4–6 introduce an optional additional layer of security using RSA for asymmetric encryption.
   - Layer 7 supports all layers by ensuring secure random number generation.

This approach provides robust protection for sensitive data and secure communication within the Darkelf browser.

## AES Encryption
Functionality: AES (Advanced Encryption Standard) is used for encrypting and decrypting data.
Key Management: A 256-bit AES key is securely generated and managed. If the key isn't already available in the environment, a new key is generated, encoded in Base64, and stored in an environment variable.

Methods:
encrypt_aes(plaintext): Encrypts the provided plaintext using AES encryption.
decrypt_aes(ciphertext): Decrypts the provided ciphertext using AES decryption.
Use Case: This encryption is typically used for securing data at rest or in transit within the application.

## RSA Encryption
Functionality: RSA (Rivest-Shamir-Adleman) is used for public-key encryption.
Key Management: RSA key pair (2048-bit) is generated and managed. If the keys aren't already available in the environment, new keys are generated, encoded in Base64, and stored in environment variables.
        
Methods:
encrypt_rsa(plaintext): Encrypts the provided plaintext using the RSA public key.
decrypt_rsa(ciphertext): Decrypts the provided ciphertext using the RSA private key.
Use Case: This encryption is typically used for securing data during transmission, such as encrypting search queries or communication data.

## ECDH Encryption
Functionality: ECDH (Elliptic Curve Diffie-Hellman) key exchange, the "bit encryption" typically refers to the length of the cryptographic keys used. In ECDH, the key length is determined by the elliptic curve parameters and is usually measured in bits. 

## Quantum Threats:

- Grover's Algorithm: Can theoretically reduce the security of symmetric encryption by half. For example, a 256-bit key would have the equivalent security of a 128-bit key against quantum attacks.
- Shor's Algorithm: Specifically affects asymmetric encryption, breaking widely used algorithms like RSA and ECC.

## ChaCha20 and Quantum Resistance:

ChaCha20, with a 256-bit key, would effectively offer 128-bit security against quantum attacks due to Grover's algorithm.
This level of security (128-bit) is generally considered sufficient for many applications even in the face of quantum computing.

## RSA and X25519: 
Asymmetric encryption algorithms used for key exchange and digital signatures, providing an additional layer of security.

Methods: Common key lengths for ECDH may include 256 bits, 384 bits, or 521 bits, depending on the specific elliptic curve parameters chosen for the key exchange. The longer the key length, the higher the level of security provided, as longer keys are generally more resistant to cryptographic attacks.

## Anti-Fingerprinting Features

1. Canvas Fingerprinting Blocking
- Functionality: Blocks attempts to use the canvas element for fingerprinting by enabling screen capture protection.
- Configuration: Set through QWebEngineSettings.ScreenCaptureEnabled.

2. WebRTC IP Leak Protection
- Functionality: Prevents IP leaks via WebRTC by modifying the HTTP User Agent.
- Configuration: Set through QWebEngineProfile.setHttpUserAgent.

3. Font Fingerprinting Protection
- Functionality: Protects against fingerprinting by restricting access to installed fonts and disallowing insecure content.
- Configuration: Set through QWebEngineSettings.AllowRunningInsecureContent.

4. Blocking Device Sensors
- Functionality: Limits access to device sensors that could be exploited for fingerprinting.
- Configuration: Set through QWebEngineSettings.Accelerated2dCanvasEnabled.

5. Limiting Browser Features
- Functionality: Restricts various browser features that could facilitate fingerprinting.
- Configuration: Set through QWebEngineSettings.FullScreenSupportEnabled.

## Other Privacy Features

HTTPS Enforcement
Functionality: Forces all HTTP requests to be upgraded to HTTPS, ensuring secure communication.
Implementation: Modifies the URL scheme of navigation requests to HTTPS in the acceptNavigationRequest method of WebEnginePage.

Tor Network Configuration
Functionality: Routes traffic through the Tor network for anonymous browsing.
Implementation: Sets up a SOCKS5 proxy to connect to the local Tor service (127.0.0.1:9050).

Cookie Management
Clear Cookies: Cookies, Cache and history clear after closing tabs.

Security Settings Management
Persistent Storage: Uses QSettings to store and retrieve security settings persistently.
Security Settings Dialog: Provides a user interface to enable or disable various security settings, such as JavaScript, anti-fingerprinting, Tor network, Post-quantum encryption capabilities, and HTTPS enforcement.
Dynamic Application: Applies the changes made in the security settings dialog dynamically to the browser's configuration.

## Summary

These features collectively enhance the privacy and security of the browser by:
- Ensuring secure communication through HTTPS.
- Providing anonymous browsing via the Tor network.
- Managing cookies and cache to protect user privacy.
- Allowing users to enable or disable security settings through a persistent storage mechanism.
- Applying a dark theme for better visual comfort.

Each feature requires careful implementation and can be integrated into a web browser application using Qt.
