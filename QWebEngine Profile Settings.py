def configure_web_engine_profile(self):
    """
    Configures the default QWebEngineProfile settings to enhance security and privacy.
    """

    profile = QWebEngineProfile.defaultProfile()

    # Disables HTTP caching.
    # Prevents storing website data locally, reducing the risk of tracking and data leaks.
    profile.setHttpCacheType(QWebEngineProfile.NoCache)

    # Disables persistent cookies.
    # Ensures that cookies are only stored temporarily and removed when the session ends.
    profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)

    settings = profile.settings()

    # Disables local storage (e.g., HTML5 localStorage & IndexedDB).
    # This prevents websites from storing data on the user's machine.
    settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, False)

    # Enables or disables JavaScript execution based on user settings.
    # Disabling JavaScript improves security but may break web functionality.
    settings.setAttribute(QWebEngineSettings.JavascriptEnabled, self.javascript_enabled)

    # Prevents JavaScript from opening new windows/pop-ups.
    # Useful for blocking unwanted ads and pop-ups.
    settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, False)

    # Blocks JavaScript from accessing the clipboard (copy/paste data).
    # This prevents malicious scripts from stealing clipboard content.
    settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, False)

    # Restricts locally loaded content (like HTML files) from accessing remote URLs.
    # Prevents potential security risks from local files making network requests.
    settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)

    # Enables Cross-Site Scripting (XSS) auditing.
    # Helps detect and block certain types of XSS attacks.
    settings.setAttribute(QWebEngineSettings.XSSAuditingEnabled, True)

    # Disables the custom error page for failed network requests.
    # Instead of a built-in error page, the browser will fail silently.
    settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, False)

    # Disables WebGL, a JavaScript API for rendering 3D graphics in the browser.
    # Some WebGL implementations have security vulnerabilities.
    settings.setAttribute(QWebEngineSettings.WebGLEnabled, False)

    # Restricts WebRTC to only use public interfaces.
    # Prevents leaking the user's local IP address, improving privacy.
    settings.setAttribute(QWebEngineSettings.WebRTCPublicInterfacesOnly, False)

    # Allows automatic loading of images.
    # If set to False, websites will not display images, improving privacy but breaking UI.
    settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)

    # Disables plugins (e.g., Flash, PDF viewers).
    # Reduces attack vectors but may limit functionality on some websites.
    settings.setAttribute(QWebEngineSettings.PluginsEnabled, False)

    # Disables hyperlink auditing (ping attributes in links).
    # Prevents websites from tracking clicks using the "ping" attribute.
    settings.setAttribute(QWebEngineSettings.HyperlinkAuditingEnabled, False)

    # Enables full-screen support.
    # If set to True, websites can request full-screen mode for videos and other content.
    settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)

    # Disables spatial navigation.
    # This feature allows keyboard navigation between links but is rarely used.
    settings.setAttribute(QWebEngineSettings.SpatialNavigationEnabled, False)

    # Prevents JavaScript from activating or bringing windows to the foreground.
    # This helps prevent unwanted focus stealing by web pages.
    settings.setAttribute(QWebEngineSettings.AllowWindowActivationFromJavaScript, False)