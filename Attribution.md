# Darkelf Browser

### Authorship

Darkelf Browser is an original project developed by Dr. Kevin Moore. While inspired by best practices from privacy-respecting tools like Brave, Tor Browser, and Puppeteer stealth techniques, all fingerprinting countermeasures and cryptographic enhancements were independently implemented and customized for this application.

This project also used generative assistance (e.g., ChatGPT) during development for research, coding, and documentation — but all architecture, decisions, and final code are authored and reviewed by Dr. Moore.

## Attribution

This project utilizes third-party libraries and resources, which are acknowledged below:  

- **Python** – Python Software Foundation (**License: PSF License**)  
- **PySide6** – The Qt Company Ltd. (**License: LGPL-3.0**)  
- **PySide6-WebEngine** – The Qt Company Ltd. (**License: LGPL-3.0**)  
- **BeautifulSoup4** – Leonard Richardson (**License: MIT**)  
- **Requests** – Kenneth Reitz & contributors (**License: Apache 2.0**)  
- **Adblockparser** – Andy Chilton (**License: MIT**)  
- **Cryptography** – The Python Cryptographic Authority (**License: Apache 2.0**)  
- **PyCryptodome** – Dario Izzo (**License: Public Domain**)  
- **PQCrypto** – Post-Quantum Cryptography library (**License: Varies, see package details**)  
- **dnspython** – Bob Halley & contributors (**License: ISC**)  
- **Stem** – The Tor Project (**License: GPL-3.0**)  
- **Base64, urllib, and other Python Standard Libraries** – Python Software Foundation (**License: PSF License**)  

For detailed licensing information, please refer to each library’s official documentation.  

## Additional Attributions

- **DuckDuckGo Lite Search**:  
  This browser uses DuckDuckGo Lite for private and anonymous searches. DuckDuckGo is a privacy-focused search engine that does not track your searches or store your personal information. Learn more at [DuckDuckGo](https://duckduckgo.com/).

- **Tor Network Integration**:  
  For enhanced privacy and anonymity, this browser offers integration with the Tor network. The Tor network helps protect your online privacy by routing your internet traffic through a series of encrypted relays. Learn more at [Tor Project](https://www.torproject.org/).

- **Tor DNS Integration**:  
  The Darkelf Browser incorporates Tor DNS, an advanced DNS resolution service that enhances privacy by preventing tracking, blocking ads, and mitigating phishing risks. By routing DNS requests through the Tor network, it ensures a cleaner, more seamless, and ad-free browsing experience. Learn more at [Tor Project](https://www.torproject.org/).

## Adblock & Tracking Lists

- **EasyList & Fanboy Lists**:  
  This project incorporates ad-blocking lists from [EasyList](https://easylist.to/) and [Fanboy Annoyance List](https://easylist.to/pages/other-supplementary-filter-lists-and-easylist-variants.html). These lists are maintained by the EasyList community and are licensed under **CC BY-SA 4.0**. More details can be found at [EasyList](https://easylist.to/).

- **Disconnect Tracking Protection Lists**:  
  This project includes tracking protection lists from [Disconnect](https://github.com/disconnectme/disconnect-tracking-protection), licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)**. More details on the license can be found [here](https://creativecommons.org/licenses/by-nc-sa/4.0/).
  
  - These lists **may only be used for non-commercial purposes**. If you would like to use them in a commercial project, please contact **support@disconnect.me** to request a commercial license.
  - If you believe a tracker has been missed or a domain has been incorrectly categorized, you can submit a report using [this form](https://github.com/disconnectme/disconnect-tracking-protection).
 
  - ⚠️ This edition includes Disconnect.me lists, which are licensed under CC BY-NC-SA 4.0. Use in commercial environments may require additional licensing. See https://disconnect.me.

  - **Note:** Pull requests are not reviewed and will be closed.

  **Copyright (c) 2024 Disconnect, Inc.**  
  
## Explanation

This application uses **PySide6-WebEngine**, which provides Python bindings for **Qt WebEngine**, a web rendering engine developed by **The Qt Company** under the **LGPL-3.0 license**.  
**PySide6-WebEngine** enables the integration of web functionality into this application using the **Qt framework**. For more information, refer to the official PySide6 documentation.  

## Code Inspiration / Adapted Techniques

This project uses anti-fingerprinting strategies inspired by or adapted from:

- puppeteer-extra-plugin-stealth (MIT License) – https://github.com/berstend/puppeteer-extra
- Brave Browser Fingerprinting Defenses – https://github.com/brave
- Librewolf Privacy Scripts – https://gitlab.com/librewolf-community

Modifications have been made to suit the PySide6 WebEngine environment and integrate with Darkelf’s privacy core.

### **Key Components and Dependencies:**  

- **Python Standard Library** – Includes built-in modules such as `sys`, `os`, `gc`, `base64`, and `urllib.parse`, essential for system operations, memory management, and URL handling.  
- **PySide6** – A set of **Python bindings** for the **Qt application framework**, covering core UI components, widgets, and WebEngine integration (**License: LGPL-3.0**).  
- **PySide6-WebEngine** – Provides **Python bindings** specifically for **Qt WebEngine**, enabling embedded web browsing in Python applications (**License: LGPL-3.0**).  
- **Qt WebEngine** – A **C++ module** that serves as the actual web rendering engine, wrapped by **PySide6-WebEngine** for Python usage (**License: LGPL-3.0**).  
- **PyCryptodome** – A **self-contained** Python package offering **low-level cryptographic primitives**, useful for encryption and security-related features (**License: Public Domain**).  
- **Adblockparser** – A **Python library** used for parsing and applying ad-blocking rules (**License: MIT**).  
- **dnspython** – A **DNS toolkit** for Python, providing functions for querying and managing DNS records (**License: ISC**).  
- **Stem** – A **controller library** for **Tor**, allowing applications to interact with the Tor network (**License: GPL-3.0**).  

For detailed licensing information, refer to each library’s official documentation.  

## License

Darkelf Browser is released under the **GNU Lesser General Public License v3.0 (LGPL-3.0)**.  
See the full license text [here](https://www.gnu.org/licenses/lgpl-3.0.html).

## Contributions

Contributions are welcome! If you wish to contribute to this project, please follow these guidelines:

1. Fork the repository and create a new branch for your feature or fix.
2. Follow coding best practices and ensure that your changes do not introduce security vulnerabilities.
3. Submit a pull request with a clear description of your changes.

For any major changes, please open an issue first to discuss the proposed modification.

Copyright © 2024 Dr. Kevin Moore. All rights reserved.
