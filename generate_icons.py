#!/usr/bin/env python3
"""Generate 16x16 pixel art icons for Yoto MYO cards.

Design philosophy: Pixel Soul
- Every pixel is a decision
- Silhouette is supreme
- Color carries identity
- Boldness over cleverness
- The grid is sacred geometry

Yoto specs: 16x16 PNG, transparent background, no black.
"""

from PIL import Image
import os

OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".out")

# ═══════════════════════════════════════════════
# Color palette — vibrant, no black, Yoto-safe
# ═══════════════════════════════════════════════
C = {
    "_": (0, 0, 0, 0),           # Transparent
    # Blues (Disney castle)
    "B": (41, 121, 255, 255),    # Royal blue
    "b": (130, 177, 255, 255),   # Sky blue (windows)
    "D": (21, 76, 187, 255),     # Deep blue (shadow)
    # Yellows
    "Y": (255, 214, 0, 255),     # Bright yellow (flag, bear)
    "y": (255, 238, 88, 255),    # Light yellow (bear highlight)
    # Reds / Warm
    "R": (213, 0, 0, 255),       # Deep red (pirate hat)
    "r": (239, 83, 80, 255),     # Bright red (hat accent)
    # Dark crimson
    "M": (136, 14, 79, 255),     # Maroon (hat shadow)
    # White / Gray
    "W": (255, 255, 255, 255),   # White (piano keys, pages)
    "A": (120, 120, 120, 255),   # Gray (headphones)
    "a": (180, 180, 180, 255),   # Light gray
    # Teal / Green
    "T": (0, 137, 123, 255),     # Teal (book)
    "t": (77, 182, 172, 255),    # Light teal
    "E": (46, 125, 50, 255),     # Dark green
    # Brown
    "N": (93, 64, 55, 255),      # Dark brown (bear features)
    "n": (141, 110, 99, 255),    # Medium brown
    # Orange
    "O": (255, 152, 0, 255),     # Orange (bear nose)
    # Skull / crossbones
    "S": (224, 224, 224, 255),   # Bone white
    # Piano
    "P": (38, 50, 56, 255),      # Very dark blue-gray (piano black keys)
}


def parse_grid(text):
    rows = [line for line in text.strip().splitlines()]
    assert len(rows) == 16, f"Expected 16 rows, got {len(rows)}"
    grid = []
    for i, row in enumerate(rows):
        assert len(row) == 16, f"Row {i} has {len(row)} chars: '{row}'"
        grid.append([C[ch] for ch in row])
    return grid


def save_icon(name, grid):
    img = Image.new("RGBA", (16, 16))
    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            img.putpixel((x, y), color)
    path = os.path.join(OUTDIR, name, "icon.png")
    img.save(path)
    # Also save a 16x upscaled preview for human review
    preview = img.resize((256, 256), Image.NEAREST)
    preview_path = os.path.join(OUTDIR, name, "icon_preview.png")
    preview.save(preview_path)
    print(f"  {name}")
    print(f"    → {path}")
    print(f"    → {preview_path}")


# ═══════════════════════════════════════════════
# 1. דיסני (Disney) — Blue castle with yellow flag
#
#    Silhouette: three turrets, central tallest,
#    flag at peak, arched doorway at base.
#    Palette: royal blue body, sky blue windows,
#    bright yellow flag.
# ═══════════════════════════════════════════════
disney = parse_grid("""
______YY________
_______B________
__B___BBB___B___
_BBB__BBB__BBB__
_BBB_BBBBB_BBB__
_BBBBBBBBBBBBB__
__BBBBBBBBBBB___
__BBbBBBBBbBB___
__BBbBBBBBbBB___
__BBBBBBBBBBB___
__BBBBBBBBBBB___
__BBBBBbBBBBB___
__BBBB___BBBB___
__BBBB___BBBB___
_BBBBBBBBBBBBB__
________________
""")

