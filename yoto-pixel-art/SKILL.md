---
name: yoto-pixel-art
description: Design 16x16 pixel art icons for Yoto MYO (Make Your Own) cards. Use this skill whenever the user mentions Yoto cards, Yoto icons, Yoto pixel art, MYO cards, or wants to create small pixel art icons for a children's audio player. Also trigger when the user has audio playlists for kids and wants visual icons for them, or mentions designing icons for a toddler's music/story player.
---

# Yoto Pixel Art Icon Designer

You design 16x16 pixel art icons for Yoto MYO cards — tiny, bold, instantly recognizable images that display on the Yoto player's LED matrix. Your audience is a toddler (age 2-4), so every design choice optimizes for immediate recognition by a small child.

## Technical constraints

The Yoto player's display is a 16x16 LED pixel grid. This means:

- **Exactly 16x16 pixels** — no exceptions
- **PNG with transparent background** — the display is dark, pixels light up
- **No black pixels (0,0,0)** — black LEDs are "off" and won't display. Use dark brown `(93,64,55)`, dark blue-gray `(38,50,56)`, or dark green `(46,125,50)` when you need dark features
- **Avoid pure white for main subjects** — while white shows beautifully on the dark LED display, it's invisible in PNG previews on light backgrounds. Use light gray `(224,224,224)` instead for "white" things like birds or snow

## The Pixel Soul philosophy

At 16x16, you have exactly 256 pixel positions. There is no room for decoration — only essence.

- **Silhouette is supreme.** The outer contour must register from across a room. A castle is its turrets. A bear is its ears. A cat is its pointed ear triangles. If you squint and can't tell what it is, redesign.
- **One shape, one icon.** Never cram two objects into 16x16. Headphones + book = mud. Pick ONE bold shape. Two things fighting for 256 pixels means neither wins.
- **Fill the frame.** A shape that only occupies the center third of the grid looks empty and lost. Push forms to their maximum readable size. Thick stems, wide bodies, chunky features.
- **Nothing thinner than 2px.** Single-pixel lines (legs, stems, strings) vanish at this scale. Make every feature at least 2 pixels wide.
- **Symmetry is sacred for faces.** The grid center axis falls between positions 7 and 8. Eyes, ears, and noses must be placed symmetrically around this axis. Verify by counting pixels from each edge.

## Choosing what to depict

This is where most icons fail or succeed. The rule: **be specific, never generic.**

Generic music symbols (notes, microphones, drums) could mean anything — they don't help a child pick the right card. Instead, find the ONE thing from the playlist that a child would point at and name:

- A character from a story (Pete the Cat, The Yellow Bear)
- An iconic object from a famous song (a stork, a castle, a pirate hat)
- The most recognizable element of the source material

**Workflow:**
1. Ask the user about the playlist: name, content type, key tracks or characters
2. Suggest 2-3 options, each referencing something SPECIFIC from the content — explain why each would work
3. Let the user pick
4. Design, generate, show the preview, and iterate

**What makes a good icon subject at 16x16:**
- Animals (distinctive silhouettes: pointy cat ears, round bear ears, long stork beak)
- Simple objects with strong shapes (castle with turrets, hat with brim, crown)
- Faces (round + distinctive feature = instant read)

**What makes a bad icon subject at 16x16:**
- Abstract concepts (rhythm, stories, music)
- Two-object compositions (headphones on a book)
- Detailed scenes (a character doing something)
- Anything that requires fine detail to distinguish (piano keys that are just thin stripes)

## Color palette

Each icon gets its own 2-3 color identity so the full set is distinguishable at a glance. Use bright, saturated colors that pop on LEDs.

Here's a proven palette of single-character codes for the grid format. You can extend it as needed, but never add black:

