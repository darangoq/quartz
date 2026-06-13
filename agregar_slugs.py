import os, re

# Configuración — cambia esta ruta a tu carpeta content
CONTENT_DIR = "content"

def make_slug(title):
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'a', 'É': 'e', 'Í': 'i', 'Ó': 'o', 'Ú': 'u',
        'ñ': 'n', 'Ñ': 'n', 'ü': 'u', 'Ü': 'u',
        ' ': '-', ',': '', '.': '', ':': '', ';': '',
        '¿': '', '?': '', '¡': '', '!': '', '"': '',
        "'": '', '(': '', ')': ''
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

    # Extraer título
    title_match = re.search(r'^title:\s*"?(.*?)"?\s*$', content, re.MULTILINE)
    if not title_match:
        return False, "sin título"

    title = title_match.group(1)

    # Solo procesar si tiene tildes o ñ
    if not needs_slug(title):
        return False, "no necesita slug"

    # No agregar si ya tiene slug
    if re.search(r'^slug:', content, re.MULTILINE):
        return False, "ya tiene slug"

    slug = make_slug(title)

    # Insertar slug justo después de la línea title
    new_content = re.sub(
        r'(^title:.*$)',
        f'\\1\nslug: {slug}',
        content,
        count=1,
        flags=re.MULTILINE
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, slug

# Ejecutar sobre todos los .md en content
updated = []
skipped = []

for filename in sorted(os.listdir(CONTENT_DIR)):
    if not filename.endswith('.md'):
        continue
    filepath = os.path.join(CONTENT_DIR, filename)
    changed, result = process_file(filepath)
    if changed:
        updated.append(f"  ✓ {filename} → slug: {result}")
    else:
        skipped.append(f"  — {filename} ({result})")

print(f"\nArchivos actualizados: {len(updated)}")
for line in updated:
    print(line)

print(f"\nArchivos omitidos: {len(skipped)}")
for line in skipped:
    print(line)

print("\nListo. Ahora haz git add . && git commit -m 'agregar slugs' && git push")
