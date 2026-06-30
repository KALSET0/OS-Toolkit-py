import platform
from users import UserManager



    
#test
admin = UserManager.is_admin_windows()
RunAsAdmin = UserManager.run_as_admin_windows()
print(f"Is the current user an admin? {admin}")
print('hello')
print('bye')
if admin:
    print("The current user has administrative privileges.")
    exit()
else:
    try:
        RunAsAdmin()
    except Exception as e:
        print(f"Error: {e}")
        __import__('traceback').print_exc()
    print(f"The current user is: {admin}")