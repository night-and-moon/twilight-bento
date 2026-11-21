#!/usr/bin/env python3
"""Bundle Twilight Bento Obsidian Theme from base Things + 11 CSS modules + 13 palettes."""

import os, re, shutil

VAULT = "/home/khai/SmartKnowledge"
OUT_DIR = "/home/khai/.gemini/antigravity/scratch/twilight-bento"
INSTALL_DIR = os.path.join(VAULT, ".obsidian/themes/Twilight Bento")

SNIPPETS = [
    "10-bento-ui.css",
    "11-dashboard-v4.css",
    "12-sketchbook-global.css",
    "13-list-indent-lines.css",
    "14-pdf-dark-tint.css",
    "15-image-adjustments-zoom.css",
    "16-aside-callout.css",
    "17-workspace-backdrop.css",
    "18-embeds-advanced-callouts.css",
    "19-emphasis-floating-bars.css",
    "21-custom-checkboxes.css",
]

parts = []

# 1. Palettes & @settings block at top so Style Settings parses it cleanly
with open(os.path.join(OUT_DIR, "palettes.css"), "r", encoding="utf-8") as f:
    pal_css = f.read()

# Split @settings comment from palette rules so @settings is at top, rules at bottom
m = re.match(r"(/\* @settings.*?\*/)(.*)", pal_css, re.S)
assert m, "Missing @settings block in palettes.css"
settings_block, palette_rules = m.group(1), m.group(2)

parts.append(settings_block + "\n")

# 2. Base Things theme.css
with open(os.path.join(VAULT, ".obsidian/themes/Things/theme.css"), "r", encoding="utf-8") as f:
    parts.append("/* === BASE THEME: Things (MIT) === */\n" + f.read() + "\n")

# 3. All 11 modular snippets in order
for sn in SNIPPETS:
    fp = os.path.join(VAULT, ".obsidian/snippets", sn)
    with open(fp, "r", encoding="utf-8") as f:
        parts.append(f"\n/* === MODULE: {sn} === */\n" + f.read() + "\n")

# 4. Palette override rules at the end so Style Settings selection wins
parts.append("\n/* === STYLE SETTINGS PALETTE OVERRIDES === */\n" + palette_rules + "\n")

theme_css = "\n".join(parts)
out_css = os.path.join(OUT_DIR, "theme.css")
with open(out_css, "w", encoding="utf-8") as f:
    f.write(theme_css)

# Validate braces across the compiled theme.css
clean = re.sub(r"/\*.*?\*/", "", theme_css, flags=re.S)
ob, cb = clean.count("{"), clean.count("}")
assert ob == cb, f"Brace mismatch in compiled theme.css: {ob} vs {cb}"

# Copy examples
ex_dir = os.path.join(OUT_DIR, "examples")
os.makedirs(ex_dir, exist_ok=True)
shutil.copy2(os.path.join(VAULT, "Dashboard.md"), os.path.join(ex_dir, "Dashboard.md"))
shutil.copy2(os.path.join(VAULT, "System/Bases/Projects.base"), os.path.join(ex_dir, "Projects.base"))

# Install locally into vault .obsidian/themes/SmartKnowledge/ for immediate testing
os.makedirs(INSTALL_DIR, exist_ok=True)
shutil.copy2(out_css, os.path.join(INSTALL_DIR, "theme.css"))
shutil.copy2(os.path.join(OUT_DIR, "manifest.json"), os.path.join(INSTALL_DIR, "manifest.json"))

print(f"Built theme.css: {len(theme_css):,} bytes | Braces: {ob}/{cb} (balanced)")
print(f"Installed to: {INSTALL_DIR}")
