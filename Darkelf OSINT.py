# Copyright (C) 2025 Dr. Kevin Moore
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# EXPORT COMPLIANCE NOTICE:
# This software, Darkelf Browser v3.0, is classified under ECCN 5D002 c.1
# and is authorized for export under License Exception ENC, as described in
# Sections 740.17(a) and 740.17(b)(1) of the U.S. Export Administration
# Regulations (EAR). The software includes encryption technologies (such
# as AES, RSA, ChaCha20, and X25519) used for secure data storage and
# transmission, which may subject it to U.S. export control laws.
#
# Prohibited Destinations:
# This software may not be exported, re-exported, or transferred, either
# directly or indirectly, to:
# - Countries or territories subject to U.S. embargoes or comprehensive
#   sanctions, as identified by the U.S. Department of Treasury’s Office of
#   Foreign Assets Control (OFAC) or the BIS E1/E2 List.
# - Entities or individuals listed on the U.S. Denied Persons List, Entity
#   List, Specially Designated Nationals (SDN) List, or any other restricted
#   parties list.
#
# End-Use Restrictions:
# This software may not be used for the development, production, or
# deployment of weapons of mass destruction, including nuclear, chemical,
# or biological weapons, or missile technology, as defined under Part 744
# of the EAR.
#
# User Obligations:
# By downloading, using, or distributing this software, you agree to comply
# with all applicable U.S. export laws and regulations. Users and redistributors
# are solely responsible for ensuring their actions adhere to these regulations.
#
# For more information, consult the Bureau of Industry and Security (BIS)
# at https://www.bis.doc.gov.
#
# This software is made available under the LGPL 3.0 license.

import sys
import random
import os
import re
import requests
import shutil
import shlex
import platform
import socket
import dns.resolver
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from base64 import urlsafe_b64encode, urlsafe_b64decode
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QPushButton, QLineEdit, QVBoxLayout, QMenuBar, QToolBar, QDialog, QMessageBox, QFileDialog, QProgressDialog, QListWidget, QMenu, QWidget, QLabel
)
from PySide6.QtGui import QPalette, QColor, QKeySequence, QShortcut, QAction, QGuiApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtNetwork import QNetworkProxy, QSslConfiguration, QSslSocket, QSsl, QSslCipher
from PySide6.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineSettings, QWebEnginePage, QWebEngineScript, QWebEngineProfile, QWebEngineDownloadRequest, QWebEngineContextMenuRequest, QWebEngineCookieStore
from PySide6.QtCore import QUrl, QSettings, Qt, QObject, Slot, QTimer
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import x25519, rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from adblockparser import AdblockRules
import subprocess # nosec - All run through sanitizing and validation
import stem.process
from stem.control import Controller
from collections import defaultdict
from cryptography.fernet import Fernet
import mimetypes
import tempfile
from PIL import Image
import piexif

class EncryptedCookieStore:
    def __init__(self, qt_cookie_store: QWebEngineCookieStore):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.store = {}
        self.qt_cookie_store = qt_cookie_store
        self.qt_cookie_store.cookieAdded.connect(self.intercept_cookie)

    def intercept_cookie(self, cookie):
        """Intercepts cookies as they are added and encrypts them."""
        name = bytes(cookie.name()).decode()
        value = bytes(cookie.value()).decode()
        self.set_cookie(name, value)

    def set_cookie(self, name, value):
        """Encrypts and stores a cookie."""
        encrypted = self.cipher.encrypt(value.encode())
        self.store[name] = encrypted

    def get_cookie(self, name):
        """Decrypts and retrieves a cookie."""
        encrypted = self.store.get(name)
        return self.cipher.decrypt(encrypted).decode() if encrypted else None

    def clear(self):
        """Clears all cookies and securely wipes in-memory values."""
        # Securely wipe the in-memory cookie values
        for key in list(self.store.keys()):
            self.store[key] = None  # Overwrite value
            del self.store[key]     # Remove key-value pair

        # Clear cookies from the QWebEngineCookieStore
        self.qt_cookie_store.deleteAllCookies()

    def wipe_memory(self):
        """Securely wipes all in-memory values."""
        for key in list(self.store.keys()):
            self.store[key] = None  # Overwrite value
        self.store.clear()          # Clear dictionary
        
# Debounce function to limit the rate at which a function can fire
def debounce(func, wait):
    timeout = None

    def debounced(*args, **kwargs):
        nonlocal timeout
        if timeout is not None:
            timeout.cancel()

        def call_it():
            func(*args, **kwargs)

        timeout = Timer(wait / 1000, call_it)
        timeout.start()

    return debounced

# AES-GCM Implementation
def generate_aes_gcm_key():
    return os.urandom(32)

def encrypt_aes_gcm(key, plaintext):
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return urlsafe_b64encode(iv + encryptor.tag + ciphertext).decode()

def decrypt_aes_gcm(key, encrypted_data):
    encrypted_data = urlsafe_b64decode(encrypted_data.encode())
    iv, tag, ciphertext = encrypted_data[:12], encrypted_data[12:28], encrypted_data[28:]
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode()

# RSA Implementation
def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    return private_key, private_key.public_key()

def encrypt_rsa(public_key, plaintext):
    return public_key.encrypt(
        plaintext.encode(),
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_rsa(private_key, ciphertext):
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode()

# ChaCha20 Implementation
def generate_chacha20_key(salt):
    password = os.urandom(32)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password)
    return key

def encrypt_chacha20(key, plaintext):
    nonce = os.urandom(12)
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return urlsafe_b64encode(nonce + ciphertext).decode()

def decrypt_chacha20(key, encrypted_data):
    encrypted_data = urlsafe_b64decode(encrypted_data.encode())
    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode()

# X25519 Implementation
def generate_ecdh_key_pair():
    private_key = x25519.X25519PrivateKey.generate()
    public_key = private_key.public_key()
    with open('ecdh_private_key.pem', 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    return private_key, public_key

def load_or_generate_ecdh_key_pair():
    try:
        with open('ecdh_private_key.pem', 'rb') as f:
            private_key_data = f.read()
            private_key = serialization.load_pem_private_key(
                private_key_data,
                password=None,
                backend=default_backend()
            )
        return private_key
    except Exception as e:
        print(f"Error: {e}")
        return None

# Trie Node
class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_end_of_rule = False

# Trie for Rule Matching
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, rule):
        node = self.root
        for char in rule:
            node = node.children[char]
        node.is_end_of_rule = True

    def search(self, url):
        node = self.root
        for char in url:
            if char not in node.children:
                return False
            node = node.children[char]
            if node.is_end_of_rule:
                return True
        return node.is_end_of_rule

# Clean adblock rule for validation
def clean_adblock_rule(rule):
    try:
        re.compile(rule)
        return rule
    except re.error:
        try:
            escaped_rule = re.escape(rule)
            re.compile(escaped_rule)
            return escaped_rule
        except re.error:
            print(f"Invalid rule discarded: {rule}")
            return None

class AdblockAndTrackerInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, adblock_rules, tracking_domains, script_block_rules):
        super().__init__()
        self.adblock_trie = Trie()
        self.script_block_trie = Trie()
        self.tracking_domains = set(tracking_domains)
        self.cache = {}

        # Insert adblock and script block rules into tries
        for rule in adblock_rules:
            self.adblock_trie.insert(rule)
        for rule in script_block_rules:
            self.script_block_trie.insert(rule)

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        if url in self.cache:
            should_block = self.cache[url]
        else:
            should_block = self.adblock_trie.search(url) or any(domain in url for domain in self.tracking_domains) or self.script_block_trie.search(url)
            self.cache[url] = should_block

        if should_block:
            print(f"Blocked by Adblock/Tracking/Script Rules: {url}")
            info.block(True)

def fetch_adblock_rules():
    urls = [
        "https://easylist.to/easylist/easylist.txt",
        "https://easylist.to/easylist/fanboy-annoyance.txt",
        "https://easylist.to/easylist/fanboy-social.txt",
        "https://easylist.to/easylist/easyprivacy.txt",
        "https://pgl.yoyo.org/as/serverlist.php?hostformat=plain&showintro=0&mimetype=plaintext",
    ]
    rules = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_rules, url) for url in urls]
        for future in futures:
            rules.extend(future.result())
    print(f"Total adblock rules fetched: {len(rules)}")
    return rules

