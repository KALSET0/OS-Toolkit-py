import platform
import sys
import ctypes



#=====================================================================
# 1. USER INFORMATION AND PRIVILEGE CHECKING
#=====================================================================

class UserManager:
    """Class to manage user information and check for administrative privileges across different operating systems."""



    @staticmethod
    def is_admin_windows():
        """Checks if the current user has administrative privileges on Windows."""
        YELLOW = "\033[33m"
        RED = "\033[31m"
        RESET = "\033[0m"
        if platform.system() != "Windows":
            print(f"is_admin_windows():{RED} Error: This function is only applicable on Windows.{RESET}")
            return
        try:
            isadmin = ctypes.windll.shell32.IsUserAnAdmin()
            return isadmin != 0  # Calling the Windows API to check for admin rights
        except Exception as e:
            print(f"{RED}Error occurred:{RESET} {e}")
            __import__('traceback').print_exc()
            return



    @classmethod
    def run_as_admin_windows(cls):
        """Attempts to relaunch the current script with administrative privileges on Windows."""
        YELLOW = "\033[33m"
        RED = "\033[31m"
        RESET = "\033[0m"
        if platform.system() != "Windows":
            print(f"run_as_admin_windows():{RED} Error: This function is only applicable on Windows.{RESET}")
            return
        if cls.is_admin_windows() != False:
            print(f"run_as_admin_windows():{YELLOW} Program running as admin already:{RESET} return")
            return
        try:
            ReLauchAdmin = ctypes.windll.shell32.ShellExecuteW
            ReLauchAdmin(None, "runas", sys.executable, " ".join(sys.argv), None, 1) # Relaunch the script with administrative privileges
        except Exception as e:
            print(f"{RED}Error occurred while trying to run as admin:{RESET} {e}")
            __import__('traceback').print_exc()
    


    @staticmethod
    def is_admin_mac():
        """Checks if the current user has administrative privileges on macOS."""
        YELLOW = "\033[33m"
        RED = "\033[31m"
        RESET = "\033[0m"
        if platform.system() != "Darwin":
            print(f"is_admin_mac():{RED} Error: This function is only applicable on macOS.{RESET}")
            return
        try:
            libc = ctypes.CDLL(None)             
            libc.getuid.restype = ctypes.c_uint  
            return libc.getuid() == 0            # Check if the user ID is 0 (root user)
        except Exception as e:
            print(f"{RED}Error occurred:{RESET} {e}")
            __import__('traceback').print_exc()
            return  