# ═══════════════════════════════════════════════
# 2. מגש הקצב (Magash HaKetsev) — Pirate hat
#
#    Silhouette: classic tricorn pirate hat with
#    skull-and-crossbones motif. ברמלי the pirate!
#    Palette: deep red body, maroon shadow,
#    bone-white skull.
# ═══════════════════════════════════════════════
magash = parse_grid("""
________________
________YY______
_______YY_______
______RRRR______
_____RRRRRR_____
____RRRRRRRR____
____RRRRRRRR____
____RRRRRRRR____
____RRRRRRRR____
___RRRRRRRRRR___
__RRRRRRRRRRRR__
_YYYYYYYYYYYYYY_
RRRRRRRRRRRRRRRR
RRRRRRRRRRRRRRRR
________________
________________
""")

# ═══════════════════════════════════════════════
# 3. שלמה גרוניך (Shlomo Gronich) — Stork (חסידה)
#
#    His most iconic song. White stork standing
#    on one red leg, red beak pointing right.
#    Bold, simple, unmistakable bird silhouette.
# ═══════════════════════════════════════════════
gronich = parse_grid("""
________________
_______aa_______
______aaaa______
_____aaaaRRR____
______aaaa______
______aaaa______
_____aaaaaa_____
____aaaAAAAa____
____aAAAAAAa____
____aAAAAAAa____
_____aaaaaa_____
_______RR_______
_______RR_______
_______RR_______
______RRRR______
________________
""")

# ═══════════════════════════════════════════════
# 4. ניר פרידמן מספר (Nir Friedman) — Cat face
#
#    שאול החתול (Pete the Cat) appears twice.
#    Blue cat face with pointy ears, brown eyes,
#    pink nose. Bold, simple, kid-friendly.
# ═══════════════════════════════════════════════
friedman = parse_grid("""
________________
_BB__________BB_
_BBBB______BBBB_
_BBBBB____BBBBB_
__BBBBBBBBBBBB__
_BBBBBBBBBBBBBB_
_BBBBBBBBBBBBBB_
_BBNNBBBBBBNNBB_
_BBNNBBBBBBNNBB_
_BBBBBBBBBBBBBB_
_BBBBBBRRBBBBBB_
_BBBBBBBBBBBBBB_
__BBBBBBBBBBBB__
___BBBBBBBBBB___
____BBBBBBBB____
________________
""")

# ═══════════════════════════════════════════════
# 5. לאה גולדברג (Leah Goldberg) — Yellow bear face
#
#    Silhouette: round bear face with two round
#    ears on top, simple dot eyes, small nose.
#    הדב הצהוב — The Yellow Bear!
#    Palette: bright yellow body, light yellow
#    inner ears/muzzle, brown eyes and nose.
# ═══════════════════════════════════════════════
goldberg = parse_grid("""
________________
___YY______YY___
__YYYY____YYYY__
__YYYY____YYYY__
___YYYYYYYYYY___
__YYYYYYYYYYYY__
__YYYYYYYYYYYY__
__YYNYYYYYYNYY__
__YYNYYYYYYNYY__
__YYYYyyyyYYYY__
__YYYYyNNyYYYY__
__YYYYyyyyYYYY__
___YYYYYYYYYY___
____YYYYYYYY____
_____YYYYYY_____
________________
""")


# ═══════════════════════════════════════════════
# Generate all icons
# ═══════════════════════════════════════════════
ICONS = {
    "דיסני": disney,
    "מגש הקצב": magash,
    "שלמה גרוניך": gronich,
    "ניר פרידמן מספר": friedman,
    "סיפורים ושירים לילדים מאת לאה גולדברג": goldberg,
}

if __name__ == "__main__":
    print("Generating Yoto 16×16 pixel art icons...\n")
    for name, grid in ICONS.items():
        save_icon(name, grid)
    print("\nDone! Each directory has icon.png (16×16) + icon_preview.png (256×256).")
