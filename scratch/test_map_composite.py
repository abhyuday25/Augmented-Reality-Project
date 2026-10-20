import os
from PIL import Image, ImageDraw, ImageFont

VIT_IMG_DIR = os.path.abspath("src/assets/images/vit")
aerial_path = os.path.join(VIT_IMG_DIR, "vit_campus_aerial.jpg")

def get_font(size, bold=False):
    candidates = [
        "C:\\Windows\\Fonts\\segoeui.ttf" if not bold else "C:\\Windows\\Fonts\\segoeuib.ttf",
        "C:\\Windows\\Fonts\\arial.ttf" if not bold else "C:\\Windows\\Fonts\\arialbd.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def create_campus_model_map_texture(output_path="scratch/test_campus_map.png", size=(2048, 1536)):
    # Create canvas
    canvas = Image.new("RGBA", size, color=(10, 20, 40, 255))
    draw = ImageDraw.Draw(canvas)

    # 1. Outer decorative architectural border
    draw.rectangle([12, 12, size[0] - 12, size[1] - 12], outline=(212, 175, 55), width=4)
    draw.rectangle([24, 24, size[0] - 24, size[1] - 24], outline=(59, 130, 246), width=2)

    # 2. Top Title Header
    header_h = 100
    draw.rectangle([26, 26, size[0] - 26, 26 + header_h], fill=(15, 30, 65, 255))
    draw.line([(26, 26 + header_h), (size[0] - 26, 26 + header_h)], fill=(212, 175, 55), width=3)
    draw.text((size[0] // 2, 55), "VIT VELLORE — 372-ACRE CAMPUS MASTER PLAN & ACADEMIC ZONES",
              font=get_font(38, bold=True), fill=(255, 255, 255), anchor="mm")
    draw.text((size[0] // 2, 95), "Interactive Architectural Diorama • Technology Tower • SJT • Central Library • Administration",
              font=get_font(20, bold=False), fill=(212, 175, 55), anchor="mm")

    # 3. Main Center: Overhead Aerial Image
    # Leave space on the left and right for inset cards of key blocks
    margin_top = 140
    margin_bottom = 40
    card_w = 340
    main_x1 = 30 + card_w + 20
    main_x2 = size[0] - 30 - card_w - 20
    main_w = main_x2 - main_x1
    main_h = size[1] - margin_top - margin_bottom

    if os.path.exists(aerial_path):
        with Image.open(aerial_path) as aerial:
            # Resize aerial to cover main area
            resized = aerial.resize((main_w, main_h), Image.Resampling.LANCZOS)
            canvas.paste(resized, (main_x1, margin_top))

    # Border around aerial photo
    draw.rectangle([main_x1, margin_top, main_x2, margin_top + main_h], outline=(212, 175, 55), width=3)

    # 4. Inset Photo Cards of Key Blocks
    cards = [
        # Left side cards
        ("Technology Tower (TT)", "Computing & Engg", os.path.join(VIT_IMG_DIR, "vit_technology_tower.jpg"), 30, margin_top, card_w, (main_h - 20) // 2),
        ("Silver Jubilee Tower", "Research & PG Complex", os.path.join(VIT_IMG_DIR, "vit_sjt_academic.jpg"), 30, margin_top + (main_h - 20) // 2 + 20, card_w, (main_h - 20) // 2),
        # Right side cards
        ("Dr. M.G.R. Central Block", "Main Administration", os.path.join(VIT_IMG_DIR, "vit_admin_building.jpg"), size[0] - 30 - card_w, margin_top, card_w, (main_h - 20) // 2),
        ("Periyar Central Library", "Resource & Digital Center", os.path.join(VIT_IMG_DIR, "vit_library.jpg"), size[0] - 30 - card_w, margin_top + (main_h - 20) // 2 + 20, card_w, (main_h - 20) // 2),
    ]

    for title, subtitle, img_p, cx, cy, cw, ch in cards:
        # Card background
        draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=12, fill=(14, 25, 50, 255), outline=(212, 175, 55), width=2)
        # Inset image
        img_h = ch - 65
        if os.path.exists(img_p):
            with Image.open(img_p) as c_img:
                c_resized = c_img.resize((cw - 12, img_h - 10), Image.Resampling.LANCZOS)
                canvas.paste(c_resized, (cx + 6, cy + 6))
        draw.rectangle([cx + 6, cy + 6, cx + cw - 6, cy + img_h - 4], outline=(70, 95, 140), width=1)
        # Text label
        draw.text((cx + cw // 2, cy + ch - 42), title, font=get_font(20, bold=True), fill=(255, 255, 255), anchor="mm")
        draw.text((cx + cw // 2, cy + ch - 18), subtitle, font=get_font(15), fill=(212, 175, 55), anchor="mm")

    # Compass Rose & Scale Bar in main area
    compass_x = main_x2 - 70
    compass_y = margin_top + 70
    draw.ellipse([compass_x - 40, compass_y - 40, compass_x + 40, compass_y + 40], fill=(10, 20, 40, 200), outline=(212, 175, 55), width=2)
    draw.polygon([(compass_x, compass_y - 32), (compass_x + 8, compass_y), (compass_x - 8, compass_y)], fill=(239, 68, 68))
    draw.polygon([(compass_x, compass_y + 32), (compass_x + 8, compass_y), (compass_x - 8, compass_y)], fill=(255, 255, 255))
    draw.text((compass_x, compass_y - 36), "N", font=get_font(14, bold=True), fill=(239, 68, 68), anchor="mb")

    canvas.save(output_path)
    print("Saved:", output_path, os.path.getsize(output_path), "bytes")

create_campus_model_map_texture()
