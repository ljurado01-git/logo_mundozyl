"""Ronda 2 de propuestas MUNDOZYL: sin globo, foco en solidez y confianza.

Uso:
    pip install fonttools cairosvg
    python3 herramientas/generar_logos_ronda2.py
"""
import os

from generar_logos import (
    AZUL_CIELO,
    AZUL_PROFUNDO,
    AZUL_ZYL,
    BLANCO,
    RAIZ,
    guardar,
    svg_doc,
    texto,
)

DIR_SALIDA = os.path.join(RAIZ, "propuestas", "ronda2")


def colores(negativo):
    """cont: contenedor del símbolo, hueco: la Z, acento: detalle azul."""
    if negativo:
        return dict(cont=BLANCO, hueco=AZUL_PROFUNDO, acento=AZUL_CIELO,
                    t1=BLANCO, t2=AZUL_CIELO, fondo=AZUL_PROFUNDO)
    return dict(cont=AZUL_PROFUNDO, hueco=BLANCO, acento=AZUL_ZYL,
                t1=AZUL_PROFUNDO, t2=AZUL_ZYL, fondo=BLANCO)


def zeta(x0, y0, w, h, t, color):
    """Z geométrica de trazo uniforme `t` dentro de la caja (x0, y0, w, h)."""
    x1, y1 = x0 + w, y0 + h
    # ancho horizontal de la diagonal para que su grosor perpendicular sea t
    d = t * 1.5
    for _ in range(8):
        dx, dy = w - d, h - 2 * t
        d = t * (dx * dx + dy * dy) ** 0.5 / dy
    pts = [(x0, y0), (x1, y0), (x1, y0 + t), (x0 + d, y1 - t), (x1, y1 - t),
           (x1, y1), (x0, y1), (x0, y1 - t), (x1 - d, y0 + t), (x0, y0 + t)]
    return f'<polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" fill="{color}"/>'


# ------------------------------------------------- D · Bloque
# Bloque sólido con la Z calada y una esquina "sellada" en azul:
# estabilidad, producto empaquetado, garantía.


def icono_bloque(cx, cy, s, c):
    x, y = cx - s / 2, cy - s / 2
    R, k, g = s * 0.16, s * 0.30, s * 0.075
    cuerpo = (
        f'<path d="M{x + R:.2f},{y:.2f}H{x + s - R:.2f}A{R:.2f},{R:.2f} 0 0 1 {x + s:.2f},{y + R:.2f}'
        f'V{y + s - k:.2f}L{x + s - k:.2f},{y + s:.2f}H{x + R:.2f}'
        f'A{R:.2f},{R:.2f} 0 0 1 {x:.2f},{y + s - R:.2f}V{y + R:.2f}A{R:.2f},{R:.2f} 0 0 1 {x + R:.2f},{y:.2f}Z" '
        f'fill="{c["cont"]}"/>'
    )
    e = g * 1.414
    esquina = (
        f'<polygon points="{x + s:.2f},{y + s - k + e:.2f} {x + s:.2f},{y + s:.2f} {x + s - k + e:.2f},{y + s:.2f}" '
        f'fill="{c["acento"]}"/>'
    )
    z = zeta(x + s * 0.22, y + s * 0.22, s * 0.52, s * 0.52, s * 0.14, c["hueco"])
    return cuerpo + esquina + z


# ------------------------------------------------- E · Píxel
# Z formada por 10 bloques en retícula 4x4: hardware, datos, módulos.


def icono_pixel(cx, cy, s, c):
    x, y = cx - s / 2, cy - s / 2
    gap = s * 0.06
    b = (s - 3 * gap) / 4
    celdas = [(0, i) for i in range(4)] + [(3, i) for i in range(4)]
    diag = [(1, 2), (2, 1)]
    out = []
    for (fila, col), color in [(rc, c["cont"]) for rc in celdas] + [(rc, c["acento"]) for rc in diag]:
        out.append(
            f'<rect x="{x + col * (b + gap):.2f}" y="{y + fila * (b + gap):.2f}" width="{b:.2f}" height="{b:.2f}" '
            f'rx="{b * 0.12:.2f}" fill="{color}"/>'
        )
    return "".join(out)


# ------------------------------------------------- F · Hexágono
# Hexágono (tuerca / chip / estructura) partido en dos tonos con la Z calada:
# ingeniería, robustez, precisión.


def icono_hex(cx, cy, s, c):
    r = s / 2
    w = r * 0.866
    izq = [(cx, cy - r), (cx, cy + r), (cx - w, cy + r / 2), (cx - w, cy - r / 2)]
    der = [(cx, cy - r), (cx + w, cy - r / 2), (cx + w, cy + r / 2), (cx, cy + r)]
    pol = lambda pts, col: f'<polygon points="{" ".join(f"{a:.2f},{b:.2f}" for a, b in pts)}" fill="{col}"/>'
    zw, zh = s * 0.46, s * 0.44
    return pol(izq, c["cont"]) + pol(der, c["acento"]) + zeta(cx - zw / 2, cy - zh / 2, zw, zh, s * 0.12, c["hueco"])


