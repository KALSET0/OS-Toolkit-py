from sys import platform


def is_admin():
    try:
        # Llama a una función de Windows que solo los administradores pueden usar con éxito
        return __import__('ctypes').windll.shell32.IsUserAnAdmin() != 0
    except:
        return False
print(is_admin())



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