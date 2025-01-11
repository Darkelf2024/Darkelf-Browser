## Darkelf Browser Installation Guide

This guide explains the step-by-step process to set up and run the Darkelf Browser on your system.

## Prerequisites

Before you begin, ensure you have the following installed:
	1. Python 3.8 or later: Download from the official website.
	2. Pip (Python Package Installer)
 
 ## Commands: Access Terminal
	1. Verify installation: pip --version
	2. (Optional) Virtual Environment: Install if needed: pip install virtualenv
	3. Create a virtual environment for dependency isolation: python -m venv darkelf_env

## Activate the virtual environment:
	1. Windows: darkelf_env\Scripts\activate
	2. MacOS/Linux: source darkelf_env/bin/activate

## Create a requirements.txt file with the following content:
	1. PyQt5==5.15.9, beautifulsoup4==4.12.2, requests==2.31.0, adblockparser==0.7, cryptography==41.0.3
	2. Install the dependencies: pip install -r requirements.txt
 
## Verify System Compatibility for PyQt5:
	1. Linux: sudo apt-get install python3-pyqt5 python3-pyqt5.qtwebengine
 	2. MacOS: brew install qt
	3. Windows: python -m pip install --upgrade pip

## Install OpenSSL for Secure Communication:
	1. Linux: sudo apt-get install openssl libssl-dev
 	2. MacOS: brew install openssl
  	3. Windows: Download and install OpenSSL from Shining Light Productions.

## Additional Setup for Cryptography
	1. Linux: sudo apt-get install build-essential libffi-dev
 	2. MacOS: brew install libffi
  	3. Windows: Install Visual Studio Build Tools: Visual Studio Build Tools.

## Running the Darkelf Browser
	1. python3 /Users/YouruserName/Desktop/DE\ Public.py
 	2. You can also drag and drop the .py file into the terminal after you type python3
  	3. Wait for it to boot! Enjoy!
   	4. Since Latest Update with Pip3 24.xx and adblock parser is running slower - Just wait 

    Python Program will autodetect what packages are needed at boot if you miss a package during 
    installation if it can't find the package to boot up etc.
 
 
