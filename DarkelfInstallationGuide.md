## Darkelf Browser Installation Guide

This guide explains the step-by-step process to set up and run the Darkelf Browser on your system.

## Prerequisites

## Before you begin, ensure you have the following installed:
	1. Python 3.12 or later: Download from the official website.
	2. Pip (Python Package Installer)
 	Note: Latest Python3/Pip3 Versions are recommended.
  	3. For MacOS/linux - It is recommended that you have Homebrew installed!
 
 ## Commands: Access Terminal
	1. Verify installation: pip --version
	2. (Optional) Virtual Environment: Install if needed: pip install virtualenv
	3. Create a virtual environment for dependency isolation: python -m venv darkelf_env

## Activate the virtual environment:
	1. Windows: darkelf_env\Scripts\activate
	2. MacOS/Linux: source darkelf_env/bin/activate

## Create a requirements.txt file with the following content:

 1. PyQt5==5.15.9
 2. beautifulsoup4
 3. requests
 4. adblockparser
 5. cryptography
 6. pycryptodome - Latest
 7. pqcrypto - Latest
 8. PyQtWebEngine - Latest
 9. dns.resolver/dnspython
 10. stem(Tor Network - Optional)
 *  Upgrade Python3/Pip3 - Latest

 * [Requirements File](https://github.com/Darkelf2024/Darkelf-Browser/blob/main/requirements.txt)

 - Install the dependencies: pip install -r requirements.txt (Creating a "requirement" txt file will batch dependencies together - It is optional)
 - You can pip install all packages manually in terminal etc. - Your choice.

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
   	4. Since Latest Update with Pip3 24.xx and adblockparser is running slower - Just wait 

    Python Program will autodetect what packages are needed at boot if you miss a package during 
    installation if it can't find the package to boot up etc. Just install the package with Pip3 - Remember - You will receive an error if a package is not installed 
 
 
