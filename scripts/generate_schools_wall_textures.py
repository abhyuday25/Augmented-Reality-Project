"""
Generate ultra-clean, museum-grade textures for the Floor 1 North Back Wall
(Schools of Excellence Gallery) in VIT Vellore Virtual Museum.
Matches the architectural aesthetic of the rest of the museum:
Deep Royal Navy, Champagne Gold Trim, refined Segoe UI typography,
VIT Seal integration, and zero visual clutter.
"""

import os
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
TEXTURES_DIR = os.path.join(PROJECT_ROOT, "scripts", "generated_textures")
VIT_IMG_DIR = os.path.join(PROJECT_ROOT, "src", "assets", "images", "vit")
ASSETS_TEX_DIR = os.path.join(PROJECT_ROOT, "src", "assets", "textures")

os.makedirs(TEXTURES_DIR, exist_ok=True)
os.makedirs(ASSETS_TEX_DIR, exist_ok=True)

def get_font(size, bold=False):
    candidates = [
        "C:\\Windows\\Fonts\\segoeui.ttf" if not bold else "C:\\Windows\\Fonts\\segoeuib.ttf",
        "C:\\Windows\\Fonts\\arial.ttf" if not bold else "C:\\Windows\\Fonts\\arialbd.ttf",
        "C:\\Windows\\Fonts\\calibri.ttf" if not bold else "C:\\Windows\\Fonts\\calibrib.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

# Color Palette (Matching the rest of VIT Museum)
C_NAVY_BG = (11, 22, 42)          # Deep museum navy #0b162a
C_NAVY_CARD = (14, 28, 54)        # Card surface #0e1c36
C_CARD_HEADER = (19, 38, 74)      # Top band #13264a
C_GOLD_BORDER = (212, 175, 55)    # Refined champagne gold #d4af37
C_GOLD_ACCENT = (245, 197, 66)    # Bright gold accent #f5c542
C_TEXT_WHITE = (248, 250, 252)    # Clean off-white
C_TEXT_MUTED = (203, 213, 225)    # Slate light #cbd5e1
C_TEXT_DIM = (148, 163, 184)      # Slate dim #94a3b8
C_BADGE_BG = (10, 18, 32)         # Deep badge backing
C_BORDER_INNER = (40, 65, 110)    # Subtle inner divider

def save_image(img, filename):
    p1 = os.path.join(TEXTURES_DIR, filename)
    p2 = os.path.join(ASSETS_TEX_DIR, filename)
    img.save(p1, "PNG", optimize=True)
    img.save(p2, "PNG", optimize=True)
    print(f"Saved: {p1} and {p2}")

def draw_ornate_border(draw, rect, border_color=C_GOLD_BORDER, width=4, corner_radius=12):
    x0, y0, x1, y1 = rect
    draw.rounded_rectangle([x0, y0, x1, y1], radius=corner_radius, outline=border_color, width=width)
    # Subtle inner corner ornamental accents
    pad = 8
    draw.rounded_rectangle([x0 + pad, y0 + pad, x1 - pad, y1 - pad], radius=max(4, corner_radius - pad), outline=C_BORDER_INNER, width=1)

# 1. GRAND HEADER BANNER
def make_header_banner(filename="tex_schools_header.png", size=(2048, 240)):
    img = Image.new("RGBA", size, color=(*C_NAVY_BG, 255))
    draw = ImageDraw.Draw(img)
    
    # Outer double gold border
    draw.rounded_rectangle([8, 8, size[0] - 8, size[1] - 8], radius=8, outline=C_GOLD_BORDER, width=4)
    draw.rounded_rectangle([16, 16, size[0] - 16, size[1] - 16], radius=6, outline=(60, 90, 140), width=1)
    
    # Optional official seal on the left & right
    seal_path = os.path.join(VIT_IMG_DIR, "vit_seal_official.png")
    if os.path.exists(seal_path):
        try:
            seal = Image.open(seal_path).convert("RGBA")
            seal = seal.resize((150, 150), Image.Resampling.LANCZOS)
            img.paste(seal, (40, (size[1] - 150) // 2), seal)
            img.paste(seal, (size[0] - 190, (size[1] - 150) // 2), seal)
        except Exception as e:
            print("Seal load error:", e)
            
    # Center Title & Subtitle
    font_sub = get_font(26, bold=True)
    font_main = get_font(52, bold=True)
    font_tag = get_font(24, bold=False)
    
    draw.text((size[0] // 2, 45), "VELLORE INSTITUTE OF TECHNOLOGY", font=font_sub, fill=C_GOLD_ACCENT, anchor="mm")
    draw.text((size[0] // 2, 105), "SCHOOLS OF EXCELLENCE", font=font_main, fill=C_TEXT_WHITE, anchor="mm")
    draw.text((size[0] // 2, 165), "SCOPE  •  SENSE  •  SMEC  •  SELECT  •  MULTIDISCIPLINARY WINGS", font=font_tag, fill=C_TEXT_MUTED, anchor="mm")
    
    save_image(img, filename)

# 2. STANDARD SCHOOL GALLERY PANEL
def make_school_panel(code, title, subtitle, highlights, filename, accent_color=C_GOLD_BORDER, size=(1024, 600)):
    img = Image.new("RGBA", size, color=(*C_NAVY_CARD, 255))
    draw = ImageDraw.Draw(img)
    
    # Border
    draw_ornate_border(draw, [10, 10, size[0] - 10, size[1] - 10], border_color=accent_color, width=4, corner_radius=16)
    
    # Header Band
    draw.rounded_rectangle([14, 14, size[0] - 14, 120], radius=12, fill=C_CARD_HEADER)
    # Acronym Code (e.g. SCOPE, SMEC)
    font_code = get_font(54, bold=True)
    draw.text((size[0] // 2, 65), code, font=font_code, fill=C_GOLD_ACCENT, anchor="mm")
    
    # Full Name Subtitle
    font_title = get_font(32, bold=True)
    draw.text((size[0] // 2, 160), title, font=font_title, fill=C_TEXT_WHITE, anchor="mm")
    
    # Domain Tag
    font_sub = get_font(22, bold=False)
    draw.text((size[0] // 2, 205), subtitle, font=font_sub, fill=C_GOLD_BORDER, anchor="mm")
    
    # Thin gold accent rule
    draw.line([(size[0] // 2 - 160, 235), (size[0] // 2 + 160, 235)], fill=C_GOLD_BORDER, width=2)
    
    # Highlights (2-3 clean, spacious bullet items)
    font_bullet = get_font(24, bold=False)
    font_bullet_bold = get_font(25, bold=True)
    start_y = 275
    line_spacing = 70
    
    for i, (head, detail) in enumerate(highlights):
        cy = start_y + i * line_spacing
        # Diamond bullet
        bx = 70
        draw.polygon([(bx, cy), (bx + 8, cy - 8), (bx + 16, cy), (bx + 8, cy + 8)], fill=C_GOLD_ACCENT)
        # Text
        draw.text((bx + 32, cy - 2), head, font=font_bullet_bold, fill=C_TEXT_WHITE, anchor="lm")
        draw.text((bx + 32, cy + 24), detail, font=font_bullet, fill=C_TEXT_MUTED, anchor="lm")
        
    # Bottom Museum Prompt Button
    btn_w, btn_h = 420, 56
    bx0 = (size[0] - btn_w) // 2
    by0 = size[1] - 88
    draw.rounded_rectangle([bx0, by0, bx0 + btn_w, by0 + btn_h], radius=10, fill=C_BADGE_BG, outline=C_GOLD_BORDER, width=2)
    font_btn = get_font(22, bold=True)
    draw.text((size[0] // 2, by0 + btn_h // 2), f"CLICK TO EXPLORE {code}", font=font_btn, fill=C_GOLD_ACCENT, anchor="mm")
    
    save_image(img, filename)

# 3. CENTRAL ACADEMIC EXCELLENCE DIRECTORY PANEL
def make_central_panel(filename="tex_schools_central.png", size=(1080, 600)):
    img = Image.new("RGBA", size, color=(*C_NAVY_BG, 255))
    draw = ImageDraw.Draw(img)
    
    # Ornate double border
    draw_ornate_border(draw, [10, 10, size[0] - 10, size[1] - 10], border_color=C_GOLD_ACCENT, width=5, corner_radius=18)
    
    # Header Band
    draw.rounded_rectangle([15, 15, size[0] - 15, 125], radius=14, fill=C_CARD_HEADER)
    
    # VIT Seal in center
    seal_path = os.path.join(VIT_IMG_DIR, "vit_seal_official.png")
    if os.path.exists(seal_path):
        try:
            seal = Image.open(seal_path).convert("RGBA")
            seal = seal.resize((96, 96), Image.Resampling.LANCZOS)
            img.paste(seal, ((size[0] - 96) // 2, 20), seal)
        except Exception as e:
            print("Central seal error:", e)
            
    # Title
    font_title = get_font(34, bold=True)
    draw.text((size[0] // 2, 165), "ACADEMIC EXCELLENCE", font=font_title, fill=C_GOLD_ACCENT, anchor="mm")
    
    font_sub = get_font(23, bold=False)
    draw.text((size[0] // 2, 210), "15+ Multidisciplinary Academic Schools", font=font_sub, fill=C_TEXT_WHITE, anchor="mm")
    
    # Divider
    draw.line([(size[0] // 2 - 200, 240), (size[0] // 2 + 200, 240)], fill=C_GOLD_BORDER, width=2)
    
    # 3 Stat Cards in a row
    stat_cards = [
        ("NIRF #1", "Private Engineering in India"),
        ("ABET (USA)", "International Quality Benchmarks"),
        ("FFCS FREEDOM", "Fully Flexible Credit System")
    ]
    card_w = 310
    card_h = 135
    spacing = (size[0] - 60 - 3 * card_w) // 2
    for idx, (stitle, sdesc) in enumerate(stat_cards):
        cx = 30 + idx * (card_w + spacing)
        cy = 265
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=10, fill=C_CARD_HEADER, outline=C_BORDER_INNER, width=1)
        font_st = get_font(24, bold=True)
        draw.text((cx + card_w // 2, cy + 42), stitle, font=font_st, fill=C_GOLD_ACCENT, anchor="mm")
        font_sd = get_font(18, bold=False)
        draw.text((cx + card_w // 2, cy + 85), sdesc, font=font_sd, fill=C_TEXT_MUTED, anchor="mm")
        
    # Bottom Button
    btn_w, btn_h = 440, 60
    bx0 = (size[0] - btn_w) // 2
    by0 = size[1] - 95
    draw.rounded_rectangle([bx0, by0, bx0 + btn_w, by0 + btn_h], radius=12, fill=C_GOLD_ACCENT, outline=C_GOLD_BORDER, width=2)
    font_btn = get_font(23, bold=True)
    draw.text((size[0] // 2, by0 + btn_h // 2), "VIEW ALL 15 SCHOOLS", font=font_btn, fill=(11, 22, 42), anchor="mm")
    
    save_image(img, filename)

# 4. FOOTER RIBBON
def make_footer_ribbon(filename="tex_schools_footer.png", size=(2048, 140)):
    img = Image.new("RGBA", size, color=(*C_NAVY_BG, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rounded_rectangle([6, 6, size[0] - 6, size[1] - 6], radius=6, outline=C_BORDER_INNER, width=2)
    
    font_head = get_font(22, bold=True)
    draw.text((size[0] // 2, 42), "MULTIDISCIPLINARY ACADEMIC WINGS", font=font_head, fill=C_GOLD_ACCENT, anchor="mm")
    
    font_schools = get_font(24, bold=False)
    text = "SBST (BioSciences)   •   SCHEME (Chemical)   •   SCE (Civil)   •   SAS (Advanced Sciences)   •   VITBS (Business)   •   V-SPARC (Architecture)"
    draw.text((size[0] // 2, 92), text, font=font_schools, fill=C_TEXT_WHITE, anchor="mm")
    
    save_image(img, filename)

def main():
    print("Generating museum-grade Schools Gallery textures...")
    
    # 1. Header
    make_header_banner()
    
    # 2. SMEC Panel
    make_school_panel(
        code="SMEC",
        title="School of Mechanical Engineering",
        subtitle="Automotive, Mechatronics, Aerospace & Robotics",
        highlights=[
            ("Automotive Research Centre (ARC):", "Vehicle dynamometers, wind tunnel & emissions cells."),
            ("Pravega Racing & Formula Student:", "Podium ranking international EV & combustion racecars."),
            ("Additive 3D Printing & Dyno Labs:", "Metal additive manufacturing & automated CAD/CAM.")
        ],
        filename="tex_panel_smec.png"
    )
    
    # 3. SCOPE Panel
    make_school_panel(
        code="SCOPE",
        title="School of Computer Science & Engineering",
        subtitle="Artificial Intelligence, Computing & Data Science",
        highlights=[
            ("High-Performance Computing:", "NVIDIA supercomputing cluster for frontier deep learning."),
            ("12,000+ Scholars & Global Reach:", "1,500+ Scopus research publications annually."),
            ("ABET International Accreditation:", "Curriculum benchmarked to global tech alliances.")
        ],
        filename="tex_panel_scope.png"
    )
    
    # 4. Central Directory Panel
    make_central_panel()
    
    # 5. SENSE Panel
    make_school_panel(
        code="SENSE",
        title="School of Electronics Engineering",
        subtitle="Semiconductors, 5G/6G Networks & Nanoelectronics",
        highlights=[
            ("Silicon VLSI Design Centre:", "Cadence, Synopsys & Mentor EDA design suites."),
            ("5G/6G RF & Microwave Labs:", "Next-generation wireless telecommunication systems."),
            ("Microchip Tape-Outs:", "Direct physical silicon tape-outs by undergraduate scholars.")
        ],
        filename="tex_panel_sense.png"
    )
    
    # 6. SELECT & SITE Panel
    make_school_panel(
        code="SELECT & SITE",
        title="Electrical & Information Systems",
        subtitle="Clean Microgrids, EV Powertrains & Cybersecurity",
        highlights=[
            ("Schneider Electric Smart Grid Lab:", "Advanced microgrid simulation & clean energy testbeds."),
            ("EV Inverters & Power Electronics:", "High-efficiency motor drives & battery management."),
            ("Enterprise Cloud & Blockchain:", "Applied cybersecurity, networks & data architectures.")
        ],
        filename="tex_panel_select.png"
    )
    
    # 7. Footer
    make_footer_ribbon()
    
    print("All Schools Gallery textures successfully generated!")

if __name__ == "__main__":
    main()
