import os
import shutil
import string
import platform



# =====================================================================
# 1. GESTIÓN DE UNIDADES Y RAÍCES
# =====================================================================



def obtener_unidades_windows():
    """Obtiene los puntos de montaje en Windows."""
    # Obtener los puntos de montaje en Windows
    bitmask = __import__('ctypes').windll.kernel32.GetLogicalDrives()
    drives = []
    
    # Iterar a través de las 26 letras del alfabeto para verificar qué los puntos de montaje están existentes
    for i in range(26):
        if bitmask & (1 << i):
            # Construir la letra de la unidad y agregarla a la lista de drives
            letra = f"{string.ascii_uppercase[i]}:\\"
            # Verificar si la letra ya está en la lista de drives antes de agregarla
            if letra not in drives:
                drives.append(letra)
    return drives


def obtener_unidades_mac():
    """Obtiene los puntos de montaje en macOS."""
    pass


# =====================================================================
# 2. BÚSQUEDA Y FILTRADO (Automatización)
# =====================================================================



def buscar_por_prefijo(ruta_acceso, prefijo):
    """Busca archivos que empiecen con un texto específico (ej: 'reporte_')."""
    pass

def buscar_por_nombre(ruta_acceso, nombre):
    """Busca archivos por coincidencia exacta o parcial."""
    pass



# =====================================================================
# 3. ORGANIZACIÓN Y ATRIBUTOS
# =====================================================================



def ordenar_por_tamano(ruta_acceso):
    """Escanea una carpeta y devuelve los archivos del más grande al más chico."""
    pass



# =====================================================================
# 4. MANIPULACIÓN (Acciones físicas)
# =====================================================================



def mover_archivos_relacionados(origen, destino, extension):
    """Mueve todos los archivos de un tipo (ej: '.pdf') a una carpeta destino."""
    pass