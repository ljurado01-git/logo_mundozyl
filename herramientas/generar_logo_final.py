"""Paquete final del logo MUNDOZYL (propuesta H2 aprobada).

Genera en logo_final/ todas las versiones (color, negativo y una tinta) en SVG y PNG.

Uso:
    pip install fonttools cairosvg
    python3 herramientas/generar_logo_final.py
"""
import os

import cairosvg

from generar_logos import AZUL_PROFUNDO, BLANCO, RAIZ, svg_doc
from generar_logos_ronda3 import (
    AZUL_M,
    horizontal,
    horizontal_2_lineas,
    monograma,
    vertical_2_lineas,
)

DIR_SALIDA = os.path.join(RAIZ, "logo_final")
AZUL_CIELO = "#5AA9FF"
NEGRO = "#000000"

# Cada variante usa la convención de ronda3: c1/c2 sobre claro, neg1/neg2 sobre fondo_neg.
COLOR = dict(c1=AZUL_PROFUNDO, c2=AZUL_M, neg1=BLANCO, neg2=AZUL_CIELO, fondo_neg=AZUL_PROFUNDO)
UNA_TINTA = {
    "azul": dict(c1=AZUL_PROFUNDO, c2=AZUL_PROFUNDO, neg1=BLANCO, neg2=BLANCO, fondo_neg=AZUL_PROFUNDO),
    "negro": dict(c1=NEGRO, c2=NEGRO, neg1=BLANCO, neg2=BLANCO, fondo_neg=NEGRO),
}


def isotipo(v, negativo=False, margen=0.12, s=400):
    c1, c2 = (v["neg1"], v["neg2"]) if negativo else (v["c1"], v["c2"])
    m = s * margen
    fondo = f'<rect width="{s + 2 * m:.0f}" height="{s + 2 * m:.0f}" fill="{v["fondo_neg"]}"/>' if negativo else ""
    return svg_doc(s + 2 * m, s + 2 * m, fondo + monograma(m, m, s, c1, c2))


def avatar(lado=1080):
    """Perfil de redes: M en negativo sobre azul profundo, con margen para recorte circular."""
    s = lado * 0.50
    return svg_doc(lado, lado, f'<rect width="{lado}" height="{lado}" fill="{AZUL_PROFUNDO}"/>'
                   + monograma((lado - s) / 2, (lado - s) / 2 - lado * 0.01, s, BLANCO, AZUL_CIELO))


def sin_fondo(svg):
    """Las versiones negativas se entregan también transparentes (para colocar sobre fotos o colores)."""
    i = svg.index("<rect")
    j = svg.index("/>", i) + 2
    return svg[:i] + svg[j:]


def guardar(nombre, svg, ancho_png=2000):
    ruta = os.path.join(DIR_SALIDA, nombre)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta + ".svg", "w", encoding="utf-8") as fh:
        fh.write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=ruta + ".png", output_width=ancho_png)


def main():
    versiones = {
        "principal_2lineas": horizontal_2_lineas,
        "horizontal_1linea": horizontal,
        "vertical": vertical_2_lineas,
    }
    for nombre, fn in versiones.items():
        guardar(f"color/mundozyl_{nombre}", fn(COLOR))
        neg = fn(COLOR, True)
        guardar(f"negativo/mundozyl_{nombre}_negativo_fondo", neg)
        guardar(f"negativo/mundozyl_{nombre}_negativo_transparente", sin_fondo(neg))
        for tinta, v in UNA_TINTA.items():
            guardar(f"una_tinta/mundozyl_{nombre}_{tinta}", fn(v))
        guardar(f"una_tinta/mundozyl_{nombre}_blanco", sin_fondo(fn(UNA_TINTA["azul"], True)))

    guardar("color/mundozyl_isotipo", isotipo(COLOR), 1000)
    guardar("negativo/mundozyl_isotipo_negativo_fondo", isotipo(COLOR, True), 1000)
    guardar("negativo/mundozyl_isotipo_negativo_transparente", sin_fondo(isotipo(COLOR, True)), 1000)
    for tinta, v in UNA_TINTA.items():
        guardar(f"una_tinta/mundozyl_isotipo_{tinta}", isotipo(v), 1000)

    guardar("redes/mundozyl_avatar_1080", avatar(), 1080)
    for px in (512, 180, 32):
        ruta = os.path.join(DIR_SALIDA, "web", f"favicon_{px}.png")
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        cairosvg.svg2png(bytestring=isotipo(COLOR, True, margen=0.16).encode(), write_to=ruta,
                         output_width=px, output_height=px)
    with open(os.path.join(DIR_SALIDA, "web", "favicon.svg"), "w", encoding="utf-8") as fh:
        fh.write(isotipo(COLOR, True, margen=0.16))
    print("Listo:", DIR_SALIDA)


if __name__ == "__main__":
    main()
