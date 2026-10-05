"""
comandos_consola.py
-------------------
Mini-biblioteca de control de terminal usando códigos de escape ANSI.
Compatible con cualquier terminal que soporte ANSI True Color (24 bits).

Uso:
    import comandos_consola as consola

    consola.limpiar_pantalla()
    consola.mover_cursor(5, 10)
    consola.establecer_color_hex("0969da")
    consola.imprimir("Hola")
    consola.restaurar_colores()
"""

import sys


# ==========================================
# SALIDA
# ==========================================

def imprimir(texto):
    """Escribe texto inmediatamente en pantalla sin salto de línea."""
    sys.stdout.write(texto)
    sys.stdout.flush()


# ==========================================
# CURSOR
# ==========================================

def mover_cursor(fila, columna):
    """Mueve el cursor a una posición específica de la terminal (base 1)."""
    imprimir(f"\033[{fila};{columna}H")

def ocultar_cursor():
    """Oculta el cursor parpadeante."""
    imprimir("\033[?25l")

def mostrar_cursor():
    """Muestra nuevamente el cursor."""
    imprimir("\033[?25h")


# ==========================================
# PANTALLA
# ==========================================

def limpiar_pantalla():
    """Borra todo el contenido visible de la consola y lleva el cursor al origen."""
    imprimir("\033[2J\033[H")

def borrar_linea():
    """Borra el contenido de la línea donde se encuentra el cursor."""
    imprimir("\033[2K\r")


# ==========================================
# COLOR
# ==========================================

def restaurar_colores():
    """Vuelve a los colores por defecto de la terminal."""
    imprimir("\033[0m")

def establecer_color_hex(hex_color):
    """
    Aplica color 'True Color' (24 bits) al texto usando el código ANSI:
        ESC[38;2;R;G;Bm

    Parámetros:
        hex_color (str): Color en formato hexadecimal sin '#', p. ej. "0969da".
    """
    # Convertir cada par de dígitos hex a su valor entero (base 10).
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    imprimir(f"\033[38;2;{r};{g};{b}m")
