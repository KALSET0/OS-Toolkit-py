import os
import shutil
import string
import platform

def obtener_unidades_windows():
    """Obtiene los puntos de montaje en Windows."""
    AMARILLO = "\033[33m"
    ROJO = "\033[31m"
    RESET = "\033[0m"
    if platform.system() != "Windows":
        print(f"obtener_unidades_windows():{ROJO} Error: Este método solo es compatible con Windows.{RESET}")
        return []
    
    drives = []
    
    try:
        # Obtener los puntos de montaje en Windows
        bitmask = __import__('ctypes').windll.kernel32.GetLogicalDrives()
        # Iterar a través de las 26 letras del alfabeto para verificar qué los puntos de montaje están existentes
        for i in range(26):
            if bitmask & (1 << i):
                # Construir la letra de la unidad y agregarla a la lista de drives
                letra = f"{string.ascii_uppercase[i]}:\\"
                # Verificar si la letra ya está en la lista de drives antes de agregarla
                if letra not in drives:
                    drives.append(letra)
                else:
                    print(f"obtener_unidades_windows():{AMARILLO} La unidad{RESET} {letra} {AMARILLO}encontrada duplicada, no se agregará a la lista.{RESET}")
        if not drives:
            print(f"obtener_unidades_windows():{AMARILLO} No se encontraron unidades montadas.{RESET}")
        return drives if drives else []
    except Exception as e:
        print(f"obtener_unidades_windows():{ROJO} Error al obtener unidades:{RESET} {e}")
        __import__('traceback').print_exc()
        return []
    
drives = obtener_unidades_windows()
for drive in drives:
    print(f"Unidad encontrada: {drive}")