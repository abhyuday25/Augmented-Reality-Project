import os, sys
from PIL import Image, ImageDraw, ImageFont

print("Python version:", sys.version)
VIT_IMG_DIR = os.path.abspath("src/assets/images/vit")
aerial_path = os.path.join(VIT_IMG_DIR, "vit_campus_aerial.jpg")
foliage_path = os.path.join(VIT_IMG_DIR, "botanical_foliage.jpg")

print("Aerial exists:", os.path.exists(aerial_path))
print("Foliage exists:", os.path.exists(foliage_path))

with Image.open(aerial_path) as img:
    print("Aerial size:", img.size)

with Image.open(foliage_path) as img:
    print("Foliage size:", img.size)
