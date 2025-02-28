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
from PySide6.QtGui import QPalette, QColor, QKeySequence, QShortcut, QAction
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtNetwork import QNetworkProxy, QSslConfiguration, QSsl
from PySide6.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineSettings, QWebEnginePage, QWebEngineScript, QWebEngineProfile, QWebEngineDownloadRequest, QWebEngineContextMenuRequest
from PySide6.QtCore import QUrl, QSettings, Qt, QObject, Slot
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import x25519, rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from adblockparser import AdblockRules
import stem.process
from stem.control import Controller
from collections import defaultdict


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

    @Slot(QWebEngineDownloadRequest)
    def handle_download(self, download_item):
        self.downloads.append(download_item)
        save_path, _ = QFileDialog.getSaveFileName(self.parent(), "Save File", download_item.path())
        if save_path:
            download_item.setPath(save_path)
            download_item.accept()
            progress_dialog = QProgressDialog("Downloading...", "Cancel", 0, 100, self.parent())
            progress_dialog.setWindowTitle("Download")
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setMinimumDuration(0)
            progress_dialog.setValue(0)
            progress_dialog.canceled.connect(lambda: download_item.cancel())
            download_item.downloadProgress.connect(
                lambda received, total: self.update_progress(progress_dialog, received, total))
            download_item.finished.connect(lambda: self.finish_download(progress_dialog, download_item))
        else:
            QMessageBox.warning(self.parent(), "Download Cancelled", "The download has been cancelled.")
            self.downloads.remove(download_item)

    def update_progress(self, progress_dialog, received, total):
        if total > 0:
            progress_dialog.setValue(int(received * 100 / total))

    def finish_download(self, progress_dialog, download_item):
        if download_item.state() == QWebEngineDownloadRequest.DownloadCompleted:
            progress_dialog.setValue(100)
            progress_dialog.close()
            QMessageBox.information(self.parent(), "Download Finished", f"Downloaded to {download_item.path()}")
        else:
            progress_dialog.close()
            QMessageBox.warning(self.parent(), "Download Failed", "The download has failed.")
        self.downloads.remove(download_item)
        
