# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code skill project that generates 16x16 pixel art icons for Yoto MYO (Make Your Own) cards. The Yoto player has a 16x16 LED matrix display. Icons are designed for toddlers (age 2-4) and must be instantly recognizable.

## Architecture

The project is a single Claude Code skill, not a traditional app:

- `.claude/skills/yoto-pixel-art/SKILL.md` — The skill definition. Contains the "Pixel Soul" design philosophy, color palette reference, grid format spec, and example icons. This is the primary source of truth for design decisions.
- `.claude/skills/yoto-pixel-art/scripts/generate_icons.py` — Python script that converts ASCII grids to PNG icons. Each character maps to an RGBA color tuple.
- `.out/` — Generated output. Each playlist gets a subdirectory with `icon.png` (512x512 upload-ready) and `icon_16x16.png` (original).
- `.venv/` — Python virtualenv with Pillow.

## Commands

Generate icons:
```sh
.venv/bin/python .claude/skills/yoto-pixel-art/scripts/generate_icons.py [output-dir]
```
Output dir defaults to `.out/` in cwd.

Set up virtualenv (if missing):
```sh
python3 -m venv .venv && .venv/bin/pip install Pillow
```

Run in sandbox:
```sh
nono run --profile nono-profile.json -- claude --dangerously-skip-permissions -p "create a yoto pixel art icon for a playlist called Lullabies"
```

## Key Constraints

- Never mention Claude or Anthropic in commits, code, comments, or generated files.
- Icons must be exactly 16x16 pixels, PNG with transparent background.
- Never use black (0,0,0) — black LEDs are "off". Use dark brown, dark blue-gray, or dark green for dark features.
- Avoid pure white for main subjects — invisible in PNG previews on light backgrounds. Use light gray (224,224,224) instead.
- Grid strings must use triple-quoted multilines, never string concatenation (Python silently joins adjacent strings into one line).
- Every feature must be at least 2px wide — single-pixel lines vanish at this scale.
- Playlist names are in Hebrew.
