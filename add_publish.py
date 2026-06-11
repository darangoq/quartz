import os

content_dir = "content"

for filename in os.listdir(content_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(content_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'publish:' not in content:
            content = content.replace('---\n', '---\npublish: true\n', 1)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Actualizado: {filename}")

print("Listo.")