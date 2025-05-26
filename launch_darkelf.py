# launch_darkelf.py

import sys
from PySide6.QtWidgets import QApplication

# Import both compiled modules
import darkelf_extreme
import darkelf_osint_stealth

# Test from both
ops = darkelf_extreme.StealthCovertOps()
ops.log_to_memory("Running from darkelf_extreme")
print("[✓] darkelf_extreme module ran successfully.")

osint_ops = darkelf_osint_stealth.StealthCovertOps()
osint_ops.log_to_memory("Running from darkelf_osint_stealth")
print("[✓] darkelf_osint_stealth module ran successfully.")

# Launch one of them (choose based on mode or argument)
if __name__ == '__main__':
    # You can switch between them if needed
    darkelf_extreme.main()
    # or: darkelf_osint_stealth.main()
