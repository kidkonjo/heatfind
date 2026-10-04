#!/usr/bin/env python3
import os
import sys
import time
import argparse
from pathlib import Path

# Archivo con el ASCII Art de la huella
LOGO_FILE = "heat_print.txt"

# ASCII Art de respaldo si no existe heat_print.txt
FALLBACK_LOGO = [
    "                :::              ",
    " .   ...   ::-::::---==-         ",
    "        :::-::=:+::::+=:==:      ",
    "       ::::=:--+-+++-+--===-.    ",
    "     :--+:+=+-=+---:=+=+:++==:   ",
    "    :--:-=*-*+-===-=-=---=====:  ",
    "   :::::----+--=+=+===-=-+-=+=-  ",
    "   -:-::+---===++##*++=*==+==+== ",
    "  ::---+--=--+#=*++#*+*=+:-++=++ ",
    "  ::--=+=+-*=#=**+*=%%=+++=:=--::",
    "  -----===---=+%++#+++#+++::+===-",
    " .-=:-=------===+++++++++=++=+++-",
    " :----=-==-==+=+==+++-=*-+++==-+=",
    " :--:--:--=---======----+:--+=-+-",
    " -:--:-=--=-=--=--=--=--+=+-==:-:",
    " ----:--==---==-=-----===-+===---",
    ".::-------:---:--=::--=+==-======",
    " :::-----:---------=======+====-: ",
    " :::::--------------=+==--==-:-- "
]