def download_rules(url):
    rules = []
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        raw_rules = response.text.splitlines()
        for rule in raw_rules:
            clean_rule = clean_adblock_rule(rule)
            if clean_rule:
                rules.append(clean_rule)
        print(f"Successfully loaded rules from {url}")
    except requests.RequestException as e:
        print(f"Failed to load rules from {url}: {e}")
    return rules

def fetch_script_block_rules():
    urls = [
        "https://easylist.to/easylist/easylist.txt",
        "https://easylist.to/easylist/easyprivacy.txt",
    ]
    rules = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_rules, url) for url in urls]
        for future in futures:
            rules.extend(future.result())
    print(f"Total script block rules fetched: {len(rules)}")
    return rules

def fetch_tracking_domains():
    tracking_domains = set()
    urls = [
        'https://raw.githubusercontent.com/disconnectme/disconnect-tracking-protection/master/services.json',
        'https://raw.githubusercontent.com/disconnectme/disconnect-tracking-protection/master/entities.json'
    ]
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_tracking_domains, url) for url in urls]
        for future in futures:
            tracking_domains.update(future.result())
    return tracking_domains

def download_tracking_domains(url):
    domains = set()
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        for entity, details in data.items():
            if 'properties' in details:
                for domain in details['properties']:
                    domains.add(domain)
    except requests.RequestException as e:
        print(f"Failed to load tracking domains from {url}: {e}")
    return domains
    
# Download Manager
class DownloadManager(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.downloads = []
        self.timers = {}

    @Slot(QWebEngineDownloadRequest)
    def handle_download(self, download_item):
        """Handles file downloads and assigns correct file extensions."""
        self.downloads.append(download_item)

        # Get the suggested file name from the URL
        suggested_name = download_item.suggestedFileName() if download_item.suggestedFileName() else download_item.url().fileName()

        # Fallback if the name is still empty
        if not suggested_name:
            suggested_name = download_item.url().path().split("/")[-1]  # Extract from URL

        file_ext = os.path.splitext(suggested_name)[1]

        # Use MIME type if no extension is detected
        if not file_ext or file_ext == "":
            mime_type = download_item.mimeType() if hasattr(download_item, 'mimeType') else None
            ext = self.get_extension_from_mime(mime_type)
            
            if ext:
                suggested_name += ext  # Append correct extension

        # Ask user where to save the file
        save_path, _ = QFileDialog.getSaveFileName(self.parent(), "Save File", suggested_name)
        if save_path:
            download_item.setDownloadDirectory(os.path.dirname(save_path))
            download_item.setDownloadFileName(os.path.basename(save_path))
            download_item.accept()

            progress_dialog = QProgressDialog("Downloading...", "Cancel", 0, 100, self.parent())
            progress_dialog.setWindowTitle("Download")
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setMinimumDuration(0)
            progress_dialog.setValue(0)
            progress_dialog.canceled.connect(lambda: download_item.cancel())

            timer = QTimer(self)
            self.timers[download_item] = timer

            def update_progress():
                received = download_item.receivedBytes()
                total = download_item.totalBytes()
                if total > 0:
                    progress_dialog.setValue(int(received * 100 / total))
                if download_item.isFinished():
                    self.finish_download(progress_dialog, download_item, save_path)

            timer.timeout.connect(update_progress)
            timer.start(500)
        else:
            QMessageBox.warning(self.parent(), "Download Cancelled", "The download has been cancelled.")
            self.downloads.remove(download_item)

    def get_extension_from_mime(self, mime_type):
        """Maps MIME types to correct file extensions."""
        mime_map = {
            "application/x-apple-diskimage": ".dmg",
            "application/octet-stream": "",  # Avoid forcing dmg for unknown types
            "application/x-msdownload": ".exe",
            "application/pdf": ".pdf",
            "application/zip": ".zip",
            "application/x-rar-compressed": ".rar",
            "application/x-7z-compressed": ".7z",
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/webp": ".webp",
            "image/gif": ".gif",
            "image/bmp": ".bmp",
            "image/tiff": ".tiff",
            "image/x-icon": ".ico",
            "text/plain": ".txt",
            "application/msword": ".doc",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
            "application/vnd.ms-excel": ".xls",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx"
        }

        # First, check our predefined mapping
        if mime_type in mime_map:
            return mime_map[mime_type]

        # If not found, use Python's mimetypes module as a fallback
        guessed_ext = mimetypes.guess_extension(mime_type)
        
        return guessed_ext if guessed_ext else ""

    def finish_download(self, progress_dialog, download_item, save_path):
        """Handles post-download tasks, including metadata stripping."""
        if download_item in self.timers:
            self.timers[download_item].stop()
            del self.timers[download_item]

        if download_item.state() == QWebEngineDownloadRequest.DownloadCompleted:
            progress_dialog.setValue(100)
            progress_dialog.close()
            self.strip_metadata(save_path)
            QMessageBox.information(self.parent(), "Download Finished", f"Downloaded to {save_path}")
        else:
            progress_dialog.close()
            QMessageBox.warning(self.parent(), "Download Failed", "The download has failed.")

        self.downloads.remove(download_item)

    def strip_metadata(self, file_path):
        """Removes metadata from images (JPEG, PNG, WebP) and PDFs."""
        try:
            if file_path.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                image = Image.open(file_path)
                if "exif" in image.info:
                    exif_bytes = piexif.dump({})
                    image.save(file_path, exif=exif_bytes)
                    print("Metadata stripped from image:", file_path)
                else:
                    print("No EXIF metadata found in image:", file_path)
            elif file_path.lower().endswith(".pdf"):
                from PyPDF2 import PdfReader, PdfWriter
                reader = PdfReader(file_path)
                writer = PdfWriter()
                
                for page in reader.pages:
                    writer.add_page(page)

                # Strip metadata
                writer.add_metadata({})
                with open(file_path, "wb") as output_pdf:
                    writer.write(output_pdf)
                print("Metadata stripped from PDF:", file_path)
            else:
                print("Metadata removal not supported for:", file_path)

        except Exception as e:
            print(f"Failed to strip metadata from {file_path}: {e}")

# Custom Web Engine Page
class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, browser, parent=None):
        super().__init__(parent)
        self.browser = browser
        self.setup_ssl_configuration()
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0")
        
        self.inject_scripts()

    def inject_scripts(self):
        self.inject_crypto_script()
        self.inject_crypto_prng_script()
        self.inject_geolocation_override()
        self.protect_fingerprinting()
        self.block_canvas_api()
        self.disable_webrtc()
        self.setup_csp()

    def createWindow(self, _type):
        return self.browser.create_new_tab().page()

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if self.browser.adblock_rules.should_block(url.toString()):
            return False
        if url.scheme() == 'http' and self.browser.https_enforced:
            secure_url = QUrl(url)
            secure_url.setScheme('https')
            self.setUrl(secure_url)
            return False
        return super().acceptNavigationRequest(url, _type, isMainFrame)

    def setup_ssl_configuration(self):
        configuration = QSslConfiguration.defaultConfiguration()
        configuration.setProtocol(QSsl.TlsV1_3)
        QSslConfiguration.setDefaultConfiguration(configuration)
        #self.ssl_errors.connect(self.handle_ssl_errors)

    def handle_ssl_errors(self, reply, errors):
        for error in errors:
            QMessageBox.critical(self, "SSL Error", f"SSL Error: {error.errorString()}")
        reply.abort()

    def runJavaScript(self, script):
        self.profile.scripts().insert(script)

    def inject_crypto_script(self):
        script = """
        // AES-GCM Implementation
        async function generateAesGcmKey() {
            return window.crypto.subtle.generateKey(
                {
                    name: "AES-GCM",
                    length: 256,
                },
                true,
                ["encrypt", "decrypt"]
            );
        }

        async function encryptAesGcm(key, data) {
            const iv = window.crypto.getRandomValues(new Uint8Array(12));
            const encodedData = new TextEncoder().encode(data);

            const encrypted = await window.crypto.subtle.encrypt(
                {
                    name: "AES-GCM",
                    iv: iv,
                },
                key,
                encodedData
            );

            return {
                iv: iv,
                ciphertext: new Uint8Array(encrypted)
            };
        }

        async function decryptAesGcm(key, iv, ciphertext) {
            const decrypted = await window.crypto.subtle.decrypt(
                {
                    name: "AES-GCM",
                    iv: iv,
                },
                key,
                ciphertext
            );

            return new TextDecoder().decode(decrypted);
        }

        // RSA Implementation
        async function generateRsaKeyPair() {
            return window.crypto.subtle.generateKey(
                {
                    name: "RSA-OAEP",
                    modulusLength: 4096,
                    publicExponent: new Uint8Array([1, 0, 1]),
                    hash: { name: "SHA-256" },
                },
                true,
                ["encrypt", "decrypt"]
            );
        }

        async function encryptRsa(publicKey, data) {
            const encodedData = new TextEncoder().encode(data);

            const encrypted = await window.crypto.subtle.encrypt(
                {
                    name: "RSA-OAEP",
                },
                publicKey,
                encodedData
            );

            return new Uint8Array(encrypted);
        }

        async function decryptRsa(privateKey, ciphertext) {
            const decrypted = await window.crypto.subtle.decrypt(
                {
                    name: "RSA-OAEP",
                },
                privateKey,
                ciphertext
            );

            return new TextDecoder().decode(decrypted);
        }

        // ECDH Implementation
        async function generateEcdhKeyPair() {
            return window.crypto.subtle.generateKey(
                {
                    name: "ECDH",
                    namedCurve: "P-256",
                },
                true,
                ["deriveKey", "deriveBits"]
            );
        }

        async function deriveSharedSecret(privateKey, publicKey) {
            return window.crypto.subtle.deriveKey(
                {
                    name: "ECDH",
                    public: publicKey,
                },
                privateKey,
                {
                    name: "AES-GCM",
                    length: 256,
                },
                true,
                ["encrypt", "decrypt"]
            );
        }
        """
        self.runJavaScript(script)

    def inject_crypto_prng_script(self):
        script = """
        (function() {
            async function getRandomBytes(length) {
                return window.crypto.getRandomValues(new Uint8Array(length));
            }

            window.cryptoPRNG = {
                getRandomBytes
            };
        })();
        """
        self.runJavaScript(script)
        
    def inject_geolocation_override(self):
        script = """
        (function() {
            if (navigator.geolocation) {
                const originalGetCurrentPosition = navigator.geolocation.getCurrentPosition;
                navigator.geolocation.getCurrentPosition = function(success, error, options) {
                    if (error) {
                        error({ code: 1, message: "Geolocation access denied." });
                    }
                };
                const originalWatchPosition = navigator.geolocation.watchPosition;
                navigator.geolocation.watchPosition = function(success, error, options) {
                    if (error) {
                        error({ code: 1, message: "Geolocation access denied." });
                    }
                };
            }
        })();
        """
        self.runJavaScript(script)
        
class SecureWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"JS [{level}]: {message} (line {lineNumber}) in {sourceID}")

    def injectSecurityScripts(self):
        """Inject JavaScript to block canvas fingerprinting"""
        script = """
        (function() {
            let originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
            let originalToBlob = HTMLCanvasElement.prototype.toBlob;
            
            HTMLCanvasElement.prototype.toDataURL = function() {
                console.warn('Blocked Canvas Fingerprinting - toDataURL');
                return "";
            };

            HTMLCanvasElement.prototype.toBlob = function() {
                console.warn('Blocked Canvas Fingerprinting - toBlob');
                return null;
            };
        })();
        """
        self.runJavaScript(script)
        
    def block_webrtc_js():
        script = """
        (function() {
            let OriginalPeerConnection = window.RTCPeerConnection || window.webkitRTCPeerConnection;
        
            if (OriginalPeerConnection) {
                window.RTCPeerConnection = function() {
                    console.warn('Blocked WebRTC - RTCPeerConnection');
                    return null;
                };
                window.webkitRTCPeerConnection = window.RTCPeerConnection;
            }
        })();
        """
        return script
        
    def injectSecurityScripts(self):
        """Inject security scripts to block fingerprinting & WebRTC"""
        self.runJavaScript("""
            (function() {
                let originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
                let originalToBlob = HTMLCanvasElement.prototype.toBlob;
            
                HTMLCanvasElement.prototype.toDataURL = function() {
                    console.warn('Blocked Canvas Fingerprinting - toDataURL');
                    return "";
                };

                HTMLCanvasElement.prototype.toBlob = function() {
                    console.warn('Blocked Canvas Fingerprinting - toBlob');
                    return null;
                };

                let OriginalPeerConnection = window.RTCPeerConnection || window.webkitRTCPeerConnection;
                if (OriginalPeerConnection) {
                    window.RTCPeerConnection = function() {
                        console.warn('Blocked WebRTC - RTCPeerConnection');
                        return null;
                    };
                    window.webkitRTCPeerConnection = window.RTCPeerConnection;
                }
            })();
        """)

    def protect_fingerprinting(self):
        script = """
        (function() {
            // Canvas Fingerprinting Protection with Randomization
            const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
            CanvasRenderingContext2D.prototype.getImageData = function(x, y, w, h) {
                let data = originalGetImageData.apply(this, arguments);
                for (let i = 0; i < data.data.length; i += 4) {
                    data.data[i] = data.data[i] + Math.floor(Math.random() * 10) - 5;       // Red
                    data.data[i + 1] = data.data[i + 1] + Math.floor(Math.random() * 10) - 5;   // Green
                    data.data[i + 2] = data.data[i + 2] + Math.floor(Math.random() * 10) - 5;   // Blue
                }
                return data;
            };

            // WebGL Fingerprinting Protection
            const originalGetParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) {  // UNMASKED_VENDOR_WEBGL
                    return 'Intel Inc.';
                }
                if (parameter === 37446) {  // UNMASKED_RENDERER_WEBGL
                    return 'Intel Iris OpenGL Engine';
                }
                return originalGetParameter.apply(this, arguments);
            };

            // Font Fingerprinting Protection
            const originalMeasureText = CanvasRenderingContext2D.prototype.measureText;
            CanvasRenderingContext2D.prototype.measureText = function(text) {
                const metrics = originalMeasureText.apply(this, arguments);
                metrics.width *= 1.2;  // Arbitrary modification
                return metrics;
            };

            // Media Device Enumeration Blocking
            Object.defineProperty(navigator, 'mediaDevices', {
                get: function() { return undefined; }
            });

            // Timezone Spoofing
            const originalDateToString = Date.prototype.toString;
            Date.prototype.toString = function() {
                return originalDateToString.apply(new Date('Thu, 01 Jan 1970 00:00:00 GMT'), arguments);
            };

            // Language and Locale Spoofing
            Object.defineProperty(navigator, 'language', { get: function() { return 'en-US'; } });
            Object.defineProperty(navigator, 'languages', { get: function() { return ['en-US', 'en']; } });

            // Screen Resolution and Color Depth Spoofing
            Object.defineProperty(screen, 'width', { get: function() { return 1920; } });
            Object.defineProperty(screen, 'height', { get: function() { return 1080; } });
            Object.defineProperty(screen, 'colorDepth', { get: function() { return 24; } });

            // Hardware Concurrency Spoofing
            Object.defineProperty(navigator, 'hardwareConcurrency', { get: function() { return 4; } });

            // Audio Fingerprinting Protection
            const originalCreateAnalyser = AudioContext.prototype.createAnalyser;
            AudioContext.prototype.createAnalyser = function() {
                const analyser = originalCreateAnalyser.apply(this, arguments);
                const originalGetFloatFrequencyData = analyser.getFloatFrequencyData;
                analyser.getFloatFrequencyData = function(array) {
                    for (let i = 0; i < array.length; i++) {
                        array[i] = -100;  // Arbitrary modification
                    }
                    return originalGetFloatFrequencyData.apply(this, arguments);
                };
                return analyser;
            };

            // Battery Status API Blocking
            Object.defineProperty(navigator, 'getBattery', {
                value: function() {
                    return Promise.resolve({
                        charging: true,
                        chargingTime: 0,
                        dischargingTime: Infinity,
                        level: 1
                    });
                }
            });

            // Network Information API Blocking
            Object.defineProperty(navigator.connection || {}, 'effectiveType', { get: function() { return '4g'; } });

            // ETag and Cache-Control Manipulation
            const originalOpen = XMLHttpRequest.prototype.open;
            XMLHttpRequest.prototype.open = function() {
                this.setRequestHeader('Cache-Control', 'no-store');
                this.setRequestHeader('Pragma', 'no-cache');
                this.setRequestHeader('If-None-Match', '');
                return originalOpen.apply(this, arguments);
            };

            // Override getComputedStyle to obfuscate font properties
            const originalGetComputedStyle = window.getComputedStyle;
            window.getComputedStyle = function(element, pseudoElt) {
                const computedStyle = originalGetComputedStyle.apply(this, arguments);
                const originalFontFamily = computedStyle.getPropertyValue('font-family');
                const obfuscatedFontFamily = 'Arial, sans-serif'; // Obfuscate font-family
                Object.defineProperty(computedStyle, 'fontFamily', {
                    get: function() { return obfuscatedFontFamily; }
                });
                return computedStyle;
            };
        })();
        """
        self.runJavaScript(script)

    def block_canvas_api(self):
        script = """
        (function() {
            // Completely block Canvas API
            const blockedApi = [
                'getContext',
                'toDataURL',
                'toBlob',
                'getImageData',
                'fillText',
                'strokeText'
            ];
            const noop = function() {};

            blockedApi.forEach(api => {
                HTMLCanvasElement.prototype[api] = noop;
                OffscreenCanvas.prototype[api] = noop;
            });

            // Block WebGL API
            const blockedWebGLApi = [
                'getExtension',
                'getSupportedExtensions',
                'getParameter',
                'getContextAttributes'
            ];
            blockedWebGLApi.forEach(api => {
                WebGLRenderingContext.prototype[api] = noop;
                WebGL2RenderingContext.prototype[api] = noop;
            });
        })();
        """
        self.runJavaScript(script)

    def disable_webrtc(self):
        script = """
        (function() {
            // Disable WebRTC
            const noop = function() {};
            window.RTCPeerConnection = noop;
            window.RTCSessionDescription = noop;
            window.RTCIceCandidate = noop;
            window.MediaStream = noop;
            window.MediaStreamTrack = noop;
            window.MediaStreamEvent = noop;
            window.RTCDataChannel = noop;
            window.RTCDataChannelEvent = noop;
        })();
        """
        self.runJavaScript(script)
        
    def setup_csp(self):
        script = """
        (function() {
            const meta = document.createElement('meta');
            meta.httpEquiv = "Content-Security-Policy";
            meta.content = "default-src 'self', script-src 'self' 'nonce-12345' 'strict-dynamic' https:, style-src 'self' 'unsafe-inline', img-src 'self' http: https: data: blob:, frame-src 'self' blob: data: https://account-api.proton.me https://account-api.tuta.io https://app.tuta.com/login, object-src 'self' blob:, child-src 'self' data: blob:, report-uri https://reports.proton.me/reports/csp, frame-ancestors 'self', base-uri 'self'";
            document.head.appendChild(meta);
        })();
        """
        self.runJavaScript(script)
        
        # Custom Web Engine View
