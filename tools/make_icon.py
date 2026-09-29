#!/usr/bin/env python3
"""Render the LibreBuds icon: two white capsule (earbud) shapes on black.

Produces:
- scripts/windows/librebuds.ico, with 16/32/48/256 px frames (Windows
  PyInstaller/NSIS icon).
- openfreebuds_qt/assets/librebuds.png, a single 256 px frame (runtime Qt
  window/taskbar icon).

This is a build tool. It is not part of the runtime application and its
only dependency, Pillow, is not added to the project's runtime
dependencies (it is already a runtime dependency of the app itself, but
this script must still work if run standalone with just Pillow installed).

Usage:
    python tools/make_icon.py
"""

from pathlib import Path

from PIL import Image, ImageDraw

REPO_ROOT = Path(__file__).resolve().parent.parent
ICO_OUTPUT_PATH = REPO_ROOT / "scripts" / "windows" / "librebuds.ico"
PNG_OUTPUT_PATH = REPO_ROOT / "openfreebuds_qt" / "assets" / "librebuds.png"
PNG_SIZE = 256

SIZES = (16, 32, 48, 256)

# Supersample factor: draw each frame at a much higher resolution, then
# downsample with a high quality filter, so small sizes stay crisp.
SUPERSAMPLE = 8

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)


def draw_capsule_glyph(size: int) -> Image.Image:
    """Draw two white capsule (earbud) shapes on a black square canvas."""
    hi_res = size * SUPERSAMPLE
    img = Image.new("RGBA", (hi_res, hi_res), BLACK)
    draw = ImageDraw.Draw(img)

    # Each capsule is a tall rounded rectangle, the two of them mirrored
    # and slightly tilted outward, similar to a pair of stemless
    # in-ear earbuds viewed from the front.
    capsule_w = hi_res * 0.24
    capsule_h = hi_res * 0.60
    radius = capsule_w / 2

    center_y = hi_res / 2
    offset_x = hi_res * 0.23

    for side, angle in ((-1, 8), (1, -8)):
        cx = hi_res / 2 + side * offset_x

        capsule = Image.new("RGBA", (hi_res, hi_res), (0, 0, 0, 0))
        capsule_draw = ImageDraw.Draw(capsule)
        left = cx - capsule_w / 2
        top = center_y - capsule_h / 2
        right = cx + capsule_w / 2
        bottom = center_y + capsule_h / 2
        capsule_draw.rounded_rectangle(
            (left, top, right, bottom),
            radius=radius,
            fill=WHITE,
        )

        capsule = capsule.rotate(
            angle,
            resample=Image.BICUBIC,
            center=(cx, center_y),
        )

        img.alpha_composite(capsule)

    return img.resize((size, size), Image.LANCZOS)


def main():
    frames = [draw_capsule_glyph(size) for size in SIZES]

    ICO_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    frames[-1].save(
        ICO_OUTPUT_PATH,
        format="ICO",
        sizes=[(s, s) for s in SIZES],
        append_images=frames[:-1],
    )
    print(f"Wrote {ICO_OUTPUT_PATH} with sizes {SIZES}")

    png_frame = (draw_capsule_glyph(PNG_SIZE) if PNG_SIZE not in SIZES
                 else frames[SIZES.index(PNG_SIZE)])
    PNG_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    png_frame.save(PNG_OUTPUT_PATH, format="PNG")
    print(f"Wrote {PNG_OUTPUT_PATH} at {PNG_SIZE}x{PNG_SIZE}")


if __name__ == "__main__":
    main()