# Custom Web Engine Page
class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, browser, parent=None):
        super().__init__(parent)
        self.browser = browser
        self.setup_ssl_configuration()
        self.inject_crypto_script()
        self.inject_crypto_prng_script()
        self.inject_geolocation_override()
        self.protect_fingerprinting()
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

    def protect_fingerprinting(self):
        script = """
        (function() {
            // Canvas Fingerprinting Protection
            const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
            CanvasRenderingContext2D.prototype.getImageData = function() {
                const imageData = originalGetImageData.apply(this, arguments);
                for (let i = 0; i < imageData.data.length; i += 4) {
                    imageData.data[i] = 0;       // Red
                    imageData.data[i + 1] = 0;   // Green
                    imageData.data[i + 2] = 0;   // Blue
                }
                return imageData;
            };

            // User-Agent Spoofing
            Object.defineProperty(navigator, 'userAgent', {
                get: function() { return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.110 Safari/537.36'; }
            });

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
        self.setPage(CustomWebEnginePage(self.browser))
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

    def contextMenuEvent(self, event):
        menu = self.page().createStandardContextMenu()
        new_tab_action = QAction('Open Link in New Tab', self)
        new_tab_action.triggered.connect(self.open_link_in_new_tab)
        menu.addAction(new_tab_action)
        new_window_action = QAction('Open Link in New Window', self)
        new_window_action.triggered.connect(self.open_link_in_new_window)
        menu.addAction(new_window_action)
        menu.exec_(event.globalPos())

    def open_link_in_new_tab(self):
        url = self.page().contextMenuData().linkUrl()
        if url.isValid():
            self.browser.create_new_tab(url.toString())

    def open_link_in_new_window(self):
        url = self.page().contextMenuData().linkUrl()
        if url.isValid():
            self.browser.create_new_window(url.toString())

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
        self.tor_network_enabled = self.settings.value("tor_network_enabled", False, type=bool)
        self.quantum_encryption_enabled = self.settings.value("quantum_encryption_enabled", False, type=bool)
        self.https_enforced = self.settings.value("https_enforced", True, type=bool)
        self.cookies_enabled = self.settings.value("cookies_enabled", False, type=bool)
        self.geolocation_enabled = self.settings.value("geolocation_enabled", False, type=bool)
        self.block_device_orientation = self.settings.value("block_device_orientation", True, type=bool)
        self.block_media_devices = self.settings.value("block_media_devices", True, type=bool)

        # Configure web engine profile
        self.configure_web_engine_profile()

        # Initialize Tor if enabled
        self.init_tor()

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
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpCacheType(QWebEngineProfile.NoCache)
        profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
        settings = profile.settings()
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, False)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, False)  # Ensure JavaScript is disabled by default
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, False)
        settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, False)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)
        settings.setAttribute(QWebEngineSettings.XSSAuditingEnabled, True)
        settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebRTCPublicInterfacesOnly, False)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, False)
        settings.setAttribute(QWebEngineSettings.HyperlinkAuditingEnabled, False)
        settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.SpatialNavigationEnabled, False)
        settings.setAttribute(QWebEngineSettings.AllowWindowActivationFromJavaScript, False)

        adblock_rules = fetch_adblock_rules()
        tracking_domains = fetch_tracking_domains()
        script_block_rules = fetch_script_block_rules()
        interceptor = AdblockAndTrackerInterceptor(adblock_rules, tracking_domains, script_block_rules)
        profile.setUrlRequestInterceptor(interceptor)

    def init_tor(self):
        self.tor_process = None
        if self.tor_network_enabled:
            self.start_tor()
            if self.is_tor_running():
                self.configure_tor_proxy()

    def start_tor(self):
        try:
            if self.tor_process:
                print("Tor is already running.")
                return

            tor_path = "/opt/homebrew/bin/tor"  # Update this with the correct path

            if not os.path.exists(tor_path):
                QMessageBox.critical(self, "Tor Error", "Tor executable not found! Install it using 'brew install tor'.")
                return

            self.tor_process = stem.process.launch_tor_with_config(
                tor_cmd=tor_path,
                config={
                    'SocksPort': '9052',
                    'ControlPort': '9053',
                },
                init_msg_handler=lambda line: print(line) if 'Bootstrapped ' in line else None,
            )

            self.controller = Controller.from_port(port=9053)
            self.controller.authenticate()
            print("Tor started successfully.")

        except OSError as e:
            QMessageBox.critical(self, "Tor Error", f"Failed to start Tor: {e}")

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
        # Note: QWebEngineProfile does not support proxy configuration directly, use QNetworkProxy
        proxy = QNetworkProxy(QNetworkProxy.Socks5Proxy, '127.0.0.1', 9052)
        QNetworkProxy.setApplicationProxy(proxy)
        print("Configured QWebEngineView to use Tor SOCKS proxy.")

    def stop_tor(self):
        if self.tor_process:
            self.tor_process.terminate()
            self.tor_process = None
            print("Tor stopped.")

    def close(self):
        self.stop_tor()
        super().close()

    def init_theme(self):
        self.black_theme_enabled = True
        self.apply_theme()

    def apply_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(40, 40, 40))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(45, 45, 45))
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
        home_button = self.create_button('⏺', self.load_homepage)
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
                    background-color: #333;
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
                    padding: 20px;
                    border-radius: 10px;
                }
                h1 {
                    font-size: 36px;
                    margin-bottom: 20px;
                    color: #34C759;
                }
                p {
                    font-size: 18px;
                    text-align: center;
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
                    background-color: #444;
                    color: #ddd;
                }
                button[type="submit"] {
                    padding: 10px 20px;
                    background-color: #34C759;
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
                    background-color: #28A745;
                }
                footer {
                    position: absolute;
                    bottom: 10px;
                    color: #ddd;
                    font-size: 14px;
                }
                footer a {
                    color: #34C759;
                    text-decoration: none;
                }
                footer a:hover {
                    text-decoration: underline;
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
        self.tab_widget.addTab(new_tab, "New Tab")
        self.tab_widget.setCurrentWidget(new_tab)

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
        quantum_action = QAction("Enable Quantum Encryption", self, checkable=True)
        quantum_action.setChecked(self.quantum_encryption_enabled)
        quantum_action.triggered.connect(self.toggle_quantum_encryption)
        security_menu.addAction(quantum_action)
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
        cookies_action = QAction("Enable Cookies", self, checkable=True)
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
    app = QApplication(sys.argv)
    darkelf_browser = Darkelf()
    darkelf_browser.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
