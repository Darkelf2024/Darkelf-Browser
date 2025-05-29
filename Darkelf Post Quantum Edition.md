# Darkelf Browser Post Quantum Edition Hybrid ML-KEM-768/1024 Features

## Security Features
1. **Adblock and Tracker Blocking**
   - Uses Trie data structure to efficiently match and block URLs based on adblock rules.
   - Fetches adblock rules from popular sources such as EasyList.
   - Blocks tracking domains using lists from Disconnect.me.

2. **Script Blocking**
   - Uses a machine learning model (pre-trained) to classify and block potentially malicious JavaScript code.
   - Extracts specific features from JavaScript code to determine if it is malicious.
   - Machine learning model is self-hosted on client-side with the installation of certain packages and script.

3. **SSL/TLS Configuration**
   - Forces the use of the latest version of TLS (v1.3) for secure communication.
   - Configures SSL settings to ensure the highest level of security.

4. **Content Security Policy (CSP)**
   - Injects a strict CSP header to restrict the sources from which content can be loaded.
   - Blocks unsafe inline scripts and restricts script sources to self and HTTPS.

5. **Sandboxing**
   - Disables potentially risky features such as LocalStorage, JavaScript, WebGL, and WebRTC.
   - Enables XSS auditing and disables error pages to prevent information leakage.

6. **Tor Network Integration**
   - Supports browsing through the Tor network for enhanced anonymity.
   - Configures Tor proxy and DNS to route traffic through the Tor network.
   - Onion Routing Available

7. **JavaScript Blocking**
   - Disables JavaScript by default to prevent script-based attacks.
   - Allows users to enable or disable JavaScript through the settings menu.

8. **Anti-Fingerprinting**
   - Overrides the user agent string to prevent browser fingerprinting.
   - Disables geolocation access to avoid location-based tracking.
   - Uses a machine learning model (pre-trained) to block all fingerprinting techniques.

## 🔐 Encryption Features

**1. Hybrid Key Exchange (Rust-Powered)**
- Implements a **hybrid key exchange mechanism** using **X25519** (Elliptic Curve Diffie-Hellman) and **ML-KEM768/1024** (a post-quantum cryptographic algorithm).  
- Rust handles the key exchange efficiently, providing **high security and performance**.  
- The final **shared secret** is derived using **HKDF (HMAC-based Key Derivation Function) with SHA-256**, ensuring strong cryptographic security.  

**2. Rust-Powered Encryption for Secure Data Handling**
- Rust is integrated into Python via `crypto_rust`, ensuring **fast and memory-safe encryption**.  
- All sensitive data, including **HTTPS requests, stored session data, and cookies**, can be **encrypted/decrypted using Rust** inside the Python-based browser.  
- The Rust implementation provides **protection against memory leaks and side-channel attacks**.  

**3. Cryptographic PRNG (Pseudo-Random Number Generator)**
- Provides a function to generate **secure random bytes** using:  
  - The **browser’s crypto API** (for in-browser security).  
  - **Rust’s cryptographically secure random generator** for Python-based encryption.  
- Ensures strong entropy for cryptographic operations like key generation and nonce creation.  

## Privacy Features
1. **HTTPS Enforcement**
   - Redirects HTTP URLs to HTTPS to ensure secure communication.
   - Can be toggled on or off through the settings menu.

2. **Cookie Management**
   - Disables persistent cookies by default to prevent tracking.
   - Allows users to enable or disable cookies through the settings menu.

3. **Geolocation Blocking**
   - Overrides geolocation functions to deny access to location information.

4. **Device Orientation and Media Devices Blocking**
   - Blocks access to device orientation and media devices to prevent unauthorized access.

5. **History and Cache Management**
   - Provides options to clear browsing history and cache.
   - Clears cache and history on browser close to maintain privacy.

6. **SSL Configuration and Protection**
   - Ensures the use of the latest SSL/TLS protocols.
   - Configures SSL settings to protect against insecure connections.

## UI and Additional Features
1. **User Interface**
   - Provides a tabbed browsing interface with customizable tabs.
   - Includes a toolbar with navigation controls, search bar, and zoom buttons.
   - Customizable homepage with a search form for DuckDuckGo.

2. **Menu and Shortcuts**
   - Includes navigation, security, settings, history, and about menus.
   - Provides keyboard shortcuts for common actions like opening new tabs, closing tabs, and reloading pages.

3. **Download Manager**
   - Manages file downloads with a progress dialog and save file dialog.
   - Allows users to cancel downloads and provides notifications upon completion.

4. **Custom Web Engine Page**
   - Extends QWebEnginePage to add custom security and privacy behaviors.
   - Intercepts JavaScript console messages to block malicious scripts.

### Summary
The Darkelf Browser is designed with a strong emphasis on security, privacy, and anonymity. It leverages advanced cryptographic techniques, strict content security policies, and various anti-tracking mechanisms to protect users from online threats. The integration of the Tor network further enhances anonymity, while the user-friendly interface and customizable settings provide a seamless browsing experience.

### Note on Key Storage
- The hybrid encryption keys are temporarily stored in RAM for the duration of the browser session. They are not written to disk to ensure maximum security and privacy.
