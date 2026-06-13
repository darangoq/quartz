import os, re

# Configuración
CONTENT_DIR = "content"
ORIGEN = "quirocinesis"

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

def classify(text):
    length = len(text.strip())
    links = text.count('[[')
    if length < 80:
        return 'espora'
    if links >= 3 and length < 300:
        return 'micelio'
    if length < 150:
        return 'espora'
    if length < 600:
        return 'micelio'
    return 'rizoma'

def has_frontmatter(content):
    return content.startswith('---')

def process_file(filepath, filename):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Si ya tiene frontmatter completo con publish, omitir
    if has_frontmatter(content):
        if 'publish:' in content:
            return False, "ya tiene frontmatter completo"
        # Tiene frontmatter parcial — agregar propiedades faltantes
        # Extraer título si existe
        title_match = re.search(r'^title:\s*"?(.*?)"?\s*$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
        else:
            title = filename.replace('.md', '')
        slug = make_slug(title)
        body = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL).strip()
        estado = classify(body)
    else:
        # Sin frontmatter — construir desde el nombre del archivo
        title = filename.replace('.md', '')
        slug = make_slug(title)
        body = content.strip()
        estado = classify(body)

    needs_slug = bool(re.search(r'[áéíóúÁÉÍÓÚñÑüÜ]', title))
    slug_line = f'slug: {slug}\n' if needs_slug else ''

    frontmatter = f'''---
title: "{title}"
{slug_line}estado: {estado}
tags:
  - {estado}
publish: false
origen: {ORIGEN}
---

'''

    new_content = frontmatter + body
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, estado

# Ejecutar
updated = []
skipped = []

for filename in sorted(os.listdir(CONTENT_DIR)):
    if not filename.endswith('.md'):
        continue
    filepath = os.path.join(CONTENT_DIR, filename)
    changed, result = process_file(filepath, filename)
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
