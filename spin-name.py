#!/usr/bin/env python3
import getpass
import json
import math
import os
import re
import signal
import sys
import time

# Config directory and file paths
CONFIG_DIR = os.path.expanduser("~/.config/spin-name")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

# 5x5 ASCII font matrix
FONT = {
    'A': [" ### ", "#   #", "#####", "#   #", "#   #"],
    'B': ["#### ", "#   #", "#### ", "#   #", "#### "],
    'C': [" ####", "#    ", "#    ", "#    ", " ####"],
    'D': ["#### ", "#   #", "#   #", "#   #", "#### "],
    'E': ["#####", "#    ", "#### ", "#    ", "#####"],
    'F': ["#####", "#    ", "#### ", "#    ", "#    "],
    'G': [" ####", "#    ", "# ###", "#   #", " ####"],
    'H': ["#   #", "#   #", "#####", "#   #", "#   #"],
    'I': [" ### ", "  #  ", "  #  ", "  #  ", " ### "],
    'J': ["  ###", "   # ", "   # ", "#  # ", " ##  "],
    'K': ["#  # ", "# #  ", "##   ", "# #  ", "#  # "],
    'L': ["#    ", "#    ", "#    ", "#    ", "#####"],
    'M': ["#   #", "## ##", "# # #", "#   #", "#   #"],
    'N': ["#   #", "##  #", "# # #", "#  ##", "#   #"],
    'O': [" ### ", "#   #", "#   #", "#   #", " ### "],
    'P': ["#### ", "#   #", "#### ", "#    ", "#    "],
    'Q': [" ### ", "#   #", "# # #", "#  ##", " ####"],
    'R': ["#### ", "#   #", "#### ", "# #  ", "#  # "],
    'S': [" ####", "#    ", " ### ", "    #", "#### "],
    'T': ["#####", "  #  ", "  #  ", "  #  ", "  #  "],
    'U': ["#   #", "#   #", "#   #", "#   #", " ### "],
    'V': ["#   #", "#   #", "#   #", " # # ", "  #  "],
    'W': ["#   #", "#   #", "# # #", "## ##", "#   #"],
    'X': ["#   #", " # # ", "  #  ", " # # ", "#   #"],
    'Y': ["#   #", " # # ", "  #  ", "  #  ", "  #  "],
    'Z': ["#####", "   # ", "  #  ", " #   ", "#####"],
    '0': [" ### ", "#  ##", "# # #", "##  #", " ### "],
    '1': ["  #  ", " ##  ", "  #  ", "  #  ", " ### "],
    '2': [" ### ", "    #", " ### ", "#    ", "#####"],
    '3': ["#### ", "    #", " ### ", "    #", "#### "],
    '4': ["#  # ", "#  # ", "#####", "   # ", "   # "],
    '5': ["#####", "#    ", "#### ", "    #", "#### "],
    '6': [" ### ", "#    ", "#### ", "#   #", " ### "],
    '7': ["#####", "   # ", "  #  ", " #   ", " #   "],
    '8': [" ### ", "#   #", " ### ", "#   #", " ### "],
    '9': [" ### ", "#   #", " ####", "    #", " ### "],
    ' ': ["     ", "     ", "     ", "     ", "     "],
    '-': ["     ", "     ", " ### ", "     ", "     "],
    '_': ["     ", "     ", "     ", "     ", "#####"],
    '.': ["     ", "     ", "     ", "     ", "  #  "],
    '*': ["     ", " # # ", "  #  ", " # # ", "     "],
    '|': ["  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
}

# Color palettes
COLOR_THEMES = {
    "arch_cyan":   {"back": [15, 30, 80],    "front": [110, 235, 255]},
    "matrix":      {"back": [0, 40, 10],     "front": [50, 255, 90]},
    "synthwave":   {"back": [60, 0, 80],     "front": [255, 70, 200]},
    "fire":        {"back": [70, 10, 0],     "front": [255, 215, 30]},
    "monochrome":  {"back": [45, 45, 45],    "front": [250, 250, 250]},
}

DEFAULT_CONFIG = {
    "texts": [],
    "repeats": 0,
    "separator": " * ",
    "speed": 0.015,
    "direction": "left-to-right",
    "letter_orientation": "default",
    "theme": "arch_cyan",
    "custom_colors": {
        "back": [20, 30, 80],
        "front": [0, 255, 240]
    },
    "wobble": True,
    "tilt_angle": 0.25,
    "radius": 16.0,
    "fps": 35
}

def strip_comments(text):
    text = re.sub(r'//.*', '', text)
    text = re.sub(r'#.*', '', text)
    return text

def load_or_create_config():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)
    
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            raw = f.read()
            cleaned = strip_comments(raw)
            cfg = json.loads(cleaned)
            res = DEFAULT_CONFIG.copy()
            res.update(cfg)
            return res
    except Exception:
        return DEFAULT_CONFIG.copy()

def restore_cursor(*args):
    sys.stdout.write("\033[?25h\033[0m\n")
    sys.stdout.flush()
    sys.exit(0)

signal.signal(signal.SIGINT, restore_cursor)
signal.signal(signal.SIGTERM, restore_cursor)

def rasterize_banner(cfg):
    texts = cfg.get("texts", [])
    if not texts:
        texts = [getpass.getuser().upper()]
    else:
        texts = [str(t).upper() for t in texts]

    sep = cfg.get("separator", " * ")
    joined = sep.join(texts) + sep

    repeats = int(cfg.get("repeats", 0))
    banner = joined
    if repeats > 1:
        banner = joined * repeats
    else:
        while len(banner) < 20:
            banner += joined

    points = []
    col_offset = 0
    substep = 0.4

    for ch in banner:
        glyph = FONT.get(ch, FONT.get(' ', ["     "] * 5))
        for r in range(5):
            for c in range(5):
                if glyph[r][c] == '#':
                    dr = 0.0
                    while dr < 1.0:
                        dc = 0.0
                        while dc < 1.0:
                            points.append((col_offset + c + dc, r + dr))
                            dc += substep
                        dr += substep
        col_offset += 6

    return points, col_offset

