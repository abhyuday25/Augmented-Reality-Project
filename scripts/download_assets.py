import urllib.request
import re
import ssl
import json
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# 1. Download official VIT Logo from Wikimedia
logo_url = "https://upload.wikimedia.org/wikipedia/en/thumb/b/bf/Vellore_Institute_of_Technology_logo.svg/1280px-Vellore_Institute_of_Technology_logo.svg.png"
seal_url = "https://upload.wikimedia.org/wikipedia/en/thumb/c/c5/Vellore_Institute_of_Technology_seal_2017.svg/1280px-Vellore_Institute_of_Technology_seal_2017.svg.png"

out_dir = os.path.join(os.path.dirname(__file__), "downloaded_assets")
os.makedirs(out_dir, exist_ok=True)

def download_file(url, out_name):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = resp.read()
            target = os.path.join(out_dir, out_name)
            with open(target, "wb") as f:
                f.write(data)
            print(f"Downloaded {out_name} ({len(data)} bytes) from {url}")
            return target
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

download_file(logo_url, "vit_logo_official.png")
download_file(seal_url, "vit_seal_official.png")

# 2. Let's check campus gallery or search for main gate image
try:
    req = urllib.request.Request("https://vit.ac.in/about/gallery", headers=headers)
    html = urllib.request.urlopen(req, context=ctx, timeout=10).read().decode('utf-8', errors='ignore')
    imgs = list(set(re.findall(r'https?://[^\s\"\'<>]+\.(?:jpg|jpeg|png|webp)', html, re.I)))
    print(f"Found {len(imgs)} gallery images from vit.ac.in:")
    for img in imgs:
        if 'gate' in img.lower() or 'campus' in img.lower() or 'entrance' in img.lower() or 'main' in img.lower() or 'gallery' in img.lower():
            print("Candidate:", img)
except Exception as e:
    print("Gallery error:", e)
