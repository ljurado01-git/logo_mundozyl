# MUNDOZYL — Rediseño de logo

## Entregables finales (logo aprobado: H2)

- **`logo_final/`**: paquete del logo listo para usar (SVG vectorial + PNG 2000 px):
  - `color/`: principal en 2 líneas, horizontal 1 línea, vertical e isotipo.
  - `negativo/`: para fondos oscuros, con fondo azul profundo o transparente.
  - `una_tinta/`: azul profundo, negro y blanco (sellos, facturas, grabado, bordado).
  - `redes/`: avatar 1080×1080. `web/`: favicon SVG y PNG 32/180/512.
- **`manual/manual_de_marca_mundozyl.pdf`**: manual de marca (12 láminas A4 horizontal): concepto, versiones, área de protección, tamaños mínimos, color, tipografía, fondos, usos incorrectos y aplicaciones.
- **`manual/mockups/`**: vistas de prueba en web, tarjeta de presentación, redes sociales y papelería (PNG).

Regenerar todo:

```bash
pip install fonttools cairosvg
python3 herramientas/generar_logo_final.py
python3 herramientas/generar_manual.py
NODE_PATH=$(npm root -g) node herramientas/exportar_manual.js   # PDF + PNG (Playwright)
```

---

**Mundo Electronic ZYL** · Caracas, Venezuela · Equipos de computación, redes, telecomunicaciones y seguridad para empresas.

## Ronda 3 (vigente) — Monograma M

Reproducción vectorial, depurada, de la referencia aportada por el cliente: una **M plegada** (cinta) con el tallo izquierdo y la V en oscuro y la diagonal + tallo derecho en azul. Geometría regularizada: todas las diagonales con la misma pendiente y grosor, ranuras de separación constantes. Wordmark en Montserrat Bold con espaciado amplio.

- **H1 · Negro + azul** (`#141414` / `#0E9BE8`): fiel a la referencia.
- **H2 · Azul profundo + azul** (`#0B2545` / `#0E9BE8`): variante más corporativa.

**Elegida: H2.** Incluye además versiones con el nombre en **dos líneas**: MUNDO (Montserrat ExtraBold) sobre ZYL más grande (Montserrat SemiBold), ambas al mismo ancho y con grosor de trazo equilibrado: `*_horizontal_2lineas*` y `*_vertical_2lineas*` (ver `propuestas/ronda3/lamina_H2_2lineas.png`).

Ver `propuestas/ronda3/lamina_comparativa.png`. Regenerar: `python3 herramientas/generar_logos_ronda3.py`

## Ronda 2

Feedback de la ronda 1: no gustó el globo ni la tipografía y faltaba impacto. Nueva dirección: **logo diferente al actual (sin globo)**, que transmita **solidez y confianza**, con tipografías más fuertes. Símbolo construido sobre la **Z** de ZYL.

Ver `propuestas/ronda2/lamina_comparativa.png`.

| | Concepto | Tipografía | Qué comunica |
|---|---|---|---|
| **D · Bloque** | Bloque sólido con la Z calada y una esquina "sellada" en azul | Archivo Expanded ExtraBold | Estabilidad, producto garantizado, marca seria. |
| **E · Píxel** | Z formada por bloques en retícula 4×4 | Red Hat Display Black | Hardware, datos, componentes que encajan. |
| **F · Hexágono** | Hexágono bicolor (tuerca/chip) con la Z calada | Saira SemiExpanded Bold | Ingeniería, robustez, precisión técnica. |
| **G · Escudo** | Escudo con banda superior y Z | Archivo Black | Protección y respaldo (seguridad, UPS, soporte). |

Regenerar: `python3 herramientas/generar_logos_ronda2.py`

## Ronda 1 (descartada)

Brief: globo simplificado · paleta azul corporativo · nombre **MUNDOZYL** · minimalista. Archivos en `propuestas/ronda1/`.

| | Concepto | Tipografía | Qué comunica |
|---|---|---|---|
| **A · Órbita** | Globo lineal con una órbita y un nodo/satélite | Montserrat Bold | Alcance global, conectividad. Evolución más cercana al logo actual. |
| **B · Red** | Globo cuya retícula une 4 nodos formando una **Z** (de ZYL) | Sora SemiBold | Infraestructura, redes, telecom. Isotipo propio y difícil de copiar. |
| **C · Globo en la O** | La O de MUNDO es el globo | Manrope ExtraBold | Máxima recordación del nombre; el más minimalista. |

Cada propuesta (ambas rondas) incluye: horizontal, vertical, versiones en negativo e isotipo 512×512 (avatar de redes / favicon), en **SVG** (texto convertido a trazos, no requiere fuentes instaladas) y **PNG**.

## Paleta

| Color | HEX | Uso |
|---|---|---|
| Azul Profundo | `#0B2545` | "MUNDO", globo, fondos |
| Azul ZYL | `#1668E3` | "ZYL", acentos |
| Azul Cielo | `#5AA9FF` | Acento sobre fondo oscuro |
| Gris | `#5B6B7F` | Textos secundarios |

Tipografías de Google Fonts (licencia OFL, uso comercial libre).

## Regenerar

```bash
pip install fonttools cairosvg
python3 herramientas/generar_logos.py          # ronda 1
python3 herramientas/generar_logos_ronda2.py   # ronda 2
python3 herramientas/generar_logos_ronda3.py   # ronda 3
```
