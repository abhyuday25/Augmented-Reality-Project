"""
VIT Vellore Virtual Museum - 3D Procedural Two-Floor GLB Generator
Generates high quality textures, architectural two-floor geometry, grand staircase,
elevator tower, research tables, wall of fame, photo galleries, interactive nodes,
and exports vit_vellore_virtual_museum.glb.
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
DOWNLOAD_DIR = os.path.join(SCRIPT_DIR, "downloaded_assets")
VIT_IMG_DIR = os.path.join(ASSETS_DIR, "images", "vit")
OUTPUT_GLB_ROOT = os.path.join(PROJECT_ROOT, "vit_vellore_virtual_museum.glb")
OUTPUT_GLB_ASSETS = os.path.join(MODELS_DIR, "vit_vellore_virtual_museum.glb")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(TEXTURES_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

print("--- Starting Two-Floor VIT Vellore Virtual Museum GLB Generator ---")

# ==============================================================================
# 1. TEXTURE GENERATION WITH PILLOW
# ==============================================================================

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

def create_marble_floor_texture(filename="tex_marble_floor.png", size=(1024, 1024)):
    img = Image.new("RGB", size, color=(242, 243, 246))
    draw = ImageDraw.Draw(img)
    tile_size = 256
    for x in range(0, size[0], tile_size):
        draw.line([(x, 0), (x, size[1])], fill=(215, 218, 224), width=3)
    for y in range(0, size[1], tile_size):
        draw.line([(0, y), (size[0], y)], fill=(215, 218, 224), width=3)
    
    draw.rectangle([10, 10, size[0]-10, size[1]-10], outline=(180, 185, 195), width=4)
    draw.rectangle([20, 20, size[0]-20, size[1]-20], outline=(30, 41, 59), width=2)
    
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path, quality=92)
    return path

def create_floor2_texture(filename="tex_floor2.png", size=(1024, 1024)):
    """Dark polished contemporary architectural stone for Floor 2."""
    img = Image.new("RGB", size, color=(22, 28, 38))
    draw = ImageDraw.Draw(img)
    tile_size = 256
    for x in range(0, size[0], tile_size):
        draw.line([(x, 0), (x, size[1])], fill=(38, 48, 64), width=2)
    for y in range(0, size[1], tile_size):
        draw.line([(0, y), (size[0], y)], fill=(38, 48, 64), width=2)
    
    draw.rectangle([8, 8, size[0]-8, size[1]-8], outline=(212, 175, 55), width=3)
    draw.rectangle([18, 18, size[0]-18, size[1]-18], outline=(59, 130, 246), width=1)
    
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path, quality=92)
    return path

def create_facade_title_texture(filename="tex_facade_title.png", size=(2048, 512)):
    img = Image.new("RGBA", size, color=(15, 23, 42, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([8, 8, size[0]-8, size[1]-8], outline=(212, 175, 55, 255), width=6)
    draw.rectangle([16, 16, size[0]-16, size[1]-16], outline=(59, 130, 246, 180), width=2)
    
    f_title = get_font(110, bold=True)
    f_sub = get_font(48, bold=True)
    f_motto = get_font(30, bold=False)
    
    draw.text((size[0]//2, 110), "VELLORE INSTITUTE OF TECHNOLOGY", font=f_sub, fill=(212, 175, 55), anchor="mm")
    draw.text((size[0]//2, 230), "VIT VELLORE", font=f_title, fill=(255, 255, 255), anchor="mm")
    draw.text((size[0]//2, 360), "VIRTUAL HERITAGE & INNOVATION MUSEUM", font=f_sub, fill=(147, 197, 253), anchor="mm")
    draw.text((size[0]//2, 440), "A Place to Learn, A Chance to Grow • Established 1984", font=f_motto, fill=(203, 213, 225), anchor="mm")
    
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path

def create_welcome_wall_texture(filename="tex_welcome_wall.png", size=(2048, 1024)):
    img = Image.new("RGBA", size, color=(10, 25, 47, 255))
    draw = ImageDraw.Draw(img)
    
    for x in range(0, size[0], 64):
        draw.line([(x, 0), (x, size[1])], fill=(16, 38, 70), width=1)
    for y in range(0, size[1], 64):
        draw.line([(0, y), (size[0], y)], fill=(16, 38, 70), width=1)
        
    draw.rectangle([20, 20, size[0]-20, size[1]-20], outline=(212, 175, 55, 255), width=8)
    draw.rectangle([36, 36, size[0]-36, size[1]-36], outline=(59, 130, 246, 200), width=3)
    
    logo_path = os.path.join(VIT_IMG_DIR, "vit_seal_official.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.join(VIT_IMG_DIR, "vit_logo_official.png")
    
    if os.path.exists(logo_path):
        try:
            logo_img = Image.open(logo_path).convert("RGBA").resize((220, 220), Image.Resampling.LANCZOS)
            img.paste(logo_img, (size[0]//2 - 110, 65), logo_img)
        except Exception:
            pass
            
    f_h1 = get_font(90, bold=True)
    f_h2 = get_font(44, bold=True)
    f_desc = get_font(30, bold=False)
    
    draw.text((size[0]//2, 350), "WELCOME TO VIT VELLORE", font=f_h1, fill=(255, 255, 255), anchor="mm")
    draw.text((size[0]//2, 440), "Explore the Journey of Excellence, Education, Research and Innovation", font=f_h2, fill=(212, 175, 55), anchor="mm")
    
    desc_lines = [
        "Founded in 1984 by Dr. G. Viswanathan as Vellore Engineering College, VIT has evolved into",
        "an Institution of Eminence (IoE) and India's premier multidisciplinary technological university.",
        "Take a guided tour across two expansive floors or freely explore iconic campus archives."
    ]
    y_pos = 550
    for line in desc_lines:
        draw.text((size[0]//2, y_pos), line, font=f_desc, fill=(226, 232, 240), anchor="mm")
        y_pos += 45
        
    draw.rounded_rectangle([size[0]//2 - 380, 750, size[0]//2 + 380, 830], radius=15, fill=(30, 58, 138), outline=(212, 175, 55), width=2)
    f_tag = get_font(30, bold=True)
    draw.text((size[0]//2, 790), "FLOOR 1: THE VIT JOURNEY • FLOOR 2: INNOVATION & IMPACT", font=f_tag, fill=(255, 255, 255), anchor="mm")

    draw.text((size[0]//2, 890), "Move: WASD • Look: Mouse • Interact: Click / E • Map: M", font=get_font(24), fill=(147, 197, 253), anchor="mm")

    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path

def create_banner_texture(title, subtitle="", filename="tex_banner.png", size=(1536, 384), bg_color=(15, 30, 60)):
    img = Image.new("RGBA", size, color=(*bg_color, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([8, 8, size[0]-8, size[1]-8], outline=(212, 175, 55), width=5)
    draw.rectangle([16, 16, size[0]-16, size[1]-16], outline=(96, 165, 250), width=2)
    
    f_title = get_font(68, bold=True)
    f_sub = get_font(32, bold=False)
    
    draw.text((size[0]//2, 140), title, font=f_title, fill=(255, 255, 255), anchor="mm")
    if subtitle:
        draw.text((size[0]//2, 245), subtitle, font=f_sub, fill=(212, 175, 55), anchor="mm")
        
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path

def create_infopanel_texture(title, year, bullets, filename="tex_panel.png", size=(1024, 1024), accent_color=(59, 130, 246)):
    img = Image.new("RGBA", size, color=(15, 23, 42, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([0, 0, size[0], 180], fill=(10, 30, 65))
    draw.rectangle([0, 180, size[0], 188], fill=accent_color)
    draw.rectangle([12, 12, size[0]-12, size[1]-12], outline=(212, 175, 55), width=3)
    
    f_yr = get_font(40, bold=True)
    f_title = get_font(52, bold=True)
    f_bullet = get_font(30, bold=False)
    
    draw.text((50, 60), year, font=f_yr, fill=(212, 175, 55))
    draw.text((50, 125), title, font=f_title, fill=(255, 255, 255))
    
    draw.rounded_rectangle([50, 230, size[0]-50, 520], radius=12, fill=(30, 41, 59), outline=(71, 85, 105), width=2)
    f_ill = get_font(34, bold=True)
    draw.text((size[0]//2, 360), f"[ {title} ]", font=f_ill, fill=(148, 163, 184), anchor="mm")
    draw.text((size[0]//2, 420), "VIT Vellore Archives & Media", font=get_font(24), fill=(100, 116, 139), anchor="mm")
    
    y = 570
    for b in bullets:
        draw.ellipse([55, y+10, 67, y+22], fill=accent_color)
        draw.text((85, y), b, font=f_bullet, fill=(226, 232, 240))
        y += 65
        
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path

def create_research_table_texture(filename="tex_research_table.png", size=(1536, 1024)):
    img = Image.new("RGBA", size, color=(12, 24, 48, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([16, 16, size[0]-16, size[1]-16], outline=(59, 130, 246), width=6)
    draw.rectangle([28, 28, size[0]-28, size[1]-28], outline=(212, 175, 55), width=2)
    
    draw.text((size[0]//2, 70), "INTERACTIVE RESEARCH PORTAL", font=get_font(52, bold=True), fill=(255, 255, 255), anchor="mm")
    draw.text((size[0]//2, 120), "Explore Strategic Research Pillars & Funded Innovation Laboratories", font=get_font(26), fill=(147, 197, 253), anchor="mm")
    
    clusters = [
        ("AI & Autonomous Systems", "Robotics, Deep Learning & Vision", ["Drone navigation algorithms", "Edge AI computing cores", "Sponsored by DRDO & DST"]),
        ("Clean Energy & EV Tech", "Solar, Green Hydrogen & Batteries", ["Electric vehicle powertrain labs", "Nanostructured solar cells", "High energy density storage"]),
        ("Biomedical & Healthcare", "Theranostics & 3D Bioprinting", ["Cancer drug delivery systems", "Antimicrobial biopolymers", "Funded by ICMR & BIRAC"]),
        ("Smart Cities & Disaster Mitigation", "Sensors, Geoinformatics & Resilient Infra", ["Real-time earthquake monitoring", "Smart water management grids", "UN Sustainable Goals alignment"])
    ]
    
    card_w = (size[0] - 100) // 2
    card_h = (size[1] - 220) // 2
    
    for idx, (head, sub, pts) in enumerate(clusters):
        cx = 40 + (idx % 2) * (card_w + 20)
        cy = 170 + (idx // 2) * (card_h + 20)
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=14, fill=(18, 36, 68), outline=(212, 175, 55), width=2)
        draw.rectangle([cx, cy, cx + card_w, cy + 50], fill=(28, 54, 96))
        draw.text((cx + card_w//2, cy + 25), head, font=get_font(26, bold=True), fill=(255, 215, 0), anchor="mm")
        draw.text((cx + card_w//2, cy + 70), sub, font=get_font(20, bold=True), fill=(226, 232, 240), anchor="mm")
        
        py = cy + 110
        for pt in pts:
            draw.text((cx + 30, py), f"•  {pt}", font=get_font(20), fill=(190, 210, 240))
            py += 40
            
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path

def create_global_map_texture(filename="tex_global_map.png", size=(2048, 1024)):
    img = Image.new("RGBA", size, color=(8, 18, 36, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([16, 16, size[0]-16, size[1]-16], outline=(212, 175, 55), width=6)
    draw.rectangle([30, 30, size[0]-30, size[1]-30], outline=(59, 130, 246), width=2)
    
    draw.text((size[0]//2, 80), "VIT AROUND THE WORLD", font=get_font(72, bold=True), fill=(255, 255, 255), anchor="mm")
    draw.text((size[0]//2, 145), "Over 300+ International Academic Collaborations Across 6 Continents", font=get_font(34, bold=True), fill=(212, 175, 55), anchor="mm")
    
    for gx in range(60, size[0]-60, 120):
        draw.line([(gx, 200), (gx, size[1]-80)], fill=(18, 36, 68), width=1)
    for gy in range(200, size[1]-80, 80):
        draw.line([(60, gy), (size[0]-60, gy)], fill=(18, 36, 68), width=1)
        
    regions = [
        ("NORTH AMERICA", "USA & Canada: 65+ Partners", "MIT, Stanford, Johns Hopkins linkages", (size[0]//4 - 80, 360)),
        ("EUROPE", "UK, Germany, France, Italy: 110+ Partners", "Erasmus+, RWTH Aachen, Deakin", (size[0]//2 - 60, 320)),
        ("ASIA-PACIFIC", "Japan, Singapore, Australia: 80+ Partners", "NTU, Tokyo Tech, Melbourne, UNSW", (3*size[0]//4, 400)),
        ("LATIN AMERICA & AFRICA", "Brazil, South Africa, Kenya: 45+ Partners", "Global Sustainable Engineering consortiums", (size[0]//3 + 60, 680)),
    ]
    
    for reg, sub, detail, (rx, ry) in regions:
        draw.rounded_rectangle([rx - 180, ry - 70, rx + 180, ry + 70], radius=12, fill=(15, 32, 62), outline=(212, 175, 55), width=3)
        draw.text((rx, ry - 35), reg, font=get_font(26, bold=True), fill=(255, 215, 0), anchor="mm")
        draw.text((rx, ry), sub, font=get_font(20, bold=True), fill=(255, 255, 255), anchor="mm")
        draw.text((rx, ry + 35), detail, font=get_font(18), fill=(147, 197, 253), anchor="mm")
        
    draw.text((size[0]//2, size[1] - 45), "Semester Abroad Program (SAP) • Dual Degrees (2+2 / 3+2) • International Transfer Programs", font=get_font(24, bold=True), fill=(212, 175, 55), anchor="mm")
    
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path

def create_finale_texture(filename="tex_finale.png", size=(2048, 1024)):
    img = Image.new("RGBA", size, color=(10, 22, 45, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([20, 20, size[0]-20, size[1]-20], outline=(212, 175, 55), width=8)
    draw.rectangle([36, 36, size[0]-36, size[1]-36], outline=(59, 130, 246), width=3)
    
    draw.text((size[0]//2, 100), "VIT — THE JOURNEY CONTINUES", font=get_font(84, bold=True), fill=(255, 255, 255), anchor="mm")
    draw.text((size[0]//2, 180), "Celebrating 40 Years of Academic Leadership • Shaping Vision 2030", font=get_font(38, bold=True), fill=(212, 175, 55), anchor="mm")
    
    draw.line([(size[0]//2 - 400, 225), (size[0]//2 + 400, 225)], fill=(212, 175, 55), width=3)
    draw.text((size[0]//2, 330), "“A Place to Learn, A Chance to Grow”", font=get_font(48, bold=True), fill=(255, 215, 0), anchor="mm")
    
    bullets = [
        "Over 200,000 Global Alumni in Industry, Academia & Governance Across 100+ Nations",
        "Pioneering Sustainable Technologies, Green Hydrogen & Carbon-Neutral Campus 2030",
        "Empowering Next-Generation Leaders Through Inclusive World-Class Education",
        "Thank You for Visiting the VIT Vellore Virtual Museum"
    ]
    
    by = 460
    for b in bullets:
        draw.rounded_rectangle([size[0]//2 - 620, by, size[0]//2 + 620, by + 75], radius=10, fill=(18, 40, 75), outline=(59, 130, 246), width=2)
        draw.text((size[0]//2, by + 37), b, font=get_font(26, bold=True), fill=(240, 245, 255), anchor="mm")
        by += 95
        
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path

def create_stair_sign_texture(filename="tex_stair_sign.png", size=(1024, 384)):
    img = Image.new("RGBA", size, color=(14, 28, 54, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([8, 8, size[0]-8, size[1]-8], outline=(212, 175, 55), width=5)
    draw.text((size[0]//2, 90), "FLOOR 2 ↑", font=get_font(60, bold=True), fill=(255, 215, 0), anchor="mm")
    draw.text((size[0]//2, 180), "RESEARCH, IMPACT & CAMPUS LIFE", font=get_font(34, bold=True), fill=(255, 255, 255), anchor="mm")
    draw.text((size[0]//2, 270), "Grand Staircase • Accessible Elevator Available", font=get_font(26), fill=(147, 197, 253), anchor="mm")
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path

def create_elevator_sign_texture(filename="tex_elevator_sign.png", size=(512, 1024)):
    img = Image.new("RGBA", size, color=(18, 26, 40, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([8, 8, size[0]-8, size[1]-8], outline=(212, 175, 55), width=4)
    draw.text((size[0]//2, 100), "ELEVATOR", font=get_font(44, bold=True), fill=(255, 215, 0), anchor="mm")
    draw.text((size[0]//2, 170), "ACCESSIBLE TRANSITION", font=get_font(22, bold=True), fill=(147, 197, 253), anchor="mm")
    
    draw.rounded_rectangle([size[0]//2 - 140, 300, size[0]//2 + 140, 440], radius=16, fill=(30, 58, 110), outline=(212, 175, 55), width=3)
    draw.text((size[0]//2, 370), "2  UPPER FLOOR", font=get_font(32, bold=True), fill=(255, 255, 255), anchor="mm")
    
    draw.rounded_rectangle([size[0]//2 - 140, 500, size[0]//2 + 140, 640], radius=16, fill=(30, 58, 110), outline=(212, 175, 55), width=3)
    draw.text((size[0]//2, 570), "1  GROUND FLOOR", font=get_font(32, bold=True), fill=(255, 255, 255), anchor="mm")
    
    draw.text((size[0]//2, 750), "PRESS [E] OR CLICK", font=get_font(26, bold=True), fill=(212, 175, 55), anchor="mm")
    draw.text((size[0]//2, 800), "TO SWITCH FLOORS", font=get_font(22), fill=(200, 220, 245), anchor="mm")
    
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path

def create_sculpture_front_logo_texture(filename="tex_sculpture_front_logo.png", size=(2048, 1536)):
    img = Image.new("RGBA", size, color=(10, 22, 45, 255))
    draw = ImageDraw.Draw(img)
    for x in range(0, size[0], 64):
        draw.line([(x, 0), (x, size[1])], fill=(16, 36, 70), width=1)
    for y in range(0, size[1], 64):
        draw.line([(0, y), (size[0], y)], fill=(16, 36, 70), width=1)

    draw.rectangle([20, 20, size[0]-20, size[1]-20], outline=(212, 175, 55), width=10)
    draw.rectangle([40, 40, size[0]-40, size[1]-40], outline=(255, 215, 0), width=3)
    draw.rectangle([54, 54, size[0]-54, size[1]-54], outline=(59, 130, 246, 180), width=2)

    draw.text((size[0]//2, 110), "VELLORE INSTITUTE OF TECHNOLOGY", font=get_font(58, bold=True), fill=(255, 215, 0), anchor="mm")
    draw.text((size[0]//2, 170), "DEEMED TO BE UNIVERSITY • INSTITUTION OF EMINENCE", font=get_font(32, bold=True), fill=(147, 197, 253), anchor="mm")
    draw.line([(180, 208), (size[0]-180, 208)], fill=(212, 175, 55), width=3)

    seal_path = os.path.join(VIT_IMG_DIR, "vit_seal_official.png")
    if not os.path.exists(seal_path):
        seal_path = os.path.join(DOWNLOAD_DIR, "vit_seal_official.png")

    cx, cy = size[0]//2, 590
    box_size = 620
    draw.ellipse([cx - box_size//2 - 20, cy - box_size//2 - 20, cx + box_size//2 + 20, cy + box_size//2 + 20],
                 fill=(14, 32, 65), outline=(212, 175, 55), width=6)

    if os.path.exists(seal_path):
        try:
            seal_img = Image.open(seal_path).convert("RGBA")
            seal_img.thumbnail((box_size, box_size), Image.Resampling.LANCZOS)
            px = cx - seal_img.width // 2
            py = cy - seal_img.height // 2
            img.paste(seal_img, (px, py), seal_img)
        except Exception:
            draw.text((cx, cy), "VIT", font=get_font(120, bold=True), fill=(255, 215, 0), anchor="mm")
    else:
        draw.text((cx, cy), "VIT", font=get_font(120, bold=True), fill=(255, 215, 0), anchor="mm")

    bw = 740
    by = 1240
    bh = 90
    draw.rounded_rectangle([size[0]//2 - bw, by - bh//2, size[0]//2 + bw, by + bh//2], radius=18, fill=(18, 40, 80), outline=(212, 175, 55), width=4)
    draw.text((size[0]//2, by), "“A Place to Learn, A Chance to Grow”", font=get_font(38, bold=True), fill=(255, 255, 255), anchor="mm")
    draw.text((size[0]//2, 1370), "FOUNDED 1984 BY DR. G. VISWANATHAN • 40 YEARS OF EXCELLENCE", font=get_font(28, bold=True), fill=(212, 175, 55), anchor="mm")

    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path, quality=95)
    return path

def create_sculpture_back_gate_texture(filename="tex_sculpture_back_gate.png", size=(2048, 1536)):
    img = Image.new("RGBA", size, color=(10, 22, 45, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, size[0]-20, size[1]-20], outline=(212, 175, 55), width=10)
    draw.text((size[0]//2, 100), "VIT VELLORE CAMPUS", font=get_font(60, bold=True), fill=(255, 215, 0), anchor="mm")
    draw.text((size[0]//2, 160), "THE ICONIC MAIN ENTRANCE GATE & ARCHITECTURAL LANDMARK", font=get_font(30, bold=True), fill=(147, 197, 253), anchor="mm")

    gate_path = os.path.join(VIT_IMG_DIR, "vit_main_gate.jpg")
    fw, fh = 1860, 880
    fx, fy = (size[0] - fw) // 2, 230

    if os.path.exists(gate_path):
        try:
            gate_img = Image.open(gate_path).convert("RGB")
            scale = max(fw / gate_img.width, fh / gate_img.height)
            nw, nh = int(gate_img.width * scale), int(gate_img.height * scale)
            gate_img = gate_img.resize((nw, nh), Image.Resampling.LANCZOS)
            left = (nw - fw) // 2
            top = (nh - fh) // 2
            gate_img = gate_img.crop((left, top, left + fw, top + fh))
            draw.rectangle([fx-8, fy-8, fx+fw+8, fy+fh+8], outline=(212, 175, 55), width=6)
            img.paste(gate_img, (fx, fy))
        except Exception:
            pass

    py = 1170
    draw.rounded_rectangle([70, py, size[0]-70, py + 290], radius=16, fill=(15, 30, 60), outline=(212, 175, 55), width=3)
    draw.text((size[0]//2, py + 45), "VIT VELLORE MAIN GATEWAY", font=get_font(38, bold=True), fill=(255, 215, 0), anchor="mm")
    draw.text((size[0]//2, py + 115), "The world-famous entrance archway welcoming students, scholars, and delegates from over 50 nations.", font=get_font(26), fill=(240, 244, 248), anchor="mm")
    draw.text((size[0]//2, py + 165), "Spanning a sprawling 372-acre campus in Vellore, Tamil Nadu, equipped with cutting-edge infrastructure.", font=get_font(25), fill=(203, 213, 225), anchor="mm")

    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path, quality=95)
    return path

def create_sculpture_side_plaque_texture(filename="tex_sculpture_side_plaque.png", size=(1024, 1536)):
    img = Image.new("RGBA", size, color=(16, 24, 40, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([16, 16, size[0]-16, size[1]-16], fill=(20, 28, 48), outline=(212, 175, 55), width=8)
    draw.text((size[0]//2, 120), "VIT VELLORE", font=get_font(52, bold=True), fill=(255, 215, 0), anchor="mm")
    draw.text((size[0]//2, 180), "INSTITUTION OF EMINENCE", font=get_font(30, bold=True), fill=(255, 255, 255), anchor="mm")
    
    bullets = [
        "Established in 1984 as VEC",
        "Deemed University in 2001",
        "ABET Accredited Engineering",
        "IoE Recognition by Govt of India",
        "Top 15 NIRF University Rank",
        "Global QS & THE World Rankings",
        "150+ Technology Startups Incubated",
        "40,000+ Students from 50+ Countries"
    ]
    y = 280
    for b in bullets:
        draw.ellipse([80, y+10, 94, y+24], fill=(212, 175, 55))
        draw.text((120, y), b, font=get_font(28), fill=(226, 232, 240))
        y += 115

    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path, quality=95)
    return path

def create_achievements_wall_texture(filename="tex_achievements_wall.png", size=(2048, 1024)):
    img = Image.new("RGBA", size, color=(8, 20, 40, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([16, 16, size[0]-16, size[1]-16], outline=(212, 175, 55), width=8)
    draw.text((size[0]//2, 100), "WALL OF ACHIEVEMENTS", font=get_font(80, bold=True), fill=(255, 255, 255), anchor="mm")
    draw.text((size[0]//2, 170), "Recognizing Excellence, Innovation & Institutional Impact", font=get_font(38, bold=True), fill=(212, 175, 55), anchor="mm")
    
    cards = [
        ("Institutional Eminence", "NIRF & Global Rankings", "Ranked consistently among top engineering and research universities in India.", (30, 58, 138)),
        ("Research Impact", "High-Impact Publications", "50,000+ Scopus publications, funded research grants from DST and ISRO.", (15, 80, 100)),
        ("Innovation & Patents", "VITTBI & Technology Startups", "Over 150+ technology startups incubated and hundreds of published patents.", (67, 35, 110)),
        ("Student Excellence", "Hackathons & Formula Student", "Consecutive Smart India Hackathon champions & international racing victories.", (110, 60, 20)),
    ]
    card_w = (size[0] - 120) // 2
    card_h = 320
    positions = [(50, 240), (size[0]//2 + 10, 240), (50, 600), (size[0]//2 + 10, 600)]
    for (title, cat, desc, col), (cx, cy) in zip(cards, positions):
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=16, fill=(15, 30, 60), outline=(212, 175, 55), width=3)
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + 70], radius=16, fill=col)
        draw.text((cx + 25, cy + 35), cat, font=get_font(28, bold=True), fill=(212, 175, 55), anchor="lm")
        draw.text((cx + 25, cy + 115), title, font=get_font(36, bold=True), fill=(255, 255, 255), anchor="lm")
        draw.text((cx + 25, cy + 185), desc, font=get_font(26), fill=(203, 213, 225), anchor="lm")
        
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
        ("Riviera Cultural Fest", "Asia's Premier ISO 9001 Festival", (180, 40, 70)),
        ("graVITas Tech Fest", "Hackathons & Autonomous Robotics", (30, 100, 170)),
        ("Clubs & Student Chapters", "120+ Active Chapters (IEEE, ACM...)", (40, 130, 90)),
        ("Formula Student Motorsports", "Team Praega & Ojas Race Cars", (170, 90, 20)),
        ("Sports Complexes & Athletics", "Olympic swimming pool & stadiums", (90, 40, 150)),
        ("Campus Life & Hostels", "Modern residential community", (50, 70, 120)),
    ]
    cols, rows = 3, 2
    margin_x, margin_y = 50, 220
    pw = (size[0] - margin_x*2 - (cols-1)*30) // cols
    ph = (size[1] - margin_y - 50 - (rows-1)*30) // rows
    for idx, (title, sub, col) in enumerate(photo_cards):
        r, c = idx // cols, idx % cols
        px = margin_x + c * (pw + 30)
        py = margin_y + r * (ph + 30)
        draw.rounded_rectangle([px, py, px + pw, py + ph], radius=14, fill=(20, 32, 54), outline=(147, 197, 253), width=2)
        draw.rounded_rectangle([px+8, py+8, px + pw-8, py + ph - 80], radius=10, fill=col)
        draw.text((px + pw//2, py + (ph-80)//2), f"[ {title} ]", font=get_font(28, bold=True), fill=(255, 255, 255), anchor="mm")
        draw.text((px + pw//2, py + ph - 50), title, font=get_font(26, bold=True), fill=(255, 255, 255), anchor="mm")
        draw.text((px + pw//2, py + ph - 22), sub, font=get_font(18), fill=(212, 175, 55), anchor="mm")
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path

def create_screen_texture(screen_title, subtitle, bullets, filename="tex_screen.png", size=(1024, 768)):
    img = Image.new("RGBA", size, color=(5, 12, 28, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, size[0]-10, size[1]-10], outline=(59, 130, 246), width=5)
    draw.rectangle([0, 0, size[0], 120], fill=(15, 35, 80))
    draw.text((size[0]//2, 50), screen_title, font=get_font(48, bold=True), fill=(255, 255, 255), anchor="mm")
    draw.text((size[0]//2, 95), subtitle, font=get_font(24), fill=(212, 175, 55), anchor="mm")
    y = 180
    for b in bullets:
        draw.rounded_rectangle([50, y, size[0]-50, y+85], radius=10, fill=(15, 25, 50), outline=(71, 85, 105), width=2)
        draw.text((80, y+42), b, font=get_font(28), fill=(226, 232, 240), anchor="lm")
        y += 105
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path

def create_campus_model_map_texture(filename="tex_campus_map.png", size=(1024, 1024)):
    img = Image.new("RGBA", size, color=(35, 45, 40, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, size[0]-40, size[1]-40], fill=(45, 80, 55))
    road_col = (100, 105, 115)
    draw.ellipse([100, 100, size[0]-100, size[1]-100], outline=road_col, width=32)
    draw.line([(size[0]//2, 100), (size[0]//2, size[1]-100)], fill=road_col, width=28)
    draw.line([(100, size[1]//2), (size[0]-100, size[1]//2)], fill=road_col, width=28)
    bldgs = [
        (size[0]//2 - 120, 200, 240, 120, "TECHNOLOGY TOWER (TT)", (20, 40, 80)),
        (size[0]//2 - 130, size[1] - 340, 260, 140, "SILVER JUBILEE TOWER (SJT)", (25, 45, 90)),
        (180, size[1]//2 - 70, 150, 140, "MAIN BUILDING (MB)", (30, 50, 95)),
        (size[0] - 330, size[1]//2 - 70, 150, 140, "ANNA AUDITORIUM", (120, 60, 30)),
    ]
    for bx, by, bw, bh, name, col in bldgs:
        draw.rectangle([bx, by, bx+bw, by+bh], fill=col, outline=(212, 175, 55), width=3)
        draw.text((bx + bw//2, by + bh//2), name, font=get_font(18, bold=True), fill=(255, 255, 255), anchor="mm")
    path = os.path.join(TEXTURES_DIR, filename)
    img.save(path)
    return path


# ==============================================================================
# 2. GLB BUILDER & GEOMETRY HELPERS
# ==============================================================================

class GLBBuilder:
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
            
        offset = len(self.bin_data)
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
        
        img_idx = len(self.gltf.images)
        mime_type = "image/png" if image_path.endswith(".png") else "image/jpeg"
        self.gltf.images.append(GLTFImage(
            bufferView=bv_idx,
            mimeType=mime_type,
            name=os.path.basename(image_path)
        ))
        
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
        pad = (4 - (len(self.bin_data) % 4)) % 4
        if pad:
            self.bin_data.extend(b'\x00' * pad)
            self.gltf.buffers[0].byteLength = len(self.bin_data)
            
        self.gltf.set_binary_blob(bytes(self.bin_data))
        self.gltf.save_binary(filepath)
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"Exported: {filepath} ({size_mb:.2f} MB)")

def create_box(extents, center=(0,0,0)):
    mesh = trimesh.creation.box(extents=extents)
    mesh.apply_translation(center)
    return mesh

def create_cylinder(radius, height, sections=24, center=(0,0,0)):
    mesh = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
    mesh.apply_translation(center)
    return mesh

def create_sphere(radius=1.0, subdivisions=2, center=(0,0,0)):
    mesh = trimesh.creation.icosphere(subdivisions=subdivisions, radius=radius)
    mesh.apply_translation(center)
    return mesh

def create_vertical_panel_plane(width, height, center=(0,0,0), normal=(0,0,1)):
    hw = width / 2.0
    hh = height / 2.0
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
    norm = np.array(normal, dtype=np.float32)
    norm = norm / np.linalg.norm(norm)
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
        verts = np.array([
            [-hw, 0.0, -hh],
            [ hw, 0.0, -hh],
            [ hw, 0.0,  hh],
            [-hw, 0.0,  hh]
        ], dtype=np.float32)
        normals = np.array([[0, 1, 0]] * 4, dtype=np.float32)
    else:
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

def create_3d_vit_letters(center_z, y_pos=3.25, scale=0.75, depth=0.08, facing_positive=True):
    bar_w = 0.09 * scale
    depth = depth * scale
    meshes = []
    
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
    
    m_i_stem = trimesh.creation.box(extents=(bar_w * 1.1, 0.72 * scale, depth))
    m_i_stem.apply_translation([0.0, y_pos, center_z])
    meshes.append(m_i_stem)
    
    m_i_top = trimesh.creation.box(extents=(0.32 * scale, bar_w * 0.9, depth))
    m_i_top.apply_translation([0.0, y_pos + 0.32 * scale, center_z])
    meshes.append(m_i_top)
    
    m_i_bot = trimesh.creation.box(extents=(0.32 * scale, bar_w * 0.9, depth))
    m_i_bot.apply_translation([0.0, y_pos - 0.32 * scale, center_z])
    meshes.append(m_i_bot)
    
    tx_center = 0.72 * scale
    m_t_stem = trimesh.creation.box(extents=(bar_w * 1.1, 0.72 * scale, depth))
    m_t_stem.apply_translation([tx_center, y_pos - 0.03 * scale, center_z])
    meshes.append(m_t_stem)
    
    m_t_top = trimesh.creation.box(extents=(0.58 * scale, bar_w * 1.05, depth))
    m_t_top.apply_translation([tx_center, y_pos + 0.33 * scale, center_z])
    meshes.append(m_t_top)
    
    combined = trimesh.util.concatenate(meshes)
    return combined

print("Generating textures...")
tex_floor1 = create_marble_floor_texture()
tex_floor2 = create_floor2_texture()
tex_facade = create_facade_title_texture()
tex_welcome = create_welcome_wall_texture()
tex_stair_sign = create_stair_sign_texture()
tex_elevator_sign = create_elevator_sign_texture()
tex_research_hdr = create_banner_texture("RESEARCH & INNOVATION", "Discovery, High-Impact Publications & Entrepreneurship", "tex_res_hdr.png", bg_color=(10, 25, 55))
tex_research_table = create_research_table_texture()
tex_global_map = create_global_map_texture()
tex_finale = create_finale_texture()
tex_history_hdr = create_banner_texture("THE VIT JOURNEY", "Four Decades of Academic & Institutional Evolution", "tex_history_hdr.png")
tex_acad_hdr = create_banner_texture("ACADEMICS AT VIT", "Multidisciplinary Schools, FFCS & Global Programs", "tex_acad_hdr.png")

# Infopanels
p1 = create_infopanel_texture("Foundation & Vision", "1984", ["Founded as Vellore Engineering College (VEC)", "Established by Dr. G. Viswanathan with 180 students", "Pioneered self-financing engineering education"], "tex_p1.png")
p2 = create_infopanel_texture("Deemed University Status", "2001", ["Conferred Deemed-to-be-University status", "Rapid academic expansion across disciplines", "National recognition for pedagogical innovation"], "tex_p2.png")
p3 = create_infopanel_texture("Campus Infrastructure", "2008", ["Construction of iconic Technology Tower (TT)", "State-of-the-art smart classrooms and research labs", "Expansion of residential and sports complexes"], "tex_p3.png")
p4 = create_infopanel_texture("International Accreditations", "2015", ["First in India to secure ABET accreditations", "Global academic exchanges with 300+ universities", "Expansion of multi-disciplinary schools"], "tex_p4.png")
p5 = create_infopanel_texture("Institution of Eminence", "2019", ["Recognized as an Institution of Eminence (IoE)", "Massive surge in international research citations", "Launch of cutting-edge AI, IoT and Robotics centers"], "tex_p5.png")
p6 = create_infopanel_texture("Global Tech & Innovation", "2023", ["VITTBI incubates 150+ student and faculty startups", "Record placement offers from Fortune 500 tech firms", "Top national rankings in innovation and patents"], "tex_p6.png")
p7 = create_infopanel_texture("VIT Today & Beyond", "Present", ["Over 40,000+ students from across 50+ countries", "Ranked among top global universities in QS & THE", "Leading future engineering & sustainable tech"], "tex_p7.png")

a1 = create_infopanel_texture("Schools of Computing & Tech", "Engineering", ["SCOPE & SITE: Computing, AI & Data Science", "SELECT: Electrical & Electronics Engineering", "SMEC: Mechanical & Automotive Innovation"], "tex_a1.png", accent_color=(16, 185, 129))
a2 = create_infopanel_texture("Advanced Research Centers", "Discovery", ["Center for Nanotechnology & Clean Energy", "Biomedical & Healthcare Innovation Labs", "Autonomous Systems & Robotics Laboratories"], "tex_a2.png", accent_color=(16, 185, 129))
a3 = create_infopanel_texture("VITTBI Innovation Incubator", "Entrepreneurship", ["Funded by DST, Government of India", "Nurturing student startup ecosystems", "Seed funding, mentorship & patent filing support"], "tex_a3.png", accent_color=(16, 185, 129))
a4 = create_infopanel_texture("Global Academic Partnerships", "Collaboration", ["Joint degree programs with top US & EU universities", "Semester Abroad Programs (SAP)", "International faculty and research symposiums"], "tex_a4.png", accent_color=(16, 185, 129))

tex_achievements = create_achievements_wall_texture()
tex_student_life = create_student_life_texture()
tex_screen_hist = create_screen_texture("VIT History Archive", "Interactive Timeline", ["1984: Foundation Story & Heritage", "2001: University Milestone Videos", "2019: Institution of Eminence Ceremony", "Notable Chancellor Addresses"], "tex_scr_hist.png")
tex_screen_res = create_screen_texture("Research & Innovation", "Live Research Metrics", ["50,000+ Scopus Indexed Papers", "Top Patent Filing Institute in India", "Funded Projects from DST, DRDO, ISRO", "Global Research Laboratories"], "tex_scr_res.png")
tex_screen_ach = create_screen_texture("Wall of Fame", "Distinguished Honors", ["QS World University Rankings", "NIRF Top 15 University Category", "Smart India Hackathon Consecutive Champions", "Distinguished Alumni in Fortune 500"], "tex_scr_ach.png")
tex_screen_stu = create_screen_texture("Campus Life & Events", "Student Experience", ["Riviera International Cultural Extravaganza", "graVITas Annual Tech Festival", "120+ Active Student Technical Chapters", "Inter-University Sports Champions"], "tex_scr_stu.png")
tex_campus_map = create_campus_model_map_texture()
tex_sculpture_front_logo = create_sculpture_front_logo_texture()
tex_sculpture_back_gate = create_sculpture_back_gate_texture()
tex_sculpture_side_plaque = create_sculpture_side_plaque_texture()
print("All textures ready.")


# ==============================================================================
# 3. 3D TWO-FLOOR SCENE GRAPH & PROCEDURAL GEOMETRY
# ==============================================================================

print("Constructing two-floor 3D museum architecture...")
builder = GLBBuilder()

# Materials
mat_floor1 = builder.get_or_create_material("Mat_Floor1_Marble", (0.96, 0.96, 0.97, 1.0), roughness=0.18, metallic=0.05, texture_path=tex_floor1)
mat_floor2 = builder.get_or_create_material("Mat_Floor2_Stone", (0.85, 0.88, 0.92, 1.0), roughness=0.25, metallic=0.1, texture_path=tex_floor2)
mat_exterior_stone = builder.get_or_create_material("Mat_Exterior_Stone", (0.88, 0.88, 0.90, 1.0), roughness=0.75, metallic=0.02)
mat_interior_walls = builder.get_or_create_material("Mat_Interior_Walls", (0.94, 0.94, 0.95, 1.0), roughness=0.85, metallic=0.0)
mat_navy_accent = builder.get_or_create_material("Mat_Navy_Accent", (0.04, 0.12, 0.28, 1.0), roughness=0.35, metallic=0.1)
mat_gold_trim = builder.get_or_create_material("Mat_Gold_Trim", (0.88, 0.72, 0.24, 1.0), roughness=0.25, metallic=0.85)
mat_dark_metal = builder.get_or_create_material("Mat_Dark_Metal", (0.12, 0.14, 0.18, 1.0), roughness=0.3, metallic=0.7)
mat_chrome = builder.get_or_create_material("Mat_Chrome", (0.95, 0.95, 0.95, 1.0), roughness=0.1, metallic=0.95)
mat_ceiling = builder.get_or_create_material("Mat_Ceiling", (0.20, 0.22, 0.26, 1.0), roughness=0.8, metallic=0.0)
mat_glass = builder.get_or_create_material("Mat_Glass", (0.85, 0.92, 1.0, 0.25), roughness=0.05, metallic=0.1, alpha_mode="BLEND", double_sided=True)
mat_walnut_wood = builder.get_or_create_material("Mat_Walnut_Wood", (0.32, 0.20, 0.12, 1.0), roughness=0.45, metallic=0.0)
mat_foliage = builder.get_or_create_material("Mat_Foliage", (0.18, 0.48, 0.22, 1.0), roughness=0.7, metallic=0.0)
mat_pot_ceramic = builder.get_or_create_material("Mat_Pot_Ceramic", (0.92, 0.92, 0.92, 1.0), roughness=0.3, metallic=0.05)
mat_light_emissive = builder.get_or_create_material("Mat_Light_Emissive", (1.0, 1.0, 1.0, 1.0), roughness=0.1, metallic=0.0, emissive_color=(0.95, 0.95, 1.0))
mat_gold_emissive = builder.get_or_create_material("Mat_Gold_Emissive", (1.0, 0.84, 0.2, 1.0), roughness=0.2, metallic=0.8, emissive_color=(0.8, 0.65, 0.15))

# Textured Materials
mat_facade_sign = builder.get_or_create_material("Mat_Facade_Sign", roughness=0.3, metallic=0.1, texture_path=tex_facade)
mat_welcome_board = builder.get_or_create_material("Mat_Welcome_Board", roughness=0.25, metallic=0.1, texture_path=tex_welcome)
mat_sculpture_front = builder.get_or_create_material("Mat_Sculpture_Front_Logo", roughness=0.2, metallic=0.15, texture_path=tex_sculpture_front_logo, double_sided=True)
mat_sculpture_back = builder.get_or_create_material("Mat_Sculpture_Back_Gate", roughness=0.2, metallic=0.1, texture_path=tex_sculpture_back_gate, double_sided=True)
mat_sculpture_side = builder.get_or_create_material("Mat_Sculpture_Side_Plaque", roughness=0.25, metallic=0.3, texture_path=tex_sculpture_side_plaque, double_sided=True)
mat_hist_hdr = builder.get_or_create_material("Mat_History_Header", roughness=0.3, metallic=0.1, texture_path=tex_history_hdr)
mat_acad_hdr = builder.get_or_create_material("Mat_Academics_Header", roughness=0.3, metallic=0.1, texture_path=tex_acad_hdr)
mat_res_hdr = builder.get_or_create_material("Mat_Research_Header", roughness=0.3, metallic=0.1, texture_path=tex_research_hdr)
mat_res_table = builder.get_or_create_material("Mat_Research_Table", roughness=0.2, metallic=0.1, texture_path=tex_research_table, double_sided=True)
mat_global_map = builder.get_or_create_material("Mat_Global_Map", roughness=0.25, metallic=0.1, texture_path=tex_global_map, double_sided=True)
mat_finale = builder.get_or_create_material("Mat_Finale_Banner", roughness=0.25, metallic=0.15, texture_path=tex_finale, double_sided=True)
mat_stair_sign = builder.get_or_create_material("Mat_Stair_Sign", roughness=0.25, metallic=0.1, texture_path=tex_stair_sign, double_sided=True)
mat_elevator_sign = builder.get_or_create_material("Mat_Elevator_Sign", roughness=0.25, metallic=0.1, texture_path=tex_elevator_sign, double_sided=True)

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

# ----------------- 1. EXTERIOR & FAÇADE (Floor 1 Entrance) -----------------
exterior_prims = []

walk_verts, walk_ind, walk_norm, walk_uv = create_plane_with_uvs(28.0, 12.0, center=(0, -0.6, 28.0), horizontal=True)
exterior_prims.append(builder.add_mesh_primitive(walk_verts, walk_ind, walk_norm, walk_uv, mat_exterior_stone))

for s_idx in range(3):
    step_y = -0.6 + s_idx * 0.2 + 0.1
    step_z = 24.5 - s_idx * 0.8
    m_step = create_box((20.0, 0.2, 1.6), center=(0, step_y, step_z))
    exterior_prims.append(builder.add_mesh_primitive(m_step.vertices, m_step.faces.flatten(), m_step.vertex_normals, material_idx=mat_exterior_stone))

m_ramp = create_box((2.4, 0.2, 5.0), center=(11.5, -0.3, 24.0))
exterior_prims.append(builder.add_mesh_primitive(m_ramp.vertices, m_ramp.faces.flatten(), m_ramp.vertex_normals, material_idx=mat_exterior_stone))
m_rail1 = create_box((0.08, 0.9, 5.0), center=(10.3, 0.15, 24.0))
m_rail2 = create_box((0.08, 0.9, 5.0), center=(12.7, 0.15, 24.0))
exterior_prims.append(builder.add_mesh_primitive(m_rail1.vertices, m_rail1.faces.flatten(), m_rail1.vertex_normals, material_idx=mat_dark_metal))
exterior_prims.append(builder.add_mesh_primitive(m_rail2.vertices, m_rail2.faces.flatten(), m_rail2.vertex_normals, material_idx=mat_dark_metal))

for px in [-11.5, 11.5]:
    m_pbox = create_box((3.2, 0.8, 3.5), center=(px, -0.2, 23.5))
    m_shrub = create_box((2.8, 0.6, 3.1), center=(px, 0.35, 23.5))
    exterior_prims.append(builder.add_mesh_primitive(m_pbox.vertices, m_pbox.faces.flatten(), m_pbox.vertex_normals, material_idx=mat_exterior_stone))
    exterior_prims.append(builder.add_mesh_primitive(m_shrub.vertices, m_shrub.faces.flatten(), m_shrub.vertex_normals, material_idx=mat_foliage))

for cx in [-9.0, -5.4, -1.8, 1.8, 5.4, 9.0]:
    m_col = create_cylinder(radius=0.45, height=9.8, sections=24, center=(cx, 4.9, 21.0))
    m_base = create_box((1.2, 0.5, 1.2), center=(cx, 0.25, 21.0))
    m_cap = create_box((1.3, 0.5, 1.3), center=(cx, 9.6, 21.0))
    exterior_prims.append(builder.add_mesh_primitive(m_col.vertices, m_col.faces.flatten(), m_col.vertex_normals, material_idx=mat_exterior_stone))
    exterior_prims.append(builder.add_mesh_primitive(m_base.vertices, m_base.faces.flatten(), m_base.vertex_normals, material_idx=mat_exterior_stone))
    exterior_prims.append(builder.add_mesh_primitive(m_cap.vertices, m_cap.faces.flatten(), m_cap.vertex_normals, material_idx=mat_exterior_stone))

m_entab = create_box((22.4, 1.0, 4.0), center=(0, 10.0, 19.8))
exterior_prims.append(builder.add_mesh_primitive(m_entab.vertices, m_entab.faces.flatten(), m_entab.vertex_normals, material_idx=mat_exterior_stone))

m_fac_left = create_box((15.0, 10.4, 0.6), center=(-11.5, 5.2, 18.0))
m_fac_right = create_box((15.0, 10.4, 0.6), center=(11.5, 5.2, 18.0))
m_fac_top = create_box((8.0, 6.6, 0.6), center=(0, 7.1, 18.0))
exterior_prims.append(builder.add_mesh_primitive(m_fac_left.vertices, m_fac_left.faces.flatten(), m_fac_left.vertex_normals, material_idx=mat_exterior_stone))
exterior_prims.append(builder.add_mesh_primitive(m_fac_right.vertices, m_fac_right.faces.flatten(), m_fac_right.vertex_normals, material_idx=mat_exterior_stone))
exterior_prims.append(builder.add_mesh_primitive(m_fac_top.vertices, m_fac_top.faces.flatten(), m_fac_top.vertex_normals, material_idx=mat_exterior_stone))

f_v, f_i, f_n, f_uv = create_vertical_panel_plane(7.2, 1.8, center=(0, 6.8, 18.35), normal=(0, 0, 1))
exterior_prims.append(builder.add_mesh_primitive(f_v, f_i, f_n, f_uv, mat_facade_sign))
m_sign_frame = create_box((7.4, 2.0, 0.1), center=(0, 6.8, 18.32))
exterior_prims.append(builder.add_mesh_primitive(m_sign_frame.vertices, m_sign_frame.faces.flatten(), m_sign_frame.vertex_normals, material_idx=mat_navy_accent))

m_glass_door = create_box((7.6, 3.7, 0.08), center=(0, 1.85, 18.0))
exterior_prims.append(builder.add_mesh_primitive(m_glass_door.vertices, m_glass_door.faces.flatten(), m_glass_door.vertex_normals, material_idx=mat_glass))
for dfx in [-3.8, 0.0, 3.8]:
    m_df = create_box((0.15, 3.8, 0.12), center=(dfx, 1.9, 18.0))
    exterior_prims.append(builder.add_mesh_primitive(m_df.vertices, m_df.faces.flatten(), m_df.vertex_normals, material_idx=mat_dark_metal))

node_exterior = builder.create_node("Museum_Exterior", exterior_prims)
root_children.append(node_exterior)


# ----------------- 2. TWO-FLOOR STRUCTURAL SHELL & FLOOR SLABS -----------------
structure_prims = []

# Floor 1 Ground Slab (Y = 0.0)
fl1_v, fl1_i, fl1_n, fl1_uv = create_plane_with_uvs(38.0, 35.0, center=(0, 0.0, 0.5), horizontal=True)
structure_prims.append(builder.add_mesh_primitive(fl1_v, fl1_i, fl1_n, fl1_uv, mat_floor1))

# Floor 2 Mezzanine Slabs (Y = 5.0m, atrium opening from X: -7 to +7, Z: -6 to +5)
m_fl2_w = create_box((12.0, 0.35, 31.0), center=(-13.0, 4.825, -1.0))
m_fl2_e = create_box((12.0, 0.35, 31.0), center=(13.0, 4.825, -1.0))
m_fl2_n = create_box((14.0, 0.35, 10.5), center=(0.0, 4.825, -11.25))
m_fl2_s = create_box((14.0, 0.35, 9.5), center=(0.0, 4.825, 9.75))

for mfl in [m_fl2_w, m_fl2_e, m_fl2_n, m_fl2_s]:
    structure_prims.append(builder.add_mesh_primitive(mfl.vertices, mfl.faces.flatten(), mfl.vertex_normals, material_idx=mat_floor2))

# Top Ceiling Slab (Y = 10.0m)
m_ceiling = create_box((38.0, 0.4, 35.0), center=(0, 10.0, 0.5))
structure_prims.append(builder.add_mesh_primitive(m_ceiling.vertices, m_ceiling.faces.flatten(), m_ceiling.vertex_normals, material_idx=mat_ceiling))

# Full-Height Perimeter Walls (Y: 0 to 10.0m)
m_wall_n = create_box((38.0, 10.0, 0.6), center=(0, 5.0, -16.5))
m_wall_w = create_box((0.6, 10.0, 25.0), center=(-18.5, 5.0, -4.0))
m_wall_e = create_box((0.6, 10.0, 25.0), center=(18.5, 5.0, -4.0))
m_lobby_w = create_box((0.6, 10.0, 9.5), center=(-10.5, 5.0, 13.25))
m_lobby_e = create_box((0.6, 10.0, 9.5), center=(10.5, 5.0, 13.25))
m_sdiv_w = create_box((8.5, 10.0, 0.6), center=(-14.25, 5.0, 8.5))
m_sdiv_e = create_box((8.5, 10.0, 0.6), center=(14.25, 5.0, 8.5))

for w in [m_wall_n, m_wall_w, m_wall_e, m_lobby_w, m_lobby_e, m_sdiv_w, m_sdiv_e]:
    structure_prims.append(builder.add_mesh_primitive(w.vertices, w.faces.flatten(), w.vertex_normals, material_idx=mat_interior_walls))

# Full-Height Interior Atrium Columns (8 pillars)
for c_pos in [(-12.0, -10.0), (-12.0, 0.0), (-12.0, 6.0),
              (12.0, -10.0), (12.0, 0.0), (12.0, 6.0),
              (-6.0, 8.2), (6.0, 8.2)]:
    col_x, col_z = c_pos
    m_icol = create_box((0.9, 9.8, 0.9), center=(col_x, 4.9, col_z))
    m_ic_base = create_box((1.2, 0.4, 1.2), center=(col_x, 0.2, col_z))
    m_ic_cap = create_box((1.2, 0.4, 1.2), center=(col_x, 9.6, col_z))
    for icm in [m_icol, m_ic_base, m_ic_cap]:
        structure_prims.append(builder.add_mesh_primitive(icm.vertices, icm.faces.flatten(), icm.vertex_normals, material_idx=mat_interior_walls))

# Guardrails around Floor 2 Atrium opening (Glass & Brass)
rail_height = 1.05
m_gr_w = create_box((0.08, rail_height, 11.0), center=(-7.0, 5.0 + rail_height/2, -0.5))
m_gr_e = create_box((0.08, rail_height, 11.0), center=(7.0, 5.0 + rail_height/2, -0.5))
m_gr_n = create_box((14.0, rail_height, 0.08), center=(0.0, 5.0 + rail_height/2, -6.0))
m_gr_s = create_box((14.0, rail_height, 0.08), center=(0.0, 5.0 + rail_height/2, 5.0))
for gr in [m_gr_w, m_gr_e, m_gr_n, m_gr_s]:
    structure_prims.append(builder.add_mesh_primitive(gr.vertices, gr.faces.flatten(), gr.vertex_normals, material_idx=mat_glass))

# Brass Handrail Caps
m_cap_w = create_box((0.14, 0.06, 11.0), center=(-7.0, 5.0 + rail_height, -0.5))
m_cap_e = create_box((0.14, 0.06, 11.0), center=(7.0, 5.0 + rail_height, -0.5))
m_cap_n = create_box((14.0, 0.06, 0.14), center=(0.0, 5.0 + rail_height, -6.0))
m_cap_s = create_box((14.0, 0.06, 0.14), center=(0.0, 5.0 + rail_height, 5.0))
for cap in [m_cap_w, m_cap_e, m_cap_n, m_cap_s]:
    structure_prims.append(builder.add_mesh_primitive(cap.vertices, cap.faces.flatten(), cap.vertex_normals, material_idx=mat_gold_trim))

# Ceiling Lights (Floor 2 downlights)
for z_lt in [-12.0, -6.0, 0.0, 6.0, 12.0]:
    for x_lt in [-12.0, 0.0, 12.0]:
        m_lt = create_box((1.4, 0.1, 1.4), center=(x_lt, 9.75, z_lt))
        structure_prims.append(builder.add_mesh_primitive(m_lt.vertices, m_lt.faces.flatten(), m_lt.vertex_normals, material_idx=mat_light_emissive))

node_structure = builder.create_node("Museum_TwoFloor_Structure", structure_prims)
root_children.append(node_structure)


# ----------------- 3. GRAND STAIRCASE & ELEVATOR TOWER -----------------
stair_prims = []

stair_steps = 25
step_rise = 5.0 / stair_steps
step_run = 7.5 / stair_steps
stair_width = 3.2
stair_center_x = 12.5

for i in range(stair_steps):
    step_y = i * step_rise + step_rise / 2.0
    step_z = 7.0 + i * step_run + step_run / 2.0
    m_stp = create_box((stair_width, step_rise, step_run * 1.1), center=(stair_center_x, step_y, step_z))
    stair_prims.append(builder.add_mesh_primitive(m_stp.vertices, m_stp.faces.flatten(), m_stp.vertex_normals, material_idx=mat_dark_metal))
    
    m_nose = create_box((stair_width + 0.02, 0.03, 0.04), center=(stair_center_x, step_y + step_rise/2, step_z + step_run/2))
    stair_prims.append(builder.add_mesh_primitive(m_nose.vertices, m_nose.faces.flatten(), m_nose.vertex_normals, material_idx=mat_gold_trim))

m_stringer_l = create_box((0.12, 5.4, 8.2), center=(stair_center_x - stair_width/2 - 0.06, 2.5, 10.75))
m_stringer_r = create_box((0.12, 5.4, 8.2), center=(stair_center_x + stair_width/2 + 0.06, 2.5, 10.75))
stair_prims.append(builder.add_mesh_primitive(m_stringer_l.vertices, m_stringer_l.faces.flatten(), m_stringer_l.vertex_normals, material_idx=mat_navy_accent))
stair_prims.append(builder.add_mesh_primitive(m_stringer_r.vertices, m_stringer_r.faces.flatten(), m_stringer_r.vertex_normals, material_idx=mat_navy_accent))

m_srail_l = create_box((0.06, 1.0, 8.0), center=(stair_center_x - stair_width/2 - 0.06, 3.2, 10.75))
m_srail_r = create_box((0.06, 1.0, 8.0), center=(stair_center_x + stair_width/2 + 0.06, 3.2, 10.75))
stair_prims.append(builder.add_mesh_primitive(m_srail_l.vertices, m_srail_l.faces.flatten(), m_srail_l.vertex_normals, material_idx=mat_glass))
stair_prims.append(builder.add_mesh_primitive(m_srail_r.vertices, m_srail_r.faces.flatten(), m_srail_r.vertex_normals, material_idx=mat_glass))

# Walkable Invisible Collision Surface for Staircase
m_ramp_coll = create_box((stair_width, 0.1, 8.6), center=(stair_center_x, 2.5, 10.75))
angle = math.atan2(5.0, 7.5)
rot_mat = trimesh.transformations.rotation_matrix(-angle, [1, 0, 0], point=[stair_center_x, 2.5, 10.75])
m_ramp_coll.apply_transform(rot_mat)
stair_prims.append(builder.add_mesh_primitive(m_ramp_coll.vertices, m_ramp_coll.faces.flatten(), m_ramp_coll.vertex_normals, material_idx=mat_floor2))

ss_v, ss_i, ss_n, ss_uv = create_vertical_panel_plane(3.0, 1.1, center=(stair_center_x, 3.2, 6.8), normal=(0, 0, -1))
stair_prims.append(builder.add_mesh_primitive(ss_v, ss_i, ss_n, ss_uv, mat_stair_sign))

# Glass Elevator Tower
for efx, efz in [(14.8, 11.0), (17.5, 11.0), (14.8, 14.5), (17.5, 14.5)]:
    m_ef = create_box((0.15, 10.0, 0.15), center=(efx, 5.0, efz))
    stair_prims.append(builder.add_mesh_primitive(m_ef.vertices, m_ef.faces.flatten(), m_ef.vertex_normals, material_idx=mat_dark_metal))

m_eg_w = create_box((0.06, 9.8, 3.4), center=(14.8, 4.9, 12.75))
m_eg_e = create_box((0.06, 9.8, 3.4), center=(17.5, 4.9, 12.75))
m_eg_s = create_box((2.6, 9.8, 0.06), center=(16.15, 4.9, 14.5))
stair_prims.append(builder.add_mesh_primitive(m_eg_w.vertices, m_eg_w.faces.flatten(), m_eg_w.vertex_normals, material_idx=mat_glass))
stair_prims.append(builder.add_mesh_primitive(m_eg_e.vertices, m_eg_e.faces.flatten(), m_eg_e.vertex_normals, material_idx=mat_glass))
stair_prims.append(builder.add_mesh_primitive(m_eg_s.vertices, m_eg_s.faces.flatten(), m_eg_s.vertex_normals, material_idx=mat_glass))

m_edoor_f1 = create_box((2.4, 2.4, 0.08), center=(16.15, 1.2, 11.0))
stair_prims.append(builder.add_mesh_primitive(m_edoor_f1.vertices, m_edoor_f1.faces.flatten(), m_edoor_f1.vertex_normals, material_idx=mat_chrome))
es1_v, es1_i, es1_n, es1_uv = create_vertical_panel_plane(0.8, 1.6, center=(14.5, 1.4, 10.95), normal=(0, 0, -1))
stair_prims.append(builder.add_mesh_primitive(es1_v, es1_i, es1_n, es1_uv, mat_elevator_sign))

m_edoor_f2 = create_box((2.4, 2.4, 0.08), center=(16.15, 6.2, 11.0))
stair_prims.append(builder.add_mesh_primitive(m_edoor_f2.vertices, m_edoor_f2.faces.flatten(), m_edoor_f2.vertex_normals, material_idx=mat_chrome))
es2_v, es2_i, es2_n, es2_uv = create_vertical_panel_plane(0.8, 1.6, center=(14.5, 6.4, 10.95), normal=(0, 0, -1))
stair_prims.append(builder.add_mesh_primitive(es2_v, es2_i, es2_n, es2_uv, mat_elevator_sign))

node_stair = builder.create_node("Grand_Staircase_And_Elevator", stair_prims)
root_children.append(node_stair)

root_children.append(builder.create_node("Floor1_StairEntry", translation=[12.5, 0.5, 7.0]))
root_children.append(builder.create_node("Floor2_StairExit", translation=[12.5, 5.5, 14.5]))
root_children.append(builder.create_node("Floor1_AccessibleTransition", translation=[16.0, 0.5, 10.0]))
root_children.append(builder.create_node("Floor2_AccessibleTransition", translation=[16.0, 5.5, 10.0]))
root_children.append(builder.create_node("INTERACT_GrandStaircase", translation=[12.5, 1.8, 8.5]))


# ----------------- 4. FLOOR 1 LOBBY, MONUMENT & CAMPUS MODEL -----------------
f1_prims = []

m_w_wall_base = create_box((9.8, 4.6, 0.4), center=(0, 2.3, 10.5))
f1_prims.append(builder.add_mesh_primitive(m_w_wall_base.vertices, m_w_wall_base.faces.flatten(), m_w_wall_base.vertex_normals, material_idx=mat_navy_accent))
wv_v, wv_i, wv_n, wv_uv = create_vertical_panel_plane(9.2, 4.2, center=(0, 2.3, 10.72), normal=(0, 0, 1))
f1_prims.append(builder.add_mesh_primitive(wv_v, wv_i, wv_n, wv_uv, mat_welcome_board))

m_desk_main = create_box((3.2, 1.1, 1.2), center=(6.2, 0.55, 14.5))
m_desk_top = create_box((3.4, 0.08, 1.3), center=(6.2, 1.14, 14.5))
m_desk_trim = create_box((3.24, 0.08, 1.22), center=(6.2, 0.06, 14.5))
f1_prims.append(builder.add_mesh_primitive(m_desk_main.vertices, m_desk_main.faces.flatten(), m_desk_main.vertex_normals, material_idx=mat_walnut_wood))
f1_prims.append(builder.add_mesh_primitive(m_desk_top.vertices, m_desk_top.faces.flatten(), m_desk_top.vertex_normals, material_idx=mat_interior_walls))
f1_prims.append(builder.add_mesh_primitive(m_desk_trim.vertices, m_desk_trim.faces.flatten(), m_desk_trim.vertex_normals, material_idx=mat_gold_trim))

for pot_pos in [(-8.5, 17.0), (8.5, 17.0), (-8.5, 11.5), (8.5, 11.5)]:
    px, pz = pot_pos
    m_pot = create_cylinder(0.4, 0.8, sections=16, center=(px, 0.4, pz))
    m_plant = create_sphere(radius=0.55, center=(px, 1.0, pz))
    f1_prims.append(builder.add_mesh_primitive(m_pot.vertices, m_pot.faces.flatten(), m_pot.vertex_normals, material_idx=mat_pot_ceramic))
    f1_prims.append(builder.add_mesh_primitive(m_plant.vertices, m_plant.faces.flatten(), m_plant.vertex_normals, material_idx=mat_foliage))

for bx, bz in [(-7.5, 14.5), (0.0, 16.5), (-6.0, -7.0), (6.0, -7.0), (-6.0, 1.0), (6.0, 1.0)]:
    m_bseat = create_box((2.4, 0.12, 0.7), center=(bx, 0.45, bz))
    m_bleg1 = create_box((0.1, 0.4, 0.6), center=(bx - 1.0, 0.2, bz))
    m_bleg2 = create_box((0.1, 0.4, 0.6), center=(bx + 1.0, 0.2, bz))
    f1_prims.append(builder.add_mesh_primitive(m_bseat.vertices, m_bseat.faces.flatten(), m_bseat.vertex_normals, material_idx=mat_walnut_wood))
    f1_prims.append(builder.add_mesh_primitive(m_bleg1.vertices, m_bleg1.faces.flatten(), m_bleg1.vertex_normals, material_idx=mat_chrome))
    f1_prims.append(builder.add_mesh_primitive(m_bleg2.vertices, m_bleg2.faces.flatten(), m_bleg2.vertex_normals, material_idx=mat_chrome))

node_f1_lobby = builder.create_node("Floor01_Lobby", f1_prims)
root_children.append(node_f1_lobby)
root_children.append(builder.create_node("INTERACT_Welcome", translation=[0, 2.3, 10.7]))

# Central Monument & Sculpture
sculpture_prims = []
m_pod_1 = create_box((5.6, 0.22, 3.8), center=(0, 0.11, -2.0))
m_pod_1_trim = create_box((5.7, 0.04, 3.9), center=(0, 0.02, -2.0))
m_pod_2 = create_box((4.8, 0.22, 3.0), center=(0, 0.33, -2.0))
m_pod_2_trim = create_box((4.9, 0.05, 3.1), center=(0, 0.44, -2.0))
m_pod_halo = create_box((4.5, 0.03, 2.7), center=(0, 0.45, -2.0))

sculpture_prims.append(builder.add_mesh_primitive(m_pod_1.vertices, m_pod_1.faces.flatten(), m_pod_1.vertex_normals, material_idx=mat_exterior_stone))
sculpture_prims.append(builder.add_mesh_primitive(m_pod_1_trim.vertices, m_pod_1_trim.faces.flatten(), m_pod_1_trim.vertex_normals, material_idx=mat_gold_trim))
sculpture_prims.append(builder.add_mesh_primitive(m_pod_2.vertices, m_pod_2.faces.flatten(), m_pod_2.vertex_normals, material_idx=mat_navy_accent))
sculpture_prims.append(builder.add_mesh_primitive(m_pod_2_trim.vertices, m_pod_2_trim.faces.flatten(), m_pod_2_trim.vertex_normals, material_idx=mat_gold_trim))
sculpture_prims.append(builder.add_mesh_primitive(m_pod_halo.vertices, m_pod_halo.faces.flatten(), m_pod_halo.vertex_normals, material_idx=mat_light_emissive))

m_monolith = create_box((3.4, 2.8, 0.65), center=(0, 2.29, -2.0))
m_col_l = create_box((0.24, 2.8, 0.72), center=(-1.7, 2.29, -2.0))
m_col_r = create_box((0.24, 2.8, 0.72), center=(1.7, 2.29, -2.0))
sculpture_prims.append(builder.add_mesh_primitive(m_monolith.vertices, m_monolith.faces.flatten(), m_monolith.vertex_normals, material_idx=mat_navy_accent))
sculpture_prims.append(builder.add_mesh_primitive(m_col_l.vertices, m_col_l.faces.flatten(), m_col_l.vertex_normals, material_idx=mat_gold_trim))
sculpture_prims.append(builder.add_mesh_primitive(m_col_r.vertices, m_col_r.faces.flatten(), m_col_r.vertex_normals, material_idx=mat_gold_trim))

m_fr_f = create_box((3.0, 2.34, 0.04), center=(0, 2.29, -2.0 + 0.33))
sculpture_prims.append(builder.add_mesh_primitive(m_fr_f.vertices, m_fr_f.faces.flatten(), m_fr_f.vertex_normals, material_idx=mat_gold_trim))
fv_v, fv_i, fv_n, fv_uv = create_vertical_panel_plane(2.86, 2.20, center=(0, 2.29, -2.0 + 0.352), normal=(0, 0, 1))
sculpture_prims.append(builder.add_mesh_primitive(fv_v, fv_i, fv_n, fv_uv, material_idx=mat_sculpture_front))

m_letters = create_3d_vit_letters(center_z=-2.0 + 0.39, y_pos=2.08, scale=0.62, depth=0.06, facing_positive=True)
sculpture_prims.append(builder.add_mesh_primitive(m_letters.vertices, m_letters.faces.flatten(), m_letters.vertex_normals, material_idx=mat_gold_trim))

m_fr_b = create_box((3.0, 2.34, 0.04), center=(0, 2.29, -2.0 - 0.33))
sculpture_prims.append(builder.add_mesh_primitive(m_fr_b.vertices, m_fr_b.faces.flatten(), m_fr_b.vertex_normals, material_idx=mat_gold_trim))
bv_v, bv_i, bv_n, bv_uv = create_vertical_panel_plane(2.86, 2.20, center=(0, 2.29, -2.0 - 0.352), normal=(0, 0, -1))
sculpture_prims.append(builder.add_mesh_primitive(bv_v, bv_i, bv_n, bv_uv, material_idx=mat_sculpture_back))

m_cornice = create_box((3.8, 0.22, 0.95), center=(0, 3.80, -2.0))
sculpture_prims.append(builder.add_mesh_primitive(m_cornice.vertices, m_cornice.faces.flatten(), m_cornice.vertex_normals, material_idx=mat_gold_trim))

node_sculpture = builder.create_node("Central_Landmark_Monument", sculpture_prims)
root_children.append(node_sculpture)
root_children.append(builder.create_node("INTERACT_Central_Sculpture", translation=[0, 2.3, -2.0]))

# Campus Miniature Model (Z = 4.2)
campus_prims = []
m_cbase = create_box((4.2, 0.85, 3.2), center=(0, 0.425, 4.2))
m_ctrim = create_box((4.3, 0.08, 3.3), center=(0, 0.86, 4.2))
campus_prims.append(builder.add_mesh_primitive(m_cbase.vertices, m_cbase.faces.flatten(), m_cbase.vertex_normals, material_idx=mat_navy_accent))
campus_prims.append(builder.add_mesh_primitive(m_ctrim.vertices, m_ctrim.faces.flatten(), m_ctrim.vertex_normals, material_idx=mat_gold_trim))

map_v, map_i, map_n, map_uv = create_plane_with_uvs(4.0, 3.0, center=(0, 0.91, 4.2), horizontal=True)
campus_prims.append(builder.add_mesh_primitive(map_v, map_i, map_n, map_uv, mat_campus_map))

m_tt = create_box((0.8, 0.7, 0.5), center=(-0.8, 1.26, 3.5))
m_sjt = create_box((0.9, 0.9, 0.5), center=(0.0, 1.36, 4.8))
m_mb = create_box((0.6, 0.45, 0.6), center=(-1.2, 1.135, 4.4))
m_anna = create_cylinder(0.4, 0.35, sections=16, center=(1.1, 1.085, 4.2))
for bm in [m_tt, m_sjt, m_mb, m_anna]:
    campus_prims.append(builder.add_mesh_primitive(bm.vertices, bm.faces.flatten(), bm.vertex_normals, material_idx=mat_interior_walls))

m_gcase = create_box((4.1, 1.0, 3.1), center=(0, 1.41, 4.2))
campus_prims.append(builder.add_mesh_primitive(m_gcase.vertices, m_gcase.faces.flatten(), m_gcase.vertex_normals, material_idx=mat_glass))

node_campus = builder.create_node("Campus_Miniature_Model", campus_prims)
root_children.append(node_campus)
root_children.append(builder.create_node("INTERACT_Campus_Model", translation=[0, 1.2, 4.2]))


# ----------------- 5. FLOOR 1 WINGS (History Timeline & Academics) -----------------
history_prims = []
h_bv, h_bi, h_bn, h_buv = create_vertical_panel_plane(7.0, 1.4, center=(-18.15, 4.2, -4.0), normal=(1, 0, 0))
history_prims.append(builder.add_mesh_primitive(h_bv, h_bi, h_bn, h_buv, mat_hist_hdr))

z_hist = [-13.5, -10.5, -7.5, -4.5, -1.5, 1.5, 4.5]
for idx, z_p in enumerate(z_hist):
    m_frame = create_box((0.08, 2.2, 2.2), center=(-18.18, 2.4, z_p))
    history_prims.append(builder.add_mesh_primitive(m_frame.vertices, m_frame.faces.flatten(), m_frame.vertex_normals, material_idx=mat_navy_accent))
    pv, pi, pn, puv = create_vertical_panel_plane(2.0, 2.0, center=(-18.12, 2.4, z_p), normal=(1, 0, 0))
    history_prims.append(builder.add_mesh_primitive(pv, pi, pn, puv, mat_panels_hist[idx]))

m_kiosk_h = create_box((0.8, 1.1, 0.4), center=(-15.5, 0.55, -5.0))
history_prims.append(builder.add_mesh_primitive(m_kiosk_h.vertices, m_kiosk_h.faces.flatten(), m_kiosk_h.vertex_normals, material_idx=mat_dark_metal))
ks_v, ks_i, ks_n, ks_uv = create_vertical_panel_plane(0.9, 0.65, center=(-15.45, 1.35, -5.0), normal=(1, 0, 0))
history_prims.append(builder.add_mesh_primitive(ks_v, ks_i, ks_n, ks_uv, mat_scr_hist))

node_hist = builder.create_node("Floor01_History_Section", history_prims)
root_children.append(node_hist)
root_children.append(builder.create_node("INTERACT_VIT_History", translation=[-18.0, 2.5, -4.0]))
root_children.append(builder.create_node("INTERACT_History_1984", translation=[-18.0, 2.4, -13.5]))
root_children.append(builder.create_node("INTERACT_Founder", translation=[-18.0, 2.4, -10.5]))
root_children.append(builder.create_node("INTERACT_History_UniversityStatus", translation=[-18.0, 2.4, -7.5]))
root_children.append(builder.create_node("INTERACT_CampusPhoto_TechnologyTower", translation=[-18.0, 2.4, -4.5]))
root_children.append(builder.create_node("INTERACT_History_ABET", translation=[-18.0, 2.4, -1.5]))
root_children.append(builder.create_node("INTERACT_History_IoE", translation=[-18.0, 2.4, 1.5]))

# Academics Wing
acad_prims = []
a_bv, a_bi, a_bn, a_buv = create_vertical_panel_plane(7.0, 1.4, center=(18.15, 4.2, -4.0), normal=(-1, 0, 0))
acad_prims.append(builder.add_mesh_primitive(a_bv, a_bi, a_bn, a_buv, mat_acad_hdr))

z_acad = [-12.0, -7.0, -2.0, 3.0]
for idx, z_p in enumerate(z_acad):
    m_frame = create_box((0.08, 2.4, 2.6), center=(18.18, 2.4, z_p))
    acad_prims.append(builder.add_mesh_primitive(m_frame.vertices, m_frame.faces.flatten(), m_frame.vertex_normals, material_idx=mat_navy_accent))
    pv, pi, pn, puv = create_vertical_panel_plane(2.4, 2.2, center=(18.12, 2.4, z_p), normal=(-1, 0, 0))
    acad_prims.append(builder.add_mesh_primitive(pv, pi, pn, puv, mat_panels_acad[idx]))

m_kiosk_a = create_box((0.8, 1.1, 0.4), center=(15.5, 0.55, -4.0))
acad_prims.append(builder.add_mesh_primitive(m_kiosk_a.vertices, m_kiosk_a.faces.flatten(), m_kiosk_a.vertex_normals, material_idx=mat_dark_metal))
aks_v, aks_i, aks_n, aks_uv = create_vertical_panel_plane(0.9, 0.65, center=(15.45, 1.35, -4.0), normal=(-1, 0, 0))
acad_prims.append(builder.add_mesh_primitive(aks_v, aks_i, aks_n, aks_uv, mat_scr_acad))

node_acad = builder.create_node("Floor01_Academics_Section", acad_prims)
root_children.append(node_acad)
root_children.append(builder.create_node("INTERACT_Academics", translation=[18.0, 2.5, -4.0]))
root_children.append(builder.create_node("INTERACT_FFCS", translation=[18.0, 2.4, -7.0]))
root_children.append(builder.create_node("INTERACT_CampusPhoto_Library", translation=[18.0, 2.4, -2.0]))
root_children.append(builder.create_node("INTERACT_CampusPhoto_MainBuilding", translation=[18.0, 2.4, 3.0]))


# ----------------- 6. FLOOR 2 GALLERIES (Research, Achievements, Global & Life) -----------------

# Floor 2 West Gallery: Research & Innovation
res_prims = []
r_bv, r_bi, r_bn, r_buv = create_vertical_panel_plane(7.0, 1.4, center=(-18.15, 8.8, -4.0), normal=(1, 0, 0))
res_prims.append(builder.add_mesh_primitive(r_bv, r_bi, r_bn, r_buv, mat_res_hdr))

for idx, z_p in enumerate([-12.0, -7.0, -1.0, 4.0]):
    m_fr = create_box((0.08, 2.4, 2.6), center=(-18.18, 7.3, z_p))
    res_prims.append(builder.add_mesh_primitive(m_fr.vertices, m_fr.faces.flatten(), m_fr.vertex_normals, material_idx=mat_navy_accent))
    pv, pi, pn, puv = create_vertical_panel_plane(2.4, 2.2, center=(-18.12, 7.3, z_p), normal=(1, 0, 0))
    res_prims.append(builder.add_mesh_primitive(pv, pi, pn, puv, mat_panels_acad[idx]))

m_rtable_base = create_box((4.2, 0.88, 2.8), center=(-12.5, 5.44, -4.0))
m_rtable_rim = create_box((4.4, 0.08, 3.0), center=(-12.5, 5.92, -4.0))
res_prims.append(builder.add_mesh_primitive(m_rtable_base.vertices, m_rtable_base.faces.flatten(), m_rtable_base.vertex_normals, material_idx=mat_dark_metal))
res_prims.append(builder.add_mesh_primitive(m_rtable_rim.vertices, m_rtable_rim.faces.flatten(), m_rtable_rim.vertex_normals, material_idx=mat_gold_trim))

rt_v, rt_i, rt_n, rt_uv = create_plane_with_uvs(4.0, 2.6, center=(-12.5, 5.98, -4.0), horizontal=True)
res_prims.append(builder.add_mesh_primitive(rt_v, rt_i, rt_n, rt_uv, mat_res_table))

node_res = builder.create_node("Floor02_Research_Section", res_prims)
root_children.append(node_res)
root_children.append(builder.create_node("INTERACT_Research", translation=[-18.0, 7.5, -4.0]))
root_children.append(builder.create_node("INTERACT_ResearchCentres", translation=[-18.0, 7.3, -7.0]))
root_children.append(builder.create_node("INTERACT_Research_Table", translation=[-12.5, 6.0, -4.0]))
root_children.append(builder.create_node("INTERACT_VITTBI", translation=[-18.0, 7.3, 1.0]))

# Floor 2 North Wall: Wall of Achievements
ach_prims = []
ac_v, ac_i, ac_n, ac_uv = create_vertical_panel_plane(14.0, 4.4, center=(8.5, 7.4, -16.15), normal=(0, 0, 1))
ach_prims.append(builder.add_mesh_primitive(ac_v, ac_i, ac_n, ac_uv, mat_achieve_wall))

for p_idx, px in enumerate([4.0, 8.5, 13.0]):
    m_pbase = create_box((1.2, 0.9, 1.0), center=(px, 5.45, -14.2))
    m_ptrim = create_box((1.26, 0.06, 1.06), center=(px, 5.92, -14.2))
    ach_prims.append(builder.add_mesh_primitive(m_pbase.vertices, m_pbase.faces.flatten(), m_pbase.vertex_normals, material_idx=mat_navy_accent))
    ach_prims.append(builder.add_mesh_primitive(m_ptrim.vertices, m_ptrim.faces.flatten(), m_ptrim.vertex_normals, material_idx=mat_gold_trim))
    
    m_tbase = create_cylinder(0.18, 0.1, center=(px, 6.0, -14.2))
    m_tcup = create_cylinder(0.22, 0.35, center=(px, 6.25, -14.2))
    ach_prims.append(builder.add_mesh_primitive(m_tbase.vertices, m_tbase.faces.flatten(), m_tbase.vertex_normals, material_idx=mat_gold_trim))
    ach_prims.append(builder.add_mesh_primitive(m_tcup.vertices, m_tcup.faces.flatten(), m_tcup.vertex_normals, material_idx=mat_gold_emissive))
    
    m_tg = create_box((1.1, 0.8, 0.9), center=(px, 6.35, -14.2))
    ach_prims.append(builder.add_mesh_primitive(m_tg.vertices, m_tg.faces.flatten(), m_tg.vertex_normals, material_idx=mat_glass))

ach_scr_v, ach_scr_i, ach_scr_n, ach_scr_uv = create_vertical_panel_plane(1.1, 0.8, center=(1.8, 6.5, -14.5), normal=(0, 0, 1))
ach_prims.append(builder.add_mesh_primitive(ach_scr_v, ach_scr_i, ach_scr_n, ach_scr_uv, mat_scr_ach))

node_ach = builder.create_node("Floor02_Achievements_Section", ach_prims)
root_children.append(node_ach)
root_children.append(builder.create_node("INTERACT_Achievements", translation=[8.5, 7.5, -16.0]))

# Floor 2 South Wall: Global VIT
global_prims = []
gm_v, gm_i, gm_n, gm_uv = create_vertical_panel_plane(13.5, 4.4, center=(0.0, 7.4, 14.15), normal=(0, 0, -1))
global_prims.append(builder.add_mesh_primitive(gm_v, gm_i, gm_n, gm_uv, mat_global_map))

node_global = builder.create_node("Floor02_Global_Section", global_prims)
root_children.append(node_global)
root_children.append(builder.create_node("INTERACT_Global", translation=[0.0, 7.5, 14.0]))

# Floor 2 East Gallery: Life at VIT
life_prims = []
st_v, st_i, st_n, st_uv = create_vertical_panel_plane(14.0, 4.4, center=(18.15, 7.4, -4.0), normal=(-1, 0, 0))
life_prims.append(builder.add_mesh_primitive(st_v, st_i, st_n, st_uv, mat_student_wall))

m_car_ped = create_box((3.2, 0.7, 1.8), center=(14.0, 5.35, 3.5))
life_prims.append(builder.add_mesh_primitive(m_car_ped.vertices, m_car_ped.faces.flatten(), m_car_ped.vertex_normals, material_idx=mat_navy_accent))
m_car_body = create_box((2.2, 0.35, 0.9), center=(14.0, 5.85, 3.5))
m_car_wing_f = create_box((0.3, 0.1, 1.4), center=(14.0, 5.8, 4.5))
m_car_wing_r = create_box((0.4, 0.25, 1.3), center=(14.0, 6.1, 2.5))
life_prims.append(builder.add_mesh_primitive(m_car_body.vertices, m_car_body.faces.flatten(), m_car_body.vertex_normals, material_idx=mat_gold_trim))
life_prims.append(builder.add_mesh_primitive(m_car_wing_f.vertices, m_car_wing_f.faces.flatten(), m_car_wing_f.vertex_normals, material_idx=mat_dark_metal))
life_prims.append(builder.add_mesh_primitive(m_car_wing_r.vertices, m_car_wing_r.faces.flatten(), m_car_wing_r.vertex_normals, material_idx=mat_dark_metal))
for wx, wz in [(13.2, 2.8), (14.8, 2.8), (13.2, 4.2), (14.8, 4.2)]:
    m_whl = create_cylinder(0.22, 0.15, sections=12, center=(wx, 5.8, wz))
    life_prims.append(builder.add_mesh_primitive(m_whl.vertices, m_whl.faces.flatten(), m_whl.vertex_normals, material_idx=mat_dark_metal))

m_car_case = create_box((3.1, 0.9, 1.7), center=(14.0, 6.2, 3.5))
life_prims.append(builder.add_mesh_primitive(m_car_case.vertices, m_car_case.faces.flatten(), m_car_case.vertex_normals, material_idx=mat_glass))

node_life = builder.create_node("Floor02_StudentLife_Section", life_prims)
root_children.append(node_life)
root_children.append(builder.create_node("INTERACT_StudentLife", translation=[18.0, 7.5, -4.0]))
root_children.append(builder.create_node("INTERACT_Riviera", translation=[18.0, 7.4, -9.0]))
root_children.append(builder.create_node("INTERACT_graVITas", translation=[18.0, 7.4, 1.0]))
root_children.append(builder.create_node("INTERACT_StudentChapters", translation=[18.0, 7.4, 6.0]))

# Floor 2 Tour Finale
finale_prims = []
fin_v, fin_i, fin_n, fin_uv = create_vertical_panel_plane(9.2, 4.0, center=(0.0, 7.4, -6.15), normal=(0, 0, 1))
finale_prims.append(builder.add_mesh_primitive(fin_v, fin_i, fin_n, fin_uv, mat_finale))

node_finale = builder.create_node("Floor02_Finale_Section", finale_prims)
root_children.append(node_finale)
root_children.append(builder.create_node("INTERACT_Convocation", translation=[6.0, 7.5, 9.5]))
root_children.append(builder.create_node("INTERACT_Finale", translation=[0.0, 7.4, -6.0]))


# ----------------- 7. COMPATIBILITY ANCHOR PLANES (PLANE_001 to PLANE_031) -----------------
for i in range(1, 11):
    code = f"{i:03d}"
    pz = -13.5 + (i - 1) * 1.9
    pv, pi, pn, puv = create_vertical_panel_plane(1.4, 1.1, center=(-18.05, 2.5, pz), normal=(1, 0, 0))
    p_node = builder.create_node(f"PLANE_{code}", [builder.add_mesh_primitive(pv, pi, pn, puv, mat_panels_hist[min(i-1, 6)])])
    root_children.append(p_node)

for i in range(11, 21):
    code = f"{i:03d}"
    pz = -13.5 + (i - 11) * 1.9
    pv, pi, pn, puv = create_vertical_panel_plane(1.4, 1.1, center=(18.05, 2.5, pz), normal=(-1, 0, 0))
    p_node = builder.create_node(f"PLANE_{code}", [builder.add_mesh_primitive(pv, pi, pn, puv, mat_panels_acad[min((i-11)%4, 3)])])
    root_children.append(p_node)

for i in range(21, 26):
    code = f"{i:03d}"
    px = 3.0 + (i - 21) * 2.8
    pv, pi, pn, puv = create_vertical_panel_plane(1.5, 1.2, center=(px, 7.5, -16.05), normal=(0, 0, 1))
    p_node = builder.create_node(f"PLANE_{code}", [builder.add_mesh_primitive(pv, pi, pn, puv, mat_achieve_wall)])
    root_children.append(p_node)

for i in range(26, 32):
    code = f"{i:03d}"
    pz = -12.0 + (i - 26) * 2.8
    pv, pi, pn, puv = create_vertical_panel_plane(1.5, 1.2, center=(18.05, 7.5, pz), normal=(-1, 0, 0))
    p_node = builder.create_node(f"PLANE_{code}", [builder.add_mesh_primitive(pv, pi, pn, puv, mat_student_wall)])
    root_children.append(p_node)


# ----------------- 8. 16 GUIDED TOUR STOP ANCHOR NODES -----------------
tour_positions = [
    ("TOUR_01_Welcome", [0.0, 0.0, 14.5]),
    ("TOUR_02_Origins", [-14.0, 0.0, -12.0]),
    ("TOUR_03_Founder", [-14.0, 0.0, -9.0]),
    ("TOUR_04_Academics", [-14.0, 0.0, -1.0]),
    ("TOUR_05_Schools", [14.0, 0.0, -11.0]),
    ("TOUR_06_FFCS", [14.0, 0.0, -4.0]),
    ("TOUR_07_CampusModel", [0.0, 0.0, 6.5]),
    ("TOUR_08_CentralMonument", [0.0, 0.0, 1.5]),
    ("TOUR_09_Staircase", [8.5, 0.0, 9.0]),
    ("TOUR_10_Research", [-13.0, 5.0, -3.0]),
    ("TOUR_11_ResearchTable", [-11.0, 5.0, -6.5]),
    ("TOUR_12_Achievements", [8.0, 5.0, -12.0]),
    ("TOUR_13_Global", [0.0, 5.0, 6.5]),
    ("TOUR_14_StudentLife", [13.0, 5.0, -6.0]),
    ("TOUR_15_TechnicalCulture", [13.0, 5.0, 2.0]),
    ("TOUR_16_Finale", [0.0, 5.0, 1.0])
]

for t_name, t_pos in tour_positions:
    root_children.append(builder.create_node(t_name, translation=t_pos))


# ----------------- 9. SPAWN POINTS & ROOT ASSEMBLY -----------------
node_spawn1 = builder.create_node("PlayerSpawn", translation=[0.0, 1.6, 15.0], rotation=[0.0, 1.0, 0.0, 0.0])
node_spawn2 = builder.create_node("Floor2Spawn", translation=[12.5, 6.6, 14.0], rotation=[0.0, 1.0, 0.0, 0.0])
node_spawna = builder.create_node("AtriumSpawn", translation=[0.0, 1.6, 1.5], rotation=[0.0, 1.0, 0.0, 0.0])

root_children.extend([node_spawn1, node_spawn2, node_spawna])

root_node_idx = builder.create_node("VIT_Vellore_Museum_Root", children=root_children)
builder.gltf.scenes[0].nodes = [root_node_idx]

print("Exporting two-floor GLB files...")
builder.export(OUTPUT_GLB_ROOT)
builder.export(OUTPUT_GLB_ASSETS)

print("--- Two-Floor VIT Vellore Virtual Museum GLB Generation Complete! ---")
