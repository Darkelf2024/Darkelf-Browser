## Darkelf Browser - Extreme Edition 
- Release of Darkelf Browser Extreme Edition v3.0 [DE Release](https://github.com/Darkelf2024/Darkelf-Browser/blob/main/Darkelf%20Extreme.py) This is the Extreme/Private Version  with Tor DNS - It is released in a Monolithic Style.
- Release of Darkelf OSINT Edition v3.0 [DE OSINT](https://github.com/Darkelf2024/Darkelf-Browser/blob/main/Darkelf%20OSINT.py)
- Relase of Darkelf Browser Privacy Edition v3.0 [DE Privacy Release](https://github.com/Darkelf2024/Darkelf-Browser/blob/main/Darkelf%20Privacy.py)
- Please Read - Updated 1/31/25: [Export Compliance Notice](ExportComplianceNotice.md)
- Reviewing Office: Office of National Security Agency on 11/27/2024 - Closed on 12/17/2024
- [Open an issue](https://github.com/Darkelf2024/Darkelf-Browser/issues)

## Tech Stack

![HTML5](https://img.shields.io/badge/HTML5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)  
![CSS3](https://img.shields.io/badge/CSS3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)  
![Python](https://img.shields.io/badge/Python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white)  
![Encryption](https://img.shields.io/badge/Encryption-%23008C45.svg?style=for-the-badge&logo=lock&logoColor=white)  
![PyCryptodome](https://img.shields.io/badge/PyCryptodome-%23007ACC.svg?style=for-the-badge&logo=python&logoColor=white)  
![Cryptography](https://img.shields.io/badge/Cryptography-%234B8BBE.svg?style=for-the-badge&logo=lock&logoColor=white)  


## Originality Statement
This project consists of over 1,300 lines of original code. A CopyLeaks report has been generated to verify its uniqueness, indicating a 1.5-6% similarity based on type of DE Browser: OSINT, Extreme/Private, or Public Version. The flagged similarity is attributed to standard coding patterns and false positives. Upon review, the content is verified as 0% plagiarized and fully original.
If you would like to review the CopyLeaks report, please feel free to reach out.

## Intro

# Darkelf Browser: Enhanced Security and Privacy with Tor Integration

Darkelf, a custom PyQt5-based browser, is equipped with a range of advanced security features aimed at safeguarding user privacy and fortifying defenses against online threats. The upcoming release of Darkelf Browser promises an enriching browsing experience, with a strong emphasis on security and privacy.

## Key Highlights and Security Features

### **AdGuard DNS Integration**  
Darkelf Browser incorporates AdGuard DNS, a powerful DNS resolution service designed to block trackers, ads, and phishing domains at the network level. By intercepting DNS requests, AdGuard DNS strengthens your browsing privacy while providing a smoother and clutter-free experience. *(This is in the codebase)*

### **Content Security Policy (CSP) Enhancements**  
Darkelf Browser emphasizes the importance of Content Security Policy (CSP) to mitigate various forms of attacks such as cross-site scripting (XSS) and data injection. We are committed to working closely with the community to fine-tune and adapt the CSP policies for optimal protection.

### **Sandboxing for Enhanced Security**  
Darkelf Browser leverages sandboxing techniques to isolate potential security vulnerabilities and prevent unauthorized access to critical system resources. By containing processes within secure boundaries, sandboxing enhances the overall security posture of the browser.

### **CHACHA20 Encryption with x25519 Key Exchange**  
Darkelf Browser employs the robust CHACHA20 encryption algorithm in conjunction with the x25519 key exchange protocol to ensure secure communication and data integrity. This cutting-edge encryption scheme offers a high level of confidentiality and protection against eavesdropping and tampering.

### **Tor Integration for Anonymity**  
Darkelf Browser integrates seamlessly with the Tor network, allowing users to anonymize their browsing activity and further safeguard their privacy. By routing internet traffic through the Tor network, Darkelf users are able to hide their IP addresses and obscure their browsing behavior from prying eyes, including websites and ISPs. This integration enables access to .onion websites, offering a truly anonymous browsing experience. Whether you're accessing standard web pages or specialized Tor sites, Darkelf ensures that your identity remains concealed, mitigating tracking risks and enhancing overall security. The Tor protocol also prevents traffic analysis, providing an additional layer of protection against potential adversaries who attempt to monitor or intercept your online activity.

### **Community Collaboration**  
We welcome community feedback and contributions to enhance the security of Darkelf Browser. Your input helps us refine our strategies and tackle emerging threats effectively. Our team is committed to providing a secure, privacy-focused browsing experience, empowering users to explore the web with confidence. Stay tuned for updates and join us in building a safer online ecosystem.

## Table of Contents
- [Attribution](Attribution.md)
- [BrowserAudit](BrowserAudit.md)
- [Encryption](Encryption.md)
- [Overview](Overview.md)
- [QSettings](QSettings.md)
- [LICENSE](LICENSE)
- [Copyright](Copyright.md)
- [Darkelf vs Tor](DarkelfvTor.md)
- [Darkelf Installation Guide](DarkelfInstallationGuide.md)
- [Tor Installation Guide](https://github.com/Darkelf2024/Darkelf-Browser/blob/main/Tor%20Installation%20Guide.md)
- [OSINT Attribution](https://github.com/Darkelf2024/Darkelf-Browser/blob/main/OSINT%20Attribution.md)
- [OSINT Resources](https://github.com/Darkelf2024/Darkelf-Browser/blob/main/OSINT%20Resources.md)
- [No JavaScript Websites](NoJavaScriptWebsites.md)
- [FAQ](FAQ.md)

## Systems
- MAC OS - Ready
- Linux - Ready
- Windows - Ready

## Variations/Types
- Darkelf Private - Extreme Privacy - Released
- Darkelf OSINT Version - Released 
- Darkelf Public Version - Released
- Each Browser/Type - Can be modified within the python code
- Pick a style

## Modify Settings 
Users can modify and tweak these settings in the codebase 

- True = Enabled 
- False = Disabled 

1. [Sandbox Settings](https://github.com/Darkelf2024/Darkelf-Browser/blob/main/Sandbox%20Settings.py)
2. [Initialize Settings](https://github.com/Darkelf2024/Darkelf-Browser/blob/main/Initialize%20Settings.py)
3. [QWebEngine Profile Settings](https://github.com/Darkelf2024/Darkelf-Browser/blob/main/QWebEngine%20Profile%20Settings.py)

## ⚠️ Important Note  

JavaScript behavior can be manipulated in the browser by enabling or disabling it in settings.  
To test this:  

1. Go to **Browser Settings** and navigate to **JavaScript** options.  
2. Enable or disable JavaScript as needed.  
3. Refresh the page by clicking the **Reload** button in your browser.  

This can affect how scripts run on the page, so keep this in mind while testing or debugging JavaScript-based features.  

## Security Features

### Sandboxing
Darkelf Browser implements sandboxing technology to provide an additional layer of security:

- **Isolated Environment**: Each browsing session is isolated from the system, preventing malicious code from affecting other parts of the browser or the device.
- **Enhanced Security**: Sandboxing helps mitigate the impact of potential security vulnerabilities by containing threats within the browser's sandboxed environment.
- **Protection Against Exploits**: By confining processes to a sandbox, Darkelf Browser reduces the risk of exploits and unauthorized access to sensitive system resources.

### Custom Ad Blocker
- **Enabled by Default**: Darkelf Browser comes with a custom ad blocker enabled by default, ensuring an ad-free browsing experience.
- **Updated Adblock Rules**: Regularly fetches and updates adblock rules from multiple trusted sources to effectively block ads and trackers.

### Content Security Policy (CSP)
- **Strict Security Policies**: Sets strict content security policies to prevent cross-site scripting (XSS), clickjacking, and other code injection attacks.

### HTTPS Enforcement
- **Automatic Upgrades**: Automatically upgrades HTTP requests to HTTPS to ensure encrypted communication whenever possible.
- **Secure Browsing**: Ensures that your data is encrypted and protected from eavesdropping.

### Anti-Fingerprinting
- **Reduced Tracking**: Reduces the amount of information available for browser fingerprinting, making it harder to track users across the web.
- **Spoofing Techniques**: Implements various techniques to spoof browser characteristics and protect against fingerprinting.

### Tor Network Integration
- **Anonymous Browsing**: Optional integration with the Tor network for anonymous browsing by routing traffic through multiple nodes to conceal users' IP addresses.
- **Privacy Protection**: Enhances privacy by preventing websites from tracking your real IP address.

### Clear Cookies and Cache on Exit
- **Automatic Clearing**: Clears HTTP cache and cookies when the browser or a tab is closed to prevent tracking and maintain privacy.
- **Enhanced Privacy**: Ensures that no browsing data is left behind after your session ends.

### Additional Features
- **AdGuard DNS Resolver**: Uses AdGuard DNS servers to enhance security and block ads and trackers at the DNS level.
- **Quantum Encryption**: Optional quantum encryption for enhanced security.
- **Custom Web Engine Page**: Implements various security measures such as disabling local storage, blocking JavaScript, and enforcing CSP.
- **Download Manager**: Secure download manager that provides progress updates and ensures safe file downloads.

Darkelf Browser is designed with privacy and security at its core, ensuring a safer and more private browsing experience for all users.

## Encryption Features

- **ChaCha20 Cipher**: 
  A robust symmetric encryption algorithm that ensures data integrity and confidentiality.

- **RSA and X25519**: 
  Asymmetric encryption algorithms used for key exchange and digital signatures, providing an additional layer of security.

- **Quantum Encryption**:
  Option to enable quantum encryption for advanced security against future quantum computing threats. (Research/Testing Phase - Kyber1024/XMSS) - Currently, there is an error with Python 3.12 where key pairs cannot be found. The module is hidden and work is ongoing to resolve this issue.

## Privacy Features

- **JavaScript Control**:
  Allows users to enable or disable JavaScript, reducing the risk of malicious scripts.

- **Cookie Management**:
  Provides the option to enable or disable cookies, offering control over data stored by websites.

- **Geolocation Control**:
  Option to enable or disable geolocation, preventing websites from accessing the user's physical location.

- **Device Orientation and Media Device Blocking**:
  Options to block device orientation sensors and media devices (camera, microphone), preventing websites from accessing this data.

- **Theme**:
  A visually unobtrusive theme to reduce eye strain and potentially avoid drawing attention in low-light environments.

- **Home Page with Integrated Search**:
  A customizable home page with integrated DuckDuckGo search, offering a privacy-focused search engine.

## Additional Features

- **Debounce Resize Function**:
  Efficiently handles resize events to optimize performance.

- **Download Manager**:
  Manages and tracks downloads, providing a secure way to handle file downloads.

- **Security Settings Dialog**:
  A user interface to configure various security settings, such as enabling/disabling JavaScript, Tor network, and encryption options.

- **Toolbar and Menu Bar**:
  Provides quick access to navigation controls, search bar, and security settings.

- **Session Management**:
  Supports restoring the previous session, including tabs and their state, enhancing usability without compromising security.

## Adblock Features 

Darkelf Browser incorporates robust adblocking functionality to enhance privacy and browsing experience:

1. **Domain Blocking**: The `AdblockUrlRequestInterceptor` class blocks requests to specific domains listed in the `blocked_domains` parameter, preventing unwanted content from loading.

2. **Rule-Based Filtering**: Custom rules in the `AdblockUrlRequestInterceptor` class enable filtering based on content type. This includes blocking CSP reports, large media files, and other specified types of requests.

3. **Adblock Pattern Management**: The `load_adblock_list` function aggregates adblock patterns from multiple sources, including popular ad-blocking lists and custom rules for sites like YouTube. Patterns are processed using the `BeautifulSoup` library to handle HTML content effectively.

4. **Tracking Protection**: The `TrackerInterceptor` class prevents requests to known tracking domains. Tracking domains are sourced from JSON files and processed with the `json` module, ensuring comprehensive tracking protection.

## Anti-Fingerprinting Techniques

- **Canvas Fingerprinting Protection**:
  Modifies or blocks the ability of websites to read canvas data. This prevents websites from creating a unique fingerprint based on the rendering of graphics on the user's device.

- **User-Agent Spoofing**:
  Randomizes or standardizes the user-agent string sent to websites, making it difficult to identify the browser and operating system version.

- **WebGL Fingerprinting Protection**:
  Alters or blocks WebGL information to prevent fingerprinting based on the graphics hardware and driver details.

- **Font Fingerprinting Protection**:
  Limits the list of available system fonts exposed to websites, preventing fingerprinting based on the unique set of installed fonts.

- **Media Device Enumeration Blocking**:
  Prevents websites from accessing detailed information about the user's media devices (e.g., cameras, microphones), which can be used for fingerprinting.

- **Timezone Spoofing**:
  Changes or hides the timezone information to prevent websites from determining the user's geographical location based on their timezone.

- **Language and Locale Spoofing**:
  Randomizes or standardizes language and locale settings to prevent fingerprinting based on these attributes.

- **Screen Resolution and Color Depth Spoofing**:
  Modifies or hides screen resolution and color depth information to prevent websites from creating a unique fingerprint based on the display properties of the device.

- **Hardware Concurrency Spoofing**:
  Changes the reported number of logical processors (CPU cores) to prevent fingerprinting based on the hardware concurrency.

- **Audio Fingerprinting Protection**:
  Alters or blocks audio context information to prevent fingerprinting based on the audio hardware and capabilities.

- **Battery Status API Blocking**:
  Blocks access to the Battery Status API, preventing websites from tracking battery levels and charging status, which can be used for fingerprinting.

- **Network Information API Blocking**:
  Blocks access to the Network Information API, preventing websites from accessing network type and speed information, which can be used for fingerprinting.

- **ETag and Cache-Control Manipulation**:
  Modifies or disables ETag headers and cache-control mechanisms to prevent tracking via caching techniques.

## Implementation Details

- **JavaScript Hooks**:
  The browser employs JavaScript hooks to intercept and modify calls to functions and APIs that can be used for fingerprinting, such as `navigator`, `screen`, `document`, and `window` properties.

- **Built-In Features**:
  Built-in features spoof or block fingerprintable attributes dynamically, providing an extra layer of protection.

- **Configuration Options**:
  Provides user-configurable options to enable or disable specific anti-fingerprinting techniques, allowing users to balance privacy and functionality according to their needs.

These techniques collectively reduce the uniqueness of the user's browser environment, making it harder for websites to track users based on their browser and device characteristics.

## Themes

- **Dark Theme**
- **White Theme**

Themes are based on an auto-detection system of user preferences. The browser adapts its theme to match the system-wide preferences set by the user on their operating system.

## Hot Key Functions 

- **Back**
- **Forward**
- **Reload**
- **Zoom In/Out**
- **Add Multiple Tabs**
- **Open/Close Tabs**
- **History Log: Open/Close**
- **Toggle Fullscreen Mode**

## Known Issues & Future Improvements

### 1. Tuta/Proton Login Access Issue
- **Problem**: Login access fails due to a **Content Security Policy (CSP)** issue.
- **Details**: This occurs when website CSP rules block specific scripts or resources, causing login failures.

### 2. Adblockparser Accuracy
- **Problem**: The **adblockparser** tool is not 100% accurate in identifying and blocking all ads and trackers.
- **Details**:
  - The scope of tracker/ad lists needs expansion to include newer or lesser-known domains.
  - Some rules are skipped or misapplied in edge cases.
  - Dynamically loaded content or obfuscated ads pose detection challenges.

### 3. Suggestions for Improvement
- Continuously update and refine filter lists by collaborating with community-maintained projects.
- Enhance parsing algorithms to address modern, complex web structures (e.g., JavaScript-heavy frameworks).
- Conduct additional testing across a wider range of websites to identify and resolve gaps.
  
## Future Implementation:
- Implementation of Rust Hybrid Encryption with Kyber1024
- ios/Android App Creation
- Desktop App dmg,exe for Mac/Windows

---

## Contributors  
- **Dr. Kevin Moore** ([Darkelf2024](https://github.com/Darkelf2024/Darkelf2024)) Creator, lead developer, initial design, implementation, and ongoing maintenance.  
- **Kevin Nguyen** ([KevinVinhN](https://github.com/KevinVinhN)) – Assisted in testing boot-up, analyzing errors, and identifying possible fixes.  

- **Please See** [Contributors List](https://github.com/Darkelf2024/Darkelf-Browser/blob/main/Contributors.md)

## Acknowledgments & Tools Used  
- **Heapy** – Used for memory leak testing.
- **ChatGPT by OpenAI** – Assisted with code optimization and error analysis.  
---

## Feedback and Contributions

Your feedback is invaluable to the growth and improvement of **Darkelf Browser**. If you have suggestions, ideas, bug reports, or feature requests, please don’t hesitate to:  
- [Open an issue](https://github.com/Darkelf2024/Darkelf-Browser/issues)
- Reach out directly via the project’s contact channels.  

I actively welcome constructive criticism and diverse perspectives, as they help make **Darkelf Browser** better for everyone. Let’s collaborate to foster a vibrant and supportive community around this project.  

Thank you for your continued support in making **Darkelf Browser** the best it can be!  
