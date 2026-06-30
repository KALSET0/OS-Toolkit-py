from storage import DriveManager
#test
drives = DriveManager()
Windows_drives = drives.get_drives()
for drive in Windows_drives:
    print(drive)