# ------------------------------------------------- G · Escudo
# Escudo con banda superior y Z: protección, respaldo, garantía
# (refuerza seguridad, UPS y servicio técnico).


def icono_escudo(cx, cy, s, c):
    h, w = s, s * 0.84
    x0, x1, y0 = cx - w / 2, cx + w / 2, cy - h / 2
    forma = (
        f"M{x0:.2f},{y0:.2f}H{x1:.2f}V{y0 + 0.52 * h:.2f}"
        f"C{x1:.2f},{y0 + 0.80 * h:.2f} {cx + 0.14 * w:.2f},{y0 + 0.92 * h:.2f} {cx:.2f},{y0 + h:.2f}"
        f"C{cx - 0.14 * w:.2f},{y0 + 0.92 * h:.2f} {x0:.2f},{y0 + 0.80 * h:.2f} {x0:.2f},{y0 + 0.52 * h:.2f}Z"
    )
    cid = f"esc{int(cx)}{int(cy)}{int(s)}"
    banda = 0.17 * h
    sep = 0.05 * h
    return (
        f'<defs><clipPath id="{cid}"><path d="{forma}"/></clipPath></defs>'
        f'<g clip-path="url(#{cid})">'
        f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{w:.2f}" height="{banda:.2f}" fill="{c["acento"]}"/>'
        f'<rect x="{x0:.2f}" y="{y0 + banda + sep:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{c["cont"]}"/>'
        f"</g>"
        + zeta(cx - w * 0.29, y0 + banda + sep + h * 0.11, w * 0.58, h * 0.40, h * 0.10, c["hueco"])
    )


PROPUESTAS = {
    "D_bloque": dict(icono=icono_bloque, fuente=("archivo", {"wght": 800, "wdth": 125}), tracking=0.01),
    "E_pixel": dict(icono=icono_pixel, fuente=("redhatdisplay", 900), tracking=0.01),
    "F_hexagono": dict(icono=icono_hex, fuente=("saira", {"wght": 700, "wdth": 112}), tracking=0.05),
    "G_escudo": dict(icono=icono_escudo, fuente=("archivo", {"wght": 900, "wdth": 100}), tracking=0.03),
}


def wordmark(clave, x, y_base, cap, c):
    fn, peso = PROPUESTAS[clave]["fuente"]
    tr = PROPUESTAS[clave]["tracking"]
    d1, w1 = texto(fn, peso, "MUNDO", cap, x, y_base, tr)
    sep = cap * tr * 1.4 + cap * 0.03
    d2, w2 = texto(fn, peso, "ZYL", cap, x + w1 + sep, y_base, tr)
    return f'<path d="{d1}" fill="{c["t1"]}"/><path d="{d2}" fill="{c["t2"]}"/>', w1 + sep + w2


def horizontal(clave, negativo=False):
    c = colores(negativo)
    cap, m = 100, 60
    s = cap * 1.55
    cx, cy = m + s / 2, m + s / 2
    ic = PROPUESTAS[clave]["icono"](cx, cy, s, c)
    x = m + s + cap * 0.5
    wm, w = wordmark(clave, x, cy + cap / 2, cap, c)
    return svg_doc(x + w + m, s + 2 * m, ic + wm, c["fondo"] if negativo else None)


def vertical(clave, negativo=False):
    c = colores(negativo)
    cap, m, s = 64, 60, 210
    _, w = wordmark(clave, 0, 0, cap, c)
    ancho = max(s, w) + 2 * m
    cx, cy = ancho / 2, m + s / 2
    ic = PROPUESTAS[clave]["icono"](cx, cy, s, c)
    yb = m + s + cap * 0.75 + cap
    wm, _ = wordmark(clave, cx - w / 2, yb, cap, c)
    return svg_doc(ancho, yb + m, ic + wm, c["fondo"] if negativo else None)


def icono_app(clave):
    lado = 512
    c = colores(True)
    return svg_doc(lado, lado, f'<rect width="{lado}" height="{lado}" fill="{c["fondo"]}"/>'
                   + PROPUESTAS[clave]["icono"](lado / 2, lado / 2, 300, c))


def main():
    for clave in PROPUESTAS:
        guardar(f"{clave}/{clave}_horizontal", horizontal(clave), DIR_SALIDA)
        guardar(f"{clave}/{clave}_horizontal_negativo", horizontal(clave, True), DIR_SALIDA)
        guardar(f"{clave}/{clave}_vertical", vertical(clave), DIR_SALIDA)
        guardar(f"{clave}/{clave}_vertical_negativo", vertical(clave, True), DIR_SALIDA)
        guardar(f"{clave}/{clave}_icono", icono_app(clave), DIR_SALIDA)
    print("Listo:", DIR_SALIDA)


if __name__ == "__main__":
    main()
