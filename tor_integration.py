import stem.process
from stem.control import Controller
from PyQt5.QtWidgets import QMessageBox

class TorIntegration:
    def __init__(self, settings):
        self.settings = settings
        self.tor_network_enabled = self.settings.value("tor_network_enabled", False, type=bool)
        self.tor_process = None
        self.controller = None
        self.init_tor()

    def init_tor(self):
        if self.tor_network_enabled:
            self.start_tor()

    def start_tor(self):
        try:
            if self.tor_process:
                return
            self.tor_process = stem.process.launch_tor_with_config(
                config={
                    'SocksPort': '9052',  # Changed port
                    'ControlPort': '9053',  # Changed port
                },
                init_msg_handler=lambda line: print(line) if 'Bootstrapped ' in line else None,
            )
            self.controller = Controller.from_port(port=9053)
            self.controller.authenticate()
            print("Tor successfully started and authenticated.")
        except OSError as e:
            QMessageBox.critical(None, "Tor Error", f"Failed to start Tor: {e}")

    def stop_tor(self):
        if self.tor_process:
            self.tor_process.terminate()
            self.tor_process = None

    def close(self):
        self.stop_tor()

# You have two options for starting Tor, Boot from Darkelf Browser or used this Tor py file for modularizing and maintaining. 
