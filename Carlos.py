import os
import random
import shutil
from collections import Counter

import comandos_consola    as consola
import controlador_teclado as teclado

# COLORES 

COLOR_ENCENDIDO   = "f5a623"
COLOR_APAGADO     = "4a5568"
COLOR_LLAMA       = "ff4500"
COLOR_CURSOR_ON   = "ff6b6b"
COLOR_CURSOR_OFF  = "56d8e4"
COLOR_AYUDA       = "c678dd"
COLOR_TITULO      = "eda73b"
COLOR_SUBTITULO   = "0969da"
COLOR_MENU_SEL    = "39d353"
COLOR_MENU_NORM   = "8b9bb4"
COLOR_BARRA       = "8b9bb4"
COLOR_VICTORIA    = "39d353"
COLOR_MOVS        = "56d8e4"
COLOR_AYUDA_IND   = "c678dd"
 
# ENCENDEDORES ASCII POR DIFICULTAD 

def _p(s, w):
    return (s + ' ' * w)[:w]

# Encendedor unico: 7 filas x 12 cols
_W = 12
ENC_ON  = [_p(r, _W) for r in [
    '___    A  ',
    '| |   {*} ',
    '| |  __V__',
    '|_|o_|%%%|',
    '   |     |',
    '   | |=| |',
    '   |_____|',
]]
ENC_OFF = [_p(r, _W) for r in [
    '___       ',
    '| |       ',
    '| |  _____',
    '|_|o_|%%%|',
    '   |     |',
    '   | |-| |',
    '   |_____|',
]]

ENCENDEDORES = {
    "Facil":   {"on": ENC_ON, "off": ENC_OFF, "alto": 7, "ancho": _W, "sep_col": 1, "sep_fila": 1},
    "Mediana": {"on": ENC_ON, "off": ENC_OFF, "alto": 7, "ancho": _W, "sep_col": 1, "sep_fila": 1},
    "Dificil": {"on": ENC_ON, "off": ENC_OFF, "alto": 7, "ancho": _W, "sep_col": 1, "sep_fila": 1},
}

# CONFIGURACION POR DIFICULTAD 

DIFICULTADES = {
    "Facil":   {"tamano": 5, "pulsaciones": 5},
    "Mediana": {"tamano": 7, "pulsaciones": 10},
    "Dificil": {"tamano": 9, "pulsaciones": 15},
}
NOMBRES = list(DIFICULTADES.keys())
 
# UTILIDADES DE PANTALLA

def ancho_terminal():
    return shutil.get_terminal_size((80, 24)).columns

def alto_terminal():
    return shutil.get_terminal_size((80, 24)).lines

