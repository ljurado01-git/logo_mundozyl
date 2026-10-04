"""Ronda 3: monograma "M" plegado (a partir de la referencia del cliente).

Uso:
    pip install fonttools cairosvg
    python3 herramientas/generar_logos_ronda3.py
"""
import math
import os

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

from generar_logos import AZUL_CIELO, AZUL_PROFUNDO, BLANCO, RAIZ, fuente, guardar, svg_doc, texto

DIR_SALIDA = os.path.join(RAIZ, "propuestas", "ronda3")

NEGRO = "#141414"
AZUL_M = "#0E9BE8"  # azul de la referencia, depurado

VARIANTES = {
    # fiel a la referencia: negro + azul brillante
    "H1_negro_azul": dict(c1=NEGRO, c2=AZUL_M, neg1=BLANCO, neg2=AZUL_M, fondo_neg=NEGRO),
    # versión corporativa: azul profundo + azul brillante
    "H2_azul_profundo": dict(c1=AZUL_PROFUNDO, c2=AZUL_M, neg1=BLANCO, neg2=AZUL_CIELO, fondo_neg=AZUL_PROFUNDO),
}


def monograma(x, y, s, c1, c2):
    """M plegada en una caja s×s: tallo izquierdo + V en c1; diagonal y tallo derecho en c2.

    Todas las diagonales comparten pendiente y grosor, y las piezas se separan
    con una ranura constante, lo que da el efecto de cinta plegada.
    """
    u = s / 100.0
    k = 0.72                      # pendiente de las diagonales
    f = math.sqrt(1 + k * k)
    t = 20                        # grosor de las piezas
    a = t * f                     # alto vertical de una banda diagonal
    g = 4.2 * f                   # ranura entre piezas (medida en vertical)
    st = 20                       # ancho de los tallos
    xl = 42                       # inicio de la diagonal azul

    def P(pts, color):
        return '<polygon points="' + " ".join(f"{x + px * u:.2f},{y + py * u:.2f}" for px, py in pts) + f'" fill="{color}"/>'

    v = [(0, 0), (50, 50 * k), (100, 0), (100, a), (50, 50 * k + a), (0, a)]
    tallo_izq = [(0, a + g), (st, a + g + k * st), (st, 100), (0, 100 - st * k)]
    sup = lambda px: a + g + k * (100 - px)
    inf = lambda px: sup(px) + a
    azul = [(xl, sup(xl)), (100, sup(100)), (100, 100 - st * k), (100 - st, 100),
            (100 - st, inf(100 - st)), (xl, inf(xl))]
    return P(tallo_izq, c1) + P(v, c1) + P(azul, c2)


def wordmark(x, y_base, cap, c1, c2):
    tr = 0.06
    d1, w1 = texto("montserrat", 700, "MUNDO", cap, x, y_base, tr)
    sep = cap * tr * 1.4
    d2, w2 = texto("montserrat", 700, "ZYL", cap, x + w1 + sep, y_base, tr)
    return f'<path d="{d1}" fill="{c1}"/><path d="{d2}" fill="{c2}"/>', w1 + sep + w2


def tinta(cadena, cap, tracking):
    """Límites horizontales reales (sin márgenes laterales) del texto en x=0."""
    f = fuente("montserrat", 700)
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    esc = cap / f["OS/2"].sCapHeight
    pen = BoundsPen(gs)
    cursor = 0.0
    for ch in cadena:
        g = gs[cmap[ord(ch)]]
        g.draw(TransformPen(pen, (esc, 0, 0, esc, cursor * esc, 0)))
        cursor += g.width + tracking * f["head"].unitsPerEm
    return pen.bounds[0], pen.bounds[2]


def wordmark_2_lineas(x, y_top, cap, interlinea, c1, c2):
    """MUNDO sobre ZYL, ambas líneas justificadas al mismo ancho de tinta."""
    tr = 0.06
    a0, a1 = tinta("MUNDO", cap, tr)
    ancho = a1 - a0
    upm_px = 1000 * cap / fuente("montserrat", 700)["OS/2"].sCapHeight
    b0, b1 = tinta("ZYL", cap, 0)
    tr_zyl = (ancho - (b1 - b0)) / 2 / upm_px
    b0, b1 = tinta("ZYL", cap, tr_zyl)
    y1 = y_top + cap
    y2 = y1 + interlinea + cap
    d1, _ = texto("montserrat", 700, "MUNDO", cap, x - a0, y1, tr)
    d2, _ = texto("montserrat", 700, "ZYL", cap, x - b0, y2, tr_zyl)
    return f'<path d="{d1}" fill="{c1}"/><path d="{d2}" fill="{c2}"/>', ancho


