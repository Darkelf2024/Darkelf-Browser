# Tor Integration

The Darkelf Browser incorporates Tor DNS, an advanced DNS resolution service that enhances privacy by blocking trackers, ads, and phishing domains at the network level. By intercepting DNS requests, it strengthens browsing privacy, ensuring a cleaner, more seamless, and ad-free online experience. Powered by the Tor Project, this integration helps safeguard user anonymity and protect against unwanted online tracking.

Here is the combined guide with the more accurate Tor DNS configuration for the `torrc` file setup, including the `sudo nano torrc` command for editing and removing the unnecessary `sh` command:

---

# Introduction

Darkelf Browser is a privacy-focused web browser that prioritizes user security and privacy. It includes advanced features such as anti-fingerprinting, ad-blocking, and encryption technologies. This guide will help you install and configure Tor to work with Darkelf Browser.

## Prerequisites

Before starting, ensure you have the following:

- A working installation of Darkelf Browser v3.0.
- Administrative privileges on your computer.
- A stable internet connection.

## Step-by-Step Installation Guide

### Step 1: Install Homebrew (MacOS & Linux)

If you're using macOS, you need to install Homebrew, a package manager for macOS. Open Terminal and run the following command:

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Tor

For macOS and Linux:

1. Open Terminal.
2. Run the following command to install Tor:
   ```sh
   brew install tor
   ```
   If you are on a Linux system, you might need to use your distribution's package manager (e.g., `apt` for Debian-based systems, `yum` for Red Hat-based systems).

For Windows:

1. Download the Tor Expert Bundle from the official Tor Project website: [Tor Project Download](https://www.torproject.org/download/)
2. Extract the contents of the downloaded zip file to a directory of your choice.

### Step 3: Configure Tor for Darkelf Browser

#### Configuration for macOS and Linux:

1. Locate the Tor configuration file. Typically, this is found at `/usr/local/etc/tor/torrc` or `/opt/homebrew/etc/tor/torrc` (for Homebrew installation).
2. Open the `torrc` file in a text editor with administrative privileges:
   ```bash
   sudo nano /usr/local/etc/tor/torrc
   ```
3. Edit the configuration file to include the following lines:
   ```sh
   SocksPort 9052
   ControlPort 9053
   DNSPort 9054
   AutomapHostsOnResolve 1
   VirtualAddrNetworkIPv4 10.192.0.0/10
   ```

#### Configuration for Windows:

1. Navigate to the directory where you extracted the Tor Expert Bundle.
2. Locate the `torrc` file and open it in a text editor with administrative privileges.
3. Add the following lines to the `torrc` file:
   ```sh
   SocksPort 9052
   ControlPort 9053
   DNSPort 9054
   AutomapHostsOnResolve 1
   VirtualAddrNetworkIPv4 10.192.0.0/10
   ```

### Step 4: Start Tor

1. Open Terminal or Command Prompt.
2. Run the following command to start Tor:
   ```sh
   tor
   ```
3. Ensure that you see the message indicating that Tor has started successfully and is accepting connections.

### Step 4: Verify Tor Connection

1. Open a new tab in Darkelf Browser.
2. Navigate to the following URL: [Check Tor Project](https://check.torproject.org/)
3. Verify that you see the confirmation message indicating that your browser is configured to use Tor.

## Troubleshooting

- If you encounter issues starting Tor, ensure that there are no conflicting applications using ports 9052, 9053, and 9054.
- If Darkelf Browser fails to connect through Tor, double-check the Tor configuration and ensure that the Tor process is running.
- For further assistance, consult the [Tor Project Documentation](https://support.torproject.org/).

## Shutdown Instructions

1. After closing Darkelf Browser, ensure you also close Tor.
2. In the terminal, run:
   ```bash
   sudo pkill tor
   ```
3. Enter your system password 


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
