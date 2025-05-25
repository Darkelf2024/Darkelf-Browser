# darkelf_run.py

import sys
from PySide6.QtWidgets import QApplication
import darkelf_extreme  # This is your compiled .so module

# Call a test function or create a class instance
ops = darkelf_extreme.StealthCovertOps()
ops.log_to_memory("Running from compiled module")
print("[✓] Compiled module ran successfully.")

# Manually call main() defined in the original script
if __name__ == '__main__':
    darkelf_extreme.main()
