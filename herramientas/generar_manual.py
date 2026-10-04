"""Construye el manual de marca (HTML autocontenido) a partir de manual/plantilla.html.

Requiere haber ejecutado antes herramientas/generar_logo_final.py.
Después, para el PDF y las imágenes de los mockups:
    node herramientas/exportar_manual.js

Uso:
    pip install fonttools cairosvg
    python3 herramientas/generar_manual.py
"""
import base64
import io
import os
import re

from fontTools import subset
from fontTools.ttLib import TTFont

from generar_logos import AZUL_PROFUNDO, BLANCO, RAIZ, fuente
from generar_logos_ronda3 import AZUL_M, monograma

DIR_LOGOS = os.path.join(RAIZ, "logo_final")
PLANTILLA = os.path.join(RAIZ, "manual", "plantilla.html")
SALIDA = os.path.join(RAIZ, "manual", "manual_de_marca_mundozyl.html")

COLORES = [
    ("Azul Profundo", "#0B2545", "Logotipo, textos, fondos institucionales", BLANCO),
    ("Azul ZYL", AZUL_M, "Acento: «ZYL», botones, detalles", BLANCO),
    ("Azul Cielo", "#5AA9FF", "«ZYL» y acentos sobre fondo oscuro", AZUL_PROFUNDO),
    ("Grafito", "#5B6B7F", "Textos secundarios", BLANCO),
    ("Niebla", "#F3F6FA", "Fondos claros, tarjetas web", AZUL_PROFUNDO),
]


def cmyk(hexa):
    r, g, b = (int(hexa[i:i + 2], 16) / 255 for i in (1, 3, 5))
    k = 1 - max(r, g, b)
    if k >= 1:
        return 0, 0, 0, 100
    c, m, y = ((1 - v - k) / (1 - k) for v in (r, g, b))
    return tuple(round(v * 100) for v in (c, m, y, k))


def rgb(hexa):
    return tuple(int(hexa[i:i + 2], 16) for i in (1, 3, 5))


def bloque_colores():
    out = []
    for nombre, hexa, uso, texto_chip in COLORES:
        c, m, y, k = cmyk(hexa)
        r, g, b = rgb(hexa)
        borde = ' style="box-shadow: inset 0 0 0 1px var(--linea)"' if hexa == "#F3F6FA" else ""
        out.append(
            f'<div class="muestra"><div class="chip" style="background:{hexa}; color:{texto_chip}"{borde}>{nombre}</div>'
            f"<dl><dt>HEX</dt><dd>{hexa}</dd><dt>RGB</dt><dd>{r} {g} {b}</dd>"
            f"<dt>CMYK</dt><dd>{c} {m} {y} {k}</dd><dt>Uso</dt><dd style=\"font-family:var(--texto)\">{uso}</dd></dl></div>"
        )
    return "\n".join(out)


def svg_inline(ruta_rel):
    with open(os.path.join(DIR_LOGOS, ruta_rel + ".svg"), encoding="utf-8") as fh:
        svg = fh.read().strip()
    # el tamaño lo controla el CSS; se conserva el viewBox
    svg = re.sub(r'\swidth="[\d.]+" height="[\d.]+"', "", svg, count=1)
    return re.sub(r"<title>.*?</title>", "", svg, count=1)


def diagonales():
    """Recurso gráfico: bandas con la inclinación de la M (pendiente 0,72)."""
    k = 0.72
    w, h = 600, 600
    bandas = []
    for i in range(-6, 10):
        y0 = i * 70
        pts = [(0, y0), (w, y0 - k * w), (w, y0 - k * w + 28), (0, y0 + 28)]
        color = AZUL_M if i % 4 == 1 else BLANCO
        bandas.append('<polygon points="' + " ".join(f"{x:.0f},{y:.0f}" for x, y in pts) + f'" fill="{color}"/>')
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{"".join(bandas)}</svg>'


def isotipo_blanco():
    return f'<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{monograma(0, 0, 100, BLANCO, BLANCO)}</svg>'


def wordmark_solo():
    from generar_logos_ronda3 import wordmark_2_lineas

    cuerpo, w, h = wordmark_2_lineas(0, 0, 60, 18, AZUL_PROFUNDO, AZUL_M)
    return f'<svg viewBox="-4 -4 {w + 8:.0f} {h + 8:.0f}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{cuerpo}</svg>'


def fuente_woff_b64():
    fuente("montserrat", 700)  # asegura la descarga
    ruta = os.path.join(RAIZ, "herramientas", "fuentes", "montserrat.ttf")
    opciones = subset.Options()
    opciones.flavor = "woff"
    opciones.layout_features = ["*"]
    f = TTFont(ruta)
    sub = subset.Subsetter(opciones)
    texto_unicodes = list(range(0x20, 0x7F)) + list(range(0xA0, 0x100)) + [
        0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2026, 0x00D7, 0x2715]
    sub.populate(unicodes=texto_unicodes)
    sub.subset(f)
    buf = io.BytesIO()
    f.flavor = "woff"
    f.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def main():
    with open(PLANTILLA, encoding="utf-8") as fh:
        html = fh.read()
    html = html.replace("{{SVG:una_tinta/mundozyl_isotipo_blanco_inline}}", isotipo_blanco())
    html = re.sub(r"\{\{SVG:([\w/]+)\}\}", lambda m: svg_inline(m.group(1)), html)
    html = html.replace("{{DIAGONALES}}", diagonales())
    html = html.replace("{{COLORES}}", bloque_colores())
    html = html.replace("{{WORDMARK_SOLO}}", wordmark_solo())
    html = html.replace("{{FUENTE}}", fuente_woff_b64())
    assert "{{" not in html, re.findall(r"\{\{[^}]+\}\}", html)
    with open(SALIDA, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("Listo:", SALIDA, f"{len(html) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
