## 🔒 Secure DNS Fallback: DoT & DoH with Tor Routing

When the Tor network is unavailable, **Darkelf** seamlessly falls back to encrypted DNS resolution using **DNS-over-TLS (DoT)** and **DNS-over-HTTPS (DoH)**. This ensures your DNS activity remains private and resistant to interception or logging by local networks or ISPs.

---

### ✅ DNS-over-TLS (DoT) Fallback

- **DoT** is used to send encrypted DNS queries directly to Cloudflare (`1.1.1.1:853`) over TLS.
- Implemented via `dnspython`, and tunneled through the **Tor SOCKS5 proxy** (`127.0.0.1:9052`) using **PySocks**.
- Ensures:
  - No DNS queries are leaked to the ISP.
  - Traffic is encrypted and anonymized, even outside the Tor network.

#### 🧱 Technical Highlights

- Secure TLS socket created using `socks.socksocket()`.
- SNI and hostname verification enabled (`server_hostname="cloudflare-dns.com"`).
- Operates asynchronously in a `QThread` for non-blocking fallback behavior.

---

### ✅ DNS-over-HTTPS (DoH) Fallback

- **DoH** queries are sent over HTTPS to Cloudflare’s DoH endpoint:  
  `https://cloudflare-dns.com/dns-query`
- Executed using `httpx.AsyncClient` with optional **SOCKS5 proxy** routing via Tor (`socks5h://127.0.0.1:9052`).
- The `socks5h` protocol ensures DNS resolution of the DoH endpoint itself is also proxied.

#### 🧱 Technical Highlights

- Fully asynchronous DNS resolution using HTTP/2-capable `httpx`.
- Optional proxy routing based on Tor state (`tor_enabled` flag).
- Non-blocking fallback thread (`DoHResolverWorker`) integrated into the browser.

---

### 🛠 Fallback Behavior Summary

| Condition         | Action                         | Method     | Routed via Tor? |
|------------------|--------------------------------|------------|------------------|
| Tor Active        | Use Tor DNS (built-in)         | –          | ✅               |
| Tor Fails         | Fallback to DoH & DoT          | DoH + DoT  | ✅ (via SOCKS5)   |
| Proxy Unavailable | Graceful failure, no fallback  | N/A        | ❌ (fails closed) |

---

### 📦 Required Dependencies

Your `requirements.txt` should include:

```
httpx>=0.27.0
dnspython>=2.7.0
PySocks==1.7.1
```

Install dependencies with:

```bash
pip install -r requirements.txt
```