def horizontal_2_lineas(v, negativo=False):
    """Símbolo a la izquierda; las dos líneas ocupan exactamente su altura."""
    c1, c2, fondo = cols(v, negativo)
    s, m = 220, 70
    interlinea = s * 0.16
    cap = (s - interlinea) / 2
    ic = monograma(m, m, s, c1, c2)
    x = m + s + s * 0.16
    wm, w = wordmark_2_lineas(x, m, cap, interlinea, c1, c2)
    return svg_doc(x + w + m, s + 2 * m, ic + wm, fondo)


def vertical_2_lineas(v, negativo=False):
    c1, c2, fondo = cols(v, negativo)
    s, m = 240, 70
    cap = 78
    interlinea = cap * 0.30
    _, w = wordmark_2_lineas(0, 0, cap, interlinea, c1, c2)
    ancho = max(s, w) + 2 * m
    ic = monograma(ancho / 2 - s / 2, m, s, c1, c2)
    y_top = m + s + cap * 0.6
    wm, _ = wordmark_2_lineas(ancho / 2 - w / 2, y_top, cap, interlinea, c1, c2)
    return svg_doc(ancho, y_top + 2 * cap + interlinea + m, ic + wm, fondo)


def cols(v, negativo):
    if negativo:
        return v["neg1"], v["neg2"], v["fondo_neg"]
    return v["c1"], v["c2"], None


def horizontal(v, negativo=False):
    c1, c2, fondo = cols(v, negativo)
    s, m = 220, 70
    cap = s * 0.42
    ic = monograma(m, m, s, c1, c2)
    x = m + s + s * 0.30
    wm, w = wordmark(x, m + s / 2 + cap / 2, cap, c1, c2)
    return svg_doc(x + w + m, s + 2 * m, ic + wm, fondo)


def vertical(v, negativo=False):
    c1, c2, fondo = cols(v, negativo)
    s, m, cap = 240, 70, 64
    _, w = wordmark(0, 0, cap, c1, c2)
    ancho = max(s, w) + 2 * m
    ic = monograma(ancho / 2 - s / 2, m, s, c1, c2)
    yb = m + s + cap * 0.8 + cap
    wm, _ = wordmark(ancho / 2 - w / 2, yb, cap, c1, c2)
    return svg_doc(ancho, yb + m, ic + wm, fondo)


def icono(v, negativo=True):
    lado, s = 512, 290
    c1, c2, fondo = cols(v, negativo)
    bg = f'<rect width="{lado}" height="{lado}" fill="{fondo or BLANCO}"/>'
    return svg_doc(lado, lado, bg + monograma((lado - s) / 2, (lado - s) / 2, s, c1, c2))


def main():
    for clave, v in VARIANTES.items():
        guardar(f"{clave}/{clave}_horizontal", horizontal(v), DIR_SALIDA)
        guardar(f"{clave}/{clave}_horizontal_negativo", horizontal(v, True), DIR_SALIDA)
        guardar(f"{clave}/{clave}_vertical", vertical(v), DIR_SALIDA)
        guardar(f"{clave}/{clave}_vertical_negativo", vertical(v, True), DIR_SALIDA)
        guardar(f"{clave}/{clave}_icono", icono(v), DIR_SALIDA)
        guardar(f"{clave}/{clave}_icono_claro", icono(v, False), DIR_SALIDA)
        guardar(f"{clave}/{clave}_horizontal_2lineas", horizontal_2_lineas(v), DIR_SALIDA)
        guardar(f"{clave}/{clave}_horizontal_2lineas_negativo", horizontal_2_lineas(v, True), DIR_SALIDA)
        guardar(f"{clave}/{clave}_vertical_2lineas", vertical_2_lineas(v), DIR_SALIDA)
        guardar(f"{clave}/{clave}_vertical_2lineas_negativo", vertical_2_lineas(v, True), DIR_SALIDA)
    print("Listo:", DIR_SALIDA)


if __name__ == "__main__":
    main()
