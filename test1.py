import platform
import string

def obtener_unidades():
    """Detecta el OS y devuelve las unidades o puntos de montaje disponibles."""
    os_actual = platform.system()
    drives = []

    # === BLOQUE WINDOWS ===
    if os_actual == "Windows":
        try:
            bitmask = __import__('ctypes').windll.kernel32.GetLogicalDrives()
            for i in range(26):
                if bitmask & (1 << i):
                    drives.append(f"{string.ascii_uppercase[i]}:\\")
            return drives
        except Exception:
            return []

    # === BLOQUE LINUX ===
    elif os_actual == "Linux":
        try:
            with open("/proc/mounts", "r", encoding="utf-8") as f:
                for linea in f:
                    partes = linea.split()
                    if len(partes) >= 2:
                        ruta = partes[1]
                        if ruta == "/" or ruta.startswith(("/media", "/mnt")):
                            if ruta not in drives:
                                drives.append(ruta)
            return drives
        except Exception:
            return []

    # === BLOQUE MAC ===
    elif os_actual == "Darwin":
        # En Mac usamos el comando 'df' a través de subprocesos
        try:
            output = __import__('subprocess').check_output(["df", "-g"]).decode("utf-8")
            for linea in output.splitlines()[1:]:
                partes = linea.split()
                if partes and (partes[-1] == "/" or partes[-1].startswith("/Volumes/")):
                    drives.append(partes[-1])
            return drives
        except Exception:
            return ["/"]

    return drives