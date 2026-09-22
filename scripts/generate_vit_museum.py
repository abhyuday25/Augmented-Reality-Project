"""
VIT Vellore Virtual Museum - 3D Procedural GLB Generator
Generates high quality textures, architectural geometry, exhibition displays,
central sculpture, miniature campus model, interactive nodes, and exports vit_vellore_virtual_museum.glb.
"""

import os
import sys
import math
import struct
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import trimesh
import pygltflib
from pygltflib import (
    GLTF2, Scene, Node, Mesh, Primitive, Attributes,
    Buffer, BufferView, Accessor, Material, PbrMetallicRoughness,
    Texture, Image as GLTFImage, TextureInfo,
    ARRAY_BUFFER, ELEMENT_ARRAY_BUFFER, FLOAT, UNSIGNED_INT, UNSIGNED_SHORT
)

# Output paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "src", "assets")
MODELS_DIR = os.path.join(ASSETS_DIR, "models")
TEXTURES_DIR = os.path.join(SCRIPT_DIR, "generated_textures")
OUTPUT_GLB_ROOT = os.path.join(PROJECT_ROOT, "vit_vellore_virtual_museum.glb")
OUTPUT_GLB_ASSETS = os.path.join(MODELS_DIR, "vit_vellore_virtual_museum.glb")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(TEXTURES_DIR, exist_ok=True)

print("--- Starting VIT Vellore Virtual Museum GLB Generator ---")

# ==============================================================================
# 1. TEXTURE GENERATION WITH PILLOW
# ==============================================================================

def get_font(size, bold=False):
    # Try common Windows TrueType fonts, fallback to default
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

def create_marble_floor_texture(filename="tex_marble_floor.png", size=(1024, 1024)):
    img = Image.new("RGB", size, color=(242, 243, 245))
    draw = ImageDraw.Draw(img)
    # Add subtle large tile grid
    tile_size = 256
    for x in range(0, size[0], tile_size):
        draw.line([(x, 0), (x, size[1])], fill=(215, 218, 222), width=3)
    for y in range(0, size[1], tile_size):
        draw.line([(0, y), (size[0], y)], fill=(215, 218, 222), width=3)
    
    # Add subtle darker border trim pattern
    draw.rectangle([10, 10, size[0]-10, size[1]-10], outline=(180, 185, 195), width=4)
    draw.rectangle([20, 20, size[0]-20, size[1]-20], outline=(30, 41, 59), width=2)
    
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path, quality=92)
    return path

