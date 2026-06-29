from sys import platform


def is_admin():
    try:
        # Llama a una función de Windows que solo los administradores pueden usar con éxito
        return __import__('ctypes').windll.shell32.IsUserAnAdmin() != 0
    except:
        return False
    
#test
print(is_admin())