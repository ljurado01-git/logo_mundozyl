# MUNDOZYL — Rediseño de logo

**Mundo Electronic ZYL** · Caracas, Venezuela · Equipos de computación, redes, telecomunicaciones y seguridad para empresas.

## Ronda 2 (vigente)

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
```
