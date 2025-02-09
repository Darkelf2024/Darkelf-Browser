# Tor DNS Integration

The Darkelf Browser incorporates Tor DNS, an advanced DNS resolution service that enhances privacy by blocking trackers, ads, and phishing domains at the network level. By intercepting DNS requests, it strengthens browsing privacy, ensuring a cleaner, more seamless, and ad-free online experience. Powered by the Tor Project, this integration helps safeguard user anonymity and protect against unwanted online tracking.

## Configuring Tor with `torrc`

To ensure proper integration and functionality of Tor with your application, you need to edit the `torrc` file. This file allows you to configure various Tor settings, including the SOCKS proxy and DNS resolution.

### Where to Find the `torrc` File

The `torrc` file is typically located in the following directories:

- **macOS**: `/usr/local/etc/tor/torrc` or `/opt/homebrew/etc/tor/torrc` (for Homebrew installation)
- **Linux**: `/etc/tor/torrc`
- **Windows**: `C:\Users\<YourUserName>\AppData\Roaming\tor\torrc`

If you can't find it, search for `torrc` or create a new one in the default directory.

### Editing the `torrc` File

1. Open the `torrc` file in a text editor with administrative privileges. For example:
   - On **macOS/Linux**:
     ```bash
     sudo nano /usr/local/etc/tor/torrc
     ```
   - On **Windows**, open a text editor as an administrator and navigate to the Tor installation directory to edit the `torrc` file.

2. Paste the following configuration into the `torrc` file:

### `torrc` Configuration
```bash
# Tor Configuration for DNS, SOCKS, and other settings
SocksPort 9052
ControlPort 9053
DNSPort 9054
AutomapHostsOnResolve 1
VirtualAddrNetworkIPv4 10.192.0.0/10
ExitNodes {us}  # Optional: restrict exit nodes to specific countries, e.g., US
Log notice file /var/log/tor/notices.log

Explanation of Key Settings

    SocksPort 9052: Configures Tor to listen on port 9052 for SOCKS proxy connections.
    ControlPort 9053: Configures the control connection for interacting with Tor, used in your Python code with the Stem library.
    DNSPort 9054: Configures Tor to handle DNS resolution through Tor, ensuring anonymity in DNS queries.
    AutomapHostsOnResolve 1: Forces Tor to use a unique IP address for each resolved hostname, further enhancing privacy.
    VirtualAddrNetworkIPv4 10.192.0.0/10: Configures Tor to use a private IP address range for virtual addresses.
    ExitNodes {us}: Optional setting to restrict Tor's exit nodes to specific countries (e.g., the US). Remove if not needed.
    Log notice file /var/log/tor/notices.log: Logs Tor notices to a file for monitoring and troubleshooting.

Saving and Restarting Tor

Once you've added the configurations, save the torrc file and restart Tor to apply the changes:

    If you're running Tor manually, restart it using:

    sudo service tor restart 

    If running Tor via a script (like your start_tor() function), simply stop and start Tor again through your code.

Additional Configuration Notes

    Firewall/Port Forwarding: Ensure that your firewall allows connections on ports 9052, 9053, and 9054 if you're running Tor on a network that restricts these ports.
    Security Considerations: Be cautious when configuring Tor to use exit nodes from specific countries (like the ExitNodes option). This can reduce anonymity if the exit node is compromised or malicious.
