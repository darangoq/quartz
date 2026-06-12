# Protocolo de escritura — Jardín digital
**darangoq.github.io/quartz**  
Basado en radiscente · Mapa de intuiciones · Quirocinesis

---

## Taxonomía de estados de germinación

Cada nodo del jardín tiene un estado que describe su madurez. No es una jerarquía de calidad sino de desarrollo.

| Estado | Símbolo | Descripción |
|--------|---------|-------------|
| `espora` | ✦ | Concepto mínimo. Solo existe como palabra y conexiones, sin desarrollo propio. |
| `micelio` | ⬡ | Nodo conector. Su función es organizar la red, no desarrollar contenido propio. |
| `rizoma` | ⌁ | En desarrollo activo. Tiene contenido parcial, sigue creciendo. |
| `floresta` | ❧ | Argumento o pieza completa. Publicable. |

Tipo estructural aparte — no es de madurez sino de origen:

| Tipo | Descripción |
|------|-------------|
| `simbionte` | Fuente o referencia externa que nutre nodos propios. No crece hacia floresta — permanece como simbionte. |

---

## Estructura de un archivo

Todo nodo es un archivo `.md` cuyo nombre coincide exactamente con el título.

### Frontmatter obligatorio

```yaml
---
title: "Nombre exacto del nodo"
estado: floresta
tags:
  - floresta
publish: true
origen: radiscente
---
```

- `title` debe coincidir exactamente con el nombre del archivo.
- `estado` y `tags` deben tener el mismo valor — `tags` es lo que Quartz muestra visualmente.
- `publish: true` es obligatorio para que el nodo aparezca en el jardín público.
- `origen` puede ser `radiscente`, `mapa-de-intuiciones`, `quirocinesis`, o el proyecto del que provenga.

### Frontmatter para nodo sin contenido desarrollado

```yaml
---
title: "Nombre del nodo"
estado: espora
tags:
  - espora
publish: true
---
```

---

## Sintaxis de escritura

### Encabezados

```markdown
## Subtítulo dentro del nodo
### Subtítulo de tercer nivel
```

Nunca uses `#` solo — ese nivel lo reserva Quartz para el título del archivo.

### Énfasis

```markdown
**negrita**
*cursiva*
```

### Párrafos

Deja siempre una línea en blanco entre párrafos. Sin línea en blanco, Quartz los une en uno solo.

---

## Enlaces internos

### Enlace simple — texto visible igual al nombre del nodo destino

```markdown
[[Nombre del nodo]]
```

### Enlace con alias — texto visible diferente al nombre del nodo destino

El orden es siempre `[[destino|texto visible]]`:

```markdown
[[Teks|Cemento]]
```

Esto muestra "Cemento" en el texto pero lleva al nodo "Teks".

### Enlace a un párrafo específico dentro de otro nodo

```markdown
[[Nombre del nodo#nombre-del-subtítulo]]
```

El subtítulo debe existir como `##` en el archivo destino. Se escribe en minúsculas con guiones en lugar de espacios y sin tildes en el ancla:

```markdown
[[Radix, proceso y agente#las-tres-fases]]
```

### Enlace externo

```markdown
[texto visible](https://url.com)
```
```markdown
[texto visible](https://url.com)
```
---

## Multimedia

Todos los archivos multimedia van dentro de la carpeta `content/media/` con esta estructura:

```
content/
  media/
    imagenes/
    audio/
    video/
    docs/
```

### Imágenes

```markdown
![descripción de la imagen](media/imagenes/nombre-archivo.jpg)
```

### Audio — archivo local

```html
<audio controls>
  <source src="media/audio/nombre-archivo.mp3" type="audio/mpeg">
</audio>
```

Para archivos de audio extensos, alojar en PeerTube y embeber desde ahí.

### Video — embed desde PeerTube (anartist.org)

```html
<iframe title="nombre del video"
  src="https://tube.anartist.org/videos/embed/ID-DEL-VIDEO"
  allowfullscreen
  sandbox="allow-same-origin allow-scripts allow-popups">
</iframe>
```

### Video — archivo local

```html
<video controls width="100%">
  <source src="media/video/nombre.mp4" type="video/mp4">
</video>
```

### PDFs — enlace de descarga

```markdown
[Descargar texto completo](media/docs/nombre.pdf)
```

### PDFs — visor incrustado

```html
<iframe src="media/docs/nombre.pdf" width="100%" height="600px"></iframe>
```

---

## Flujo de publicación

Cada vez que agregues o edites contenido, ejecuta en PowerShell desde la carpeta `quartz`:

```bash
git add .
git commit -m "descripción breve de lo que agregaste o editaste"
git push
```

El jardín se reconstruye automáticamente en 2 a 3 minutos después del push.

### Convenciones para los mensajes de commit

El mensaje del commit es la bitácora del jardín — escríbelo con intención:

```
git commit -m "agregar nodo Quirocinesis — floresta"
git commit -m "expandir rizoma sobre el gesto manual"
git commit -m "corregir enlace en Mitologías de la atención"
git commit -m "migración fichas zettelkasten — esporas"
```

---

## Notas sobre caracteres especiales

- Las tildes y la ñ funcionan en nombres de archivo y en enlaces — no las elimines.
- Los nombres de archivo y los títulos en el frontmatter deben coincidir exactamente, incluyendo mayúsculas, tildes y signos de puntuación.
- En anclas de párrafo (`#nombre-del-subtítulo`) usa minúsculas, guiones en lugar de espacios, y sin tildes.

---

## Límites técnicos

- GitHub tiene un límite de **100MB por archivo**. No subas audio o video de alta calidad directamente al repositorio — usa PeerTube.
- El repositorio completo tiene un límite de **1GB** en el plan gratuito de GitHub.
- Para archivos pesados de documentación de obra, considera un repositorio separado o almacenamiento externo enlazado.

---

*Protocolo generado en sesión de trabajo — junio 2026*  
*Jardín: darangoq.github.io/quartz*  
*Fediverso: anartist.org/@darangoq*