def centrar_col(contenido_ancho):
    return max(1, (ancho_terminal() - contenido_ancho) // 2 + 1)

def centrar_fila(contenido_alto):
    return max(1, (alto_terminal() - contenido_alto) // 2 + 1)
 
# LOGICA DEL JUEGO 

def crear_tablero(n):
    return [[False] * n for _ in range(n)]

def pulsar(tablero, f, c):
    n = len(tablero)
    for df, dc in [(0,0),(-1,0),(1,0),(0,-1),(0,1)]:
        nf, nc = f+df, c+dc
        if 0 <= nf < n and 0 <= nc < n:
            tablero[nf][nc] = not tablero[nf][nc]

def generar_tablero(n, pulsaciones):
    tablero  = crear_tablero(n)
    celdas   = [(f, c) for f in range(n) for c in range(n)]
    solucion = random.sample(celdas, pulsaciones)
    for f, c in solucion:
        pulsar(tablero, f, c)
    return tablero, solucion

def es_victoria(tablero):
    return all(not c for fila in tablero for c in fila)

def celdas_afectadas(tablero, f, c):
    n = len(tablero)
    resultado = []
    for df, dc in [(0,0),(-1,0),(1,0),(0,-1),(0,1)]:
        nf, nc = f+df, c+dc
        if 0 <= nf < n and 0 <= nc < n:
            resultado.append((nf, nc))
    return resultado

# DIBUJO DE ENCENDEDORES

def dibujar_encendedor(fila_pan, col_pan, encendido, es_cursor, enc, es_ayuda=False):
    if es_cursor:
        color = "ff6b6b" if encendido else "56d8e4"
    elif es_ayuda:
        color = COLOR_AYUDA
    else:
        color = COLOR_ENCENDIDO if encendido else COLOR_APAGADO

    filas = enc["on"] if encendido else enc["off"]

    for i, linea in enumerate(filas):
        consola.mover_cursor(fila_pan + i, col_pan)
        # Llama en la fila que contiene {*} o A, solo encendidos sin ayuda/cursor especial
        if encendido and not es_ayuda and not es_cursor:
            if '{*}' in linea:
                idx = linea.find('{*}')
                consola.establecer_color_hex(color)
                consola.imprimir(linea[:idx])
                consola.establecer_color_hex(COLOR_LLAMA)
                consola.imprimir('{*}')
                consola.establecer_color_hex(color)
                consola.imprimir(linea[idx+3:])
                continue
            elif linea.strip().startswith('A'):
                idx = linea.find('A')
                consola.establecer_color_hex(color)
                consola.imprimir(linea[:idx])
                consola.establecer_color_hex(COLOR_LLAMA)
                consola.imprimir('A')
                consola.establecer_color_hex(color)
                consola.imprimir(linea[idx+1:])
                continue
        consola.establecer_color_hex(color)
        consola.imprimir(linea)

    consola.restaurar_colores()

# DIBUJO DEL TABLERO

def ancho_tablero(n, enc):
    return n * enc["ancho"] + (n - 1) * enc["sep_col"]

def alto_tablero(n, enc):
    return n * enc["alto"] + (n - 1) * enc["sep_fila"]

def col_celda(c, enc):
    return c * (enc["ancho"] + enc["sep_col"])

def fila_celda(f, enc):
    return f * (enc["alto"] + enc["sep_fila"])

def dibujar_tablero_completo(tablero, cur_f, cur_c, orig_fila, orig_col, enc, ayuda_fc=None):
    n = len(tablero)
    for f in range(n):
        for c in range(n):
            fp       = orig_fila + fila_celda(f, enc)
            cp       = orig_col  + col_celda(c, enc)
            es_ayuda = (ayuda_fc is not None and (f, c) == ayuda_fc)
            dibujar_encendedor(fp, cp, tablero[f][c],
                               f == cur_f and c == cur_c, enc, es_ayuda)

def redibujar_celdas(tablero, lista_fc, cur_f, cur_c, orig_fila, orig_col, enc, ayuda_fc=None):
    vistas = set()
    for f, c in lista_fc:
        if (f, c) in vistas:
            continue
        vistas.add((f, c))
        fp       = orig_fila + fila_celda(f, enc)
        cp       = orig_col  + col_celda(c, enc)
        es_ayuda = (ayuda_fc is not None and (f, c) == ayuda_fc)
        dibujar_encendedor(fp, cp, tablero[f][c],
                           f == cur_f and c == cur_c, enc, es_ayuda)

# ENCABEZADO, ESTADO Y BARRA DE BOTONES

BANNER = [
    "                                                                                    ",
    "  ██╗     ██╗ ██████╗ ██╗  ██╗████████╗███████╗     ██████╗ ██╗   ██╗████████╗  ",
    "  ██║     ██║██╔════╝ ██║  ██║╚══██╔══╝██╔════╝    ██╔═══██╗██║   ██║╚══██╔══╝  ",
    "  ██║     ██║██║  ███╗███████║   ██║   ███████╗    ██║   ██║██║   ██║   ██║      ",
    "  ██║     ██║██║   ██║██╔══██║   ██║   ╚════██║    ██║   ██║██║   ██║   ██║      ",
    "  ███████╗██║╚██████╔╝██║  ██║   ██║   ███████║    ╚██████╔╝╚██████╔╝   ██║      ",
    "  ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝     ╚═════╝  ╚═════╝    ╚═╝      ",
    "                                                                                    ",
    "  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ",
    "                                                                                    ",
]

def dibujar_encabezado_juego(nombre_dif, orig_fila, orig_col, n, enc):
    ancho  = ancho_tablero(n, enc)
    titulo = "[ LIGHTS OUT ]"
    pad    = max(0, (ancho - len(titulo)) // 2)
    consola.mover_cursor(orig_fila - 4, orig_col + pad)
    consola.establecer_color_hex(COLOR_TITULO)
    consola.imprimir(titulo)
    consola.mover_cursor(orig_fila - 3, orig_col)
    consola.establecer_color_hex(COLOR_SUBTITULO)
    consola.imprimir(f"Dificultad: {nombre_dif}")
    consola.restaurar_colores()

def actualizar_movimientos(movs, modo_ayuda, pendientes_count,
                           orig_fila, orig_col):
    consola.mover_cursor(orig_fila - 2, orig_col)
    consola.establecer_color_hex(COLOR_MOVS)
    consola.imprimir(f"Movimientos: {movs:<4}")
    if modo_ayuda:
        consola.establecer_color_hex(COLOR_AYUDA_IND)
        consola.imprimir(f"  [ AYUDA: {pendientes_count} restantes ]")
    else:
        consola.establecer_color_hex(COLOR_BARRA)
        consola.imprimir("                            ")
    consola.restaurar_colores()

def dibujar_barra_botones(orig_fila, orig_col, n, enc, modo_ayuda):
    col_panel = orig_col + ancho_tablero(n, enc) + 3

    botones_normal = [
        ("[Flechas]", "Mover cursor   "),
        ("[Enter]",   "Presionar celda"),
        ("[A]",       "Ayuda ON       "),
        ("[Q/ESC]",   "Volver al menu "),
    ]
    botones_ayuda = [
        ("[Flechas]", "Mover cursor   "),
        ("[Enter]",   "Presionar celda"),
        ("[A]",       "Ayuda OFF      "),
        ("[Q/ESC]",   "Volver al menu "),
    ]

    botones    = botones_ayuda if modo_ayuda else botones_normal
    # B=30: ║ + 9 tecla + 2 sep + 15 accion + 2 pad + ║ = 30
    B = 30
    I = B - 2

    alto_panel = 3 + len(botones) * 2
    fila_panel = orig_fila + max(0, (alto_tablero(n, enc) - alto_panel) // 2)

    def fila(f, s):
        consola.mover_cursor(f, col_panel)
        consola.establecer_color_hex(COLOR_BARRA)
        consola.imprimir(s)

    fila(fila_panel,     '╔' + '═'*I + '╗')
    fila(fila_panel + 1, '║')
    consola.establecer_color_hex(COLOR_TITULO)
    titulo = ' C O N T R O L E S '
    consola.imprimir(titulo.center(I))
    consola.establecer_color_hex(COLOR_BARRA)
    consola.imprimir('║')
    fila(fila_panel + 2, '╠' + '═'*I + '╣')

    for idx, (tecla, accion) in enumerate(botones):
        fl = fila_panel + 3 + idx * 2
        consola.mover_cursor(fl, col_panel)
        consola.establecer_color_hex(COLOR_BARRA)
        consola.imprimir('║ ')
        if modo_ayuda and '[A]' in tecla:
            consola.establecer_color_hex(COLOR_AYUDA_IND)
        else:
            consola.establecer_color_hex(COLOR_TITULO)
        consola.imprimir(f'{tecla:<9}')
        consola.establecer_color_hex(COLOR_BARRA)
        consola.imprimir(f'  {accion} ║')
        if idx < len(botones) - 1:
            fila(fl + 1, '╠' + '═'*I + '╣')
        else:
            fila(fl + 1, '╚' + '═'*I + '╝')

    consola.restaurar_colores()

# MENU PRINCIPAL

ANCHO_BANNER = len(BANNER[1])
ALTO_MENU    = 26

def _fila_ini_menu():
    return centrar_fila(ALTO_MENU)

def _fila_opcion(fila_ini, i):
    return fila_ini + 11 + i * 4

def _dibujar_opcion(fila_ini, i, seleccionada):
    nombre = NOMBRES[i]
    cfg    = DIFICULTADES[nombre]
    color  = COLOR_MENU_SEL if seleccionada else COLOR_MENU_NORM
    B      = 52        # ancho total del cuadro
    I      = B - 2     # interior
    flecha = '▶' if seleccionada else ' '
    detalle   = f"tablero {cfg['tamano']}x{cfg['tamano']}  ·  {cfg['pulsaciones']} pulsaciones"
    contenido = f"  {flecha}  {nombre:<10}  {detalle}"
    contenido = (contenido + ' ' * I)[:I]   # ajustar exactamente a I chars
    if seleccionada:
        borde_t = '╔' + '═'*I + '╗'
        borde_b = '╚' + '═'*I + '╝'
        interior_l, interior_r = '║', '║'
    else:
        borde_t = '┌' + '─'*I + '┐'
        borde_b = '└' + '─'*I + '┘'
        interior_l, interior_r = '│', '│'
    linea  = interior_l + contenido + interior_r
    fila_b = _fila_opcion(fila_ini, i)
    col_b  = centrar_col(B)
    consola.mover_cursor(fila_b,     col_b)
    consola.establecer_color_hex(color)
    consola.imprimir(borde_t)
    consola.mover_cursor(fila_b + 1, col_b)
    consola.imprimir(linea)
    consola.mover_cursor(fila_b + 2, col_b)
    consola.imprimir(borde_b)
    consola.restaurar_colores()

def dibujar_menu_completo(seleccion):
    consola.limpiar_pantalla()
    fila_ini = _fila_ini_menu()

    for i, linea in enumerate(BANNER):
        consola.mover_cursor(fila_ini + i, centrar_col(ANCHO_BANNER))
        consola.establecer_color_hex(COLOR_TITULO)
        consola.imprimir(linea)

    sep = "═" * ANCHO_BANNER
    consola.mover_cursor(fila_ini + 10, centrar_col(len(sep)))
    consola.establecer_color_hex(COLOR_BARRA)
    consola.imprimir(sep)

    sub = "───  Selecciona la dificultad  ───"
    consola.mover_cursor(fila_ini + 11, centrar_col(len(sub)))
    consola.establecer_color_hex(COLOR_SUBTITULO)
    consola.imprimir(sub)

    for i in range(len(NOMBRES)):
        _dibujar_opcion(fila_ini, i, i == seleccion)

    inst = "[Flechas]  Elegir   |   [Enter]  Confirmar   |   [Q]  Salir"
    consola.mover_cursor(fila_ini + 25, centrar_col(len(inst)))
    consola.establecer_color_hex(COLOR_TITULO)
    consola.imprimir("[Flechas]")
    consola.establecer_color_hex(COLOR_BARRA)
    consola.imprimir("  Elegir   |   ")
    consola.establecer_color_hex(COLOR_TITULO)
    consola.imprimir("[Enter]")
    consola.establecer_color_hex(COLOR_BARRA)
    consola.imprimir("  Confirmar   |   ")
    consola.establecer_color_hex(COLOR_TITULO)
    consola.imprimir("[Q]")
    consola.establecer_color_hex(COLOR_BARRA)
    consola.imprimir("  Salir")
    consola.restaurar_colores()

def bucle_menu():
    seleccion = 0
    dibujar_menu_completo(seleccion)
    fila_ini  = _fila_ini_menu()

    while True:
        cmd = teclado.esperar_tecla()
        if cmd is None:
            continue
        if cmd == teclado.SALIR:
            return None
        if cmd in (teclado.ARRIBA, teclado.FLECHA_ARRIBA):
            ant       = seleccion
            seleccion = (seleccion - 1) % len(NOMBRES)
            _dibujar_opcion(fila_ini, ant,       False)
            _dibujar_opcion(fila_ini, seleccion, True)
        elif cmd in (teclado.ABAJO, teclado.FLECHA_ABAJO):
            ant       = seleccion
            seleccion = (seleccion + 1) % len(NOMBRES)
            _dibujar_opcion(fila_ini, ant,       False)
            _dibujar_opcion(fila_ini, seleccion, True)
        elif cmd == teclado.ENTRAR:
            return NOMBRES[seleccion]
 
# PANTALLA DE VICTORIA 

def pantalla_victoria(movs):
    consola.limpiar_pantalla()
    I = 69  # ancho interior del cuadro

    def pc(s):  # pad center dentro del cuadro
        diff = I - len(s)
        l = diff // 2
        return '║' + ' '*l + s + ' '*(diff - l) + '║'

    lineas = [
        '╔' + '═'*I + '╗',
        pc(''),
        pc(' ██████╗   █████╗  ███╗  ██╗  █████╗  ███████╗ ████████╗ ███████╗'),
        pc('██╔════╝  ██╔══██╗ ████╗ ██║ ██╔══██╗ ██╔════╝ ╚══██╔══╝ ██╔════╝'),
        pc('██║  ███╗ ███████║ ██╔██╗██║ ███████║ ███████╗    ██║    █████╗  '),
        pc('██║   ██║ ██╔══██║ ██║╚████║ ██╔══██║ ╚════██║    ██║    ██╔══╝  '),
        pc('╚██████╔╝ ██║  ██║ ██║ ╚███║ ██║  ██║ ███████║    ██║    ███████╗'),
        pc(' ╚═════╝  ╚═╝  ╚═╝ ╚═╝  ╚══╝ ╚═╝  ╚═╝ ╚══════╝    ╚═╝    ╚══════╝'),
        pc(''),
        pc('·  ·  ·  ·  ·  ¡ A P A G A S T E   T O D O !  ·  ·  ·  ·  ·'),
        pc(''),
        '╠' + '═'*I + '╣',
        pc(''),
        pc(f'Movimientos realizados:   {movs}'),
        pc(''),
        pc('Presiona  [ ENTER ]  para volver al menu'),
        pc(''),
        '╚' + '═'*I + '╝',
    ]
    fila_ini = centrar_fila(len(lineas))
    for i, linea in enumerate(lineas):
        consola.mover_cursor(fila_ini + i, centrar_col(len(linea)))
        consola.establecer_color_hex(COLOR_VICTORIA)
        consola.imprimir(linea)
    consola.restaurar_colores()

# BUCLE DEL JUEGO 

def bucle_juego(nombre_dif):
    cfg     = DIFICULTADES[nombre_dif]
    enc     = ENCENDEDORES[nombre_dif]
    n       = cfg["tamano"]
    tablero, solucion_base = generar_tablero(n, cfg["pulsaciones"])
    cur_f   = n // 2
    cur_c   = n // 2
    movs    = 0

    alto_total  = alto_tablero(n, enc) + 5
    ancho_total = ancho_tablero(n, enc)
    orig_fila   = centrar_fila(alto_total) + 5
    orig_col    = centrar_col(ancho_total)

    modo_ayuda = False
    historial  = []

    def pendientes():
        conteo = Counter(solucion_base)
        for fc in historial:
            conteo[fc] += 1
        return [fc for fc, v in conteo.items() if v % 2 == 1]

    def celda_sugerida():
        if not modo_ayuda:
            return None
        p = pendientes()
        return p[0] if p else None

    consola.limpiar_pantalla()
    dibujar_encabezado_juego(nombre_dif, orig_fila, orig_col, n, enc)
    actualizar_movimientos(movs, False, 0, orig_fila, orig_col)
    dibujar_tablero_completo(tablero, cur_f, cur_c, orig_fila, orig_col, enc)
    dibujar_barra_botones(orig_fila, orig_col, n, enc, False)

    while True:
        cmd = teclado.esperar_tecla()
        if cmd is None:
            continue

        if cmd == teclado.SALIR:
            return True

        fila_ant, col_ant = cur_f, cur_c
        sugerida_ant = celda_sugerida()

        if cmd in ("a", "A"):
            modo_ayuda = not modo_ayuda
            if modo_ayuda and not pendientes():
                modo_ayuda = False
            p = pendientes() if modo_ayuda else []
            dibujar_tablero_completo(tablero, cur_f, cur_c,
                                     orig_fila, orig_col, enc, celda_sugerida())
            actualizar_movimientos(movs, modo_ayuda, len(p), orig_fila, orig_col)
            dibujar_barra_botones(orig_fila, orig_col, n, enc, modo_ayuda)
            continue

        if cmd in (teclado.ARRIBA, teclado.FLECHA_ARRIBA):
            cur_f = max(0, cur_f - 1)
        elif cmd in (teclado.ABAJO, teclado.FLECHA_ABAJO):
            cur_f = min(n - 1, cur_f + 1)
        elif cmd in (teclado.DERECHA, teclado.FLECHA_DERECHA):
            cur_c = min(n - 1, cur_c + 1)
        elif cmd in (teclado.IZQUIERDA, teclado.FLECHA_IZQUIERDA):
            cur_c = max(0, cur_c - 1)

        elif cmd == teclado.ENTRAR:
            afectadas = celdas_afectadas(tablero, cur_f, cur_c)
            pulsar(tablero, cur_f, cur_c)
            movs += 1
            historial.append((cur_f, cur_c))

            p = pendientes()
            if modo_ayuda and not p:
                modo_ayuda = False

            sugerida_nueva = celda_sugerida()
            todas = set(afectadas)
            if sugerida_ant is not None:
                todas.add(sugerida_ant)
            if sugerida_nueva is not None:
                todas.add(sugerida_nueva)
            redibujar_celdas(tablero, list(todas), cur_f, cur_c,
                             orig_fila, orig_col, enc, sugerida_nueva)
            actualizar_movimientos(movs, modo_ayuda, len(p), orig_fila, orig_col)
            if modo_ayuda:
                dibujar_barra_botones(orig_fila, orig_col, n, enc, modo_ayuda)

            if es_victoria(tablero):
                pantalla_victoria(movs)
                while True:
                    cmd2 = teclado.esperar_tecla()
                    if cmd2 in (teclado.ENTRAR, teclado.SALIR):
                        break
                return True

        if cur_f != fila_ant or cur_c != col_ant:
            sugerida_nueva = celda_sugerida()
            todas = {(fila_ant, col_ant), (cur_f, cur_c)}
            if sugerida_ant is not None:
                todas.add(sugerida_ant)
            if sugerida_nueva is not None:
                todas.add(sugerida_nueva)
            redibujar_celdas(tablero, list(todas), cur_f, cur_c,
                             orig_fila, orig_col, enc, sugerida_nueva)

# PUNTO DE ENTRADA

def main():
    os.system("")
    consola.ocultar_cursor()

    try:
        while True:
            dificultad = bucle_menu()
            if dificultad is None:
                break
            bucle_juego(dificultad)
    finally:
        teclado.limpiar()
        consola.restaurar_colores()
        consola.mostrar_cursor()
        consola.limpiar_pantalla()
        consola.mover_cursor(1, 1)
        print("Hasta luego!")

if __name__ == "__main__":
    main()
