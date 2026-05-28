from __future__ import annotations

from pathlib import Path


def _pick_multimedia_root() -> Path:
    candidates = [
        Path("MULTIMEDIA TEATRO OCULTO"),
        Path("teatro_project") / "MULTIMEDIA TEATRO OCULTO",
        Path.cwd() / "teatro_project" / "MULTIMEDIA TEATRO OCULTO",
    ]

    for c in candidates:
        if c.exists() and c.is_dir():
            return c

    return Path("MULTIMEDIA TEATRO OCULTO")


def main() -> None:
    multimedia_root = _pick_multimedia_root()
    src_dir = multimedia_root / "nosotros"
    out_dir = src_dir / "bw"

    raster_exts = (".jpg", ".jpeg", ".png", ".webp")

    print("DEBUG: multimedia_root=", multimedia_root.resolve())
    print("DEBUG: src_dir=", src_dir.resolve())

    if not src_dir.exists():
        raise SystemExit(f"No existe la carpeta: {src_dir}")

    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        from PIL import Image, ImageOps
    except Exception as e:
        raise SystemExit(
            "Pillow no está instalado. Instala con: python -m pip install --upgrade pillow\n"
            f"Detalle: {e}"
        )

    created: list[str] = []
    skipped: list[str] = []

    # Only process images directly inside /nosotros (not subfolders)
    for p in sorted(src_dir.iterdir()):
        if not p.is_file():
            continue
        if p.suffix.lower() not in raster_exts:
            continue
        if p.name.lower().endswith("-bw.jpg"):
            continue

        out_path = out_dir / f"{p.stem}-bw.jpg"
        if out_path.exists() and out_path.stat().st_mtime >= p.stat().st_mtime:
            skipped.append(out_path.name)
            continue

        with Image.open(p) as im:
            im = ImageOps.exif_transpose(im)
            # square crop then resize with high-quality resampling
            im = ImageOps.fit(im, (600, 600), method=Image.Resampling.LANCZOS)
            im = ImageOps.grayscale(im).convert("RGB")
            im.save(out_path, format="JPEG", quality=90, optimize=True, progressive=True)

        created.append(out_path.name)

    print("created:", created)
    print("skipped:", skipped)


if __name__ == "__main__":
    main()
