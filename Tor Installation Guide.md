# Tor Installation & Configuration (Darkelf Browser)

This guide gives you a clean, up-to-date, **cross-platform** setup for Tor with the ports Darkelf uses:
- **SOCKS**: `9052`
- **Control**: `9053`
- **DNS**: `9054`

It also covers **bridges (obfs4)**, verification, background services, and quick troubleshooting.  
Use this as your drop-in `INSTALL.md`.

---

## Supported setups

- **macOS** (Homebrew)
- **Linux** (Debian/Ubuntu, Fedora/RHEL)
- **Windows 10/11** (via **WSL2 + Ubuntu**)

> On Windows, we recommend **WSL2** instead of “Homebrew on Windows”. Windows apps (including Darkelf) can still use Tor via localhost port forwarding.

---

## 1) Install prerequisites

### macOS
```bash
# Install Homebrew (if you don’t have it)
 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add brew to your shell
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

# Install Tor + obfs4 transport
brew install tor obfs4proxy
```

### Linux

**Debian/Ubuntu:**
```bash
sudo apt update
sudo apt install -y tor obfs4proxy
```

**Fedora/RHEL (dnf):**
```bash
sudo dnf install -y tor
# obfs4proxy package name varies; if unavailable via repo, install from your distro’s backports or build from source.
```

### Windows 10/11 (WSL2 + Ubuntu)

1. **Install WSL** (Windows 11 or Windows 10 2004+):
   ```powershell
   wsl --install -d Ubuntu
   ```
   Reboot if prompted. Launch **Ubuntu** from Start Menu.

2. **Inside WSL Ubuntu:**
   ```bash
   sudo apt update
   sudo apt install -y tor obfs4proxy
   ```

3. (Optional) **Forward ports** so Windows apps can reach Tor in WSL:
   Open **PowerShell as Administrator**:
   ```powershell
   # Map Windows localhost -> WSL localhost
   netsh interface portproxy add v4tov4 listenport=9052 listenaddress=127.0.0.1 connectport=9052 connectaddress=127.0.0.1
   netsh interface portproxy add v4tov4 listenport=9053 listenaddress=127.0.0.1 connectport=9053 connectaddress=127.0.0.1
   netsh interface portproxy add v4tov4 listenport=9054 listenaddress=127.0.0.1 connectport=9054 connectaddress=127.0.0.1
   ```
   > After this, Darkelf on Windows can use `127.0.0.1:9052/9053/9054` backed by Tor inside WSL.

---

## 2) Configure `torrc`

### File locations
- **macOS (Homebrew):** `/opt/homebrew/etc/tor/torrc`
- **Linux / WSL (Ubuntu):** `/etc/tor/torrc`

Open in an editor (pick the path for your OS):
```bash
sudo nano /opt/homebrew/etc/tor/torrc   # macOS (brew)
# or
sudo nano /etc/tor/torrc                # Linux / WSL
```

### Minimal Darkelf configuration (paste this)

```ini
# === Darkelf / Tor configuration ===

# Listeners
SOCKSPort 127.0.0.1:9052
DNSPort 127.0.0.1:9054
ControlPort 127.0.0.1:9053
CookieAuthentication 1

# DNS automapping (optional but recommended for Tor DNS use)
AutomapHostsOnResolve 1
VirtualAddrNetworkIPv4 10.192.0.0/10

# Logging (raise to "info" while debugging)
Log notice stdout

# === Bridges (enable for censored networks) ===
# If you don't need bridges, comment out UseBridges and the lines below.
UseBridges 1

# macOS (Homebrew) obfs4 binary:
ClientTransportPlugin obfs4 exec /opt/homebrew/bin/obfs4proxy
# Linux/WSL obfs4 binary (uncomment if you're on Linux/WSL):
# ClientTransportPlugin obfs4 exec /usr/bin/obfs4proxy

# Paste your obfs4 bridges EXACTLY as issued, one per line:
# Example (replace with fresh bridges):
# Bridge obfs4 87.121.52.247:9216 8C51BB761FF9D89B09A3670892E84019D60D7210 cert=xCIrRXBuV44z3u8QzTFCL5zTqFYe7sTADQ4oHqs91YIbC7kap3WV6TzbvezmJKUGYsY7aQ iat-mode=0
```

**Validate syntax** before starting:
```bash
# macOS (brew path shown), or use your system path
tor --verify-config -f /opt/homebrew/etc/tor/torrc
# or
tor --verify-config -f /etc/tor/torrc
```
You want: `Configuration was valid`.

---

## 3) Start Tor

### Foreground (see live logs)
```bash
# macOS
tor -f /opt/homebrew/etc/tor/torrc
# Linux / WSL
tor -f /etc/tor/torrc
```
Look for: `Bootstrapped 100% (done)`.

### Background services

**macOS (Homebrew services):**
```bash
brew services start tor
# after edits:
brew services restart tor
# tail logs:
brew services log tor
```

**Linux (systemd):**
```bash
sudo systemctl enable tor
sudo systemctl start tor
# after edits:
sudo systemctl restart tor
journalctl -u tor -f
```

**WSL:** start in a dedicated terminal:
```bash
tor -f /etc/tor/torrc
# (optional) set up a systemd user service if you run systemd inside WSL.
```

---

## 4) Verify it’s working

**SOCKS through Tor:**
```bash
curl --socks5-hostname 127.0.0.1:9052 https://check.torproject.org/api/ip
```

You should see JSON like:
```json
{"IsTor":true,"IP":"185.220.101.xxx"}
```

---

## 5) Troubleshooting

- **Ports in use**: stop existing service first:  
  ```bash
  brew services stop tor     # macOS
  sudo systemctl stop tor    # Linux
  sudo pkill tor             # fallback (all)
  ```

- **Bridges not working**:  
  - Ensure `UseBridges 1` is set.  
  - Have at least 2 obfs4 bridges.  
  - Make sure `obfs4proxy` binary path matches your OS.  

- **Reload after editing**:  
  ```bash
  brew services restart tor   # macOS
  sudo systemctl restart tor  # Linux
  ```

---

✅ Tor with Darkelf ports (9052/9053/9054) should now be running.  