class CustomWebEngineView(QWebEngineView):
    def __init__(self, browser, parent=None):
        super().__init__(parent)
        self.browser = browser
        self.setPage(CustomWebEnginePage(self))
        self.configure_sandbox()

    def configure_sandbox(self):
        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, False)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, False)
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, False)
        settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, False)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)
        settings.setAttribute(QWebEngineSettings.XSSAuditingEnabled, True)
        settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebRTCPublicInterfacesOnly, False)
        settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, False)

class WebEngineView(QWebEngineView):
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        context_menu_data = self.page().contextMenuData()

        if context_menu_data.isContentEditable():
            menu.addAction("Undo", self.page().triggerAction, QWebEnginePage.Undo)
            menu.addAction("Redo", self.page().triggerAction, QWebEnginePage.Redo)
            menu.addSeparator()
            menu.addAction("Cut", self.page().triggerAction, QWebEnginePage.Cut)
            menu.addAction("Copy", self.page().triggerAction, QWebEnginePage.Copy)
            menu.addAction("Paste", self.page().triggerAction, QWebEnginePage.Paste)
            menu.addAction("Delete", self.page().triggerAction, QWebEnginePage.Delete)
            menu.addSeparator()
            menu.addAction("Select All", self.page().triggerAction, QWebEnginePage.SelectAll)
        else:
            menu.addAction("Back", self.page().triggerAction, QWebEnginePage.Back)
            menu.addAction("Forward", self.page().triggerAction, QWebEnginePage.Forward)
            menu.addAction("Reload", self.page().triggerAction, QWebEnginePage.Reload)
            menu.addSeparator()

            if context_menu_data.linkUrl().isValid():
                new_tab_action = QAction('Open Link in New Tab', self)
                new_tab_action.triggered.connect(lambda: self.open_link_in_new_tab(context_menu_data))
                menu.addAction(new_tab_action)

                new_window_action = QAction('Open Link in New Window', self)
                new_window_action.triggered.connect(lambda: self.open_link_in_new_window(context_menu_data))
                menu.addAction(new_window_action)

                menu.addAction("Copy Link Address", self.page().triggerAction, QWebEnginePage.CopyLinkToClipboard)

        menu.exec(event.globalPos())

    def open_link_in_new_tab(self, context_menu_data):
        url = context_menu_data.linkUrl()
        if url.isValid():
            self.browser.create_new_tab(url.toString())

    def open_link_in_new_window(self, context_menu_data):
        url = context_menu_data.linkUrl()
        if url.isValid():
            self.browser.create_new_window(url.toString())

class TorManager:
    def __init__(self):
        self.tor_process = None
        self.controller = None

    def start_tor(self):
        try:
            if self.tor_process:
                print("Tor is already running.")
                return

            tor_path = "/opt/homebrew/bin/tor"  # Update this with the correct path

            if not os.path.exists(tor_path):
                QMessageBox.critical(None, "Tor Error", "Tor executable not found! Install it using 'brew install tor'.")
                return

            self.tor_process = stem.process.launch_tor_with_config(
                tor_cmd=tor_path,
                config={
                    'SocksPort': '9052',
                    'ControlPort': '9053',
                    'DNSPort': '9054',
                    'AutomapHostsOnResolve': '1',
                    'VirtualAddrNetworkIPv4': '10.192.0.0/10',
                },
                init_msg_handler=lambda line: print(line) if 'Bootstrapped ' in line else None,
            )

            self.controller = Controller.from_port(port=9053)
            self.controller.authenticate()
            print("Tor started successfully.")

        except OSError as e:
            QMessageBox.critical(None, "Tor Error", f"Failed to start Tor: {e}")

    def is_tor_running(self):
        try:
            with Controller.from_port(port=9053) as controller:
                controller.authenticate()
                print("Tor is running.")
                return True
        except Exception as e:
            print(f"Tor is not running: {e}")
            return False

    def configure_tor_proxy(self):
        proxy = QNetworkProxy(QNetworkProxy.Socks5Proxy, '127.0.0.1', 9052)
        QNetworkProxy.setApplicationProxy(proxy)
        print("Configured QWebEngineView to use Tor SOCKS proxy.")

    def configure_tor_dns(self):
        os.environ['DNSPORT'] = '127.0.0.1:9054'
        print("Configured Tor DNS.")

    def stop_tor(self):
        if self.tor_process:
            self.tor_process.terminate()
            self.tor_process = None
            print("Tor stopped.")

    def close(self):
        self.stop_tor()

    def switch_node(self):
        try:
            if self.controller:
                self.controller.signal(Signal.NEWNYM)
                print("Switched to a new Tor node.")
        except Exception as e:
            print(f"Failed to switch Tor node: {e}")