def create_facade_title_texture(filename="tex_facade_title.png", size=(2048, 512)):
    img = Image.new("RGBA", size, color=(15, 23, 42, 255))
    draw = ImageDraw.Draw(img)
    
    # Gold & blue border lines
    draw.rectangle([8, 8, size[0]-8, size[1]-8], outline=(212, 175, 55, 255), width=6)
    draw.rectangle([16, 16, size[0]-16, size[1]-16], outline=(59, 130, 246, 180), width=2)
    
    f_title = get_font(120, bold=True)
    f_sub = get_font(52, bold=True)
    f_motto = get_font(32, bold=False)
    
    # VIT VELLORE
    title_text = "VELLORE INSTITUTE OF TECHNOLOGY"
    draw.text((size[0]//2, 120), title_text, font=f_sub, fill=(212, 175, 55), anchor="mm")
    
    main_text = "VIT VELLORE"
    draw.text((size[0]//2, 240), main_text, font=f_title, fill=(255, 255, 255), anchor="mm")
    
    sub_text = "VIRTUAL HERITAGE & INNOVATION MUSEUM"
    draw.text((size[0]//2, 370), sub_text, font=f_sub, fill=(147, 197, 253), anchor="mm")
    
    motto = "A Place to Learn, A Chance to Grow"
    draw.text((size[0]//2, 445), motto, font=f_motto, fill=(203, 213, 225), anchor="mm")
    
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path

def create_welcome_wall_texture(filename="tex_welcome_wall.png", size=(2048, 1024)):
    img = Image.new("RGBA", size, color=(10, 25, 47, 255))
    draw = ImageDraw.Draw(img)
    
    # Geometric architectural background pattern
    for x in range(0, size[0], 64):
        draw.line([(x, 0), (x, size[1])], fill=(16, 38, 70), width=1)
    for y in range(0, size[1], 64):
        draw.line([(0, y), (size[0], y)], fill=(16, 38, 70), width=1)
        
    draw.rectangle([20, 20, size[0]-20, size[1]-20], outline=(212, 175, 55, 255), width=8)
    draw.rectangle([36, 36, size[0]-36, size[1]-36], outline=(59, 130, 246, 200), width=3)
    
    # Official VIT Logo Emblem Box
    emblem_box = [size[0]//2 - 160, 60, size[0]//2 + 160, 310]
    draw.rounded_rectangle(emblem_box, radius=20, fill=(15, 33, 64), outline=(212, 175, 55), width=4)
    
    # Check if dedicated logo emblem texture exists to paste inside
    logo_path = os.path.join(TEXTURES_DIR, "tex_vit_logo_emblem.png")
    if os.path.exists(logo_path):
        try:
            logo_img = Image.open(logo_path).convert("RGBA").resize((220, 220), Image.Resampling.LANCZOS)
            img.paste(logo_img, (size[0]//2 - 110, 75), logo_img)
        except Exception:
            f_logo = get_font(70, bold=True)
            draw.text((size[0]//2, 160), "VIT", font=f_logo, fill=(255, 215, 0), anchor="mm")
            draw.text((size[0]//2, 235), "VELLORE", font=get_font(28, bold=True), fill=(147, 197, 253), anchor="mm")
    else:
        f_logo = get_font(70, bold=True)
        draw.text((size[0]//2, 160), "VIT", font=f_logo, fill=(255, 215, 0), anchor="mm")
        draw.text((size[0]//2, 235), "VELLORE", font=get_font(28, bold=True), fill=(147, 197, 253), anchor="mm")
    
    f_h1 = get_font(95, bold=True)
    f_h2 = get_font(48, bold=True)
    f_desc = get_font(32, bold=False)
    
    draw.text((size[0]//2, 380), "WELCOME TO VIT VELLORE", font=f_h1, fill=(255, 255, 255), anchor="mm")
    draw.text((size[0]//2, 480), "A Journey Through Excellence, Innovation and Impact", font=f_h2, fill=(212, 175, 55), anchor="mm")
    
    desc_lines = [
        "Established in 1984 as Vellore Engineering College, VIT has transformed into an Institution of Eminence",
        "and a premier destination for world-class technical education, research, and holistic student development.",
        "Explore university history, transformative innovations, celebrated achievements, and vibrant campus life.",
    ]
    y_pos = 610
    for line in desc_lines:
        draw.text((size[0]//2, y_pos), line, font=f_desc, fill=(226, 232, 240), anchor="mm")
        y_pos += 50
        
    draw.rounded_rectangle([size[0]//2 - 320, 830, size[0]//2 + 320, 910], radius=15, fill=(30, 58, 138), outline=(212, 175, 55), width=2)
    f_tag = get_font(34, bold=True)
    draw.text((size[0]//2, 870), "PRESS [WASD] TO WALK | MOUSE TO LOOK", font=f_tag, fill=(255, 255, 255), anchor="mm")

    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path

def create_banner_texture(title, subtitle="", filename="tex_banner.png", size=(1536, 384), bg_color=(15, 30, 60)):
    img = Image.new("RGBA", size, color=(*bg_color, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([8, 8, size[0]-8, size[1]-8], outline=(212, 175, 55), width=5)
    draw.rectangle([16, 16, size[0]-16, size[1]-16], outline=(96, 165, 250), width=2)
    
    f_title = get_font(72, bold=True)
    f_sub = get_font(34, bold=False)
    
    draw.text((size[0]//2, 140), title, font=f_title, fill=(255, 255, 255), anchor="mm")
    if subtitle:
        draw.text((size[0]//2, 250), subtitle, font=f_sub, fill=(212, 175, 55), anchor="mm")
        
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path

def create_infopanel_texture(title, year, bullets, filename="tex_panel.png", size=(1024, 1024), accent_color=(59, 130, 246)):
    img = Image.new("RGBA", size, color=(15, 23, 42, 255))
    draw = ImageDraw.Draw(img)
    
    # Header bar
    draw.rectangle([0, 0, size[0], 180], fill=(10, 30, 65))
    draw.rectangle([0, 180, size[0], 188], fill=accent_color)
    draw.rectangle([12, 12, size[0]-12, size[1]-12], outline=(212, 175, 55), width=3)
    
    f_yr = get_font(42, bold=True)
    f_title = get_font(56, bold=True)
    f_bullet = get_font(32, bold=False)
    
    draw.text((50, 60), year, font=f_yr, fill=(212, 175, 55))
    draw.text((50, 125), title, font=f_title, fill=(255, 255, 255))
    
    # Graphic preview card placeholder
    draw.rounded_rectangle([50, 230, size[0]-50, 520], radius=12, fill=(30, 41, 59), outline=(71, 85, 105), width=2)
    f_ill = get_font(36, bold=True)
    draw.text((size[0]//2, 360), f"[ Visual Display: {title} ]", font=f_ill, fill=(148, 163, 184), anchor="mm")
    draw.text((size[0]//2, 420), "VIT Vellore Archives & Media", font=get_font(26), fill=(100, 116, 139), anchor="mm")
    
    y = 570
    for b in bullets:
        draw.ellipse([55, y+10, 67, y+22], fill=accent_color)
        draw.text((85, y), b, font=f_bullet, fill=(226, 232, 240))
        y += 65
        
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path

def create_achievements_wall_texture(filename="tex_achievements_wall.png", size=(2048, 1024)):
    img = Image.new("RGBA", size, color=(8, 20, 40, 255))
    draw = ImageDraw.Draw(img)
    
    # Gold & Navy Trim
    draw.rectangle([16, 16, size[0]-16, size[1]-16], outline=(212, 175, 55), width=8)
    draw.rectangle([32, 32, size[0]-32, size[1]-32], outline=(37, 99, 235), width=3)
    
    f_head = get_font(80, bold=True)
    f_sub = get_font(38, bold=True)
    draw.text((size[0]//2, 100), "WALL OF ACHIEVEMENTS", font=f_head, fill=(255, 255, 255), anchor="mm")
    draw.text((size[0]//2, 170), "Recognizing Excellence, Innovation & Institutional Impact", font=f_sub, fill=(212, 175, 55), anchor="mm")
    
    cards = [
        ("Institutional Eminence", "NIRF & Global Rankings", "Ranked consistently among top engineering and research universities in India.", (30, 58, 138)),
        ("Research Impact", "High-Impact Publications", "Extensive international journal publications, funded research, and high citation index.", (15, 80, 100)),
        ("Innovation & Patents", "VITTBI & Technology Startups", "Over 150+ technology startups incubated and hundreds of published patents.", (67, 35, 110)),
        ("Student Excellence", "Hackathons & Formula Student", "National and international awards in robotics, computing, and motorsport engineering.", (110, 60, 20)),
    ]
    
    card_w = (size[0] - 120) // 2
    card_h = 320
    positions = [
        (50, 240),
        (size[0]//2 + 10, 240),
        (50, 600),
        (size[0]//2 + 10, 600)
    ]
    
    for (title, cat, desc, col), (cx, cy) in zip(cards, positions):
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=16, fill=(15, 30, 60), outline=(212, 175, 55), width=3)
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + 70], radius=16, fill=col)
        draw.text((cx + 25, cy + 35), cat, font=get_font(28, bold=True), fill=(212, 175, 55), anchor="lm")
        draw.text((cx + 25, cy + 115), title, font=get_font(38, bold=True), fill=(255, 255, 255), anchor="lm")
        
        # Wrapped description
        f_cdesc = get_font(26)
        words = desc.split()
        lines = []
        cur = ""
        for w in words:
            test = cur + (" " if cur else "") + w
            if len(test) > 42:
                lines.append(cur)
                cur = w
            else:
                cur = test
        if cur:
            lines.append(cur)
            
        ly = cy + 175
        for l in lines:
            draw.text((cx + 25, ly), l, font=f_cdesc, fill=(203, 213, 225))
            ly += 36
            
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path

def create_student_life_texture(filename="tex_student_life.png", size=(2048, 1024)):
    img = Image.new("RGBA", size, color=(12, 22, 38, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([16, 16, size[0]-16, size[1]-16], outline=(59, 130, 246), width=6)
    draw.rectangle([30, 30, size[0]-30, size[1]-30], outline=(212, 175, 55), width=2)
    
    draw.text((size[0]//2, 90), "LIFE AT VIT", font=get_font(80, bold=True), fill=(255, 255, 255), anchor="mm")
    draw.text((size[0]//2, 160), "Culture, Innovation, Sports & Campus Camaraderie", font=get_font(36, bold=False), fill=(212, 175, 55), anchor="mm")
    
    photo_cards = [
        ("Riviera Cultural Fest", "Asia's Premier College Festival", (180, 40, 70)),
        ("graVITas Tech Fest", "Innovation, Hackathons & Tech", (30, 100, 170)),
        ("Clubs & Student Chapters", "100+ Active Chapters (IEEE, ACM...)", (40, 130, 90)),
        ("Sports & Athletic Meets", "Olympic standard facilities", (170, 90, 20)),
        ("Research & Hackathons", "24hr Coding & Smart Solutions", (90, 40, 150)),
        ("Campus Life & Graduation", "Lifelong friendships & memories", (50, 70, 120)),
    ]
    
    cols = 3
    rows = 2
    margin_x = 50
    margin_y = 220
    pw = (size[0] - margin_x*2 - (cols-1)*30) // cols
    ph = (size[1] - margin_y - 50 - (rows-1)*30) // rows
    
    for idx, (title, sub, col) in enumerate(photo_cards):
        r = idx // cols
        c = idx % cols
        px = margin_x + c * (pw + 30)
        py = margin_y + r * (ph + 30)
        
        draw.rounded_rectangle([px, py, px + pw, py + ph], radius=14, fill=(20, 32, 54), outline=(147, 197, 253), width=2)
        draw.rounded_rectangle([px+8, py+8, px + pw-8, py + ph - 80], radius=10, fill=col)
        
        draw.text((px + pw//2, py + (ph-80)//2), f"[ {title} ]", font=get_font(30, bold=True), fill=(255, 255, 255), anchor="mm")
        draw.text((px + pw//2, py + ph - 50), title, font=get_font(28, bold=True), fill=(255, 255, 255), anchor="mm")
        draw.text((px + pw//2, py + ph - 22), sub, font=get_font(20), fill=(212, 175, 55), anchor="mm")
        
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path

def create_screen_texture(screen_title, subtitle, bullets, filename="tex_screen.png", size=(1024, 768)):
    img = Image.new("RGBA", size, color=(5, 12, 28, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([10, 10, size[0]-10, size[1]-10], outline=(59, 130, 246), width=5)
    draw.rectangle([0, 0, size[0], 120], fill=(15, 35, 80))
    
    draw.text((size[0]//2, 50), screen_title, font=get_font(50, bold=True), fill=(255, 255, 255), anchor="mm")
    draw.text((size[0]//2, 95), subtitle, font=get_font(24), fill=(212, 175, 55), anchor="mm")
    
    y = 180
    for b in bullets:
        draw.rounded_rectangle([50, y, size[0]-50, y+85], radius=10, fill=(15, 25, 50), outline=(71, 85, 105), width=2)
        draw.text((80, y+42), b, font=get_font(28), fill=(226, 232, 240), anchor="lm")
        draw.text((size[0]-80, y+42), "›", font=get_font(38, bold=True), fill=(59, 130, 246), anchor="rm")
        y += 105
        
    draw.rounded_rectangle([size[0]//2 - 180, size[1]-90, size[0]//2 + 180, size[1]-30], radius=15, fill=(37, 99, 235))
    draw.text((size[0]//2, size[1]-60), "INTERACTIVE SCREEN", font=get_font(26, bold=True), fill=(255, 255, 255), anchor="mm")
    
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path

def create_campus_model_map_texture(filename="tex_campus_map.png", size=(1024, 1024)):
    img = Image.new("RGBA", size, color=(35, 45, 40, 255))
    draw = ImageDraw.Draw(img)
    
    # Green lawns
    draw.rectangle([40, 40, size[0]-40, size[1]-40], fill=(45, 80, 55))
    
    # Campus roads
    road_col = (100, 105, 115)
    # Main ring road
    draw.ellipse([100, 100, size[0]-100, size[1]-100], outline=road_col, width=32)
    # Cross avenues
    draw.line([(size[0]//2, 100), (size[0]//2, size[1]-100)], fill=road_col, width=28)
    draw.line([(100, size[1]//2), (size[0]-100, size[1]//2)], fill=road_col, width=28)
    
    # Building footprint markers
    bldgs = [
        (size[0]//2 - 120, 200, 240, 120, "TECHNOLOGY TOWER (TT)", (20, 40, 80)),
        (size[0]//2 - 130, size[1] - 340, 260, 140, "SILVER JUBILEE TOWER (SJT)", (25, 45, 90)),
        (180, size[1]//2 - 70, 150, 140, "MAIN BUILDING (MB)", (30, 50, 95)),
        (size[0] - 330, size[1]//2 - 70, 150, 140, "ANNA AUDITORIUM", (120, 60, 30)),
    ]
    for bx, by, bw, bh, name, col in bldgs:
        draw.rectangle([bx, by, bx+bw, by+bh], fill=col, outline=(212, 175, 55), width=3)
        draw.text((bx + bw//2, by + bh//2), name, font=get_font(18, bold=True), fill=(255, 255, 255), anchor="mm")
        
def create_vit_logo_emblem_texture(filename="tex_vit_logo_emblem.png", size=(2048, 2048)):
    path = os.path.join(TEXTURES_DIR, filename)
    # Check if a pre-generated high-fidelity emblem exists
    if os.path.exists(path):
        return path
        
    img = Image.new("RGBA", size, color=(10, 25, 47, 255))
    draw = ImageDraw.Draw(img)
    cx, cy = size[0] // 2, size[1] // 2

    # Concentric background rings
    for r in range(size[0]//2 - 20, 100, -20):
        alpha = int(30 + (1.0 - r / (size[0]/2)) * 40)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(12, 32, 64, alpha), outline=(20, 50, 95, 120), width=1)

    # Outer ornate gold double ring
    draw.ellipse([50, 50, size[0]-50, size[1]-50], outline=(212, 175, 55, 255), width=18)
    draw.ellipse([80, 80, size[0]-80, size[1]-80], outline=(255, 215, 0, 180), width=6)
    draw.ellipse([105, 105, size[0]-105, size[1]-105], outline=(59, 130, 246, 220), width=4)

    # Decorative perimeter dots / studs
    num_studs = 48
    for i in range(num_studs):
        angle = (2 * math.pi / num_studs) * i
        sx = cx + int((size[0]//2 - 65) * math.cos(angle))
        sy = cy + int((size[1]//2 - 65) * math.sin(angle))
        draw.ellipse([sx-7, sy-7, sx+7, sy+7], fill=(255, 215, 0), outline=(180, 140, 30), width=2)

    # Inner Navy Shield / Disc background
    inner_r = size[0]//2 - 130
    draw.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r], fill=(6, 18, 38), outline=(212, 175, 55), width=8)

    # University Name Header Banner (Upper Arc)
    f_univ = get_font(56, bold=True)
    f_sub = get_font(36, bold=True)
    f_motto = get_font(40, bold=True)
    f_estd = get_font(34, bold=True)

    draw.text((cx, 280), "VELLORE INSTITUTE OF TECHNOLOGY", font=f_univ, fill=(255, 215, 0), anchor="mm")
    draw.text((cx, 345), "DEEMED TO BE UNIVERSITY", font=get_font(30, bold=True), fill=(147, 197, 253), anchor="mm")

    # Center Crest / Emblem Box
    crest_top = 420
    crest_bottom = 1400
    crest_w = 460
    
    shield_pts = [
        (cx - crest_w, crest_top),
        (cx + crest_w, crest_top),
        (cx + crest_w, crest_top + 450),
        (cx, crest_bottom),
        (cx - crest_w, crest_top + 450),
    ]
    draw.polygon(shield_pts, fill=(12, 30, 62), outline=(212, 175, 55))
    draw.line(shield_pts + [shield_pts[0]], fill=(255, 215, 0), width=8)

    inset_w = crest_w - 24
    inner_shield_pts = [
        (cx - inset_w, crest_top + 24),
        (cx + inset_w, crest_top + 24),
        (cx + inset_w, crest_top + 435),
        (cx, crest_bottom - 36),
        (cx - inset_w, crest_top + 435),
    ]
    draw.polygon(inner_shield_pts, fill=(16, 38, 76), outline=(59, 130, 246))
    draw.line(inner_shield_pts + [inner_shield_pts[0]], fill=(59, 130, 246), width=4)

    # Sun rays / torch
    sun_cy = crest_top + 210
    for a_deg in range(200, 345, 15):
        rad = math.radians(a_deg)
        rx1 = cx + math.cos(rad) * 60
        ry1 = sun_cy + math.sin(rad) * 40
        rx2 = cx + math.cos(rad) * 260
        ry2 = sun_cy + math.sin(rad) * 160
        draw.line([(rx1, ry1), (rx2, ry2)], fill=(255, 215, 0, 150), width=5)
    
    draw.ellipse([cx - 70, sun_cy - 45, cx + 70, sun_cy + 45], fill=(255, 215, 0), outline=(212, 175, 55), width=4)
    draw.ellipse([cx - 45, sun_cy - 30, cx + 45, sun_cy + 30], fill=(255, 255, 255))

    # Large Iconic "VIT" Letters Emblem in Center
    f_vit = get_font(260, bold=True)
    draw.text((cx + 8, 868), "VIT", font=f_vit, fill=(5, 12, 25), anchor="mm")
    draw.text((cx + 4, 864), "VIT", font=f_vit, fill=(180, 140, 30), anchor="mm")
    draw.text((cx, 860), "VIT", font=f_vit, fill=(255, 225, 77), anchor="mm")

    # Lower Ribbon Banner: Motto
    banner_y = 1560
    bw = 660
    bh = 100
    draw.rounded_rectangle([cx - bw, banner_y - bh//2, cx + bw, banner_y + bh//2], radius=24, fill=(15, 30, 60), outline=(212, 175, 55), width=6)
    draw.rounded_rectangle([cx - bw + 10, banner_y - bh//2 + 10, cx + bw - 10, banner_y + bh//2 - 10], radius=16, fill=(24, 48, 92), outline=(59, 130, 246), width=2)
    draw.text((cx, banner_y), "A Place to Learn, A Chance to Grow", font=f_motto, fill=(255, 255, 255), anchor="mm")

    # Bottom Tag: Institution of Eminence & Estd 1984
    draw.text((cx, 1720), "INSTITUTION OF EMINENCE", font=f_sub, fill=(212, 175, 55), anchor="mm")
    draw.text((cx, 1790), "ESTD. 1984 • VELLORE • CHENNAI • AP • BHOPAL", font=f_estd, fill=(190, 210, 240), anchor="mm")

    img.save(path)
    return path

def create_vit_plaque_texture(filename="tex_vit_plaque.png", size=(1024, 512)):
    path = os.path.join(TEXTURES_DIR, filename)
    img = Image.new("RGBA", size, color=(18, 22, 30, 255))
    draw = ImageDraw.Draw(img)

    # Brass brushed gold plate border
    draw.rectangle([12, 12, size[0]-12, size[1]-12], fill=(24, 30, 42), outline=(212, 175, 55), width=8)
    draw.rectangle([24, 24, size[0]-24, size[1]-24], outline=(255, 215, 0), width=2)
    draw.rectangle([34, 34, size[0]-34, size[1]-34], outline=(59, 130, 246, 150), width=2)

    # 4 Corner brass screws
    for sx, sy in [(30, 30), (size[0]-30, 30), (30, size[1]-30), (size[0]-30, size[1]-30)]:
        draw.ellipse([sx-10, sy-10, sx+10, sy+10], fill=(212, 175, 55), outline=(100, 80, 20), width=2)
        draw.line([(sx-6, sy-6), (sx+6, sy+6)], fill=(50, 40, 10), width=2)

    f_p_main = get_font(50, bold=True)
    f_p_sub = get_font(32, bold=True)
    f_p_motto = get_font(28, bold=False)
    f_p_body = get_font(22, bold=False)

    draw.text((size[0]//2, 90), "VELLORE INSTITUTE OF TECHNOLOGY", font=f_p_main, fill=(255, 215, 0), anchor="mm")
    draw.text((size[0]//2, 160), "INSTITUTION OF EMINENCE (IoE)", font=f_p_sub, fill=(255, 255, 255), anchor="mm")
    
    draw.line([(120, 205), (size[0]-120, 205)], fill=(212, 175, 55), width=3)
    
    draw.text((size[0]//2, 255), "“A Place to Learn, A Chance to Grow”", font=f_p_motto, fill=(212, 175, 55), anchor="mm")
    draw.text((size[0]//2, 330), "Dedicated to global excellence in higher education, research, and innovation.", font=f_p_body, fill=(226, 232, 240), anchor="mm")
    draw.text((size[0]//2, 375), "Founded in 1984 by Dr. G. Viswanathan • Empowering Future Leaders", font=f_p_body, fill=(148, 163, 184), anchor="mm")
    draw.text((size[0]//2, 440), "[ 40 YEARS OF TRANSFORMATIVE EXCELLENCE ]", font=get_font(24, bold=True), fill=(212, 175, 55), anchor="mm")

    img.save(path)
    return path

print("Generating texture assets...")
tex_floor = create_marble_floor_texture()
tex_facade = create_facade_title_texture()
tex_vit_logo = create_vit_logo_emblem_texture()
tex_vit_plaque = create_vit_plaque_texture()
tex_welcome = create_welcome_wall_texture()
tex_history_hdr = create_banner_texture("THE VIT JOURNEY", "Four Decades of Academic & Institutional Evolution", "tex_history_hdr.png")
tex_acad_hdr = create_banner_texture("ACADEMICS & INNOVATION", "Pioneering Research, World-Class Labs & Global Tech", "tex_acad_hdr.png")

# Generate timeline panels
p1 = create_infopanel_texture("Foundation & Vision", "1984", ["Founded as Vellore Engineering College (VEC)", "Established by Dr. G. Viswanathan with 180 students", "Pioneered self-financing engineering education"], "tex_p1.png")
p2 = create_infopanel_texture("Deemed University Status", "2001", ["Conferred Deemed-to-be-University status", "Rapid academic expansion across disciplines", "National recognition for pedagogical innovation"], "tex_p2.png")
p3 = create_infopanel_texture("Campus Infrastructure", "2008", ["Construction of iconic Technology Tower (TT)", "State-of-the-art smart classrooms and research labs", "Expansion of residential and sports complexes"], "tex_p3.png")
p4 = create_infopanel_texture("International Accreditations", "2015", ["First in India to secure ABET accreditations", "Global academic exchanges with 300+ universities", "Expansion of multi-disciplinary schools"], "tex_p4.png")
p5 = create_infopanel_texture("Institution of Eminence", "2019", ["Recognized as an Institution of Eminence (IoE)", "Massive surge in international research citations", "Launch of cutting-edge AI, IoT and Robotics centers"], "tex_p5.png")
p6 = create_infopanel_texture("Global Tech & Innovation", "2023", ["VITTBI incubates 150+ student and faculty startups", "Record placement offers from Fortune 500 tech firms", "Top national rankings in innovation and patents"], "tex_p6.png")
p7 = create_infopanel_texture("VIT Today & Beyond", "Present", ["Over 40,000+ students from across 50+ countries", "Ranked among top global universities in QS & THE", "Leading future engineering & sustainable tech"], "tex_p7.png")

# Academics panels
a1 = create_infopanel_texture("Schools of Computing & Tech", "Engineering", ["SCOPE & SITE: Computing, AI & Data Science", "SELECT: Electrical & Electronics Engineering", "SMEC: Mechanical & Automotive Innovation"], "tex_a1.png", accent_color=(16, 185, 129))
a2 = create_infopanel_texture("Advanced Research Centers", "Discovery", ["Center for Nanotechnology & Clean Energy", "Biomedical & Healthcare Innovation Labs", "Autonomous Systems & Robotics Laboratories"], "tex_a2.png", accent_color=(16, 185, 129))
a3 = create_infopanel_texture("VITTBI Innovation Incubator", "Entrepreneurship", ["Funded by DST, Government of India", "Nurturing student startup ecosystems", "Seed funding, mentorship & patent filing support"], "tex_a3.png", accent_color=(16, 185, 129))
a4 = create_infopanel_texture("Global Academic Partnerships", "Collaboration", ["Joint degree programs with top US & EU universities", "Semester Abroad Programs (SAP)", "International faculty and research symposiums"], "tex_a4.png", accent_color=(16, 185, 129))

tex_achievements = create_achievements_wall_texture()
tex_student_life = create_student_life_texture()

tex_screen_hist = create_screen_texture("VIT History Archive", "Interactive Timeline", ["1984: Foundation Story & Heritage", "2001: University Milestone Videos", "2019: Institution of Eminence Ceremony", "Notable Chancellor Addresses"], "tex_scr_hist.png")
tex_screen_res = create_screen_texture("Research & Innovation", "Live Research Metrics", ["50,000+ Scopus Indexed Papers", "Top Patent Filing Institute in India", "Funded Projects from DST, DRDO, ISRO", "Global Research Laboratories"], "tex_scr_res.png")
tex_screen_ach = create_screen_texture("Wall of Fame", "Distinguished Honors", ["QS World University Rankings", "NIRF Top 10 University Category", "Smart India Hackathon Consecutive Champions", "Distinguished Alumni in Fortune 500"], "tex_scr_ach.png")
tex_screen_stu = create_screen_texture("Campus Life & Events", "Student Experience", ["Riviera International Cultural Extravaganza", "graVITas Annual Tech Festival", "120+ Active Student Technical Chapters", "Inter-University Sports Champions"], "tex_scr_stu.png")

tex_campus_map = create_campus_model_map_texture()
print("All textures created successfully.")


# ==============================================================================
# 2. 3D PROCEDURAL MESH GENERATION
# ==============================================================================

class GLBBuilder:
    """Helper to assemble geometries, materials, and nodes into standard glTF 2.0 GLB."""
    def __init__(self):
        self.gltf = GLTF2(
            scene=0,
            scenes=[Scene(nodes=[])],
            nodes=[],
            meshes=[],
            materials=[],
            textures=[],
            images=[],
            accessors=[],
            bufferViews=[],
            buffers=[Buffer(byteLength=0)]
        )
        self.bin_data = bytearray()
        self.material_cache = {}
        self.texture_cache = {}

    def get_or_create_texture(self, image_path):
        if image_path in self.texture_cache:
            return self.texture_cache[image_path]
        
        with open(image_path, "rb") as f:
            img_bytes = f.read()
            
        # Add buffer view for image
        offset = len(self.bin_data)
        # Pad to 4 bytes
        pad = (4 - (offset % 4)) % 4
        if pad:
            self.bin_data.extend(b'\x00' * pad)
            offset = len(self.bin_data)
            
        self.bin_data.extend(img_bytes)
        bv_idx = len(self.gltf.bufferViews)
        self.gltf.bufferViews.append(BufferView(
            buffer=0,
            byteOffset=offset,
            byteLength=len(img_bytes)
        ))
        
        # Image
        img_idx = len(self.gltf.images)
        mime_type = "image/png" if image_path.endswith(".png") else "image/jpeg"
        self.gltf.images.append(GLTFImage(
            bufferView=bv_idx,
            mimeType=mime_type,
            name=os.path.basename(image_path)
        ))
        
        # Texture
        tex_idx = len(self.gltf.textures)
        self.gltf.textures.append(Texture(source=img_idx))
        self.texture_cache[image_path] = tex_idx
        return tex_idx

    def get_or_create_material(self, name, base_color=(0.8, 0.8, 0.8, 1.0), roughness=0.5, metallic=0.0,
                               emissive_color=(0,0,0), texture_path=None, alpha_mode="OPAQUE", double_sided=False):
        cache_key = (name, base_color, roughness, metallic, emissive_color, texture_path, alpha_mode, double_sided)
        if cache_key in self.material_cache:
            return self.material_cache[cache_key]
        
        pbr = PbrMetallicRoughness(
            baseColorFactor=list(base_color),
            roughnessFactor=float(roughness),
            metallicFactor=float(metallic)
        )
        
        if texture_path and os.path.exists(texture_path):
            tex_idx = self.get_or_create_texture(texture_path)
            pbr.baseColorTexture = TextureInfo(index=tex_idx)
            
        mat = Material(
            name=name,
            pbrMetallicRoughness=pbr,
            emissiveFactor=list(emissive_color),
            alphaMode=alpha_mode,
            doubleSided=double_sided
        )
        mat_idx = len(self.gltf.materials)
        self.gltf.materials.append(mat)
        self.material_cache[cache_key] = mat_idx
        return mat_idx

    def _append_data(self, data_bytes, target=None):
        offset = len(self.bin_data)
        pad = (4 - (offset % 4)) % 4
        if pad:
            self.bin_data.extend(b'\x00' * pad)
            offset = len(self.bin_data)
        self.bin_data.extend(data_bytes)
        bv_idx = len(self.gltf.bufferViews)
        bv = BufferView(
            buffer=0,
            byteOffset=offset,
            byteLength=len(data_bytes),
            target=target
        )
        self.gltf.bufferViews.append(bv)
        return bv_idx

    def add_mesh_primitive(self, vertices, indices, normals=None, uvs=None, material_idx=0):
        vertices = np.ascontiguousarray(vertices, dtype=np.float32)
        indices = np.ascontiguousarray(indices, dtype=np.uint32)
        
        # Positions
        pos_min = vertices.min(axis=0).tolist()
        pos_max = vertices.max(axis=0).tolist()
        bv_pos = self._append_data(vertices.tobytes(), target=ARRAY_BUFFER)
        acc_pos = len(self.gltf.accessors)
        self.gltf.accessors.append(Accessor(
            bufferView=bv_pos,
            byteOffset=0,
            componentType=FLOAT,
            count=len(vertices),
            type="VEC3",
            min=pos_min,
            max=pos_max
        ))
        
        # Indices
        ind_min = [int(indices.min())]
        ind_max = [int(indices.max())]
        bv_ind = self._append_data(indices.tobytes(), target=ELEMENT_ARRAY_BUFFER)
        acc_ind = len(self.gltf.accessors)
        self.gltf.accessors.append(Accessor(
            bufferView=bv_ind,
            byteOffset=0,
            componentType=UNSIGNED_INT,
            count=len(indices),
            type="SCALAR",
            min=ind_min,
            max=ind_max
        ))
        
        attributes = Attributes(POSITION=acc_pos)
        
        # Normals
        if normals is not None and len(normals) == len(vertices):
            normals = np.ascontiguousarray(normals, dtype=np.float32)
            bv_norm = self._append_data(normals.tobytes(), target=ARRAY_BUFFER)
            acc_norm = len(self.gltf.accessors)
            self.gltf.accessors.append(Accessor(
                bufferView=bv_norm,
                byteOffset=0,
                componentType=FLOAT,
                count=len(normals),
                type="VEC3"
            ))
            attributes.NORMAL = acc_norm
            
        # UVs
        if uvs is not None and len(uvs) == len(vertices):
            uvs = np.ascontiguousarray(uvs, dtype=np.float32)
            bv_uv = self._append_data(uvs.tobytes(), target=ARRAY_BUFFER)
            acc_uv = len(self.gltf.accessors)
            self.gltf.accessors.append(Accessor(
                bufferView=bv_uv,
                byteOffset=0,
                componentType=FLOAT,
                count=len(uvs),
                type="VEC2"
            ))
            attributes.TEXCOORD_0 = acc_uv
            
        primitive = Primitive(
            attributes=attributes,
            indices=acc_ind,
            material=material_idx
        )
        return primitive

    def create_node(self, name, mesh_primitives=None, translation=None, rotation=None, scale=None, children=None):
        node = Node(name=name)
        if translation is not None:
            node.translation = list(translation)
        if rotation is not None:
            node.rotation = list(rotation)
        if scale is not None:
            node.scale = list(scale)
        if children is not None:
            node.children = list(children)
            
        if mesh_primitives:
            mesh_idx = len(self.gltf.meshes)
            self.gltf.meshes.append(Mesh(name=name+"_mesh", primitives=mesh_primitives))
            node.mesh = mesh_idx
            
        node_idx = len(self.gltf.nodes)
        self.gltf.nodes.append(node)
        return node_idx

    def export(self, filepath):
        self.gltf.buffers[0].byteLength = len(self.bin_data)
        # Pad binary buffer to 4 bytes
        pad = (4 - (len(self.bin_data) % 4)) % 4
        if pad:
            self.bin_data.extend(b'\x00' * pad)
            self.gltf.buffers[0].byteLength = len(self.bin_data)
            
        self.gltf.set_binary_blob(bytes(self.bin_data))
        self.gltf.save_binary(filepath)
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"Exported: {filepath} ({size_mb:.2f} MB)")


# ==============================================================================
# 3. GEOMETRY HELPER FUNCTIONS
# ==============================================================================

def create_box(extents, center=(0,0,0)):
    """Returns trimesh Box with proper faces and normals."""
    mesh = trimesh.creation.box(extents=extents)
    mesh.apply_translation(center)
    return mesh

def create_cylinder(radius, height, sections=24, center=(0,0,0)):
    mesh = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
    mesh.apply_translation(center)
    return mesh

def create_torus(ring_radius, section_radius, radial_sections=32, tubular_sections=16, center=(0,0,0)):
    # Procedural parametric torus
    u = np.linspace(0, 2*np.pi, radial_sections, endpoint=False)
    v = np.linspace(0, 2*np.pi, tubular_sections, endpoint=False)
    u, v = np.meshgrid(u, v)
    u = u.flatten()
    v = v.flatten()
    
    x = (ring_radius + section_radius * np.cos(v)) * np.cos(u)
    y = section_radius * np.sin(v)
    z = (ring_radius + section_radius * np.cos(v)) * np.sin(u)
    
    verts = np.stack([x + center[0], y + center[1], z + center[2]], axis=1)
    
    indices = []
    for i in range(radial_sections):
        next_i = (i + 1) % radial_sections
        for j in range(tubular_sections):
            next_j = (j + 1) % tubular_sections
            
            p1 = j * radial_sections + i
            p2 = j * radial_sections + next_i
            p3 = next_j * radial_sections + next_i
            p4 = next_j * radial_sections + i
            
            indices.extend([p1, p2, p3, p1, p3, p4])
            
    mesh = trimesh.Trimesh(vertices=verts, faces=np.array(indices).reshape(-1, 3))
    mesh.fix_normals()
    return mesh

def create_sphere(radius=1.0, subdivisions=2, center=(0,0,0)):
    mesh = trimesh.creation.icosphere(subdivisions=subdivisions, radius=radius)
    mesh.apply_translation(center)
    return mesh

def create_vertical_panel_plane(width, height, center=(0,0,0), normal=(0,0,1)):
    """Create a 2-sided vertical plane with 0-1 UVs."""
    hw = width / 2.0
    hh = height / 2.0
    
    # Base XY plane
    verts = np.array([
        [-hw, -hh, 0.0],
        [ hw, -hh, 0.0],
        [ hw,  hh, 0.0],
        [-hw,  hh, 0.0],
    ], dtype=np.float32)
    
    uvs = np.array([
        [0.0, 1.0],
        [1.0, 1.0],
        [1.0, 0.0],
        [0.0, 0.0]
    ], dtype=np.float32)
    
    indices = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)
    
    # Orient according to normal
    norm = np.array(normal, dtype=np.float32)
    norm = norm / np.linalg.norm(norm)
    
    # Default normal is (0, 0, 1)
    if not np.allclose(norm, [0, 0, 1]):
        z_axis = np.array([0, 0, 1], dtype=np.float32)
        v = np.cross(z_axis, norm)
        c = np.dot(z_axis, norm)
        s = np.linalg.norm(v)
        if s > 1e-6:
            vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
            R = np.eye(3) + vx + (vx @ vx) * ((1 - c) / (s ** 2))
            verts = (R @ verts.T).T
            
    verts += np.array(center, dtype=np.float32)
    
    normals = np.tile(norm, (4, 1))
    return verts, indices, normals, uvs

def create_plane_with_uvs(width, height, center=(0,0,0), horizontal=True):
    hw = width / 2.0
    hh = height / 2.0
    if horizontal:
        # XZ plane
        verts = np.array([
            [-hw, 0.0, -hh],
            [ hw, 0.0, -hh],
            [ hw, 0.0,  hh],
            [-hw, 0.0,  hh]
        ], dtype=np.float32)
        normals = np.array([[0, 1, 0]] * 4, dtype=np.float32)
    else:
        # XY plane
        verts = np.array([
            [-hw, -hh, 0.0],
            [ hw, -hh, 0.0],
            [ hw,  hh, 0.0],
            [-hw,  hh, 0.0]
        ], dtype=np.float32)
        normals = np.array([[0, 0, 1]] * 4, dtype=np.float32)
        
    verts += np.array(center, dtype=np.float32)
    uvs = np.array([[0, 0], [width/4.0, 0], [width/4.0, height/4.0], [0, height/4.0]], dtype=np.float32)
    indices = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)
    return verts, indices, normals, uvs

def create_circular_disc_with_uvs(radius=1.5, center=(0, 3.2, -2.0), normal=(0, 0, 1), sections=48):
    """Creates a flat circular disc with proper 0..1 UV mapping suitable for circular emblem textures."""
    cx, cy, cz = center
    norm = np.array(normal, dtype=np.float32)
    norm = norm / np.linalg.norm(norm)

    verts = [[cx, cy, cz]]
    uvs = [[0.5, 0.5]]
    normals = [norm]

    # Calculate tangent and bitangent for plane orientation
    if abs(norm[2]) > 0.9:
        tangent = np.cross(norm, [0, 1, 0])
    else:
        tangent = np.cross(norm, [0, 0, 1])
    tangent = tangent / np.linalg.norm(tangent)
    bitangent = np.cross(norm, tangent)
    bitangent = bitangent / np.linalg.norm(bitangent)

    for i in range(sections):
        angle = 2.0 * math.pi * i / sections
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        pt = np.array([cx, cy, cz], dtype=np.float32) + radius * (cos_a * tangent + sin_a * bitangent)
        verts.append(pt.tolist())

        # Standard circular UV mapping
        u = 0.5 + 0.5 * cos_a
        v = 0.5 - 0.5 * sin_a
        uvs.append([u, v])
        normals.append(norm)

    indices = []
    for i in range(sections):
        next_i = (i + 1) % sections
        indices.extend([0, i + 1, next_i + 1])

    return np.array(verts, dtype=np.float32), np.array(indices, dtype=np.uint32), np.array(normals, dtype=np.float32), np.array(uvs, dtype=np.float32)

def create_3d_vit_letters(center_z, y_pos=3.25, scale=0.75, depth=0.08, facing_positive=True):
    """Builds 3D extruded mesh blocks for letters 'V', 'I', 'T' in trimesh."""
    bar_w = 0.09 * scale
    depth = depth * scale
    meshes = []
    
    # --- Letter 'V' (Left letter at X = -0.72 * scale) ---
    vx_center = -0.72 * scale
    v_height = 0.72 * scale
    v_half_w = 0.28 * scale
    v_diag_len = math.sqrt(v_height**2 + v_half_w**2)
    v_angle = math.atan2(v_half_w, v_height)
    
    m_v1 = trimesh.creation.box(extents=(bar_w, v_diag_len, depth))
    m_v1.apply_transform(trimesh.transformations.rotation_matrix(-v_angle, [0, 0, 1]))
    m_v1.apply_translation([vx_center - v_half_w/2, y_pos, center_z])
    meshes.append(m_v1)
    
    m_v2 = trimesh.creation.box(extents=(bar_w, v_diag_len, depth))
    m_v2.apply_transform(trimesh.transformations.rotation_matrix(v_angle, [0, 0, 1]))
    m_v2.apply_translation([vx_center + v_half_w/2, y_pos, center_z])
    meshes.append(m_v2)
    
    # --- Letter 'I' (Center letter at X = 0.0) ---
    m_i_stem = trimesh.creation.box(extents=(bar_w * 1.1, 0.72 * scale, depth))
    m_i_stem.apply_translation([0.0, y_pos, center_z])
    meshes.append(m_i_stem)
    
    m_i_top = trimesh.creation.box(extents=(0.32 * scale, bar_w * 0.9, depth))
    m_i_top.apply_translation([0.0, y_pos + 0.32 * scale, center_z])
    meshes.append(m_i_top)
    
    m_i_bot = trimesh.creation.box(extents=(0.32 * scale, bar_w * 0.9, depth))
    m_i_bot.apply_translation([0.0, y_pos - 0.32 * scale, center_z])
    meshes.append(m_i_bot)
    
    # --- Letter 'T' (Right letter at X = +0.72 * scale) ---
    tx_center = 0.72 * scale
    m_t_stem = trimesh.creation.box(extents=(bar_w * 1.1, 0.72 * scale, depth))
    m_t_stem.apply_translation([tx_center, y_pos - 0.03 * scale, center_z])
    meshes.append(m_t_stem)
    
    m_t_top = trimesh.creation.box(extents=(0.58 * scale, bar_w * 1.05, depth))
    m_t_top.apply_translation([tx_center, y_pos + 0.33 * scale, center_z])
    meshes.append(m_t_top)
    
    combined = trimesh.util.concatenate(meshes)
    return combined


# ==============================================================================
# 4. BUILDING SCENE GRAPH & PROCEDURAL ARCHITECTURE
# ==============================================================================

print("Constructing 3D museum architecture and exhibits...")
builder = GLBBuilder()

# ----------------- MATERIALS -----------------
# Architectural
mat_marble_floor = builder.get_or_create_material("Mat_Marble_Floor", (0.96, 0.96, 0.97, 1.0), roughness=0.18, metallic=0.05, texture_path=tex_floor)
mat_exterior_stone = builder.get_or_create_material("Mat_Exterior_Stone", (0.88, 0.88, 0.90, 1.0), roughness=0.75, metallic=0.02)
mat_interior_walls = builder.get_or_create_material("Mat_Interior_Walls", (0.94, 0.94, 0.95, 1.0), roughness=0.85, metallic=0.0)
mat_navy_accent = builder.get_or_create_material("Mat_Navy_Accent", (0.04, 0.12, 0.28, 1.0), roughness=0.35, metallic=0.1)
mat_gold_trim = builder.get_or_create_material("Mat_Gold_Trim", (0.88, 0.72, 0.24, 1.0), roughness=0.25, metallic=0.85)
mat_dark_metal = builder.get_or_create_material("Mat_Dark_Metal", (0.12, 0.14, 0.18, 1.0), roughness=0.3, metallic=0.7)
mat_chrome = builder.get_or_create_material("Mat_Chrome", (0.95, 0.95, 0.95, 1.0), roughness=0.1, metallic=0.95)
mat_ceiling_coffer = builder.get_or_create_material("Mat_Ceiling", (0.22, 0.24, 0.28, 1.0), roughness=0.8, metallic=0.0)
mat_glass = builder.get_or_create_material("Mat_Glass", (0.85, 0.92, 1.0, 0.25), roughness=0.05, metallic=0.1, alpha_mode="BLEND", double_sided=True)
mat_walnut_wood = builder.get_or_create_material("Mat_Walnut_Wood", (0.32, 0.20, 0.12, 1.0), roughness=0.45, metallic=0.0)
mat_foliage = builder.get_or_create_material("Mat_Foliage", (0.18, 0.48, 0.22, 1.0), roughness=0.7, metallic=0.0)
mat_pot_ceramic = builder.get_or_create_material("Mat_Pot_Ceramic", (0.92, 0.92, 0.92, 1.0), roughness=0.3, metallic=0.05)
mat_light_emissive = builder.get_or_create_material("Mat_Light_Emissive", (1.0, 1.0, 1.0, 1.0), roughness=0.1, metallic=0.0, emissive_color=(0.9, 0.95, 1.0))

# Textured Exhibition Materials & VIT Logo Materials
mat_facade_sign = builder.get_or_create_material("Mat_Facade_Sign", roughness=0.3, metallic=0.1, texture_path=tex_facade)
mat_welcome_board = builder.get_or_create_material("Mat_Welcome_Board", roughness=0.25, metallic=0.1, texture_path=tex_welcome)
mat_vit_logo = builder.get_or_create_material("Mat_VIT_Logo_Emblem", roughness=0.2, metallic=0.25, texture_path=tex_vit_logo, double_sided=True)
mat_vit_plaque = builder.get_or_create_material("Mat_VIT_Plaque", roughness=0.25, metallic=0.4, texture_path=tex_vit_plaque)
mat_hist_hdr = builder.get_or_create_material("Mat_History_Header", roughness=0.3, metallic=0.1, texture_path=tex_history_hdr)
mat_acad_hdr = builder.get_or_create_material("Mat_Academics_Header", roughness=0.3, metallic=0.1, texture_path=tex_acad_hdr)

mat_panels_hist = [
    builder.get_or_create_material(f"Mat_History_P{i+1}", roughness=0.2, texture_path=p)
    for i, p in enumerate([p1, p2, p3, p4, p5, p6, p7])
]

mat_panels_acad = [
    builder.get_or_create_material(f"Mat_Acad_P{i+1}", roughness=0.2, texture_path=p)
    for i, p in enumerate([a1, a2, a3, a4])
]

mat_achieve_wall = builder.get_or_create_material("Mat_Achievements_Wall", roughness=0.25, metallic=0.2, texture_path=tex_achievements)
mat_student_wall = builder.get_or_create_material("Mat_Student_Life_Wall", roughness=0.25, metallic=0.1, texture_path=tex_student_life)

mat_scr_hist = builder.get_or_create_material("Mat_Screen_Hist", roughness=0.2, emissive_color=(0.1, 0.15, 0.25), texture_path=tex_screen_hist)
mat_scr_acad = builder.get_or_create_material("Mat_Screen_Acad", roughness=0.2, emissive_color=(0.1, 0.15, 0.25), texture_path=tex_screen_res)
mat_scr_ach = builder.get_or_create_material("Mat_Screen_Ach", roughness=0.2, emissive_color=(0.1, 0.15, 0.25), texture_path=tex_screen_ach)
mat_scr_stu = builder.get_or_create_material("Mat_Screen_Stu", roughness=0.2, emissive_color=(0.1, 0.15, 0.25), texture_path=tex_screen_stu)
mat_campus_map = builder.get_or_create_material("Mat_Campus_Map", roughness=0.4, metallic=0.05, texture_path=tex_campus_map)


root_children = []

# ----------------- 1. EXTERIOR, STEPS, COLUMNS, FAÇADE -----------------
exterior_prims = []

# Exterior Walkway / Approach (Z: 22 to 34, X: -14 to +14, Y: -0.6)
walk_verts, walk_ind, walk_norm, walk_uv = create_plane_with_uvs(28.0, 12.0, center=(0, -0.6, 28.0), horizontal=True)
exterior_prims.append(builder.add_mesh_primitive(walk_verts, walk_ind, walk_norm, walk_uv, mat_exterior_stone))

# Entrance Steps (3 wide steps leading from Y: -0.6 up to Y: 0.0)
for s_idx in range(3):
    step_y = -0.6 + s_idx * 0.2 + 0.1
    step_z = 24.5 - s_idx * 0.8
    step_w = 20.0
    step_d = 1.6
    m_step = create_box((step_w, 0.2, step_d), center=(0, step_y, step_z))
    exterior_prims.append(builder.add_mesh_primitive(m_step.vertices, m_step.faces.flatten(), m_step.vertex_normals, material_idx=mat_exterior_stone))

# Accessibility Ramp (X = 11.5, Z: 22 to 26, Y: -0.6 to 0)
m_ramp = create_box((2.4, 0.2, 5.0), center=(11.5, -0.3, 24.0))
exterior_prims.append(builder.add_mesh_primitive(m_ramp.vertices, m_ramp.faces.flatten(), m_ramp.vertex_normals, material_idx=mat_exterior_stone))
# Ramp Railings (dark metal)
m_rail1 = create_box((0.08, 0.9, 5.0), center=(10.3, 0.15, 24.0))
m_rail2 = create_box((0.08, 0.9, 5.0), center=(12.7, 0.15, 24.0))
exterior_prims.append(builder.add_mesh_primitive(m_rail1.vertices, m_rail1.faces.flatten(), m_rail1.vertex_normals, material_idx=mat_dark_metal))
exterior_prims.append(builder.add_mesh_primitive(m_rail2.vertices, m_rail2.faces.flatten(), m_rail2.vertex_normals, material_idx=mat_dark_metal))

# Landscaped Planters on either side of steps (X = -11.5 and +11.5)
for px in [-11.5, 11.5]:
    # Planter box
    m_pbox = create_box((3.2, 0.8, 3.5), center=(px, -0.2, 23.5))
    exterior_prims.append(builder.add_mesh_primitive(m_pbox.vertices, m_pbox.faces.flatten(), m_pbox.vertex_normals, material_idx=mat_exterior_stone))
    # Green shrubs inside
    m_shrub = create_box((2.8, 0.6, 3.1), center=(px, 0.35, 23.5))
    exterior_prims.append(builder.add_mesh_primitive(m_shrub.vertices, m_shrub.faces.flatten(), m_shrub.vertex_normals, material_idx=mat_foliage))

# Portico Columns (6 columns at Z = 21.0, X = [-9.0, -5.4, -1.8, 1.8, 5.4, 9.0])
for cx in [-9.0, -5.4, -1.8, 1.8, 5.4, 9.0]:
    # Column shaft
    m_col = create_cylinder(radius=0.45, height=6.2, sections=24, center=(cx, 3.1, 21.0))
    # Base
    m_base = create_box((1.2, 0.4, 1.2), center=(cx, 0.2, 21.0))
    # Capital
    m_cap = create_box((1.3, 0.4, 1.3), center=(cx, 6.0, 21.0))
    exterior_prims.append(builder.add_mesh_primitive(m_col.vertices, m_col.faces.flatten(), m_col.vertex_normals, material_idx=mat_exterior_stone))
    exterior_prims.append(builder.add_mesh_primitive(m_base.vertices, m_base.faces.flatten(), m_base.vertex_normals, material_idx=mat_exterior_stone))
    exterior_prims.append(builder.add_mesh_primitive(m_cap.vertices, m_cap.faces.flatten(), m_cap.vertex_normals, material_idx=mat_exterior_stone))

# Portico Entablature & Roof (Z: 18 to 21.6, X: -11 to +11, Y: 6.2 to 7.0)
m_entab = create_box((22.4, 0.8, 4.0), center=(0, 6.4, 19.8))
exterior_prims.append(builder.add_mesh_primitive(m_entab.vertices, m_entab.faces.flatten(), m_entab.vertex_normals, material_idx=mat_exterior_stone))

# Exterior Facade Wall (Z = 18.0, X: -20 to +20, Y: 0 to 6.8) with central door opening
m_fac_left = create_box((15.0, 6.8, 0.6), center=(-11.5, 3.4, 18.0))
m_fac_right = create_box((15.0, 6.8, 0.6), center=(11.5, 3.4, 18.0))
m_fac_top = create_box((8.0, 3.0, 0.6), center=(0, 5.3, 18.0))
exterior_prims.append(builder.add_mesh_primitive(m_fac_left.vertices, m_fac_left.faces.flatten(), m_fac_left.vertex_normals, material_idx=mat_exterior_stone))
exterior_prims.append(builder.add_mesh_primitive(m_fac_right.vertices, m_fac_right.faces.flatten(), m_fac_right.vertex_normals, material_idx=mat_exterior_stone))
exterior_prims.append(builder.add_mesh_primitive(m_fac_top.vertices, m_fac_top.faces.flatten(), m_fac_top.vertex_normals, material_idx=mat_exterior_stone))

# Facade Signboard ("VIT VELLORE" & "VIRTUAL MUSEUM")
# Centered on facade above entrance at Z = 18.35, Y = 5.2, width = 7.2m, height = 1.8m
f_v, f_i, f_n, f_uv = create_vertical_panel_plane(7.2, 1.8, center=(0, 5.2, 18.35), normal=(0, 0, 1))
exterior_prims.append(builder.add_mesh_primitive(f_v, f_i, f_n, f_uv, mat_facade_sign))
m_sign_frame = create_box((7.4, 2.0, 0.1), center=(0, 5.2, 18.32))
exterior_prims.append(builder.add_mesh_primitive(m_sign_frame.vertices, m_sign_frame.faces.flatten(), m_sign_frame.vertex_normals, material_idx=mat_navy_accent))

# Glass Entrance Doors (Z = 18.0, X = [-3.8, +3.8], Y: 0 to 3.8m)
m_glass_door = create_box((7.6, 3.7, 0.08), center=(0, 1.85, 18.0))
exterior_prims.append(builder.add_mesh_primitive(m_glass_door.vertices, m_glass_door.faces.flatten(), m_glass_door.vertex_normals, material_idx=mat_glass))
# Metal Door Frames & Handles
m_door_frame1 = create_box((0.15, 3.8, 0.12), center=(-3.8, 1.9, 18.0))
m_door_frame2 = create_box((0.15, 3.8, 0.12), center=(3.8, 1.9, 18.0))
m_door_frame3 = create_box((0.15, 3.8, 0.12), center=(0, 1.9, 18.0))
m_handle1 = create_cylinder(0.025, 1.2, center=(-0.3, 1.5, 18.1))
m_handle2 = create_cylinder(0.025, 1.2, center=(0.3, 1.5, 18.1))
for df in [m_door_frame1, m_door_frame2, m_door_frame3, m_handle1, m_handle2]:
    exterior_prims.append(builder.add_mesh_primitive(df.vertices, df.faces.flatten(), df.vertex_normals, material_idx=mat_dark_metal))

node_exterior = builder.create_node("Museum_Exterior", exterior_prims)
root_children.append(node_exterior)


# ----------------- 2. INTERIOR ENCLOSURE & FLOORING -----------------
interior_prims = []

# Floor (Main Hall + Lobby: X from -19 to +19, Z from -17 to +18, Y = 0.0)
fl_v, fl_i, fl_n, fl_uv = create_plane_with_uvs(38.0, 35.0, center=(0, 0.0, 0.5), horizontal=True)
interior_prims.append(builder.add_mesh_primitive(fl_v, fl_i, fl_n, fl_uv, mat_marble_floor))

# Main Hall Perimeter Walls (Y: 0 to 6.5)
# North Wall (Back): Z = -16.5, X: -19 to +19
m_wall_n = create_box((38.0, 6.5, 0.6), center=(0, 3.25, -16.5))
# West Wall (Left): X = -18.5, Z: -16.5 to +8.5
m_wall_w = create_box((0.6, 6.5, 25.0), center=(-18.5, 3.25, -4.0))
# East Wall (Right): X = +18.5, Z: -16.5 to +8.5
m_wall_e = create_box((0.6, 6.5, 25.0), center=(18.5, 3.25, -4.0))
# Lobby Side Walls: X = -10.5 and +10.5, Z: 8.5 to 18.0
m_lobby_w = create_box((0.6, 6.5, 9.5), center=(-10.5, 3.25, 13.25))
m_lobby_e = create_box((0.6, 6.5, 9.5), center=(10.5, 3.25, 13.25))
# South dividing walls between Main Hall and Lobby (X = [-18.5, -10.0] and [10.0, 18.5], Z = 8.5)
m_south_div_w = create_box((8.5, 6.5, 0.6), center=(-14.25, 3.25, 8.5))
m_south_div_e = create_box((8.5, 6.5, 0.6), center=(14.25, 3.25, 8.5))

for w in [m_wall_n, m_wall_w, m_wall_e, m_lobby_w, m_lobby_e, m_south_div_w, m_south_div_e]:
    interior_prims.append(builder.add_mesh_primitive(w.vertices, w.faces.flatten(), w.vertex_normals, material_idx=mat_interior_walls))

# Ceiling & Structural Beams (Y = 6.2 to 6.5)
m_ceiling = create_box((38.0, 0.4, 35.0), center=(0, 6.4, 0.5))
interior_prims.append(builder.add_mesh_primitive(m_ceiling.vertices, m_ceiling.faces.flatten(), m_ceiling.vertex_normals, material_idx=mat_ceiling_coffer))

# Ceiling Light Strips / Downlight Fixtures (Emissive warm white)
for z_light in [-12.0, -6.0, 0.0, 6.0, 12.0]:
    m_lt_w = create_box((1.2, 0.1, 1.2), center=(-10.0, 6.15, z_light))
    m_lt_c = create_box((1.2, 0.1, 1.2), center=(0.0, 6.15, z_light))
    m_lt_e = create_box((1.2, 0.1, 1.2), center=(10.0, 6.15, z_light))
    for lt in [m_lt_w, m_lt_c, m_lt_e]:
        interior_prims.append(builder.add_mesh_primitive(lt.vertices, lt.faces.flatten(), lt.vertex_normals, material_idx=mat_light_emissive))

# Interior Columns in Main Hall (Grand atrium feel: 8 columns)
for c_pos in [(-12.0, -10.0), (-12.0, 0.0), (-12.0, 6.0),
              (12.0, -10.0), (12.0, 0.0), (12.0, 6.0),
              (-6.0, 8.2), (6.0, 8.2)]:
    col_x, col_z = c_pos
    m_icol = create_box((0.9, 6.2, 0.9), center=(col_x, 3.1, col_z))
    m_ic_base = create_box((1.2, 0.3, 1.2), center=(col_x, 0.15, col_z))
    m_ic_cap = create_box((1.2, 0.3, 1.2), center=(col_x, 6.05, col_z))
    for icm in [m_icol, m_ic_base, m_ic_cap]:
        interior_prims.append(builder.add_mesh_primitive(icm.vertices, icm.faces.flatten(), icm.vertex_normals, material_idx=mat_interior_walls))

node_interior = builder.create_node("Museum_Interior_Structure", interior_prims)
root_children.append(node_interior)


# ----------------- 3. GRAND ENTRANCE LOBBY & RECEPTION -----------------
lobby_prims = []

# Feature Welcome Wall (Z = 10.5, X: -4.8 to +4.8, Y: 0 to 4.5)
m_w_wall_base = create_box((9.8, 4.6, 0.4), center=(0, 2.3, 10.5))
lobby_prims.append(builder.add_mesh_primitive(m_w_wall_base.vertices, m_w_wall_base.faces.flatten(), m_w_wall_base.vertex_normals, material_idx=mat_navy_accent))

# Welcome Wall Graphic (Facing +Z towards entrance at Z = 10.72)
wv_v, wv_i, wv_n, wv_uv = create_vertical_panel_plane(9.2, 4.2, center=(0, 2.3, 10.72), normal=(0, 0, 1))
lobby_prims.append(builder.add_mesh_primitive(wv_v, wv_i, wv_n, wv_uv, mat_welcome_board))

# Reception Desk (X = 6.2, Z = 14.5, facing -X / +Z)
m_desk_main = create_box((3.2, 1.1, 1.2), center=(6.2, 0.55, 14.5))
m_desk_top = create_box((3.4, 0.08, 1.3), center=(6.2, 1.14, 14.5))
m_desk_trim = create_box((3.24, 0.08, 1.22), center=(6.2, 0.06, 14.5))
lobby_prims.append(builder.add_mesh_primitive(m_desk_main.vertices, m_desk_main.faces.flatten(), m_desk_main.vertex_normals, material_idx=mat_walnut_wood))
lobby_prims.append(builder.add_mesh_primitive(m_desk_top.vertices, m_desk_top.faces.flatten(), m_desk_top.vertex_normals, material_idx=mat_interior_walls))
lobby_prims.append(builder.add_mesh_primitive(m_desk_trim.vertices, m_desk_trim.faces.flatten(), m_desk_trim.vertex_normals, material_idx=mat_gold_trim))

# Reception Screen / Monitor placeholder
m_monitor = create_box((0.6, 0.4, 0.05), center=(6.2, 1.4, 14.3))
lobby_prims.append(builder.add_mesh_primitive(m_monitor.vertices, m_monitor.faces.flatten(), m_monitor.vertex_normals, material_idx=mat_dark_metal))

# Decorative Ceramic Pots with Plants in Lobby corners
for pot_pos in [(-8.5, 17.0), (8.5, 17.0), (-8.5, 11.5), (8.5, 11.5)]:
    px, pz = pot_pos
    m_pot = create_cylinder(0.4, 0.8, sections=16, center=(px, 0.4, pz))
    m_plant = create_sphere(radius=0.55, center=(px, 1.0, pz))
    lobby_prims.append(builder.add_mesh_primitive(m_pot.vertices, m_pot.faces.flatten(), m_pot.vertex_normals, material_idx=mat_pot_ceramic))
    lobby_prims.append(builder.add_mesh_primitive(m_plant.vertices, m_plant.faces.flatten(), m_plant.vertex_normals, material_idx=mat_foliage))

# Lobby Benches (`Bench_01`, `Bench_02`)
for bx, bz in [(-7.5, 14.5), (0.0, 16.5)]:
    m_bench_seat = create_box((2.4, 0.12, 0.7), center=(bx, 0.45, bz))
    m_bench_leg1 = create_box((0.1, 0.4, 0.6), center=(bx - 1.0, 0.2, bz))
    m_bench_leg2 = create_box((0.1, 0.4, 0.6), center=(bx + 1.0, 0.2, bz))
    lobby_prims.append(builder.add_mesh_primitive(m_bench_seat.vertices, m_bench_seat.faces.flatten(), m_bench_seat.vertex_normals, material_idx=mat_walnut_wood))
    lobby_prims.append(builder.add_mesh_primitive(m_bench_leg1.vertices, m_bench_leg1.faces.flatten(), m_bench_leg1.vertex_normals, material_idx=mat_chrome))
    lobby_prims.append(builder.add_mesh_primitive(m_bench_leg2.vertices, m_bench_leg2.faces.flatten(), m_bench_leg2.vertex_normals, material_idx=mat_chrome))

node_lobby = builder.create_node("Main_Lobby", lobby_prims)
root_children.append(node_lobby)


# ----------------- 4. CENTRAL VIT LOGO MONUMENT & ATRIUM FEATURE -----------------
sculpture_prims = []

# Circular 2-tier raised podium (Center: X = 0, Z = -2.0)
# Tier 1 (Base): Polished exterior stone dais
m_pod_1 = create_cylinder(radius=4.4, height=0.22, sections=48, center=(0, 0.11, -2.0))
# Tier 2: Deep royal navy marble tier
m_pod_2 = create_cylinder(radius=3.6, height=0.22, sections=48, center=(0, 0.33, -2.0))
# Gold Torus Rim around Tier 2
m_pod_trim = create_torus(ring_radius=3.6, section_radius=0.05, radial_sections=48, tubular_sections=16, center=(0, 0.44, -2.0))
# Emissive LED halo ring inset into the podium
m_pod_halo = create_torus(ring_radius=3.2, section_radius=0.025, radial_sections=48, tubular_sections=12, center=(0, 0.445, -2.0))

sculpture_prims.append(builder.add_mesh_primitive(m_pod_1.vertices, m_pod_1.faces.flatten(), m_pod_1.vertex_normals, material_idx=mat_exterior_stone))
sculpture_prims.append(builder.add_mesh_primitive(m_pod_2.vertices, m_pod_2.faces.flatten(), m_pod_2.vertex_normals, material_idx=mat_navy_accent))
sculpture_prims.append(builder.add_mesh_primitive(m_pod_trim.vertices, m_pod_trim.faces.flatten(), m_pod_trim.vertex_normals, material_idx=mat_gold_trim))
sculpture_prims.append(builder.add_mesh_primitive(m_pod_halo.vertices, m_pod_halo.faces.flatten(), m_pod_halo.vertex_normals, material_idx=mat_light_emissive))

# 8 Directional Mini-Spotlight Fixtures around perimeter of the podium
for sp_idx in range(8):
    sp_angle = (2.0 * math.pi / 8) * sp_idx
    sp_x = math.cos(sp_angle) * 3.3
    sp_z = math.sin(sp_angle) * 3.3 - 2.0
    m_sp_base = create_cylinder(radius=0.12, height=0.15, sections=12, center=(sp_x, 0.51, sp_z))
    m_sp_lens = create_sphere(radius=0.09, subdivisions=1, center=(sp_x, 0.58, sp_z))
    sculpture_prims.append(builder.add_mesh_primitive(m_sp_base.vertices, m_sp_base.faces.flatten(), m_sp_base.vertex_normals, material_idx=mat_dark_metal))
    sculpture_prims.append(builder.add_mesh_primitive(m_sp_lens.vertices, m_sp_lens.faces.flatten(), m_sp_lens.vertex_normals, material_idx=mat_light_emissive))

# Central Plinth / Pedestal (Sculpted octagonal base in deep navy & gold trim)
m_plinth_base = create_cylinder(radius=1.5, height=0.12, sections=32, center=(0, 0.50, -2.0))
m_plinth_body = create_cylinder(radius=1.35, height=1.2, sections=32, center=(0, 1.16, -2.0))
m_plinth_cap = create_cylinder(radius=1.5, height=0.12, sections=32, center=(0, 1.82, -2.0))
m_plinth_trim_bot = create_torus(ring_radius=1.5, section_radius=0.03, radial_sections=32, tubular_sections=12, center=(0, 0.56, -2.0))
m_plinth_trim_top = create_torus(ring_radius=1.5, section_radius=0.03, radial_sections=32, tubular_sections=12, center=(0, 1.88, -2.0))

sculpture_prims.append(builder.add_mesh_primitive(m_plinth_base.vertices, m_plinth_base.faces.flatten(), m_plinth_base.vertex_normals, material_idx=mat_gold_trim))
sculpture_prims.append(builder.add_mesh_primitive(m_plinth_body.vertices, m_plinth_body.faces.flatten(), m_plinth_body.vertex_normals, material_idx=mat_navy_accent))
sculpture_prims.append(builder.add_mesh_primitive(m_plinth_cap.vertices, m_plinth_cap.faces.flatten(), m_plinth_cap.vertex_normals, material_idx=mat_gold_trim))
sculpture_prims.append(builder.add_mesh_primitive(m_plinth_trim_bot.vertices, m_plinth_trim_bot.faces.flatten(), m_plinth_trim_bot.vertex_normals, material_idx=mat_gold_trim))
sculpture_prims.append(builder.add_mesh_primitive(m_plinth_trim_top.vertices, m_plinth_trim_top.faces.flatten(), m_plinth_trim_top.vertex_normals, material_idx=mat_gold_trim))

# 4 Brass Dedication Plaques on Plinth Faces (Front, Back, Left, Right)
plaque_configs = [
    ((0.0, 1.16, -2.0 + 1.37), (0, 0, 1), 1.2, 0.6),    # Front (+Z)
    ((0.0, 1.16, -2.0 - 1.37), (0, 0, -1), 1.2, 0.6),   # Back (-Z)
    ((-1.37, 1.16, -2.0), (-1, 0, 0), 1.2, 0.6),        # Left (-X)
    ((1.37, 1.16, -2.0), (1, 0, 0), 1.2, 0.6),          # Right (+X)
]
for p_pos, p_norm, pw, ph in plaque_configs:
    pq_v, pq_i, pq_n, pq_uv = create_vertical_panel_plane(pw, ph, center=p_pos, normal=p_norm)
    sculpture_prims.append(builder.add_mesh_primitive(pq_v, pq_i, pq_n, pq_uv, material_idx=mat_vit_plaque))
    if abs(p_norm[2]) > 0.5:
        m_pq_frame = create_box((pw + 0.08, ph + 0.08, 0.04), center=(p_pos[0], p_pos[1], p_pos[2] - p_norm[2]*0.02))
    else:
        m_pq_frame = create_box((0.04, ph + 0.08, pw + 0.08), center=(p_pos[0] - p_norm[0]*0.02, p_pos[1], p_pos[2]))
    sculpture_prims.append(builder.add_mesh_primitive(m_pq_frame.vertices, m_pq_frame.faces.flatten(), m_pq_frame.vertex_normals, material_idx=mat_gold_trim))

# Sculpted Gold Stand & Architectural Brackets
m_stand_col = create_cylinder(radius=0.38, height=0.65, sections=24, center=(0, 2.20, -2.0))
m_stand_ring1 = create_torus(ring_radius=0.42, section_radius=0.04, radial_sections=24, tubular_sections=12, center=(0, 2.05, -2.0))
m_stand_ring2 = create_torus(ring_radius=0.42, section_radius=0.04, radial_sections=24, tubular_sections=12, center=(0, 2.35, -2.0))
sculpture_prims.append(builder.add_mesh_primitive(m_stand_col.vertices, m_stand_col.faces.flatten(), m_stand_col.vertex_normals, material_idx=mat_gold_trim))
sculpture_prims.append(builder.add_mesh_primitive(m_stand_ring1.vertices, m_stand_ring1.faces.flatten(), m_stand_ring1.vertex_normals, material_idx=mat_gold_trim))
sculpture_prims.append(builder.add_mesh_primitive(m_stand_ring2.vertices, m_stand_ring2.faces.flatten(), m_stand_ring2.vertex_normals, material_idx=mat_gold_trim))

# Sweeping Curved Gold Arch Brackets supporting medallion sides
for bx in [-1.15, 1.15]:
    m_bkt = create_cylinder(radius=0.08, height=1.35, sections=16, center=(bx, 2.75, -2.0))
    m_bkt.apply_transform(trimesh.transformations.rotation_matrix(math.radians(-18 if bx < 0 else 18), [0, 0, 1]))
    sculpture_prims.append(builder.add_mesh_primitive(m_bkt.vertices, m_bkt.faces.flatten(), m_bkt.vertex_normals, material_idx=mat_gold_trim))

# ----------------- 3D VIT LOGO MEDALLION CENTERPIECE (Center: Y = 3.35, Z = -2.0) -----------------
medallion_y = 3.35
medallion_z = -2.0
medallion_r = 1.55
medallion_depth = 0.22

# 1. Outer Heavy Beveled Gold Casing
m_rim = trimesh.creation.cylinder(radius=medallion_r + 0.05, height=medallion_depth, sections=48)
m_rim.apply_transform(trimesh.transformations.rotation_matrix(math.radians(90), [1, 0, 0]))
m_rim.apply_translation([0, medallion_y, medallion_z])
sculpture_prims.append(builder.add_mesh_primitive(m_rim.vertices, m_rim.faces.flatten(), m_rim.vertex_normals, material_idx=mat_gold_trim))

# Front & Back Beveled Gold Torus Bezels
front_z = medallion_z + medallion_depth / 2.0
back_z = medallion_z - medallion_depth / 2.0

m_bezel_f = create_torus(ring_radius=medallion_r + 0.04, section_radius=0.055, radial_sections=48, tubular_sections=16, center=(0, medallion_y, front_z))
m_bezel_b = create_torus(ring_radius=medallion_r + 0.04, section_radius=0.055, radial_sections=48, tubular_sections=16, center=(0, medallion_y, back_z))
m_bezel_inner_f = create_torus(ring_radius=medallion_r * 0.96, section_radius=0.035, radial_sections=48, tubular_sections=16, center=(0, medallion_y, front_z + 0.01))
m_bezel_inner_b = create_torus(ring_radius=medallion_r * 0.96, section_radius=0.035, radial_sections=48, tubular_sections=16, center=(0, medallion_y, back_z - 0.01))

for bz in [m_bezel_f, m_bezel_b, m_bezel_inner_f, m_bezel_inner_b]:
    sculpture_prims.append(builder.add_mesh_primitive(bz.vertices, bz.faces.flatten(), bz.vertex_normals, material_idx=mat_gold_trim))

# 2. Dual-Sided High-Resolution VIT Logo Emblem Discs
df_v, df_i, df_n, df_uv = create_circular_disc_with_uvs(radius=medallion_r * 0.95, center=(0, medallion_y, front_z + 0.005), normal=(0, 0, 1), sections=48)
sculpture_prims.append(builder.add_mesh_primitive(df_v, df_i, df_n, df_uv, material_idx=mat_vit_logo))

db_v, db_i, db_n, db_uv = create_circular_disc_with_uvs(radius=medallion_r * 0.95, center=(0, medallion_y, back_z - 0.005), normal=(0, 0, -1), sections=48)
sculpture_prims.append(builder.add_mesh_primitive(db_v, db_i, db_n, db_uv, material_idx=mat_vit_logo))

# 3. 3D Extruded Polished Gold Relief "V", "I", "T" Letters on Front & Back
m_letters_front = create_3d_vit_letters(center_z=front_z + 0.035, y_pos=medallion_y - 0.02, scale=0.72, depth=0.06, facing_positive=True)
sculpture_prims.append(builder.add_mesh_primitive(m_letters_front.vertices, m_letters_front.faces.flatten(), m_letters_front.vertex_normals, material_idx=mat_gold_trim))

m_letters_back = create_3d_vit_letters(center_z=back_z - 0.035, y_pos=medallion_y - 0.02, scale=0.72, depth=0.06, facing_positive=False)
sculpture_prims.append(builder.add_mesh_primitive(m_letters_back.vertices, m_letters_back.faces.flatten(), m_letters_back.vertex_normals, material_idx=mat_gold_trim))

# 4. Top Crown / Golden Finial
m_finial_base = create_cylinder(radius=0.22, height=0.1, sections=24, center=(0, medallion_y + medallion_r + 0.08, medallion_z))
m_finial_crown = create_sphere(radius=0.18, subdivisions=2, center=(0, medallion_y + medallion_r + 0.22, medallion_z))
m_finial_star = create_torus(ring_radius=0.22, section_radius=0.03, radial_sections=24, tubular_sections=12, center=(0, medallion_y + medallion_r + 0.22, medallion_z))
for fin in [m_finial_base, m_finial_crown, m_finial_star]:
    sculpture_prims.append(builder.add_mesh_primitive(fin.vertices, fin.faces.flatten(), fin.vertex_normals, material_idx=mat_gold_trim))

# 5. Concentric Dynamic Orbital Rings framing the Medallion
ring_orbit1 = create_torus(ring_radius=2.05, section_radius=0.035, radial_sections=48, tubular_sections=16)
ring_orbit1.apply_transform(trimesh.transformations.rotation_matrix(math.radians(28), [1, 0, 0]))
ring_orbit1.apply_transform(trimesh.transformations.rotation_matrix(math.radians(20), [0, 1, 0]))
ring_orbit1.apply_translation([0, medallion_y, medallion_z])

ring_orbit2 = create_torus(ring_radius=2.25, section_radius=0.035, radial_sections=48, tubular_sections=16)
ring_orbit2.apply_transform(trimesh.transformations.rotation_matrix(math.radians(-32), [1, 0, 0]))
ring_orbit2.apply_transform(trimesh.transformations.rotation_matrix(math.radians(-25), [0, 1, 0]))
ring_orbit2.apply_translation([0, medallion_y, medallion_z])

sculpture_prims.append(builder.add_mesh_primitive(ring_orbit1.vertices, ring_orbit1.faces.flatten(), ring_orbit1.vertex_normals, material_idx=mat_chrome))
sculpture_prims.append(builder.add_mesh_primitive(ring_orbit2.vertices, ring_orbit2.faces.flatten(), ring_orbit2.vertex_normals, material_idx=mat_gold_trim))

node_sculpture = builder.create_node("VIT_Central_Sculpture", sculpture_prims)
root_children.append(node_sculpture)

# Interaction node for Central Sculpture
node_sculpture_interact = builder.create_node("INTERACT_Central_Sculpture", translation=[0, 2.5, -2.0])
root_children.append(node_sculpture_interact)


# ----------------- 5. CAMPUS MINIATURE MODEL DISPLAY -----------------
campus_prims = []
# Table Base (X = 0, Z = 4.2, Y = 0 to 0.85)
m_tbl_base = create_box((4.2, 0.85, 3.2), center=(0, 0.425, 4.2))
m_tbl_trim = create_box((4.3, 0.08, 3.3), center=(0, 0.86, 4.2))
campus_prims.append(builder.add_mesh_primitive(m_tbl_base.vertices, m_tbl_base.faces.flatten(), m_tbl_base.vertex_normals, material_idx=mat_navy_accent))
campus_prims.append(builder.add_mesh_primitive(m_tbl_trim.vertices, m_tbl_trim.faces.flatten(), m_tbl_trim.vertex_normals, material_idx=mat_gold_trim))

# Model Tabletop Map Surface (Z = 4.2, Y = 0.91)
map_v, map_i, map_n, map_uv = create_plane_with_uvs(4.0, 3.0, center=(0, 0.91, 4.2), horizontal=True)
campus_prims.append(builder.add_mesh_primitive(map_v, map_i, map_n, map_uv, mat_campus_map))

# 3D Stylized Miniature Campus Buildings
# Technology Tower (TT)
m_tt = create_box((0.8, 0.7, 0.5), center=(-0.8, 1.26, 3.5))
# Silver Jubilee Tower (SJT)
m_sjt = create_box((0.9, 0.9, 0.5), center=(0.0, 1.36, 4.8))
# Main Building
m_mb = create_box((0.6, 0.45, 0.6), center=(-1.2, 1.135, 4.4))
# Anna Auditorium
m_anna = create_cylinder(0.4, 0.35, sections=16, center=(1.1, 1.085, 4.2))

for b_mod in [m_tt, m_sjt, m_mb, m_anna]:
    campus_prims.append(builder.add_mesh_primitive(b_mod.vertices, b_mod.faces.flatten(), b_mod.vertex_normals, material_idx=mat_interior_walls))

# Glass Protective Enclosure Box
m_glass_case = create_box((4.1, 1.0, 3.1), center=(0, 1.41, 4.2))
campus_prims.append(builder.add_mesh_primitive(m_glass_case.vertices, m_glass_case.faces.flatten(), m_glass_case.vertex_normals, material_idx=mat_glass))

node_campus = builder.create_node("Campus_Model", campus_prims)
root_children.append(node_campus)

# Interaction node
node_campus_interact = builder.create_node("INTERACT_Campus_Model", translation=[0, 1.2, 4.2])
root_children.append(node_campus_interact)


# ----------------- 6. EXHIBITION WALLS & PANELS (4 SECTIONS) -----------------

# --- SECTION 1: THE VIT JOURNEY (West Wall: X = -18.15, Z: -15 to +6) ---
history_prims = []
# Section Header Banner
h_bv, h_bi, h_bn, h_buv = create_vertical_panel_plane(7.0, 1.4, center=(-18.15, 5.0, -4.0), normal=(1, 0, 0))
history_prims.append(builder.add_mesh_primitive(h_bv, h_bi, h_bn, h_buv, mat_hist_hdr))

# 7 Timeline Panels along West Wall
# Z positions spaced from Z = -14.0 to +4.0
z_hist = [-13.5, -10.5, -7.5, -4.5, -1.5, 1.5, 4.5]
for idx, z_p in enumerate(z_hist):
    # Mounting Frame
    m_frame = create_box((0.08, 2.2, 2.2), center=(-18.18, 2.6, z_p))
    history_prims.append(builder.add_mesh_primitive(m_frame.vertices, m_frame.faces.flatten(), m_frame.vertex_normals, material_idx=mat_navy_accent))
    # Graphic panel
    pv, pi, pn, puv = create_vertical_panel_plane(2.0, 2.0, center=(-18.12, 2.6, z_p), normal=(1, 0, 0))
    history_prims.append(builder.add_mesh_primitive(pv, pi, pn, puv, mat_panels_hist[idx]))

# Interactive History Digital Kiosk (At Z = -5.0, X = -15.5)
m_kiosk_base = create_box((0.8, 1.1, 0.4), center=(-15.5, 0.55, -5.0))
history_prims.append(builder.add_mesh_primitive(m_kiosk_base.vertices, m_kiosk_base.faces.flatten(), m_kiosk_base.vertex_normals, material_idx=mat_dark_metal))
ks_v, ks_i, ks_n, ks_uv = create_vertical_panel_plane(0.9, 0.65, center=(-15.45, 1.35, -5.0), normal=(1, 0, 0))
history_prims.append(builder.add_mesh_primitive(ks_v, ks_i, ks_n, ks_uv, mat_scr_hist))

node_history = builder.create_node("History_Section", history_prims)
root_children.append(node_history)

# History interaction nodes
root_children.append(builder.create_node("INTERACT_VIT_History", translation=[-18.0, 2.5, -4.0]))
root_children.append(builder.create_node("INTERACT_HistoryScreen", translation=[-15.45, 1.35, -5.0]))


# --- SECTION 2: ACADEMICS & INNOVATION (East Wall: X = +18.15, Z: -15 to +6) ---
acad_prims = []
# Section Header Banner
a_bv, a_bi, a_bn, a_buv = create_vertical_panel_plane(7.0, 1.4, center=(18.15, 5.0, -4.0), normal=(-1, 0, 0))
acad_prims.append(builder.add_mesh_primitive(a_bv, a_bi, a_bn, a_buv, mat_acad_hdr))

# 4 Academic & Innovation Panels
z_acad = [-12.0, -7.0, -2.0, 3.0]
for idx, z_p in enumerate(z_acad):
    m_frame = create_box((0.08, 2.4, 2.6), center=(18.18, 2.6, z_p))
    acad_prims.append(builder.add_mesh_primitive(m_frame.vertices, m_frame.faces.flatten(), m_frame.vertex_normals, material_idx=mat_navy_accent))
    pv, pi, pn, puv = create_vertical_panel_plane(2.4, 2.2, center=(18.12, 2.6, z_p), normal=(-1, 0, 0))
    acad_prims.append(builder.add_mesh_primitive(pv, pi, pn, puv, mat_panels_acad[idx]))

# Interactive Research Kiosk (At Z = -4.0, X = 15.5)
m_akiosk_base = create_box((0.8, 1.1, 0.4), center=(15.5, 0.55, -4.0))
acad_prims.append(builder.add_mesh_primitive(m_akiosk_base.vertices, m_akiosk_base.faces.flatten(), m_akiosk_base.vertex_normals, material_idx=mat_dark_metal))
aks_v, aks_i, aks_n, aks_uv = create_vertical_panel_plane(0.9, 0.65, center=(15.45, 1.35, -4.0), normal=(-1, 0, 0))
acad_prims.append(builder.add_mesh_primitive(aks_v, aks_i, aks_n, aks_uv, mat_scr_acad))

node_acad = builder.create_node("Academics_Section", acad_prims)
root_children.append(node_acad)

root_children.append(builder.create_node("INTERACT_Academics", translation=[18.0, 2.5, -4.0]))
root_children.append(builder.create_node("INTERACT_ResearchScreen", translation=[15.45, 1.35, -4.0]))


# --- SECTION 3: WALL OF ACHIEVEMENTS (North-East Back Wall: Z = -16.15, X: 1.5 to 16.5) ---
achieve_prims = []
# Wall Board
ac_v, ac_i, ac_n, ac_uv = create_vertical_panel_plane(14.0, 4.4, center=(9.0, 2.8, -16.15), normal=(0, 0, 1))
achieve_prims.append(builder.add_mesh_primitive(ac_v, ac_i, ac_n, ac_uv, mat_achieve_wall))

# 3 Glass Display Cases / Trophy Pedestals along front of Achievements Wall
for p_idx, px in enumerate([4.5, 9.0, 13.5]):
    # Pedestal base
    m_pbase = create_box((1.2, 0.9, 1.0), center=(px, 0.45, -14.2))
    m_ptrim = create_box((1.26, 0.06, 1.06), center=(px, 0.92, -14.2))
    achieve_prims.append(builder.add_mesh_primitive(m_pbase.vertices, m_pbase.faces.flatten(), m_pbase.vertex_normals, material_idx=mat_navy_accent))
    achieve_prims.append(builder.add_mesh_primitive(m_ptrim.vertices, m_ptrim.faces.flatten(), m_ptrim.vertex_normals, material_idx=mat_gold_trim))
    
    # 3D Trophy / Medal placeholder inside case
    m_trophy_base = create_cylinder(0.18, 0.1, center=(px, 1.0, -14.2))
    m_trophy_cup = create_cylinder(0.22, 0.35, center=(px, 1.25, -14.2))
    achieve_prims.append(builder.add_mesh_primitive(m_trophy_base.vertices, m_trophy_base.faces.flatten(), m_trophy_base.vertex_normals, material_idx=mat_gold_trim))
    achieve_prims.append(builder.add_mesh_primitive(m_trophy_cup.vertices, m_trophy_cup.faces.flatten(), m_trophy_cup.vertex_normals, material_idx=mat_gold_trim))
    
    # Glass Cover
    m_gcase = create_box((1.1, 0.8, 0.9), center=(px, 1.35, -14.2))
    achieve_prims.append(builder.add_mesh_primitive(m_gcase.vertices, m_gcase.faces.flatten(), m_gcase.vertex_normals, material_idx=mat_glass))

# Interactive Achievements Screen (At X = 1.8, Z = -14.5)
ach_scr_v, ach_scr_i, ach_scr_n, ach_scr_uv = create_vertical_panel_plane(1.1, 0.8, center=(1.8, 1.4, -14.5), normal=(0, 0, 1))
achieve_prims.append(builder.add_mesh_primitive(ach_scr_v, ach_scr_i, ach_scr_n, ach_scr_uv, mat_scr_ach))

node_achieve = builder.create_node("Achievements_Wall", achieve_prims)
root_children.append(node_achieve)

root_children.append(builder.create_node("INTERACT_Achievements", translation=[9.0, 2.8, -16.0]))
root_children.append(builder.create_node("INTERACT_AchievementsScreen", translation=[1.8, 1.4, -14.5]))


# --- SECTION 4: LIFE AT VIT (North-West Back Wall: Z = -16.15, X: -16.5 to -1.5) ---
student_prims = []
st_v, st_i, st_n, st_uv = create_vertical_panel_plane(14.0, 4.4, center=(-9.0, 2.8, -16.15), normal=(0, 0, 1))
student_prims.append(builder.add_mesh_primitive(st_v, st_i, st_n, st_uv, mat_student_wall))

# Interactive Student Life Screen (At X = -1.8, Z = -14.5)
stu_scr_v, stu_scr_i, stu_scr_n, stu_scr_uv = create_vertical_panel_plane(1.1, 0.8, center=(-1.8, 1.4, -14.5), normal=(0, 0, 1))
student_prims.append(builder.add_mesh_primitive(stu_scr_v, stu_scr_i, stu_scr_n, stu_scr_uv, mat_scr_stu))

node_student = builder.create_node("StudentLife_Section", student_prims)
root_children.append(node_student)

root_children.append(builder.create_node("INTERACT_StudentLife", translation=[-9.0, 2.8, -16.0]))
root_children.append(builder.create_node("INTERACT_StudentLifeScreen", translation=[-1.8, 1.4, -14.5]))


# ----------------- 7. MAIN HALL BENCHES & SEATING -----------------
bench_prims = []
bench_coords = [
    (-6.0, -7.0), (6.0, -7.0),
    (-6.0, 1.0), (6.0, 1.0),
]
for b_idx, (bx, bz) in enumerate(bench_coords):
    m_seat = create_box((2.4, 0.12, 0.7), center=(bx, 0.45, bz))
    m_leg1 = create_box((0.1, 0.4, 0.6), center=(bx - 1.0, 0.2, bz))
    m_leg2 = create_box((0.1, 0.4, 0.6), center=(bx + 1.0, 0.2, bz))
    bench_prims.append(builder.add_mesh_primitive(m_seat.vertices, m_seat.faces.flatten(), m_seat.vertex_normals, material_idx=mat_walnut_wood))
    bench_prims.append(builder.add_mesh_primitive(m_leg1.vertices, m_leg1.faces.flatten(), m_leg1.vertex_normals, material_idx=mat_chrome))
    bench_prims.append(builder.add_mesh_primitive(m_leg2.vertices, m_leg2.faces.flatten(), m_leg2.vertex_normals, material_idx=mat_chrome))

node_benches = builder.create_node("Hall_Benches", bench_prims)
root_children.append(node_benches)


# ----------------- 8. VIRTU-MUSEUM COMPATIBILITY PLANES (PLANE_001 to PLANE_031) -----------------
# We create anchor planes PLANE_001 to PLANE_031 positioned on the walls so that
# existing VirtuMuseum painting binders / hotspots bind seamlessly!
# 001 to 010 (West wall / History)
for i in range(1, 11):
    code = f"{i:03d}"
    pz = -13.5 + (i - 1) * 1.9
    pv, pi, pn, puv = create_vertical_panel_plane(1.4, 1.1, center=(-18.05, 2.5, pz), normal=(1, 0, 0))
    p_node = builder.create_node(f"PLANE_{code}", [builder.add_mesh_primitive(pv, pi, pn, puv, mat_panels_hist[min(i-1, 6)])])
    root_children.append(p_node)

# 011 to 020 (East wall / Academics)
for i in range(11, 21):
    code = f"{i:03d}"
    pz = -13.5 + (i - 11) * 1.9
    pv, pi, pn, puv = create_vertical_panel_plane(1.4, 1.1, center=(18.05, 2.5, pz), normal=(-1, 0, 0))
    p_node = builder.create_node(f"PLANE_{code}", [builder.add_mesh_primitive(pv, pi, pn, puv, mat_panels_acad[min((i-11)%4, 3)])])
    root_children.append(p_node)

# 021 to 025 (North-East wall / Achievements)
for i in range(21, 26):
    code = f"{i:03d}"
    px = 3.0 + (i - 21) * 2.8
    pv, pi, pn, puv = create_vertical_panel_plane(1.5, 1.2, center=(px, 2.7, -16.05), normal=(0, 0, 1))
    p_node = builder.create_node(f"PLANE_{code}", [builder.add_mesh_primitive(pv, pi, pn, puv, mat_achieve_wall)])
    root_children.append(p_node)

# 026 to 031 (North-West wall / Student Life)
for i in range(26, 32):
    code = f"{i:03d}"
    px = -15.0 + (i - 26) * 2.3
    pv, pi, pn, puv = create_vertical_panel_plane(1.4, 1.1, center=(px, 2.7, -16.05), normal=(0, 0, 1))
    p_node = builder.create_node(f"PLANE_{code}", [builder.add_mesh_primitive(pv, pi, pn, puv, mat_student_wall)])
    root_children.append(p_node)


# ----------------- 9. SPAWN POINTS & ROOT ASSEMBLY -----------------
# PlayerSpawn: At entrance lobby facing -Z towards welcome wall and main hall entrance
node_playerspawn = builder.create_node("PlayerSpawn", translation=[0.0, 1.6, 16.2], rotation=[0.0, 1.0, 0.0, 0.0])
# AtriumSpawn: Center atrium near central sculpture
node_atriumspawn = builder.create_node("AtriumSpawn", translation=[0.0, 1.6, 1.5], rotation=[0.0, 1.0, 0.0, 0.0])

root_children.extend([node_playerspawn, node_atriumspawn])

# Root Scene Node
root_node_idx = builder.create_node("VIT_Vellore_Museum_Root", children=root_children)
builder.gltf.scenes[0].nodes = [root_node_idx]

# Export GLB files
print("Exporting GLB files...")
builder.export(OUTPUT_GLB_ROOT)
builder.export(OUTPUT_GLB_ASSETS)

print("--- GLB Generation Complete! ---")
