"""Genera las propuestas de logo MUNDOZYL en SVG (texto convertido a trazos) y PNG.

Uso:
    pip install fonttools cairosvg
    python3 herramientas/generar_logos.py

Las fuentes (Google Fonts, licencia OFL) se descargan en herramientas/fuentes/.
"""
import math
import os
import urllib.request

import cairosvg
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_FUENTES = os.path.join(RAIZ, "herramientas", "fuentes")
DIR_SALIDA = os.path.join(RAIZ, "propuestas")

FUENTES = {
    "montserrat": "montserrat/Montserrat%5Bwght%5D.ttf",
    "sora": "sora/Sora%5Bwght%5D.ttf",
    "manrope": "manrope/Manrope%5Bwght%5D.ttf",
}

# Paleta "Azul corporativo"
AZUL_PROFUNDO = "#0B2545"   # confianza, solidez
AZUL_ZYL = "#1668E3"        # tecnología, energía
AZUL_CIELO = "#5AA9FF"      # acento sobre fondos oscuros
GRIS = "#5B6B7F"
BLANCO = "#FFFFFF"


# ---------------------------------------------------------------- fuentes

_cache = {}


def fuente(nombre, peso):
    clave = (nombre, peso)
    if clave in _cache:
        return _cache[clave]
    os.makedirs(DIR_FUENTES, exist_ok=True)
    ruta = os.path.join(DIR_FUENTES, nombre + ".ttf")
    if not os.path.exists(ruta):
        url = "https://raw.githubusercontent.com/google/fonts/main/ofl/" + FUENTES[nombre]
        urllib.request.urlretrieve(url, ruta)
    f = instancer.instantiateVariableFont(TTFont(ruta), {"wght": peso})
    _cache[clave] = f
    return f


def texto(nombre, peso, cadena, alto_mayus, x, y_base, tracking=0.0):
    """Devuelve (path_d, ancho) del texto escalado para que la altura de
    mayúsculas sea `alto_mayus`. tracking en fracción de em."""
    f = fuente(nombre, peso)
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    upm = f["head"].unitsPerEm
    cap = f["OS/2"].sCapHeight
    esc = alto_mayus / cap
    pen = SVGPathPen(gs)
    cursor = 0.0
    kern = _kerning(f)
    nombres = [cmap[ord(c)] for c in cadena]
    for i, g in enumerate(nombres):
        tp = TransformPen(pen, (esc, 0, 0, -esc, x + cursor * esc, y_base))
        gs[g].draw(tp)
        cursor += gs[g].width + tracking * upm
        if i + 1 < len(nombres):
            cursor += kern.get((g, nombres[i + 1]), 0)
    ancho = (cursor - tracking * upm) * esc
    return pen.getCommands(), ancho


def _kerning(f):
    """Kerning simple (pares de clase 1 de GPOS PairPos formato 1/2)."""
    pares = {}
    if "GPOS" not in f:
        return pares
    for lookup in f["GPOS"].table.LookupList.Lookup:
        for st in lookup.SubTable:
            if lookup.LookupType == 9:
                st = st.ExtSubTable
            if getattr(st, "LookupType", None) != 2 and lookup.LookupType not in (2, 9):
                continue
            if not hasattr(st, "Format"):
                continue
            if st.Format == 1:
                for g1, ps in zip(st.Coverage.glyphs, st.PairSet):
                    for pv in ps.PairValueRecord:
                        v = getattr(pv.Value1, "XAdvance", 0) or 0
                        pares.setdefault((g1, pv.SecondGlyph), v)
            elif st.Format == 2:
                c1 = st.ClassDef1.classDefs
                c2 = st.ClassDef2.classDefs
                for g1 in st.Coverage.glyphs:
                    k1 = c1.get(g1, 0)
                    for g2, k2 in c2.items():
                        rec = st.Class1Record[k1].Class2Record[k2]
                        v = getattr(rec.Value1, "XAdvance", 0) or 0
                        if v:
                            pares.setdefault((g1, g2), v)
    return pares


# ---------------------------------------------------------------- geometría


def elipse_arco(cx, cy, rx, ry):
    return f"M{cx - rx:.2f},{cy:.2f}a{rx:.2f},{ry:.2f} 0 1,0 {2 * rx:.2f},0a{rx:.2f},{ry:.2f} 0 1,0 {-2 * rx:.2f},0Z"