class WebsiteBlockDetector:
    def handle_website_block(self, url):
        try:
            response = requests.get(url, timeout=10)  # Adding a timeout of 10 seconds
            # Check if the status code indicates that the website is blocked
            if response.status_code == 403:
                website_blocked = True
            else:
                website_blocked = False
        except requests.exceptions.RequestException as e:
            # Handle other exceptions such as connection errors
            website_blocked = True

        if website_blocked:
            print("Website blocked. Switching Tor node...")
            self.switch_node()

    def switch_node(self):
        # Implement logic to switch Tor node
        print("Switching Tor node...")

class Darkelf(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Darkelf Browser")
        self.showMaximized()

        # Initialize settings first
        self.init_settings()

        # Initialize security configurations
        self.init_security()

        # Initialize UI elements
        self.init_ui()

        # Initialize theme and download manager
        self.init_theme()
        self.init_download_manager()

        # Initialize history log
        self.history_log = []
        
        # Add shortcuts for various actions
        self.init_shortcuts()
        
    def init_settings(self):
        self.settings = QSettings("DarkelfBrowser", "Darkelf")
        self.load_settings()

    def load_settings(self):
        self.download_path = self.settings.value("download_path", os.path.expanduser("~"), type=str)

    def save_settings(self):
        self.settings.setValue("download_path", self.download_path)

    def init_security(self):
        self.aes_key = self.load_aes_key()
        self.ecdh_key_pair = self.load_or_generate_ecdh_key_pair()
        self.rsa_key_pair = self.load_or_generate_rsa_key_pair()
        self.chacha20_key = self.generate_chacha20_key(os.urandom(16))

        # Initialize settings
        self.javascript_enabled = self.settings.value("javascript_enabled", False, type=bool)
        self.anti_fingerprinting_enabled = self.settings.value("anti_fingerprinting_enabled", True, type=bool)
        self.tor_network_enabled = self.settings.value("tor_network_enabled", True, type=bool)
        self.quantum_encryption_enabled = self.settings.value("quantum_encryption_enabled", False, type=bool)
        self.https_enforced = self.settings.value("https_enforced", True, type=bool)
        self.cookies_enabled = self.settings.value("cookies_enabled", False, type=bool)
        self.geolocation_enabled = self.settings.value("geolocation_enabled", False, type=bool)
        self.block_device_orientation = self.settings.value("block_device_orientation", True, type=bool)
        self.block_media_devices = self.settings.value("block_media_devices", True, type=bool)

        # Configure web engine profile
        self.configure_web_engine_profile()

        # Initialize Tor if enabled
        if self.tor_network_enabled:
            self.init_tor()
            
        # Configure user agent to mimic Firefox ESR
        self.configure_user_agent()
    
    def configure_tls(self):
        ssl_configuration = QSslConfiguration.defaultConfiguration()

        # Mimic Firefox ESR cipher suites
        firefox_cipher_suites = [
            'TLS_AES_128_GCM_SHA256',
            'TLS_AES_256_GCM_SHA384',
            'TLS_CHACHA20_POLY1305_SHA256',
            'TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256',
            'TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256',
            'TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384',
            'TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384',
            'TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256',
            'TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256'
        ]

        # Convert the cipher suite strings to QSslCipher objects
        cipher_objects = [QSslCipher(cipher) for cipher in firefox_cipher_suites]
        ssl_configuration.setCiphers(cipher_objects)

        # Set the modified configuration as the default
        QSslConfiguration.setDefaultConfiguration(ssl_configuration)

        # Mimic Firefox ESR TLS versions
        ssl_configuration.setProtocol(QSsl.TlsV1_2OrLater)
        QSslSocket.setDefaultSslConfiguration(ssl_configuration)
        
    def configure_user_agent(self):
        profile = QWebEngineProfile.defaultProfile()
        # Default to Firefox 137.0
        firefox_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0"
        profile.setHttpUserAgent(firefox_user_agent)

    def toggle_firefox_user_agent(self, enabled):
        profile = QWebEngineProfile.defaultProfile()
        if enabled:
            firefox_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0"
            profile.setHttpUserAgent(firefox_user_agent)
        else:
            chrome_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
            profile.setHttpUserAgent(chrome_user_agent)
        
    def load_aes_key(self):
        pass

    def load_or_generate_rsa_key_pair(self):
        try:
            with open('private_key.pem', 'rb') as f:
                private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend()
                )
        except FileNotFoundError:
            private_key, public_key = self.generate_rsa_key_pair()
            with open('private_key.pem', 'wb') as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ))
        return private_key

    def generate_rsa_key_pair(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    def load_or_generate_ecdh_key_pair(self):
        try:
            with open('ecdh_private_key.pem', 'rb') as f:
                private_key_data = f.read()
                private_key = serialization.load_pem_private_key(
                    private_key_data,
                    password=None,
                    backend=default_backend()
                )
                return private_key, private_key.public_key()
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading ECDH private key: {e}")
            return self.generate_ecdh_key_pair()

    def generate_ecdh_key_pair(self):
        private_key = x25519.X25519PrivateKey.generate()
        public_key = private_key.public_key()
        with open('ecdh_private_key.pem', 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        return private_key, public_key

    def generate_chacha20_key(self, salt):
        password = os.urandom(32)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password)
        return key

    def encrypt_chacha20(self, key, plaintext):
        nonce = os.urandom(12)
        cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return urlsafe_b64encode(nonce + ciphertext).decode()

    def decrypt_chacha20(self, key, encrypted_data):
        encrypted_data = urlsafe_b64decode(encrypted_data.encode())
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]
        cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext.decode()

    def configure_web_engine_profile(self):
        self.ram_path = tempfile.mkdtemp()
        profile = QWebEngineProfile.defaultProfile()
        profile.setCachePath(self.ram_path)
        profile.setPersistentStoragePath(self.ram_path)
        profile.setHttpCacheType(QWebEngineProfile.NoCache)
        profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
        profile.setPersistentStoragePath("")
        profile.setHttpCacheMaximumSize(0)
        profile.setSpellCheckEnabled(False)
        settings = profile.settings()
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, False)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, False)  # Ensure JavaScript is disabled by default
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, False)
        settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, False)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)
        settings.setAttribute(QWebEngineSettings.XSSAuditingEnabled, True)
        settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebRTCPublicInterfacesOnly, False)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, False)
        settings.setAttribute(QWebEngineSettings.HyperlinkAuditingEnabled, False)
        settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.SpatialNavigationEnabled, False)
        settings.setAttribute(QWebEngineSettings.AllowWindowActivationFromJavaScript, False)
        settings.setAttribute(QWebEngineSettings.ScreenCaptureEnabled, False)
        settings.setAttribute(QWebEngineSettings.PdfViewerEnabled, False)
        
        # Assuming fetch_adblock_rules and fetch_tracking_domains are defined elsewhere
        adblock_rules = fetch_adblock_rules()
        tracking_domains = fetch_tracking_domains()
        script_block_rules = fetch_script_block_rules()
        interceptor = AdblockAndTrackerInterceptor(adblock_rules, tracking_domains, script_block_rules)
        profile.setUrlRequestInterceptor(interceptor)

        # Attach encrypted in-memory cookie store
        cookie_store = profile.cookieStore()
        self.encrypted_store = EncryptedCookieStore(cookie_store)

    def init_tor(self):
        self.tor_manager = TorManager()
        self.tor_manager.start_tor()
        self.tor_manager.configure_tor_proxy()
        self.tor_manager.configure_tor_dns()
        
    def init_theme(self):
        self.black_theme_enabled = True
        self.apply_theme()

    def apply_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.setPalette(palette)

    def init_download_manager(self):
        self.download_manager = DownloadManager(self)
        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.download_manager.handle_download)

    def init_ui(self):
        self.setWindowTitle("Darkelf Browser")
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.setMovable(True)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 0;
            }
            QTabBar::tab {
                background: #333;
                color: #fff;
                padding: 5px 10px;
                border-radius: 10px;
                margin: 2px;
            }
            QTabBar::tab:selected, QTabBar::tab:hover {
                background: #34C759;
                color: #000;
                border-radius: 10px;
            }
        """)
        self.create_toolbar()
        self.create_menu_bar()
        self.create_new_tab("home")

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        back_button = self.create_button('◄', self.go_back)
        toolbar.addWidget(back_button)
        forward_button = self.create_button('►', self.go_forward)
        toolbar.addWidget(forward_button)
        reload_button = self.create_button('↺', self.reload_page)
        toolbar.addWidget(reload_button)
        home_button = self.create_button('⏻', self.load_homepage)  # Unicode character for power button
        toolbar.addWidget(home_button)
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search or enter URL")
        self.search_bar.returnPressed.connect(self.search_or_load_url)
        self.style_line_edit(self.search_bar)
        toolbar.addWidget(self.search_bar)
        zoom_in_button = self.create_button('+', self.zoom_in)
        toolbar.addWidget(zoom_in_button)
        zoom_out_button = self.create_button('-', self.zoom_out)
        toolbar.addWidget(zoom_out_button)
        full_screen_button = self.create_button('⛶', self.toggle_full_screen)
        toolbar.addWidget(full_screen_button)

    def create_button(self, text, callback):
        button = QPushButton(text)
        button.clicked.connect(callback)
        self.style_button(button)
        return button

    def style_button(self, button):
        button.setStyleSheet("""
            QPushButton {
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 5px;
                margin: 3px;
                font-size: 12px;
                background-color: #333;
                color: #fff;
            }
            QPushButton:hover {
                color: #34C759;
            }
        """)

    def style_line_edit(self, line_edit):
        line_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 5px;
                margin: 3px;
                font-size: 12px;
                background-color: #333;
                color: #fff;
            }
        """)

    def load_homepage(self):
        current_tab = self.tab_widget.currentWidget()
        web_view = current_tab.findChild(QWebEngineView)
        if web_view:
            web_view.setHtml(self.custom_homepage_html())

    def custom_homepage_html(self):
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Darkelf</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
            <style id="theme-style">
                body {
                    font-family: Arial, sans-serif;
                    background-color: #000;
                    color: #ddd;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    flex-direction: column;
                    height: 100vh;
                    align-items: center;
                    justify-content: center;
                }
                .content {
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                }
                h1 {
                    font-size: 36px;
                    margin-bottom: 20px;
                    color: #34C759; /* Same green as the tab */
                }
                form {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-top: 20px;
                }
                input[type="text"] {
                    padding: 10px;
                    width: 500px;
                    margin-right: 10px;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                    background-color: #333;
                    color: #ddd;
                }
                button[type="submit"] {
                    padding: 10px 20px;
                    background-color: #333;
                    border: none;
                    color: white;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                button[type="submit"]:hover {
                    color: #34C759;
                }
            </style>
        </head>
        <body>
            <div class="content">
                <h1>Darkelf Browser</h1>
                <p>Your privacy is our priority.</p>
                <form id="searchForm" action="https://lite.duckduckgo.com/lite/" method="get">
                    <input type="text" id="searchInput" name="q" placeholder="Search DuckDuckGo">
                    <button type="submit"><i class="bi bi-search"></i></button>
                </form>
            </div>
        </body>
        </html>
        """
        return html_content
        
    def current_web_view(self):
        return self.tab_widget.currentWidget().findChild(QWebEngineView)

    def update_tab_title(self):
        web_view = self.current_web_view()
        if web_view:
            self.tab_widget.setTabText(self.tab_widget.currentIndex(), web_view.page().title())

    def update_url_bar(self, url):
        self.search_bar.setText(url.toString())

    def create_menu_bar(self):
        menu_bar = QMenuBar(self)

        # Create menus
        navigation_menu = menu_bar.addMenu("Navigation")
        self.add_navigation_actions(navigation_menu)
        security_menu = menu_bar.addMenu("Security")
        self.set_up_security_actions(security_menu)
        settings_menu = menu_bar.addMenu("Settings")
        self.add_settings_actions(settings_menu)
        history_menu = menu_bar.addMenu("History")
        view_history_action = QAction("View History", self)
        view_history_action.triggered.connect(self.view_history)
        history_menu.addAction(view_history_action)
        clear_history_action = QAction("Clear History", self)
        clear_history_action.triggered.connect(self.clear_history)
        history_menu.addAction(clear_history_action)
        osint_menu = menu_bar.addMenu("OSINT")
        self.add_osint_actions(osint_menu)
        mapping_menu = menu_bar.addMenu("Mapping")
        self.add_mapping_actions(mapping_menu)
        tools_menu = menu_bar.addMenu("Tools")
        self.add_tools_actions(tools_menu)
        about_menu = menu_bar.addMenu("About")
        about_privacy_action = QAction("Privacy Policy", self)
        about_privacy_action.triggered.connect(self.show_privacy_policy)
        about_menu.addAction(about_privacy_action)
        about_terms_action = QAction("Terms of Service", self)
        about_terms_action.triggered.connect(self.show_terms_of_service)
        about_menu.addAction(about_terms_action)
    
        self.setMenuBar(menu_bar)

    # Method to show Privacy Policy
    def show_privacy_policy(self):
        self.create_new_tab("https://github.com/Darkelf2024/Darkelf-Browser/blob/main/Privacy%20Policy.md")

    # Method to show Terms of Service
    def show_terms_of_service(self):
        self.create_new_tab("https://github.com/Darkelf2024/Darkelf-Browser/blob/main/Terms.md")
        
    def open_new_tab(self, url):
        new_tab = QWebEngineView()
        new_tab.setUrl(QUrl(url))
        self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentWidget(new_tab)
        self.setMenuBar(menu_bar)

    def add_navigation_actions(self, navigation_menu):
        back_action = QAction("Back", self)
        back_action.triggered.connect(self.go_back)
        navigation_menu.addAction(back_action)
        forward_action = QAction("Forward", self)
        forward_action.triggered.connect(self.go_forward)
        navigation_menu.addAction(forward_action)
        reload_action = QAction("Reload", self)
        reload_action.triggered.connect(self.reload_page)
        navigation_menu.addAction(reload_action)
        home_action = QAction("Home", self)
        home_action.triggered.connect(self.load_homepage)
        navigation_menu.addAction(home_action)
        new_tab_action = QAction("New Tab", self)
        new_tab_action.triggered.connect(lambda: self.create_new_tab())
        navigation_menu.addAction(new_tab_action)
        close_tab_action = QAction("Close Tab", self)
        close_tab_action.triggered.connect(lambda: self.close_tab(self.tab_widget.currentIndex()))
        navigation_menu.addAction(close_tab_action)
        close_window_action = QAction("Close Window", self)
        close_window_action.triggered.connect(self.close)
        navigation_menu.addAction(close_window_action)

    def set_up_security_actions(self, security_menu):
        javascript_action = QAction("Enable JavaScript", self, checkable=True)
        javascript_action.setChecked (False) # Ensure it is unchecked at startup
        javascript_action.triggered.connect(lambda: self.toggle_javascript(javascript_action.isChecked()))
        security_menu.addAction(javascript_action)
        fingerprinting_action = QAction("Enable Anti-Fingerprinting", self, checkable=True)
        fingerprinting_action.setChecked(self.anti_fingerprinting_enabled)
        fingerprinting_action.triggered.connect(self.toggle_anti_fingerprinting)
        security_menu.addAction(fingerprinting_action)
        tor_action = QAction("Enable Tor Network", self, checkable=True)
        tor_action.setChecked(self.tor_network_enabled)
        tor_action.triggered.connect(self.toggle_tor_network)
        security_menu.addAction(tor_action)
        firefox_user_agent_action = QAction("Enable Firefox Agent", self, checkable=True)
        firefox_user_agent_action.setChecked(True)
        firefox_user_agent_action.triggered.connect(lambda: self.toggle_firefox_user_agent(firefox_user_agent_action.isChecked()))
        security_menu.addAction(firefox_user_agent_action)
        clear_cache_action = QAction("Clear Cache", self)
        clear_cache_action.triggered.connect(self.clear_cache)
        security_menu.addAction(clear_cache_action)
        clear_cookies_action = QAction("Clear Cookies", self)
        clear_cookies_action.triggered.connect(self.clear_cookies)
        security_menu.addAction(clear_cookies_action)

    def add_settings_actions(self, settings_menu):
        https_action = QAction("Enforce HTTPS", self, checkable=True)
        https_action.setChecked(self.https_enforced)
        https_action.triggered.connect(self.toggle_https_enforcement)
        settings_menu.addAction(https_action)
        cookies_action = QAction("Enable Cookies", self, checkable=False)
        cookies_action.setChecked(not self.cookies_enabled)
        cookies_action.triggered.connect(self.toggle_cookies)
        settings_menu.addAction(cookies_action)
        geolocation_action = QAction("Enable Geolocation", self, checkable=True)
        geolocation_action.setChecked(self.geolocation_enabled)
        geolocation_action.triggered.connect(self.toggle_geolocation)
        settings_menu.addAction(geolocation_action)
        orientation_action = QAction("Block Device Orientation", self, checkable=True)
        orientation_action.setChecked(self.block_device_orientation)
        orientation_action.triggered.connect(self.toggle_device_orientation)
        settings_menu.addAction(orientation_action)
        media_devices_action = QAction("Block Media Devices", self, checkable=True)
        media_devices_action.setChecked(self.block_media_devices)
        media_devices_action.triggered.connect(self.toggle_media_devices)
        settings_menu.addAction(media_devices_action)
        
    def open_url(self, url):
        """
        Open the specified URL in a new tab or in the current tab.
        """
        self.create_new_tab(url)

    def add_osint_actions(self, osint_menu):
        urls = [
            ("Apify", "https://www.apify.com/"),
            ("Graph.tips", "https://graph.tips/"),
            ("Intelx.io", "https://intelx.io/"),
            ("Lookup-id.com", "https://lookup-id.com/"),
            ("Sowsearch.info", "https://sowsearch.info/"),
            ("Whopostedwhat.com", "https://whopostedwhat.com/"),
            ("Hunchly", "https://www.hunch.ly/"),
            ("OSINT Combine", "https://www.osintcombine.com/"),
            ("Internet Archive", "https://archive.org/"),
            ("InfoGalactic", "https://infogalactic.com/info/Main_Page"),
            ("Maltego", "https://www.maltego.com/"),
            ("HackerOne", "https://www.hackerone.com/"),
            ("OSINT Framework", "https://osintframework.com/"),
            ("Censys", "https://censys.io/"),
            ("LeakCheck", "https://leakcheck.io/"),
            ("MX ToolBox", "https://mxtoolbox.com/whois.aspx"),
            ("PublicWWW", "https://publicwww.com/"),
            ("W3Techs", "https://w3techs.com/sites/"),
            ("Social Search", "https://social-searcher.com/"),
            ("GeoIP Lookup", "https://ipinfo.io/"),
            ("DomainTools", "https://www.domaintools.com/"),
            ("Zoom Earth", "https://zoom.earth/"),
            ("NASA Worldview", "https://worldview.earthdata.nasa.gov/"),
            ("Yeti", "https://yeti-platform.github.io/"),
            ("MISP", "https://www.misp-project.org/"),
            ("Dork's Collection List", "https://github.com/cipher387/Dorks-collections-list")
        ]
        for name, url in urls:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, u=url: self.open_url(u))
            osint_menu.addAction(action)

    def add_mapping_actions(self, mapping_menu):
        urls = [
            ("OpenStreetMap", "https://www.openstreetmap.org/"),
            ("MapLibre", "https://maplibre.org/"),
            ("OpenMapTiles", "https://openmaptiles.org/"),
            ("Leaflet", "https://leafletjs.com/")
        ]
        for name, url in urls:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, u=url: self.open_url(u))
            mapping_menu.addAction(action)

    def add_tools_actions(self, tools_menu):
        urls = [
            # OSINT Tools that can be installed via Homebrew
            ("Sherlock", "sherlock"),
            ("Shodan", "shodan"),
            ("Recon-ng", "recon-ng"),
            ("The Harvester", "theharvester"),
            ("Nmap", "nmap"),
            ("Yt-Dlp", "yt-dlp"),
            ("Maltego", "maltego"),
            ("Masscan", "masscan"),
            ("Amass", "amass"),
            ("Subfinder", "subfinder"),
            ("Exiftool", "exiftool"),
            ("Mat2", "mat2"),
            ("Neomutt", "neomutt"),
            ("Thunderbird", "thunderbird"),
        ]
        
        def open_tool(url):
            system = platform.system()

            def run_command(command):
                # Ensure command is a list of arguments
                if isinstance(command, list) and all(isinstance(arg, str) for arg in command):
                    subprocess.run(command, check=True)  # nosec B602
                else:
                    raise ValueError("Invalid command format")
                    
            # Define a list of allowed tools
            allowed_tools = ["sherlock", "shodan", "recon-ng", "theharvester", "nmap", "yt-dlp", "maltego", "masscan", "amass", "subfinder", "exiftool", "mat2", "Neomutt", "Thunderbird"]

            # Ensure the provided url is in the list of allowed tools
            if url in allowed_tools:
                sanitized_url = shlex.quote(url)

                # Execute platform-specific commands to open the too
                if system == "Darwin":  # macOS
                    apple_script = f'''
                    tell application "Terminal"
                        do script "brew install {sanitized_url} && exec $SHELL"
                        activate
                    end tell
                    '''
                    run_command(["osascript", "-e", apple_script]) # nosec B603
                elif system == "Linux":
                    run_command(["gnome-terminal", "--", "sh", "-c", f"brew install {sanitized_url} && exec bash"])
                elif system == "Windows":
                    run_command(["cmd.exe", "/c", "start", "cmd.exe", "/k", f"brew install {sanitized_url}"])
                else:
                    raise OSError("Unsupported operating system: " + system)
            else:
                self.open_url(url)

        def open_url(self, url):
            """
            Open the specified URL in a new tab or in the current tab.
            """
            self.create_new_tab(url)
        
        for tool_name, tool_url in urls:
            action = QAction(tool_name, self)
            action.triggered.connect(lambda checked, url=tool_url: open_tool(url))
            tools_menu.addAction(action)
                
    def init_shortcuts(self):
        # Shortcut for creating a new tab (Cmd+T on macOS, Ctrl+T on other systems)
        QShortcut(QKeySequence("Ctrl+T" if sys.platform != 'darwin' else "Meta+T"), self, self.create_new_tab)

        # Shortcut for closing the current tab (Cmd+W on macOS, Ctrl+W on other systems)
        QShortcut(QKeySequence("Ctrl+W" if sys.platform != 'darwin' else "Meta+W"), self, lambda: self.close_tab(self.tab_widget.currentIndex()))

        # Shortcut for reloading the current page (Cmd+R on macOS, Ctrl+R on other systems)
        QShortcut(QKeySequence("Ctrl+R" if sys.platform != 'darwin' else "Meta+R"), self, self.reload_page)

        # Shortcut for going back (Cmd+Left on macOS, Ctrl+Left on other systems)
        QShortcut(QKeySequence("Ctrl+Left" if sys.platform != 'darwin' else "Meta+Left"), self, self.go_back)

        # Shortcut for going forward (Cmd+Right on macOS, Ctrl+Right on other systems)
        QShortcut(QKeySequence("Ctrl+Right" if sys.platform != 'darwin' else "Meta+Right"), self, self.go_forward)

        # Shortcut for toggling full screen (F11)
        QShortcut(QKeySequence("F11"), self, self.toggle_full_screen)

        # Shortcut for viewing history (Cmd+H on macOS, Ctrl+H on other systems)
        QShortcut(QKeySequence("Ctrl+H" if sys.platform != 'darwin' else "Meta+H"), self, self.view_history)

        # Shortcut for zooming in (Cmd++ on macOS, Ctrl++ on other systems)
        QShortcut(QKeySequence("Ctrl++" if sys.platform != 'darwin' else "Meta++"), self, self.zoom_in)

        # Shortcut for zooming out (Cmd+- on macOS, Ctrl+- on other systems)
        QShortcut(QKeySequence("Ctrl+-" if sys.platform != 'darwin' else "Meta+-"), self, self.zoom_out)
        
    def create_new_tab(self, url="home"):
        web_view = QWebEngineView()
        web_view.loadFinished.connect(self.update_tab_title)
        web_view.urlChanged.connect(self.update_url_bar)
        if url == "home":
            web_view.setHtml(self.custom_homepage_html())
            tab_title = "Darkelf"
        else:
            web_view.setUrl(QUrl(url))
            tab_title = "New Tab"

        index = self.tab_widget.addTab(web_view, tab_title)
        self.tab_widget.setCurrentIndex(index)
        return web_view

    def load_url(self, url):
        return QUrl(url)

    def create_new_window(self, url=None):
        new_window = Darkelf()
        if url:
            new_window.create_new_tab(url)
        new_window.show()
        return new_window

    def close_tab(self, index):
        if self.tab_widget.count() < 2:
            return
        widget = self.tab_widget.widget(index)
        widget.deleteLater()
        self.tab_widget.removeTab(index)
        self.clear_cache_and_history()

    def go_back(self):
        if self.tab_widget.currentWidget():
            self.tab_widget.currentWidget().back()

    def go_forward(self):
        if self.tab_widget.currentWidget():
            self.tab_widget.currentWidget().forward()

    def reload_page(self):
        if self.tab_widget.currentWidget():
            self.tab_widget.currentWidget().reload()

    def update_tab_title(self):
        index = self.tab_widget.currentIndex()
        web_view = self.tab_widget.widget(index)
        title = web_view.page().title()
        self.tab_widget.setTabText(index, title)

    def update_url_bar(self, q):
        url_str = q.toString()
        if not url_str.startswith("data:text/html"):
            self.search_bar.setText(url_str)
            self.history_log.append(url_str)

    def load_homepage(self):
        index = self.tab_widget.currentIndex()
        web_view = self.tab_widget.widget(index)
        web_view.setHtml(self.custom_homepage_html())

    def zoom_in(self):
        current_tab = self.tab_widget.currentWidget()
        if isinstance(current_tab, QWebEngineView):
            current_tab.setZoomFactor(current_tab.zoomFactor() + 0.1)

    def zoom_out(self):
        current_tab = self.tab_widget.currentWidget()
        if isinstance(current_tab, QWebEngineView):
            current_tab.setZoomFactor(current_tab.zoomFactor() - 0.1)

    def toggle_full_screen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def clear_cache(self):
        profile = QWebEngineProfile.defaultProfile()
        profile.clearHttpCache()
        QMessageBox.information(self, "Cache Cleared", "The cache has been successfully cleared.")

    def clear_cookies(self):
        profile = QWebEngineProfile.defaultProfile()
        profile.cookieStore().deleteAllCookies()
        QMessageBox.information(self, "Cookies Cleared", "All cookies have been successfully cleared.")

    def search_or_load_url(self):
        text = self.search_bar.text()
        if text.startswith(('http://', 'https://')):
            self.create_new_tab(text)
        else:
            self.create_new_tab(f"https://lite.duckduckgo.com/lite/?q={text}")

    def toggle_javascript(self, enabled):
        self.javascript_enabled = enabled
        self.settings.setValue("javascript_enabled", enabled)
        index = self.tab_widget.currentIndex()
        if index != -1:
            web_view = self.tab_widget.widget(index)
            web_view.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, enabled)
            
    def toggle_anti_fingerprinting(self, enabled):
        self.anti_fingerprinting_enabled = enabled
        self.settings.setValue("anti_fingerprinting_enabled", enabled)

    def toggle_tor_network(self, enabled):
        self.tor_network_enabled = enabled
        self.settings.setValue("tor_network_enabled", enabled)
        if enabled:
            self.start_tor()
        else:
            self.stop_tor()

    def toggle_quantum_encryption(self, enabled):
        self.quantum_encryption_enabled = enabled
        self.settings.setValue("quantum_encryption_enabled", enabled)

    def toggle_https_enforcement(self, enabled):
        self.https_enforced = enabled
        self.settings.setValue("https_enforced", enabled)

    def toggle_cookies(self, enabled):
        self.cookies_enabled = enabled
        self.settings.setValue("cookies_enabled", enabled)
        self.configure_web_engine_profile()

    def toggle_geolocation(self, enabled):
        self.geolocation_enabled = enabled
        self.settings.setValue("geolocation_enabled", enabled)

    def toggle_device_orientation(self, enabled):
        self.block_device_orientation = enabled
        self.settings.setValue("block_device_orientation", enabled)

    def toggle_media_devices(self, enabled):
        self.block_media_devices = enabled
        self.settings.setValue("block_media_devices", enabled)

    def closeEvent(self, event):
        self.save_settings()
        self.clear_cache_and_history()
        super().closeEvent(event)

    def handle_download(self, download_item):
        self.download_manager.handle_download(download_item)

    def clear_cache_and_history(self):
        profile = QWebEngineProfile.defaultProfile()
        profile.clearHttpCache()
        profile.clearAllVisitedLinks()
        self.history_log.clear()

    def view_history(self):
        dialog = HistoryDialog(self.history_log, self)
        dialog.exec()

    def clear_history(self):
        self.history_log.clear()
        self.clear_cache_and_history()
        QMessageBox.information(self, "Clear History", "Browsing history cleared.")

class HistoryDialog(QDialog):
    def __init__(self, history_log, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Browsing History")
        
        layout = QVBoxLayout()
        self.history_list = QListWidget()
        self.history_list.addItems(history_log)
        layout.addWidget(self.history_list)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
        self.setLayout(layout)

def main():
    # Apply correct High DPI scaling
    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Set Chromium flags to disable WebRTC, WebGL, Canvas API, GPU, etc.
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
        "--disable-webrtc "
        "--disable-webgl "
        "--disable-3d-apis "
        "--disable-rtc-sctp-data-channels "
        "--disable-rtc-multiple-routes "
        "--disable-rtc-stun-origin "
        "--force-webrtc-ip-handling-policy=disable_non_proxied_udp "
        "--disable-rtc-event-log "
        "--disable-rtc-sdp-logs "
        "--disable-webgl-2 "
        "--disable-gpu "
        "--disable-d3d11 "
        "--disable-accelerated-2d-canvas "
        "--disable-software-rasterizer "
        "--disable-features=Canvas2DImageChromium,WebGLImageChromium "
        "--disable-reading-from-canvas "
        "--disable-offscreen-canvas "
        "--use-angle=none "
        "--disable-extensions "
        "--disable-sync "
        "--disable-translate "
        "--disable-plugins "
        "--disable-features=CookiesWithoutSameSiteMustBeSecure,AutofillServerCommunication "
        "--disable-client-side-phishing-detection "
        "--disable-font-subpixel-positioning "
        "--disable-kerning "
        "--disable-web-fonts "
        "--disable-background-networking "
        "--disable-sync "
        "--disable-translate "
        "--disable-speech-api "
        "--disable-sensor "
        "--disable-features=InterestCohortAPI,PrivacySandboxAdsAPIs "
        "--disable-javascript-harmony "
        "--no-referrers "
        "--incognito "
        "--enable-features=StrictOriginIsolation,PartitionedCookies "
        "--disable-third-party-cookies "
        "--use-fake-ui-for-media-stream "
    )

    # Create the application
    app = QApplication.instance() or QApplication(sys.argv)

    # Initialize and show the browser
    darkelf_browser = Darkelf()
    darkelf_browser.show()

    # Run the application
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
