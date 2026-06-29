import os
import shutil
import string
import platform
import traceback

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
        

    @staticmethod
    def get_mac_drives():
        """Gets the mount points in macOS."""
        YELLOW = "\033[33m"
        RED = "\033[31m"
        RESET = "\033[0m"
        if platform.system() != "Darwin":
            print(f"get_mac_drives():{RED} Error: This method is only compatible with macOS.{RESET}")
            return []

        drives = []

        try:
            # Get the mount points in macOS using the 'df' command
            ctypes = __import__('ctypes')
            # Call getfsstat to get the number of mounted file systems
            libc = ctypes.CDLL(None)
            # Define the getfsstat function with the correct argument and return types
            num_disks = libc.getfsstat(None, 0, 2) # 2 = MNT_NOWAIT
            
            # If there are no disks, we return an empty list.
            if num_disks <= 0:
                print(f"get_mac_drives():{YELLOW} No mounted drives were found.{RESET}")
                return []
            # Size of the statfs structure in macOS is 2160 bytes
            statfs_size = 2160 
            # Create a buffer to store the file systems information
            buffer = ctypes.create_string_buffer(statfs_size * num_disks)
            # Call getfsstat to fill the buffer with the file systems information
            libc.getfsstat(buffer, buffer._length_, 2)
            # Iterate through each statfs structure to get the mount points
            for i in range(num_disks):
                # Calculate the start of the statfs structure in the buffer
                struct_start = i * statfs_size
                # Get the path of the mount point from the statfs structure
                path_offset = struct_start + 1024
                # Read the path data from the buffer
                path_data = buffer.raw[path_offset : path_offset + 1024]
                # Split the path data by the null character and decode to UTF-8
                final_path = path_data.split(b'\x00')[0].decode('utf-8', errors='ignore')
                # If the path is valid and is not already in the drives list, add it
                if not final_path:
                    continue
                if final_path not in drives:
                    drives.append(final_path)
                else:
                    print(f"get_mac_drives():{YELLOW} The path{RESET} {final_path} {YELLOW}was found duplicated, it will not be added to the list.{RESET}")
            if not drives:
                print(f"get_mac_drives():{YELLOW} No mounted drives were found.{RESET}")
            return drives if drives else []
        except Exception as e:
            print(f"get_mac_drives():{RED} Error getting drives:{RESET} {e}")
            __import__('traceback').print_exc()
            return []
        
    @staticmethod
    def get_drives():
        OSystem = platform.system()
        if OSystem == "Windows":
            return DriveManager.get_windows_drives()
        elif OSystem == "Darwin":
            return DriveManager.get_mac_drives()
        else:
            print("Unsupported operating system.")
            return []

print(DriveManager.get_mac_drives())