def svg_doc(ancho, alto, cuerpo, fondo=None, titulo="MUNDOZYL"):
    bg = f'<rect width="{ancho:.0f}" height="{alto:.0f}" fill="{fondo}"/>' if fondo else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho:.0f} {alto:.0f}" '
        f'width="{ancho:.0f}" height="{alto:.0f}" role="img" aria-label="{titulo}">'
        f"<title>{titulo}</title>{bg}{cuerpo}</svg>\n"
    )


# ------------------------------------------------- Propuesta A: "Órbita"
# Globo lineal (meridiano + paralelos) con una órbita inclinada y un nodo:
# el mundo conectado. Wordmark Montserrat Bold.


def icono_orbita(cx, cy, r, c_globo, c_orbita, fondo):
    sw = r * 0.12
    swi = r * 0.085
    p = []
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r - sw / 2:.2f}" fill="none" stroke="{c_globo}" stroke-width="{sw:.2f}"/>')
    ri = r - sw / 2
    g = f'fill="none" stroke="{c_globo}" stroke-width="{swi:.2f}" stroke-linecap="round"'
    p.append(f'<path d="{elipse_arco(cx, cy, ri * 0.42, ri)}" {g}/>')
    p.append(f'<line x1="{cx}" y1="{cy - ri:.2f}" x2="{cx}" y2="{cy + ri:.2f}" {g}/>')
    for k in (-0.5, 0.0, 0.5):
        y = cy + k * ri
        hw = ri * math.sqrt(1 - k * k)
        p.append(f'<line x1="{cx - hw:.2f}" y1="{y:.2f}" x2="{cx + hw:.2f}" y2="{y:.2f}" {g}/>')
    # órbita
    rx, ry, ang = r * 1.38, r * 0.40, -22
    orb = elipse_arco(cx, cy, rx, ry)
    sw_o = r * 0.10
    tr = f'transform="rotate({ang} {cx} {cy})"'
    # Forma simple: frente (mitad inferior de la elipse rotada) sobre el globo con
    # halo del color de fondo; trasera (mitad superior) solo fuera del globo.
    frente = f"M{cx - rx:.2f},{cy:.2f}a{rx:.2f},{ry:.2f} 0 0,0 {2 * rx:.2f},0"
    trasera = f"M{cx - rx:.2f},{cy:.2f}a{rx:.2f},{ry:.2f} 0 0,1 {2 * rx:.2f},0"
    clip_id = f"m{abs(hash((cx, cy, r, fondo))) % 10**6}"
    defs = (
        f'<defs><mask id="{clip_id}" maskUnits="userSpaceOnUse" x="{cx - 2 * r}" y="{cy - 2 * r}" width="{4 * r}" height="{4 * r}">'
        f'<rect x="{cx - 2 * r}" y="{cy - 2 * r}" width="{4 * r}" height="{4 * r}" fill="#fff"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r + sw_o * 0.8:.2f}" fill="#000"/></mask></defs>'
    )
    p.append(defs)
    p.append(f'<g {tr}><path d="{trasera}" fill="none" stroke="{c_orbita}" stroke-width="{sw_o:.2f}" stroke-linecap="round" mask="url(#{clip_id})"/></g>')
    if fondo:
        p.append(f'<g {tr}><path d="{frente}" fill="none" stroke="{fondo}" stroke-width="{sw_o * 2.6:.2f}" stroke-linecap="round"/></g>')
    p.append(f'<g {tr}><path d="{frente}" fill="none" stroke="{c_orbita}" stroke-width="{sw_o:.2f}" stroke-linecap="round"/></g>')
    # nodo (satélite) sobre la órbita, en el frente derecho
    t = math.radians(35)
    nx, ny = rx * math.cos(t), ry * math.sin(t)
    a = math.radians(ang)
    px = cx + nx * math.cos(a) - ny * math.sin(a)
    py = cy + nx * math.sin(a) + ny * math.cos(a)
    if fondo:
        p.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{r * 0.2:.2f}" fill="{fondo}"/>')
    p.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{r * 0.13:.2f}" fill="{c_orbita}"/>')
    return "".join(p)


# ------------------------------------------------- Propuesta B: "Red"
# Globo construido con una retícula y nodos conectados: infraestructura,
# redes y telecomunicaciones. Wordmark Sora SemiBold.


