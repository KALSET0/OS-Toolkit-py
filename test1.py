import os
import shutil
import string
import platform

from files import DriveManager as DM

#test
drives = DM()
Windows_drives = drives.get_windows_drives()
print(Windows_drives)