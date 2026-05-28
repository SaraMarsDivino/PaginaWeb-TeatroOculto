from __future__ import annotations

from pathlib import Path


def _square_pad_rgba(image):
    from PIL import Image

    im = image.convert("RGBA")
    w, h = im.size
    side = max(w, h)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(im, ((side - w) // 2, (side - h) // 2))
    return canvas


def main() -> None:
    brand_dir = Path(__file__).resolve().parents[1] / "web" / "static" / "web" / "brand"
    src = brand_dir / "favicon.png"
    if not src.exists():
        raise SystemExit(f"Source not found: {src}")

    try:
        from PIL import Image
    except Exception as exc:  # pragma: no cover
        raise SystemExit(
            "Pillow (PIL) is required to generate favicons. "
            "Install it with `pip install Pillow` and retry. "
            f"Details: {exc}"
        )

    base = _square_pad_rgba(Image.open(src))

    sizes: dict[str, int] = {
        "favicon-16.png": 16,
        "favicon-32.png": 32,
        "favicon-180.png": 180,  # apple-touch-icon
        "favicon-192.png": 192,
        "favicon-512.png": 512,
    }

    for filename, size in sizes.items():
        out = base.resize((size, size), Image.Resampling.LANCZOS)
        out_path = brand_dir / filename
        out.save(out_path, format="PNG", optimize=True)
        print(f"Wrote: {out_path} ({out_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
