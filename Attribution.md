# Darkelf Browser

## Attribution

This project utilizes third-party libraries and resources, which are acknowledged below:

- **Python**: [Python Software Foundation](https://www.python.org/) (License: [PSF License](https://docs.python.org/3/license.html))
- **PyQt5**: [Riverbank Computing Limited](https://www.riverbankcomputing.com/software/pyqt/) (License: [GPL](https://www.riverbankcomputing.com/software/pyqt/intro))
- **PyQt-WebEngine**: [Riverbank Computing Limited](https://www.riverbankcomputing.com/software/pyqtwebengine/) (License: [GPL](https://www.riverbankcomputing.com/software/pyqtwebengine/intro))
- **Crypto**: [PyCryptodome](https://www.pycryptodome.org/) (License: [Public Domain](https://github.com/Legrandin/pycryptodome/blob/main/LICENSE))
- **base64**: [Python Standard Library](https://docs.python.org/3/library/base64.html) (License: [PSF License](https://docs.python.org/3/license.html))
- **urllib**: [Python Standard Library](https://docs.python.org/3/library/urllib.html) (License: [PSF License](https://docs.python.org/3/license.html))
- **Other standard libraries**: Refer to their respective documentation.

## Additional Attributions

- **DuckDuckGo Lite Search**: 
This browser uses DuckDuckGo Lite for private and anonymous searches. DuckDuckGo is a privacy-focused search engine that does not track your searches or store your personal information. Learn more about DuckDuckGo at [DuckDuckGo](https://duckduckgo.com/).

- **Tor Network Integration**: 
For enhanced privacy and anonymity, this browser offers integration with the Tor network. The Tor network helps protect your online privacy by routing your internet traffic through a series of encrypted relays. Learn more about the Tor Project at [Tor Project](https://www.torproject.org/).

- **Tor DNS Integration**:
The Darkelf Browser incorporates Tor DNS, an advanced DNS resolution service that enhances privacy by blocking trackers, ads, and phishing domains at the network level. By intercepting DNS requests, it strengthens browsing privacy, ensuring a cleaner, more seamless, and ad-free online experience. Powered by the Tor Project, this integration helps safeguard user anonymity and protect against unwanted online tracking. Learn more about the Tor Project at [Tor Project](https://www.torproject.org/).

## Adblock & Tracking Lists
- **EasyList & Fanboy Lists**: This project incorporates ad-blocking lists from [EasyList](https://easylist.to/) and [Fanboy Annoyance List](https://easylist.to/pages/other-supplementary-filter-lists-and-easylist-variants.html). These lists are maintained by the EasyList community and are licensed under **CC BY-SA 4.0**. More details can be found at [EasyList](https://easylist.to/).  

- **Disconnect Tracking Protection Lists**: This project includes tracking protection lists from [Disconnect](https://github.com/disconnectme/disconnect-tracking-protection), licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)**. More details on the license can be found [here](https://creativecommons.org/licenses/by-nc-sa/4.0/).  

  - These lists **may only be used for non-commercial purposes**. If you would like to use them in a commercial project, please contact **support@disconnect.me** to request a commercial license.  
  - If you believe a tracker has been missed or a domain has been incorrectly categorized, you can submit a report using [this form](https://github.com/disconnectme/disconnect-tracking-protection).  
  - **Note:** Pull requests are not reviewed and will be closed.  

  **Copyright (c) 2024 Disconnect, Inc.**  
  

## Explanation
This application uses PyQt-WebEngine, which provides Python bindings for Qt WebEngine, and Qt WebEngine, which is provided by The Qt Company under the LGPL license.
PyQt-WebEngine enables the integration of web functionality into this application using the Qt framework.
For more information about PyQt-WebEngine, please refer to the PyQt documentation. 

- Python Standard Library: Covers the standard modules provided by Python, including sys, os, gc, base64, and urllib.parse.
- PyQt5: A set of Python bindings for the Qt application framework, covering core and widget components.
- PyQt-WebEngine: Python bindings specifically for the Qt WebEngine module, facilitating web content embedding in Python    applications.
    
- Qt WebEngine: The C++ module providing the actual web rendering engine, which PyQt-WebEngine wraps for use in Python.
- PyCryptodome: A self-contained Python package of low-level cryptographic primitives.
- Guppy: A Python programming environment & heap analysis toolset, with heapy for heap analysis.

## License
This project is licensed under the terms of the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for more details.

### Third-Party Libraries
- **PyQt5**: Licensed under the GNU General Public License v3.0. For more details, visit the [PyQt5 project page](https://riverbankcomputing.com/software/pyqt/intro).
- **Qt WebEngine**: Licensed under the GNU Lesser General Public License v3.0. For more details, visit the [Qt project page](https://www.qt.io/).

Copyright © 2024 Dr. Kevin Moore. All rights reserved.