def icono_red(cx, cy, r, c_globo, c_red, fondo):
    sw = r * 0.10
    ri = r - sw / 2
    g = f'fill="none" stroke="{c_globo}" stroke-width="{sw * 0.7:.2f}" stroke-linecap="round"'
    p = [f'<circle cx="{cx}" cy="{cy}" r="{ri:.2f}" fill="none" stroke="{c_globo}" stroke-width="{sw:.2f}"/>']
    p.append(f'<path d="{elipse_arco(cx, cy, ri * 0.55, ri)}" {g}/>')
    for k in (-0.55, 0.55):
        y = cy + k * ri
        hw = ri * math.sqrt(1 - k * k)
        p.append(f'<line x1="{cx - hw:.2f}" y1="{y:.2f}" x2="{cx + hw:.2f}" y2="{y:.2f}" {g}/>')
    # nodos en intersecciones meridiano/paralelo + borde
    def en_elipse(k, lado):
        y = cy + k * ri
        x = cx + lado * ri * 0.55 * math.sqrt(1 - k * k)
        return x, y
    # Los nodos dibujan una "Z" (de ZYL) sobre la retícula del globo.
    n1 = en_elipse(-0.55, -1)
    n2 = en_elipse(-0.55, 1)
    n3 = en_elipse(0.55, -1)
    n4 = en_elipse(0.55, 1)
    nodos = [n1, n2, n3, n4]
    conex = [(n1, n2), (n2, n3), (n3, n4)]
    for a, b in conex:
        p.append(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="{c_red}" stroke-width="{sw * 0.95:.2f}" stroke-linecap="round"/>')
    for (x, y) in nodos:
        if fondo:
            p.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r * 0.2:.2f}" fill="{fondo}"/>')
        p.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r * 0.135:.2f}" fill="{c_red}"/>')
    return "".join(p)


# ------------------------------------------------- Propuesta C: "Globo en la O"
# La O de MUNDO se convierte en el mundo. Wordmark Manrope ExtraBold.


def globo_o(cx, cy, r, grosor, c_aro, c_lineas):
    ri = r - grosor / 2
    rin = ri - grosor / 2
    g = f'fill="none" stroke="{c_lineas}" stroke-width="{grosor * 0.34:.2f}"'
    return (
        f'<path d="{elipse_arco(cx, cy, rin * 0.5, rin + grosor * 0.2)}" {g}/>'
        f'<line x1="{cx - rin - grosor * 0.2:.2f}" y1="{cy:.2f}" x2="{cx + rin + grosor * 0.2:.2f}" y2="{cy:.2f}" {g}/>'
        f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{ri:.2f}" fill="none" stroke="{c_aro}" stroke-width="{grosor:.2f}"/>'
    )


# ---------------------------------------------------------------- layouts

PROPUESTAS = {
    "A_orbita": dict(
        nombre="Órbita",
        fuente=("montserrat", 700),
        tracking=0.04,
        icono=icono_orbita,
    ),
    "B_red": dict(
        nombre="Red",
        fuente=("sora", 600),
        tracking=0.02,
        icono=icono_red,
    ),
    "C_globo_o": dict(
        nombre="Globo en la O",
        fuente=("manrope", 800),
        tracking=0.0,
        icono=None,
    ),
}


def wordmark(clave, x, y_base, cap, c1, c2):
    cfg = PROPUESTAS[clave]
    fn, peso = cfg["fuente"]
    d1, w1 = texto(fn, peso, "MUNDO", cap, x, y_base, cfg["tracking"])
    sep = cap * cfg["tracking"] * 1.4 + cap * 0.02
    d2, w2 = texto(fn, peso, "ZYL", cap, x + w1 + sep, y_base, cfg["tracking"])
    return f'<path d="{d1}" fill="{c1}"/><path d="{d2}" fill="{c2}"/>', w1 + sep + w2


def wordmark_c(x, y_base, cap, c1, c2, c_lineas):
    fn, peso = PROPUESTAS["C_globo_o"]["fuente"]
    d1, w1 = texto(fn, peso, "MUND", cap, x, y_base, 0)
    grosor = cap * 0.205
    r = cap * 0.53
    gap = cap * 0.07
    cx = x + w1 + gap + r
    cy = y_base - cap / 2
    o = globo_o(cx, cy, r, grosor, c1, c_lineas)
    d2, w2 = texto(fn, peso, "ZYL", cap, cx + r + gap, y_base, 0)
    return f'<path d="{d1}" fill="{c1}"/>{o}<path d="{d2}" fill="{c2}"/>', w1 + 2 * gap + 2 * r + w2


