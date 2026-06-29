import os
import shutil
import string
import platform

from files import DriveManager

#test
drives = DriveManager()
Windows_drives = drives.get_windows_drives()
print(Windows_drives)