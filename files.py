import os
import shutil
import string
import platform



# =====================================================================
# 1. DRIVE AND ROOT MANAGEMENT
# =====================================================================

class DriveManager:
    """Class to manage and retrieve drive information across different operating systems."""



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
            ctypes = __import__('ctypes')   # Get the mount points in macOS using the 'df' command
            libc = ctypes.CDLL(None)        # Call getfsstat to get the number of mounted file systems
            # Define the getfsstat function with the correct argument and return types
            num_disks = libc.getfsstat(None, 0, 2) # 2 = MNT_NOWAIT
            
            if num_disks <= 0:
                print(f"get_mac_drives():{YELLOW} No mounted drives were found.{RESET}")
                return []
            statfs_size = 2160                                             # Size of the statfs structure in macOS is 2160 bytes
            buffer = ctypes.create_string_buffer(statfs_size * num_disks)  # Create a buffer to store the file systems information
            libc.getfsstat(buffer, buffer._length_, 2)                     # Call getfsstat to fill the buffer with the file systems information
            # Iterate through each statfs structure to get the mount points
            for i in range(num_disks):
                struct_start = i * statfs_size                             # Calculate the start of the statfs structure in the buffer
                path_offset = struct_start + 1024                          # Get the path of the mount point from the statfs structure
                path_data = buffer.raw[path_offset : path_offset + 1024]   # Read the path data from the buffer
                final_path = path_data.split(b'\x00')[0].decode('utf-8', errors='ignore') # Split the path data by the null character and decode to UTF-8
                if not final_path:
                    continue  # Skip empty paths
                if final_path not in drives:
                    drives.append(final_path)
                else:
                    print(f"get_mac_drives():{YELLOW} The drive{RESET} {final_path} {YELLOW}was found duplicated, it will not be added to the list.{RESET}")
            if not drives:
                print(f"get_mac_drives():{YELLOW} No mounted drives were found.{RESET}")
            return drives if drives else []
        except Exception as e:
            print(f"get_mac_drives():{RED} Error getting drives:{RESET} {e}")
            __import__('traceback').print_exc()
            return []
        


    @staticmethod
    def get_linux_drives():
        """Gets the mount points in Linux."""
        YELLOW = "\033[33m"
        RED = "\033[31m"
        RESET = "\033[0m"
        
        if platform.system() != "Linux":
            print(f"get_linux_drives():{RED} Error: This method is only compatible with Linux.{RESET}")
            return []

        # Define a ctypes Structure to represent the mntent structure in Linux
        class mntent(__import__('ctypes').Structure):
            _fields_ = [
                ("mnt_fsname", __import__('ctypes').c_char_p), # name of mounted file system
                ("mnt_dir", __import__('ctypes').c_char_p),    # directory where the file system is mounted
                ("mnt_type", __import__('ctypes').c_char_p),   # type of the file system
                ("mnt_opts", __import__('ctypes').c_char_p),   # mount options
                ("mnt_freq", __import__('ctypes').c_int),      # dump frequency
                ("mnt_passno", __import__('ctypes').c_int)     # pass number
            ]

        drives = []

        try:
            ctypes = __import__('ctypes')
            libc = ctypes.CDLL(None)      # Load the standard C library (libc) to access Linux system calls

            # Configure the argument and return types for the setmntent, getmntent, and endmntent functions
            libc.setmntent.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
            libc.setmntent.restype = ctypes.c_void_p
            
            libc.getmntent.argtypes = [ctypes.c_void_p]
            libc.getmntent.restype = ctypes.POINTER(mntent)
            
            libc.endmntent.argtypes = [ctypes.c_void_p]
            libc.endmntent.restype = ctypes.c_int

            # Open the /proc/mounts file to read the list of mounted file systems
            fp = libc.setmntent(b"/proc/mounts", b"r")
            if not fp:
                print(f"get_linux_drives():{RED} Error: Could not read mount points.{RESET}")
                return []

            while True:
                entry_ptr = libc.getmntent(fp)
                if not entry_ptr:  # NULL pointer means no more entries
                    break
                
                entry = entry_ptr.contents
                dispositivo = entry.mnt_fsname.decode('utf-8', errors='ignore')
                punto_montaje = entry.mnt_dir.decode('utf-8', errors='ignore')

                # Filter out non-device entries and duplicates, only add valid mount points
                if dispositivo.startswith("/dev/"):
                    if punto_montaje not in drives:
                        drives.append(punto_montaje)
                    else:
                        print(f"get_linux_drives():{YELLOW} The drive{RESET} {punto_montaje} {YELLOW}was found duplicated.{RESET}")

            libc.endmntent(fp) # Close the file pointer to /proc/mounts after reading all entries
            
            if not drives:
                print(f"get_linux_drives():{YELLOW} No mounted drives were found.{RESET}")
            return drives if drives else []
            
        except Exception as e:
            print(f"get_linux_drives():{RED} Error getting drives:{RESET} {e}")
            __import__('traceback').print_exc()
            return []



    @classmethod
    def get_drives(cls):
        """Gets the mount points based on the current operating system."""
        YELLOW = "\033[33m"
        RED = "\033[31m"
        RESET = "\033[0m"
        current_os = platform.system()
        return {
            "Windows": cls.get_windows_drives,
            "Darwin": cls.get_mac_drives,
            "Linux": cls.get_linux_drives
        }.get(current_os, lambda: print(f"get_drives():{RED} Error: Unsupported operating system:{RESET} {current_os}"))()



# =====================================================================
# 2. SEARCH AND FILTERING (Automation)
# =====================================================================



def search_by_prefix(access_path, prefix):
    """Searches for files that start with a specific text (e.g., 'report_')."""
    pass



def search_by_name(access_path, name):
    """Searches for files by exact or partial match."""
    pass



# =====================================================================
# 3. ORGANIZATION AND ATTRIBUTES
# =====================================================================



def sort_by_size(access_path):
    """Scans a folder and returns the files from largest to smallest."""
    pass



# =====================================================================
# 4. MANIPULATION (Physical actions)
# =====================================================================



def move_related_files(source, destination, extension):
    """Moves all files of a certain type (e.g., '.pdf') to a destination folder."""
    pass