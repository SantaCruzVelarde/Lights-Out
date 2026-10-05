"""
controlador_teclado.py
----------------------
Abstrae la entrada del teclado para el juego usando la librería `keyboard`,
la cual funciona en Windows, Linux y macOS.

Teclas reconocidas (constantes exportadas):
    ARRIBA, ABAJO, DERECHA, IZQUIERDA, ENTRAR, SALIR

Uso:
    import controlador_teclado as teclado

    if teclado.se_esta_presionando(teclado.ARRIBA):
        ...

    teclado.esperar_tecla()   # bloquea hasta que se presione alguna tecla conocida
    teclado.limpiar()         # libera todos los hooks al terminar el programa

Dependencia:
    pip install keyboard
"""

import keyboard


# ==========================================
# CONSTANTES DE TECLAS
# ==========================================

ARRIBA    = "up"
ABAJO     = "down"
DERECHA   = "right"
IZQUIERDA = "left"
FLECHA_ARRIBA    = "flecha arriba"
FLECHA_ABAJO     = "flecha abajo"
FLECHA_DERECHA   = "flecha derecha"
FLECHA_IZQUIERDA = "flecha izquierda"
ENTRAR    = "enter"
SALIR     = "q"
AYUDA     = "a"

# Todas las teclas que el juego reconoce.
_TECLAS_JUEGO = [ARRIBA, ABAJO, DERECHA, IZQUIERDA, FLECHA_ARRIBA, FLECHA_ABAJO, FLECHA_DERECHA, FLECHA_IZQUIERDA, ENTRAR, SALIR, AYUDA, "esc"]


# ==========================================
# CONSULTA DE ESTADO
# ==========================================

def se_esta_presionando(tecla):
    """
    Devuelve True si la tecla indicada está siendo presionada en este momento.

    Parámetros:
        tecla (str): Nombre de la tecla según la librería `keyboard`
                     (p. ej. "up", "enter", "q").
    """
    return keyboard.is_pressed(tecla)

def no_se_esta_presionando(tecla):
    """
    Devuelve True si la tecla indicada NO está siendo presionada.
    Útil para detectar el momento en que el jugador suelta una tecla.

    Parámetros:
        tecla (str): Nombre de la tecla según la librería `keyboard`.
    """
    return not keyboard.is_pressed(tecla)


# ==========================================
# LECTURA Y BLOQUEO
# ==========================================

def esperar_tecla():
    """
    Bloquea la ejecución hasta que el jugador presione una tecla reconocida
    y devuelve su nombre normalizado.

    Retorna:
        str: Una de las constantes del módulo —
             "up", "down", "right", "left", "enter", "q" — o None si la
             tecla presionada no forma parte del juego.
    """
    evento = keyboard.read_event(suppress=False)

    # Solo reaccionar al momento de presionar (keydown), no al soltar.
    if evento.event_type != keyboard.KEY_DOWN:
        return None

    nombre = evento.name.lower()

    # Unificar ESC y Q como señal de salida.
    if nombre in ("q", "esc"):
        return SALIR

    if nombre in _TECLAS_JUEGO:
        return nombre

    return None


# ==========================================
# LIMPIEZA
# ==========================================

def limpiar():
    """Libera todos los hooks registrados por la librería keyboard."""
    keyboard.unhook_all()
