# Initialize settings from stored values or set defaults.

# Enables or disables JavaScript execution.
# Setting this to False improves security by blocking malicious scripts,
# but it may break websites that rely on JavaScript for functionality.
self.javascript_enabled = self.settings.value("javascript_enabled", False, type=bool)

# Enables anti-fingerprinting measures to reduce tracking.
# When set to True, the browser tries to mask or randomize browser characteristics
# to prevent websites from uniquely identifying users based on their hardware, fonts, etc.
self.anti_fingerprinting_enabled = self.settings.value("anti_fingerprinting_enabled", True, type=bool)

# Enables routing traffic through the Tor network for anonymity.
# If set to True, the browser will use Tor to hide the user's IP address and encrypt traffic.
# Requires Tor to be properly configured on the system.
self.tor_network_enabled = self.settings.value("tor_network_enabled", False, type=bool)

# Enables quantum encryption (hypothetical feature).
# This setting would allow quantum-resistant encryption for securing communications,
# but in most cases, standard encryption methods are used.
self.quantum_encryption_enabled = self.settings.value("quantum_encryption_enabled", False, type=bool)

# Forces all connections to use HTTPS instead of HTTP when possible.
# This protects against man-in-the-middle attacks and improves privacy.
self.https_enforced = self.settings.value("https_enforced", True, type=bool)

# Enables or disables browser cookies.
# Setting this to False blocks cookies, which prevents tracking and session storage
# but may break login functionality on some websites.
self.cookies_enabled = self.settings.value("cookies_enabled", False, type=bool)

# Enables or disables access to the user's geolocation.
# If set to False, websites cannot request or access the user's location.
self.geolocation_enabled = self.settings.value("geolocation_enabled", False, type=bool)

# Blocks websites from accessing device orientation data (e.g., gyroscope and accelerometer).
# Setting this to True prevents potential tracking or motion-based fingerprinting.
self.block_device_orientation = self.settings.value("block_device_orientation", True, type=bool)

# Prevents websites from accessing media devices like the microphone and webcam.
# Setting this to True improves privacy by blocking unauthorized access to these devices.
self.block_media_devices = self.settings.value("block_media_devices", True, type=bool)