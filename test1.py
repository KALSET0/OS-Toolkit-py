import os
import shutil
import string
import platform

class DriveManager:
    @staticmethod
    def get_windows_drives():
    """Gets the mount points in Windows."""
    YELLOW = "\033[33m"
    RED = "\033[31m"
    RESET = "\033[0m"
    if platform.system() != "Windows":
        print(f"get_windows_drives():{RED} Error: This method is only compatible with Windows.{RESET}")
        return []
    
    drives = []
    
    try:
        # Get the mount points in Windows
        bitmask = __import__('ctypes').windll.kernel32.GetLogicalDrives()
        # Iterate through the 26 letters of the alphabet to check which mount points exist
        for i in range(26):
            if bitmask & (1 << i):
                # Build the drive letter and add it to the drives list
                letter = f"{string.ascii_uppercase[i]}:\\"
                # Check if the letter is already in the drives list before adding it
                if letter not in drives:
                    drives.append(letter)
                else:
                    print(f"get_windows_drives():{YELLOW} The drive{RESET} {letter} {YELLOW}was found duplicated, it will not be added to the list.{RESET}")
        if not drives:
            print(f"get_windows_drives():{YELLOW} No mounted drives were found.{RESET}")
        return drives if drives else []
    except Exception as e:
        print(f"get_windows_drives():{RED} Error getting drives:{RESET} {e}")
        __import__('traceback').print_exc()
        return []