def main():
    cfg = load_or_create_config()
    last_mtime = 0
    try:
        last_mtime = os.path.getmtime(CONFIG_PATH)
    except Exception:
        pass

    bitmap_points, total_cols = rasterize_banner(cfg)

    # Hide cursor and clear terminal
    sys.stdout.write("\033[?25l\033[2J")
    sys.stdout.flush()

    angle_y = 0.0
    wobble_time = 0.0
    shades = ".:-=+*#%@"
    last_cfg_check = 0.0

    try:
        while True:
            t0 = time.time()

            # Hot-reload configuration every 0.4s
            if t0 - last_cfg_check > 0.4:
                last_cfg_check = t0
                try:
                    mtime = os.path.getmtime(CONFIG_PATH)
                    if mtime != last_mtime:
                        last_mtime = mtime
                        new_cfg = load_or_create_config()
                        if (new_cfg.get("texts") != cfg.get("texts") or 
                            new_cfg.get("repeats") != cfg.get("repeats") or
                            new_cfg.get("separator") != cfg.get("separator")):
                            bitmap_points, total_cols = rasterize_banner(new_cfg)
                        cfg = new_cfg
                except Exception:
                    pass

            speed = float(cfg.get("speed", 0.015))
            direction_str = str(cfg.get("direction", "left-to-right")).strip().lower()
            dir_mult = 1.0 if "right-to-left" in direction_str or "rtl" in direction_str else -1.0

            orientation = str(cfg.get("letter_orientation", "default")).strip().lower()
            invert_letters = (orientation == "inverted")

            wobble = cfg.get("wobble", True)
            tilt_angle = float(cfg.get("tilt_angle", 0.25))
            radius = float(cfg.get("radius", 16.0))
            fps = max(10, min(60, int(cfg.get("fps", 35))))

            theme = cfg.get("theme", "arch_cyan")
            if theme in COLOR_THEMES:
                c_back = COLOR_THEMES[theme]["back"]
                c_front = COLOR_THEMES[theme]["front"]
            else:
                cust = cfg.get("custom_colors", {})
                c_back = cust.get("back", [20, 30, 80])
                c_front = cust.get("front", [0, 255, 240])

            cols, rows = os.get_terminal_size()
            zbuffer = [[-1e9] * cols for _ in range(rows)]
            frame = [[' '] * cols for _ in range(rows)]
            colors = [[''] * cols for _ in range(rows)]

            # Wobble / floating motion
            if wobble:
                tilt_x = tilt_angle + 0.08 * math.sin(wobble_time * 0.7)
                roll_z = 0.04 * math.cos(wobble_time * 0.5)
            else:
                tilt_x = tilt_angle
                roll_z = 0.0

            cos_tx, sin_tx = math.cos(tilt_x), math.sin(tilt_x)
            cos_rz, sin_rz = math.cos(roll_z), math.sin(roll_z)

            cam_dist = radius * 2.3
            k_persp = 33.0

            for u, v in bitmap_points:
                # Radial mapping
                if invert_letters:
                    phi = -(2.0 * math.pi * (u / total_cols)) + angle_y
                else:
                    phi = (2.0 * math.pi * (u / total_cols)) + angle_y

                x = radius * math.sin(phi)
                z = radius * math.cos(phi)
                y = (v - 2.0) * 1.5

                # Pitch
                y1 = y * cos_tx - z * sin_tx
                z1 = y * sin_tx + z * cos_tx
                x1 = x

                # Roll
                x_final = x1 * cos_rz - y1 * sin_rz
                y_final = x1 * sin_rz + y1 * cos_rz
                z_final = z1

                # Distance to viewer
                dist = cam_dist - z_final
                ooz = 1.0 / dist

                xp = int(cols / 2 + (x_final * k_persp / dist))
                yp = int(rows / 2 + (y_final * (k_persp * 0.55) / dist))

                if 0 <= xp < cols and 0 <= yp < rows:
                    if ooz > zbuffer[yp][xp]:
                        zbuffer[yp][xp] = ooz

                        # Depth normalized
                        d = (z_final + radius) / (2.0 * radius)
                        d = max(0.0, min(1.0, d))

                        char_idx = int(d * (len(shades) - 1))
                        frame[yp][xp] = shades[char_idx]

                        r_c = int(c_back[0] + (c_front[0] - c_back[0]) * d)
                        g_c = int(c_back[1] + (c_front[1] - c_back[1]) * d)
                        b_c = int(c_back[2] + (c_front[2] - c_back[2]) * d)
                        colors[yp][xp] = f"\033[38;2;{r_c};{g_c};{b_c}m"

            # Double-buffered flicker-free rendering
            out = ["\033[H"]
            cur_col = ""
            for r in range(rows):
                line = []
                for c in range(cols):
                    if frame[r][c] != ' ':
                        col = colors[r][c]
                        if col != cur_col:
                            line.append(col)
                            cur_col = col
                        line.append(frame[r][c])
                    else:
                        line.append(' ')
                out.append("".join(line))

            out.append("\033[0m")
            sys.stdout.write("\n".join(out))
            sys.stdout.flush()

            angle_y += speed * dir_mult
            wobble_time += speed

            dt = time.time() - t0
            sleep_time = (1.0 / fps) - dt
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        restore_cursor()

if __name__ == '__main__':
    main()