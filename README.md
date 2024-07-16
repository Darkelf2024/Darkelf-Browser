# Darkelf Browser - Release Soon


## Web Tech
<div style="display: flex;">

<div style="display:flex; align-items:center;">
    <img src="https://www.freepnglogos.com/uploads/html5-logo-png/html5-logo-devextreme-multi-purpose-controls-html-javascript-3.png" width="120" height="60" alt="HTML5 Logo">
    <img src="https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/community/logos/python-logo-only.png" alt="Python Logo" style="width:67px; height:48px; margin-right:10px;">
    <img src="https://pypi.org/static/images/white-cube.2351a86c.svg" width="67" height="48" alt="Cube Logo">
</div>

## Intro

Darkelf, as a custom PyQt5-based browser, incorporates several security features designed to enhance user privacy and protect against various online threats. Here are some of its notable security features and Highlights. I made some improvements. Thank you for following me! The Darkelf Browser will release soon, Hope everyone enjoys it! I will need the communities help to address the CSP Policy for modifications as needed.

## Table of Contents
- [Attribution](Attribution.md)
- [Encryption](Encryption.md)
- [Overview](Overview.md)
- [QSettings](QSettings.md)
- [LICENSE](LICENSE)
- [Copyright](Copyright.md)
- [Darkelf vs Tor](DarkelfvTor.md)

## Systems
- MAC OS - Ready
- Linux - Ready
- Windows - Ready

## Security Features

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

- Black Theme:
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
Alters or hides TLS fingerprinting information (such as supported cipher suites and TLS extensions) to prevent fingerprinting based on SSL/TLS handshakes.

## Implementation Details

- JavaScript Hooks:
The browser employs JavaScript hooks to intercept and modify calls to functions and APIs that can be used for fingerprinting, such as navigator, screen, document, and window properties.

- Built-In:
Built-in features to spoof or block fingerprintable attributes dynamically, providing an extra layer of protection.

- Configuration Options:
Provides user-configurable options to enable or disable specific anti-fingerprinting techniques, allowing users to balance privacy and functionality according to their needs.

These techniques collectively reduce the uniqueness of the user's browser environment, making it harder for websites to track users based on their browser and device characteristics.

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
