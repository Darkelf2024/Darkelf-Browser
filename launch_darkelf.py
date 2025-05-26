# launch_darkelf.py

import sys
from PySide6.QtWidgets import QApplication

# Import both compiled modules
import darkelf_extreme
import darkelf_osint_stealth

# Run test operations for both modules (optional diagnostics)
ops = darkelf_extreme.StealthCovertOps()
ops.log_to_memory("Running from darkelf_extreme")
print("[✓] darkelf_extreme module ran successfully.")

osint_ops = darkelf_osint_stealth.StealthCovertOps()
osint_ops.log_to_memory("Running from darkelf_osint_stealth")
print("[✓] darkelf_osint_stealth module ran successfully.")

# Entry point with mode selector
if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else "extreme"

    if mode == "extreme":
        darkelf_extreme.main()
    elif mode == "osint":
        darkelf_osint_stealth.main()
    else:
        print("[!] Unknown mode. Use: 'extreme' or 'osint'")

# Usage - Run in Terminal - User has 2 options
# python3 launch_darkelf.py          # Defaults to 'extreme'
# python3 launch_darkelf.py osint    # Runs the OSINT+Stealth version
