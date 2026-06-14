import subprocess
from datetime import datetime

# Generar nombre del commit con fecha y hora
commit_name = datetime.now().strftime("%Y%m%d%H%M")

# Ejecutar los tres comandos
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", commit_name], check=True)
subprocess.run(["git", "push"], check=True)

print(f"\nPush completado: {commit_name}")