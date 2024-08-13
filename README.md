## Darkelf Browser
- Release Soon (Waiting for ECCN #)


## Web Tech
<div style="display: flex;">

<div style="display:flex; align-items:center;">
    <img src="https://www.freepnglogos.com/uploads/html5-logo-png/html5-logo-devextreme-multi-purpose-controls-html-javascript-3.png" width="120" height="60" alt="HTML5 Logo">
    <img src="https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/community/logos/python-logo-only.png" alt="Python Logo" style="width:67px; height:48px; margin-right:10px;">
    <img src="https://pypi.org/static/images/white-cube.2351a86c.svg" width="67" height="48" alt="Cube Logo">
</div>

## Intro

Darkelf, a custom PyQt5-based browser, is equipped with a range of advanced security features aimed at safeguarding user privacy and fortifying defenses against online threats. The upcoming release of the Darkelf Browser promises an enriching browsing experience, with a strong emphasis on security and privacy.

Key Highlights and Security Features:

1. **Content Security Policy (CSP) Enhancements:** Darkelf Browser emphasizes the importance of Content Security Policy (CSP) to mitigate various forms of attacks such as cross-site scripting (XSS) and data injection. We are committed to working closely with the community to fine-tune and adapt the CSP policies for optimal protection.

2. **Sandboxing for Enhanced Security:** Darkelf Browser leverages sandboxing techniques to isolate potential security vulnerabilities and prevent unauthorized access to critical system resources. By containing processes within secure boundaries, sandboxing enhances the overall security posture of the browser.

3. **CHACHA20 Encryption with x25519 Key Exchange:** Darkelf Browser employs the robust CHACHA20 encryption algorithm in conjunction with the x25519 key exchange protocol to ensure secure communication and data integrity. This cutting-edge encryption scheme offers a high level of confidentiality and protection against eavesdropping and tampering.

4. **Community Collaboration:** We value community feedback and contributions in shaping the security features and policies of Darkelf Browser. Your active participation will be instrumental in refining our security strategies and addressing emerging threats effectively.

As we prepare for the imminent release of Darkelf Browser, our team is dedicated to delivering a secure and privacy-focused browsing environment that empowers users to explore the web with confidence. Stay tuned for updates and join us in our mission to create a safer online ecosystem for all users.

## Table of Contents
- [Attribution](Attribution.md)
- [Encryption](Encryption.md)
- [Overview](Overview.md)
- [QSettings](QSettings.md)
- [LICENSE](LICENSE)
- [Copyright](Copyright.md)
- [Darkelf vs Tor](DarkelfvTor.md)
- [OSINT Resources](https://github.com/Darkelf2024/Darkelf-Browser/blob/main/OSINT%20Resources.md)

## Systems
- MAC OS - Ready
- Linux - Ready
- Windows - Ready

## Variations/Types
- Darkelf OSINT - Browser for OSINT 
- Darkelf Private - Extreme Privacy
- Darkelf Public - Balanced/Mixed
- Each Browser/Type - Can be modified
- Pick a style

## Security Features

- Sandboxing:
Darkelf Browser implements sandboxing technology to provide an additional layer of security:
- Isolated Environment: Each browsing session is isolated from the system, preventing malicious code from affecting other parts of the browser or the device.
- Enhanced Security: Sandboxing helps mitigate the impact of potential security vulnerabilities by containing threats within the browser's sandboxed
environment. 
- Protection Against Exploits: By confining processes to a sandbox, Darkelf Browser reduces the risk of
exploits and unauthorized access to sensitive system resources.

- Custom Ad Blocker - Enabled by default 
- Content Security Policy (CSP):
Sets strict content security policies to prevent cross-site scripting (XSS), clickjacking, and other code injection attacks.

- HTTPS Enforcement:
Automatically upgrades HTTP requests to HTTPS to ensure encrypted communication whenever possible.

- Anti-Fingerprinting:
Reduces the amount of information available for browser fingerprinting, making it harder to track users across the web.

- Tor Network Integration:
Optional integration with the Tor network for anonymous browsing by routing traffic through multiple nodes to conceal users' IP addresses.

- Clear Cookies and Cache on Exit:
Clears HTTP cache and cookies when the browser or a tab is closed to prevent tracking and maintain privacy.

## Encryption Features

- ChaCha20 Cipher: 
A robust symmetric encryption algorithm that ensures data integrity and confidentiality.

- RSA and X25519: 
Asymmetric encryption algorithms used for key exchange and digital signatures, providing an additional layer of security.

- Quantum Encryption:
Option to enable quantum encryption for advanced security against future quantum computing threats.

## Privacy Features

- JavaScript Control:
Allows users to enable or disable JavaScript, reducing the risk of malicious scripts.

- Cookie Management:
Provides the option to enable or disable cookies, offering control over data stored by websites.

- Geolocation Control:
Option to enable or disable geolocation, preventing websites from accessing the user's physical location.

- Device Orientation and Media Device Blocking:
Options to block device orientation sensors and media devices (camera, microphone), preventing websites from accessing this data.

- Theme:
A visually unobtrusive theme to reduce eye strain and potentially avoid drawing attention in low-light environments.

- Home Page with Integrated Search:
A customizable home page with integrated DuckDuckGo search, offering a privacy-focused search engine.

## Additional Features

- Debounce Resize Function:
Efficiently handles resize events to optimize performance.

- Download Manager:
Manages and tracks downloads, providing a secure way to handle file downloads.

- Security Settings Dialog:
A user interface to configure various security settings, such as enabling/disabling JavaScript, Tor network, and encryption options.

- Toolbar and Menu Bar:
Provides quick access to navigation controls, search bar, and security settings.

- Session Management:
Supports restoring the previous session, including tabs and their state, enhancing usability without compromising security.

## Adblock Features 

Darkelf Browser incorporates robust adblocking functionality to enhance privacy and browsing experience:

1. **Domain Blocking**: The `AdblockUrlRequestInterceptor` class blocks requests to specific domains listed in the `blocked_domains` parameter, preventing unwanted content from loading.

2. **Rule-Based Filtering**: Custom rules in the `AdblockUrlRequestInterceptor` class enable filtering based on content type. This includes blocking CSP reports, large media files, and other specified types of requests.

3. **Adblock Pattern Management**: The `load_adblock_list` function aggregates adblock patterns from multiple sources, including popular ad-blocking lists and custom rules for sites like YouTube. Patterns are processed using the `BeautifulSoup` library to handle HTML content effectively.

4. **Tracking Protection**: The `TrackerInterceptor` class prevents requests to known tracking domains. Tracking domains are sourced from JSON files and processed with the `json` module, ensuring comprehensive tracking protection.

## Anti-Fingerprinting Techniques

- Canvas Fingerprinting Protection:
Modifies or blocks the ability of websites to read canvas data. This prevents websites from creating a unique fingerprint based on the rendering of graphics on the user's device.

- User-Agent Spoofing:
Randomizes or standardizes the user-agent string sent to websites, making it difficult to identify the browser and operating system version.

- WebGL Fingerprinting Protection:
Alters or blocks WebGL information to prevent fingerprinting based on the graphics hardware and driver details.

- Font Fingerprinting Protection:
Limits the list of available system fonts exposed to websites, preventing fingerprinting based on the unique set of installed fonts.

- Media Device Enumeration Blocking:
Prevents websites from accessing detailed information about the user's media devices (e.g., cameras, microphones), which can be used for fingerprinting.

- Timezone Spoofing:
Changes or hides the timezone information to prevent websites from determining the user's geographical location based on their timezone.

- Language and Locale Spoofing:
Randomizes or standardizes language and locale settings to prevent fingerprinting based on these attributes.

- Screen Resolution and Color Depth Spoofing:
Modifies or hides screen resolution and color depth information to prevent websites from creating a unique fingerprint based on the display properties of the device.

- Hardware Concurrency Spoofing:
Changes the reported number of logical processors (CPU cores) to prevent fingerprinting based on the hardware concurrency.

- Audio Fingerprinting Protection:
Alters or blocks audio context information to prevent fingerprinting based on the audio hardware and capabilities.

- Battery Status API Blocking:
Blocks access to the Battery Status API, preventing websites from tracking battery levels and charging status, which can be used for fingerprinting.

- Network Information API Blocking:
Blocks access to the Network Information API, preventing websites from accessing network type and speed information, which can be used for fingerprinting.

- ETag and Cache-Control Manipulation:
Modifies or disables ETag headers and cache-control mechanisms to prevent tracking via caching techniques.

- TLS Fingerprinting Protection:
Alters or hides TLS fingerprinting information (such as supported cipher suites and TLS extensions) to prevent fingerprinting based on SSL/TLS handshakes. - Not Enabled: Needs Configuration on Serverside.

## Implementation Details

- JavaScript Hooks:
The browser employs JavaScript hooks to intercept and modify calls to functions and APIs that can be used for fingerprinting, such as navigator, screen, document, and window properties.

- Built-In:
Built-in features to spoof or block fingerprintable attributes dynamically, providing an extra layer of protection.

- Configuration Options:
Provides user-configurable options to enable or disable specific anti-fingerprinting techniques, allowing users to balance privacy and functionality according to their needs.

These techniques collectively reduce the uniqueness of the user's browser environment, making it harder for websites to track users based on their browser and device characteristics.

## Themes
- Dark Theme
- White Theme

Themes are based on your personal system preferences.

## Not Working(Currently)

Tuta/Proton - Can't access login due to CSP issue.
Everything else is working though.


## Contributors

Dr. Kevin Moore [Darkelf2024](https://github.com/Darkelf2024) ([Kjm489](https://github.com/Kjm489)) Initial work, design, and implementation, additional contributions. 
Heapy for memory leak testing.
ChatGPT by OpenAI for code optimization, and error analysis.


## Feedback and Contributions

Your feedback is valuable for the improvement of Darkelf Browser. If you have any suggestions, ideas, bug reports, or feature requests, please don't hesitate to open an issue or reach out to me.

I welcome constructive criticism and diverse perspectives as they can help make Darkelf Browser better for everyone. Let's work together to create a vibrant and supportive community around this project.

Thank you for your support and for helping make Darkelf Browser the best it can be!
