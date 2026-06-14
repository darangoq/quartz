import os, re

# Configuración
CONTENT_DIR = "content"

COMENTARIOS_BLOQUE_VIEJO = """

---
*¿Quieres comentar? Responde desde el fediverso.*

<div id="mastodon-comments" data-status-id=""></div>
"""

COMENTARIOS_BLOQUE_NUEVO = """

<!-- 
---
*¿Quieres comentar? Responde desde el fediverso.*

<div id="mastodon-comments" data-status-id=""></div>
-->
"""

def make_slug(title):
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'a', 'É': 'e', 'Í': 'i', 'Ó': 'o', 'Ú': 'u',
        'ñ': 'n', 'Ñ': 'n', 'ü': 'u', 'Ü': 'u',
        ' ': '-', ',': '', '.': '', ':': '', ';': '',
        '¿': '', '?': '', '¡': '', '!': '', '"': '',
        "'": '', '(': '', ')': '', '/': '-'
    }
    slug = title.lower()
    for char, replacement in replacements.items():
        slug = slug.replace(char, replacement)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')

def needs_slug(title):
    return bool(re.search(r'[áéíóúÁÉÍÓÚñÑüÜ]', title))

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Solo archivos con frontmatter
    if not content.startswith('---'):
        return False, "sin frontmatter"

    # Separar frontmatter del cuerpo
    parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return False, "frontmatter malformado"

    frontmatter = parts[1]
    body = parts[2]

    changes = []

    # 1. Extraer título
    title_match = re.search(r'^title:\s*"?(.*?)"?\s*$', frontmatter, re.MULTILINE)
    if not title_match:
        return False, "sin título"
    title = title_match.group(1).strip()

    # 2. Agregar slug si tiene tildes y no lo tiene
    if needs_slug(title) and not re.search(r'^slug:', frontmatter, re.MULTILINE):
        slug = make_slug(title)
        frontmatter = re.sub(
            r'(^title:.*$)',
            f'\\1\nslug: {slug}',
            frontmatter,
            count=1,
            flags=re.MULTILINE
        )
        changes.append(f"slug: {slug}")

    # 3. Agregar toot_id si no existe
    if not re.search(r'^toot_id:', frontmatter, re.MULTILINE):
        frontmatter = frontmatter.rstrip() + '\ntoot_id: ""\n'
        changes.append("toot_id")

    # 4. Reemplazar bloque viejo por nuevo comentado, o agregar si no existe
    if COMENTARIOS_BLOQUE_VIEJO.strip() in body:
        body = body.replace(COMENTARIOS_BLOQUE_VIEJO.strip(), COMENTARIOS_BLOQUE_NUEVO.strip())
        changes.append("bloque comentarios actualizado")
    elif 'mastodon-comments' not in body:
        body = body.rstrip() + COMENTARIOS_BLOQUE_NUEVO
        changes.append("bloque comentarios agregado")

    # Reconstruir archivo
    new_content = f'---{frontmatter}---{body}'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, ", ".join(changes)

# Ejecutar
updated = []
skipped = []

for filename in sorted(os.listdir(CONTENT_DIR)):
    if not filename.endswith('.md'):
        continue
    # Omitir archivos en subcarpetas — solo raíz de content
    filepath = os.path.join(CONTENT_DIR, filename)
    if not os.path.isfile(filepath):
        continue
    changed, result = process_file(filepath)
    if changed:
        updated.append(f"  ✓ {filename} → {result}")
    else:
        skipped.append(f"  — {filename} ({result})")

print(f"\nArchivos actualizados: {len(updated)}")
for line in updated:
    print(line)

print(f"\nArchivos omitidos: {len(skipped)}")
for line in skipped:
    print(line)

print("\nListo. Revisa algunos archivos antes de hacer git push.")