def colores(negativo):
    if negativo:
        return dict(c1=BLANCO, c2=AZUL_CIELO, acento=AZUL_CIELO, fondo=AZUL_PROFUNDO)
    return dict(c1=AZUL_PROFUNDO, c2=AZUL_ZYL, acento=AZUL_ZYL, fondo=BLANCO)


def horizontal(clave, negativo=False):
    c = colores(negativo)
    cap = 100
    m = 60
    if clave == "C_globo_o":
        cuerpo, w = wordmark_c(m, m + cap, cap, c["c1"], c["c2"], c["acento"])
        return svg_doc(w + 2 * m, cap + 2 * m, cuerpo, c["fondo"] if negativo else None)
    r = cap * 0.95
    cfg = PROPUESTAS[clave]
    ext = r * 1.45 if clave == "A_orbita" else r
    cx = m + ext
    cy = m + max(r, r * 0.95)
    ic = cfg["icono"](cx, cy, r, c["c1"], c["acento"], c["fondo"])
    x = cx + (r * 1.3 if clave == "A_orbita" else r) + cap * 0.5
    wm, w = wordmark(clave, x, cy + cap / 2, cap, c["c1"], c["c2"])
    return svg_doc(x + w + m, cy * 2, ic + wm, c["fondo"] if negativo else None)


def vertical(clave, negativo=False):
    c = colores(negativo)
    cap = 70
    m = 60
    r = 120
    if clave == "C_globo_o":
        _, w = wordmark_c(0, 0, cap, "#000", "#000", "#000")
    else:
        _, w = wordmark(clave, 0, 0, cap, "#000", "#000")
    ext = r * 1.45 if clave == "A_orbita" else r
    ancho = max(2 * ext, w) + 2 * m
    cx = ancho / 2
    cy = m + r * (1.05 if clave == "A_orbita" else 1)
    if clave == "C_globo_o":
        ic = globo_o(cx, cy, r, r * 0.205 / 0.53, c["c1"], c["acento"])
    else:
        ic = PROPUESTAS[clave]["icono"](cx, cy, r, c["c1"], c["acento"], c["fondo"])
    yb = cy + r * 1.05 + cap * 0.6 + cap
    if clave == "C_globo_o":
        wm, _ = wordmark_c(cx - w / 2, yb, cap, c["c1"], c["c2"], c["acento"])
    else:
        wm, _ = wordmark(clave, cx - w / 2, yb, cap, c["c1"], c["c2"])
    return svg_doc(ancho, yb + m, ic + wm, c["fondo"] if negativo else None)


def icono_app(clave, negativo=False):
    """Isotipo en cuadrado 512x512 (avatar de redes, favicon)."""
    lado = 512
    c = colores(not negativo)  # por defecto el avatar va en fondo azul profundo
    fondo = c["fondo"]
    cuerpo = f'<rect width="{lado}" height="{lado}" rx="0" fill="{fondo}"/>'
    if clave == "A_orbita":
        r = 140
        cuerpo += icono_orbita(lado / 2, lado / 2, r, c["c1"], c["acento"], fondo)
    elif clave == "B_red":
        r = 170
        cuerpo += icono_red(lado / 2, lado / 2, r, c["c1"], c["acento"], fondo)
    else:
        r = 170
        cuerpo += globo_o(lado / 2, lado / 2, r, r * 0.24, c["c1"], c["acento"])
    return svg_doc(lado, lado, cuerpo)


def guardar(nombre, svg):
    ruta = os.path.join(DIR_SALIDA, nombre)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta + ".svg", "w", encoding="utf-8") as fh:
        fh.write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=ruta + ".png", scale=2)


def main():
    for clave in PROPUESTAS:
        guardar(f"{clave}/{clave}_horizontal", horizontal(clave))
        guardar(f"{clave}/{clave}_horizontal_negativo", horizontal(clave, True))
        guardar(f"{clave}/{clave}_vertical", vertical(clave))
        guardar(f"{clave}/{clave}_vertical_negativo", vertical(clave, True))
        guardar(f"{clave}/{clave}_icono", icono_app(clave))
    print("Listo:", DIR_SALIDA)


if __name__ == "__main__":
    main()
