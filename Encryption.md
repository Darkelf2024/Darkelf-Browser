# Encryption Features

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
Functionality: Protects against fingerprinting through installed fonts by allowing insecure content.
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
Clear Cookies: Provides a function to clear all cookies.

Security Settings Management
Persistent Storage: Uses QSettings to store and retrieve security settings persistently.
Security Settings Dialog: Provides a user interface to enable or disable various security settings, such as JavaScript, anti-fingerprinting, Tor network, quantum encryption, and HTTPS enforcement.
Dynamic Application: Applies the changes made in the security settings dialog dynamically to the browser's configuration.

Default Dark Theme

CSS Injection: Applies a dark theme by injecting CSS into the web pages.

These features collectively enhance the privacy and security of the browser, providing protections against common tracking techniques and ensuring secure data transmission and storage.