# --- CÓDIGOS DE COLOR ANSI ---
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[90m"

# Paleta de la huella
COLOR_CENTER = "\033[38;5;229m"
COLOR_LVL1   = "\033[38;5;220m"
COLOR_LVL2   = "\033[38;5;208m"
COLOR_LVL3   = "\033[38;5;196m"
COLOR_LVL4   = "\033[38;5;166m"
COLOR_LVL5   = "\033[38;5;36m"
COLOR_LVL6   = "\033[38;5;31m"
COLOR_EDGE   = "\033[38;5;24m"

# Paleta Estándar de antigüedad
COLOR_WHITE  = "\033[1;37m"
COLOR_RED    = "\033[38;5;196m"
COLOR_ORANGE = "\033[38;5;208m"
COLOR_YELLOW = "\033[38;5;220m"
COLOR_GREEN  = "\033[38;5;36m"
COLOR_BLUE   = "\033[38;5;33m"

# Paleta MODO DALTÓNICO
CB_WHITE   = "\033[1;37m"
CB_CYAN    = "\033[38;5;51m"
CB_YELLOW  = "\033[38;5;226m"
CB_MAGENTA = "\033[38;5;201m"
CB_BLUE    = "\033[38;5;33m"
CB_GRAY    = "\033[38;5;245m"


def get_logo_lines():
    """Lee el archivo de la huella o usa el de respaldo."""
    if os.path.exists(LOGO_FILE):
        with open(LOGO_FILE, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\r\n") for line in f.readlines()]
            if lines:
                return lines
    return FALLBACK_LOGO


def render_header(colorblind=False):
    """Dibuja la huella a la izquierda y la leyenda a la derecha (Solo al pedir ayuda sin argumentos)."""
    logo_lines = get_logo_lines()

    if colorblind:
        legend_lines = [
            "",
            f"{BOLD}=== LEYENDA (MODO DALTÓNICO) ==={RESET}",
            f" {CB_WHITE}██{RESET} [MUY NUEVO]  < 5 min",
            f" {CB_CYAN}██{RESET} [NUEVO]      5 min - 1 hora",
            f" {CB_YELLOW}██{RESET} [RECIENTE]   1h - 24 horas",
            f" {CB_MAGENTA}██{RESET} [MEDIO]      1d - 7d",
            f" {CB_BLUE}██{RESET} [ANTIGUO]    7d - 30d",
            f" {CB_GRAY}██{RESET} [MUY VIEJO]  > 30d",
        ]
    else:
        legend_lines = [
            "",
            f"{BOLD}=== LEYENDA DE ANTIGÜEDAD ==={RESET}",
            f" {COLOR_WHITE}██{RESET} Muy muy reciente (< 5 min)",
            f" {COLOR_RED}██{RESET} Muy reciente (5 min - 1 hora)",
            f" {COLOR_ORANGE}██{RESET} Reciente (1h - 24 horas)",
            f" {COLOR_YELLOW}██{RESET} Hace un poco de tiempo (1d - 7d)",
            f" {COLOR_GREEN}██{RESET} Ha pasado un tiempo (7d - 30d)",
            f" {COLOR_BLUE}██{RESET} Ha pasado bastante tiempo (> 30d)",
        ]

    num_rows = max(len(logo_lines), len(legend_lines))
    max_cols = max((len(line) for line in logo_lines), default=0)
    center_y = (len(logo_lines) - 1) / 2 if logo_lines else 0
    center_x = (max_cols - 1) / 2 if max_cols > 0 else 0

    for y in range(num_rows):
        if y < len(logo_lines):
            line = logo_lines[y]
            line_str = []
            for x, char in enumerate(line):
                if char == " ":
                    line_str.append(" ")
                    continue

                dy = y - center_y
                dx = x - center_x
                dist_sq = dy * dy + (dx * 10 / 18) ** 2

                if dist_sq <= 4:      color = COLOR_CENTER
                elif dist_sq <= 16:   color = COLOR_LVL1
                elif dist_sq <= 36:   color = COLOR_LVL2
                elif dist_sq <= 64:   color = COLOR_LVL3
                elif dist_sq <= 100:  color = COLOR_LVL4
                elif dist_sq <= 144:  color = COLOR_LVL5
                elif dist_sq <= 200:  color = COLOR_LVL6
                else:                 color = COLOR_EDGE

                line_str.append(f"{color}{char}{RESET}")

            padding = " " * (max_cols - len(line) + 4)
            print("".join(line_str) + padding, end="")
        else:
            print(" " * (max_cols + 4), end="")

        if y < len(legend_lines):
            print(legend_lines[y])
        else:
            print()
    print()


def format_time_ago(diff_seconds):
    """Devuelve la cadena de tiempo transcurrido."""
    days = int(diff_seconds // 86400)
    hours = int((diff_seconds % 86400) // 3600)
    mins = int((diff_seconds % 3600) // 60)
    secs = int(diff_seconds % 60)

    parts = []
    if days > 0: parts.append(f"{days}d")
    if hours > 0: parts.append(f"{hours}h")
    if mins > 0: parts.append(f"{mins}m")
    parts.append(f"{secs}s")
    return " ".join(parts)


def get_file_style(diff_seconds, colorblind=False):
    """Devuelve tupla (color, etiqueta) según antigüedad y modo."""
    if colorblind:
        if diff_seconds < 300:        return CB_WHITE, "[MUY NUEVO] "
        elif diff_seconds < 3600:     return CB_CYAN, "[NUEVO]     "
        elif diff_seconds < 86400:    return CB_YELLOW, "[RECIENTE]  "
        elif diff_seconds < 604800:   return CB_MAGENTA, "[MEDIO]     "
        elif diff_seconds < 2592000:  return CB_BLUE, "[ANTIGUO]   "
        else:                         return CB_GRAY, "[MUY VIEJO] "
    else:
        if diff_seconds < 300:        return COLOR_WHITE, ""
        elif diff_seconds < 3600:     return COLOR_RED, ""
        elif diff_seconds < 86400:    return COLOR_ORANGE, ""
        elif diff_seconds < 604800:   return COLOR_YELLOW, ""
        elif diff_seconds < 2592000:  return COLOR_GREEN, ""
        else:                         return COLOR_BLUE, ""


def evaluate_and_print(item_path, now, max_mins, min_mins, pattern, is_dir=False, colorblind=False, use_atime=False):
    """Evalúa e imprime el elemento considerando tiempos de modificación, creación y acceso (atime)."""
    if pattern and not item_path.match(pattern):
        return

    try:
        stat_info = item_path.stat()
        mtime = stat_info.st_mtime
        ctime = getattr(stat_info, 'st_ctime', mtime)
        atime = stat_info.st_atime
        
        # Si se especifica la opción de acceso estricto (-a), usar atime; de lo contrario, el más reciente entre todos.
        if use_atime:
            last_change = atime
        else:
            last_change = max(mtime, ctime, atime)

        diff = now - last_change
        diff_mins = diff / 60

        if max_mins is not None and diff_mins > max_mins:
            return
        if min_mins is not None and diff_mins < min_mins:
            return

        color, tag = get_file_style(diff, colorblind=colorblind)
        time_ago = format_time_ago(diff)
        prefix = f"{BOLD}[DIR]{RESET} " if is_dir else ""
        
        print(f"{prefix}{color}{tag}{item_path}{RESET} {DIM}(hace {time_ago}){RESET}")

    except (PermissionError, FileNotFoundError):
        pass


def search_files_and_dirs(directory, max_mins=None, min_mins=None, pattern=None, max_depth=3, colorblind=False, use_atime=False):
    """Realiza la búsqueda de archivos y directorios."""
    now = time.time()
    base_path = Path(directory)

    if not base_path.exists():
        print(f"Error: El directorio '{directory}' no existe.")
        return

    mode_label = "Último acceso (atime)" if use_atime else "Modificación / Creación / Acceso"
    print(f"\033[1;34m[+] Búsqueda en:\033[0m {base_path.resolve()} \033[90m[{mode_label}]\033[0m")
    print("\033[1;30m--------------------------------------------------------\033[0m")

    for root, dirs, files in os.walk(base_path):
        rel_path = Path(root).relative_to(base_path)
        depth = len(rel_path.parts)
        if depth >= max_depth:
            dirs.clear()

        for d in list(dirs):
            dir_path = Path(root) / d
            evaluate_and_print(dir_path, now, max_mins, min_mins, pattern, is_dir=True, colorblind=colorblind, use_atime=use_atime)

        for f in files:
            file_path = Path(root) / f
            evaluate_and_print(file_path, now, max_mins, min_mins, pattern, is_dir=False, colorblind=colorblind, use_atime=use_atime)


def main():
    parser = argparse.ArgumentParser(
        description="Buscador térmico de archivos y directorios.",
        add_help=False
    )
    parser.add_argument("directory", nargs="?", default=".", help="Directorio donde buscar")
    parser.add_argument("-r", "--recent", action="store_true", help="Modificados/creados/leídos en los últimos 5 minutos")
    parser.add_argument("-t", "--today", action="store_true", help="Modificados/creados/leídos en las últimas 24 horas")
    parser.add_argument("-a", "--access", action="store_true", help="Filtrar estrictamente por fecha de último acceso/lectura (atime)")
    parser.add_argument("--days", type=float, help="Modificados/creados/leídos en los últimos N días")
    parser.add_argument("--mmin", type=str, help="Filtro en minutos (-N: hace menos de N min, +N: hace más de N min)")
    parser.add_argument("--name", type=str, help="Filtrar por nombre (ej: '*.py')")
    parser.add_argument("--cb", "--colorblind", action="store_true", help="Activar modo accesible para daltónicos")
    parser.add_argument("-h", "--help", action="store_true", help="Muestra este mensaje de ayuda")

    # SI NO SE LE PASA NINGÚN ARGUMENTO/FLAG: Se dibuja el logo y salta la ayuda por defecto
    if len(sys.argv) == 1:
        render_header(colorblind=False)
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    # Si pide la ayuda explícitamente (-h/--help)
    if args.help:
        render_header(colorblind=args.cb)
        parser.print_help()
        sys.exit(0)

    max_mins = None
    min_mins = None

    if args.recent:
        max_mins = 5
    elif args.today:
        max_mins = 1440
    elif args.days:
        max_mins = args.days * 1440

    if args.mmin:
        if args.mmin.startswith("-"):
            max_mins = float(args.mmin[1:])
        elif args.mmin.startswith("+"):
            min_mins = float(args.mmin[1:])

    # Búsqueda limpia sin dibujar la huella
    search_files_and_dirs(
        args.directory,
        max_mins=max_mins,
        min_mins=min_mins,
        pattern=args.name,
        colorblind=args.cb,
        use_atime=args.access
    )


if __name__ == "__main__":
    main()