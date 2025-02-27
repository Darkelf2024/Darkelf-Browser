# Darkelf Post-Quantum Edition

Welcome to the Darkelf Post-Quantum Edition, a highly secure and privacy-focused web browser designed to protect your online activities using advanced encryption techniques, including post-quantum cryptography.

## Features

### Security Features

- **Anti-Fingerprinting Techniques:**
  - Canvas Fingerprinting Protection
  - User-Agent Spoofing
  - WebGL Fingerprinting Protection
  - Font Fingerprinting Protection
  - Media Device Enumeration Blocking
  - Timezone Spoofing
  - Language and Locale Spoofing
  - Screen Resolution and Color Depth Spoofing
  - Hardware Concurrency Spoofing
  - Audio Fingerprinting Protection
  - Battery Status API Blocking
  - Network Information API Blocking
  - ETag and Cache-Control Manipulation

- **HTTPS Enforcement:**
  - Forces all HTTP requests to be upgraded to HTTPS for secure communication.

- **Tor Network Integration:**
  - Routes traffic through the Tor network for anonymous browsing.
  - Configures Tor DNS and SOCKS proxy for enhanced privacy.

- **Cookie Management:**
  - Options to enable or disable cookies.
  - Automatically clears cookies and cache after closing tabs.

- **Security Settings Management:**
  - Persistent storage of security settings using `QSettings`.
  - User interface for enabling or disabling various security settings dynamically.

### Encryption Features

- **ChaCha20 Cipher:**
  - Symmetric encryption algorithm known for its speed and security.

- **RSA and X25519:**
  - Asymmetric encryption algorithms for key exchange and digital signatures.

- **Hybrid Quantum Encryption:**
  - Combines x25519 and Kyber512 for advanced security against quantum computing threats.

- **AES-GCM Implementation:**
  - Ensures data integrity and confidentiality with AES-GCM encryption.

- **ECDH Implementation:**
  - Derives shared secrets securely using ECDH, ensuring perfect forward secrecy.

### Privacy Features

- **JavaScript Control:**
  - Allows users to enable or disable JavaScript to reduce the risk of malicious scripts.

- **Geolocation Control:**
  - Option to enable or disable geolocation to prevent websites from accessing physical location data.

- **Device Orientation and Media Device Blocking:**
  - Blocks device orientation sensors and media devices (camera, microphone) to prevent unauthorized access.

- **Customizable Home Page with Integrated Search:**
  - Offers a customizable home page with DuckDuckGo search for privacy-focused search functionality.

- **Adblock Features:**
  - **Domain Blocking:** Blocks requests to specific domains.
  - **Rule-Based Filtering:** Custom rules to filter content based on type.
  - **Adblock Pattern Management:** Aggregates adblock patterns from multiple sources.
  - **Tracking Protection:** Prevents requests to known tracking domains.

- **Session Management:**
  - Supports restoring previous sessions, including tabs and their state.
