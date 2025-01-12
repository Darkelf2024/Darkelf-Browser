# Encryption Features

The current implementation of Darkelf includes several layers of encryption and security features. Here's a detailed breakdown.

## ECDH (Elliptic Curve Diffie-Hellman) Key Exchange
- Purpose: Used for secure key exchange.
- Details: An ECDH key pair is generated for secure key exchange, which ensures that a shared secret can be established securely over an untrusted channel.

## AES-GCM (Advanced Encryption Standard in Galois/Counter Mode)
- Purpose: Used for encrypting data.
- Details: After deriving a shared secret using ECDH, AES-GCM is used for encrypting and decrypting data. This provides both confidentiality and integrity of the data.

## RSA-OAEP (Rivest-Shamir-Adleman with Optimal Asymmetric Encryption Padding)
- Purpose: Used for encrypting data.
- Details: RSA-OAEP is used for public-key encryption and decryption, offering secure encryption of data with added padding for enhanced security.

## Encryption Layers in Darkelf

ECDH Key Exchange
- Layer 1: ECDH key pair generation and public key exchange.
- Layer 2: Derivation of a shared secret using the exchanged public keys.

AES-GCM Encryption
- Layer 3: Using the derived shared secret for symmetric encryption and decryption with AES-GCM.

RSA-OAEP Encryption
- Layer 4: Generation of an RSA key pair for asymmetric encryption.
- Layer 5: Encrypting data using the RSA public key.
- Layer 6: Decrypting data using the RSA private key.

Post Quantum Encryption (Placeholder):
- Key Generation: Generates key pairs for ECDH and RSA within the browser using the Web Cryptography API.
- Encryption and Decryption: Placeholder functions for encrypting and decrypting messages using post-quantum keys.
- Need to install - If you need to implement post-quantum cryptographic algorithms, you should look into libraries and standards that specifically address post-quantum security, such as those provided by the Open Quantum Safe project (liboqs).

WebCrypto API for Random Number Generation
- Layer 7: Utilizing WebCrypto PRNG for generating secure random bytes.

## Summary of Encryption Layers

Darkelf effectively uses up to seven layers of encryption and security mechanisms to ensure data confidentiality and integrity.

- ECDH Key Exchange (2 layers)
- AES-GCM Encryption (1 layer)
- RSA-OAEP Encryption (3 layers)
- WebCrypto PRNG (1 layer)
- Post Quantum Encryption Currently (Optional - Implementation of Liboqs and Generate Keys/Pairs)

This layered approach provides robust security for sensitive data and communication within the Darkelf browser.

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

## ChaCha20 Cipher: 
A robust symmetric encryption algorithm that ensures data integrity and confidentiality.

## RSA and X25519: 
Asymmetric encryption algorithms used for key exchange and digital signatures, providing an additional layer of security.

Methods: Common key lengths for ECDH may include 256 bits, 384 bits, or 521 bits, depending on the specific elliptic curve parameters chosen for the key exchange. The longer the key length, the higher the level of security provided, as longer keys are generally more resistant to cryptographic attacks.

## Anti-Fingerprinting Features

Canvas Fingerprinting Blocking
Functionality: Blocks attempts to use the canvas element for fingerprinting by enabling screen capture protection.
Configuration: Set through QWebEngineSettings.ScreenCaptureEnabled.

WebRTC IP Leaks Protection
Functionality: Protects against IP leaks through WebRTC by modifying the HTTP User Agent.
Configuration: Set through QWebEngineProfile.setHttpUserAgent.

Font Fingerprinting Protection
Functionality: Protects against fingerprinting through installed fonts by not allowing insecure content.
Configuration: Set through QWebEngineSettings.AllowRunningInsecureContent.

Blocking Device Sensors
Functionality: Limits access to device sensors that could be used for fingerprinting.
Configuration: Set through QWebEngineSettings.Accelerated2dCanvasEnabled.

Limiting Browser Features
Functionality: Limits various browser features that can be used for fingerprinting.
Configuration: Set through QWebEngineSettings.FullScreenSupportEnabled.

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
Security Settings Dialog: Provides a user interface to enable or disable various security settings, such as JavaScript, anti-fingerprinting, Tor network, quantum encryption, and HTTPS enforcement.
Dynamic Application: Applies the changes made in the security settings dialog dynamically to the browser's configuration.

Default Dark Theme

CSS Injection: Applies a dark theme by injecting CSS into the web pages.

These features collectively enhance the privacy and security of the browser, providing protections against common tracking techniques and ensuring secure data transmission and storage.
