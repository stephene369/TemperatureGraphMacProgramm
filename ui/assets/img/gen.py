from PIL import Image
import os

# Dossier courant (là où tu exécutes le script)
BASE_DIR = os.getcwd()

SOURCE_PNG = os.path.join(BASE_DIR, "logo.png")
ICON_1024 = os.path.join(BASE_DIR, "icon_1024.png")
ICONSET_DIR = os.path.join(BASE_DIR, "ISCGraph.iconset")

if not os.path.exists(SOURCE_PNG):
    raise FileNotFoundError("logo.png introuvable dans le dossier courant")

# Charger l'image source
img = Image.open(SOURCE_PNG).convert("RGBA")

# Assurer une image carrée (padding transparent si besoin)
w, h = img.size
side = max(w, h)
if w != h:
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    square.paste(img, ((side - w) // 2, (side - h) // 2))
    img = square

# Générer le master 1024x1024
img_1024 = img.resize((1024, 1024), Image.LANCZOS)
img_1024.save(ICON_1024, "PNG")

# Créer le dossier iconset
os.makedirs(ICONSET_DIR, exist_ok=True)

# Tailles requises par macOS
sizes = [
    ("icon_16x16.png", 16),
    ("icon_16x16@2x.png", 32),
    ("icon_32x32.png", 32),
    ("icon_32x32@2x.png", 64),
    ("icon_128x128.png", 128),
    ("icon_128x128@2x.png", 256),
    ("icon_256x256.png", 256),
    ("icon_256x256@2x.png", 512),
    ("icon_512x512.png", 512),
    ("icon_512x512@2x.png", 1024),
]

# Génération des fichiers
for name, size in sizes:
    out_path = os.path.join(ICONSET_DIR, name)
    img_1024.resize((size, size), Image.LANCZOS).save(out_path, "PNG")

print("✅ Génération terminée")
print(" - icon_1024.png créé")
print(" - Dossier ISCGraph.iconset prêt pour iconutil (macOS)")
