# MUNDOZYL — Rediseño de logo (Ronda 1)

**Mundo Electronic ZYL** · Caracas, Venezuela · Equipos de computación, redes, telecomunicaciones y seguridad para empresas.

Brief acordado: globo simplificado · paleta azul corporativo · nombre **MUNDOZYL** · estilo minimalista, que transmita confianza.

Ver `propuestas/lamina_comparativa.png` para comparar las tres direcciones.

## Propuestas

| | Concepto | Tipografía | Qué comunica |
|---|---|---|---|
| **A · Órbita** | Globo lineal con una órbita y un nodo/satélite | Montserrat Bold | Alcance global, conectividad. Evolución más cercana al logo actual. |
| **B · Red** | Globo cuya retícula une 4 nodos formando una **Z** (de ZYL) | Sora SemiBold | Infraestructura, redes, telecom. Isotipo propio y difícil de copiar. |
| **C · Globo en la O** | La O de MUNDO es el globo | Manrope ExtraBold | Máxima recordación del nombre; el más minimalista. |

Cada propuesta incluye: horizontal, vertical, versiones en negativo e isotipo 512×512 (avatar de redes / favicon), en **SVG** (texto convertido a trazos, no requiere fuentes instaladas) y **PNG**.

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
python3 herramientas/generar_logos.py
```