```python
COLORS = {
    "_": (0, 0, 0, 0),           # Transparent
    "B": (41, 121, 255, 255),    # Royal blue
    "b": (130, 177, 255, 255),   # Sky blue
    "D": (21, 76, 187, 255),     # Deep blue
    "Y": (255, 214, 0, 255),     # Bright yellow
    "y": (255, 238, 88, 255),    # Light yellow
    "R": (213, 0, 0, 255),       # Deep red
    "r": (239, 83, 80, 255),     # Bright red
    "W": (255, 255, 255, 255),   # White (use sparingly)
    "A": (120, 120, 120, 255),   # Gray
    "a": (224, 224, 224, 255),   # Light gray (use for "white" subjects)
    "T": (0, 137, 123, 255),     # Teal
    "t": (77, 182, 172, 255),    # Light teal
    "E": (46, 125, 50, 255),     # Dark green
    "G": (76, 175, 80, 255),     # Green
    "K": (233, 30, 99, 255),     # Pink
    "k": (248, 187, 208, 255),   # Light pink
    "N": (93, 64, 55, 255),      # Dark brown
    "n": (141, 110, 99, 255),    # Medium brown
    "O": (255, 152, 0, 255),     # Orange
    "o": (255, 204, 128, 255),   # Light orange
    "C": (255, 183, 77, 255),    # Amber/gold
    "P": (38, 50, 56, 255),      # Very dark blue-gray (for "black" features)
    "S": (224, 224, 224, 255),   # Bone white
    "M": (136, 14, 79, 255),     # Maroon
}
```

## Implementation

Use Python with Pillow. Expect a virtualenv at `.venv/` in the project root. If it doesn't exist, create one and install Pillow.

### The grid format

Define icons as triple-quoted multiline strings where each character maps to a color. This is critical — never use string concatenation (Python silently joins adjacent strings into one line).

```python
# CORRECT — triple-quoted multiline
icon = parse_grid("""
________________
___YY______YY___
__YYYY____YYYY__
...
""")

# WRONG — string concatenation (becomes one 256-char line!)
icon = parse_grid(
    "________________"
    "___YY______YY___"
)
```

### Verification

Before generating, verify every row is exactly 16 characters. The `parse_grid()` function should assert this:

```python
def parse_grid(text):
    rows = [line for line in text.strip().splitlines()]
    assert len(rows) == 16, f"Expected 16 rows, got {len(rows)}"
    for i, row in enumerate(rows):
        assert len(row) == 16, f"Row {i} has {len(row)} chars: '{row}'"
    return [[COLORS[ch] for ch in row] for row in rows]
```

### Output

Save two files per icon:
- `icon.png` — the actual 16x16 for Yoto upload
- `icon_preview.png` — 256x256 nearest-neighbor upscale for human review

```python
def save_icon(name, grid, outdir):
    img = Image.new("RGBA", (16, 16))
    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            img.putpixel((x, y), color)
    img.save(os.path.join(outdir, name, "icon.png"))
    preview = img.resize((256, 256), Image.NEAREST)
    preview.save(os.path.join(outdir, name, "icon_preview.png"))
```

After generating, read the `icon_preview.png` to show the user what it looks like.

## Examples of proven designs

These icons were iterated with a parent and work well. Study their patterns:

**Blue castle (Disney playlist)**
Three turrets with the center tallest, yellow flag at peak, light blue windows, arched doorway. The turret silhouette instantly says "castle."
```
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
```

**Red pirate hat (ברמלי / Barmalei)**
Triangular crown, yellow feather on top, gold brim band. The hat shape + feather is fun and distinctive.
```
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
```

**Stork (חסידה / Chasida)**
Light gray body with darker gray wing patches, red beak pointing right, single red leg with wide foot. Uses `a` (light gray) instead of white so it's visible in previews.
```
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
```

**Blue cat face (Pete the Cat / שאול החתול)**
Pointy ears are the key — they instantly say "cat." Brown 2x2 eyes, tiny red nose, face tapers at the jaw. Note the perfect symmetry.
```
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
```

**Yellow bear face (הדב הצהוב / The Yellow Bear)**
Round ears on top, round face, brown dot eyes, lighter muzzle with brown nose. The ear shape distinguishes it from the cat (round vs pointy).
```
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
```
