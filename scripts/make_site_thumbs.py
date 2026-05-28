from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


RASTER_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


@dataclass(frozen=True)
class ThumbSpec:
    max_size: tuple[int, int]
    quality: int = 85


def _find_multimedia_root() -> Path:
    candidates = [
        Path("MULTIMEDIA TEATRO OCULTO"),
        Path("teatro_project") / "MULTIMEDIA TEATRO OCULTO",
        Path.cwd() / "teatro_project" / "MULTIMEDIA TEATRO OCULTO",
    ]
    for c in candidates:
        if c.exists() and c.is_dir():
            return c
    return Path("MULTIMEDIA TEATRO OCULTO")


def _is_raster_image(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in RASTER_EXTS


def _ensure_thumb(src: Path, dst: Path, spec: ThumbSpec, *, force: bool = False) -> bool:
    """Return True if created/updated a thumb."""

    if not _is_raster_image(src):
        return False

    try:
        from PIL import Image, ImageOps
    except Exception as e:  # pragma: no cover
        raise SystemExit(
            "Pillow no está instalado. Ejecuta: python -m pip install --upgrade pillow"
        ) from e

    dst.parent.mkdir(parents=True, exist_ok=True)

    if not force:
        # Skip when thumb exists and is newer than source.
        try:
            if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
                return False
        except Exception:
            pass

    img = Image.open(src)
    img = ImageOps.exif_transpose(img)
    img.thumbnail(spec.max_size)

    suffix = src.suffix.lower()
    save_kwargs: dict = {"optimize": True}
    if suffix in {".jpg", ".jpeg", ".webp"}:
        save_kwargs["quality"] = spec.quality

    img.save(dst, **save_kwargs)
    return True


def _iter_images(folder: Path) -> list[Path]:
    if not folder.exists() or not folder.is_dir():
        return []

    images: list[Path] = []
    for p in sorted(folder.iterdir()):
        if p.is_dir() and p.name.lower() == "thumbs":
            continue
        if _is_raster_image(p) and "placeholder" not in p.name.lower():
            images.append(p)
    return images


def main() -> int:
    force = "--force" in {a.strip().lower() for a in sys.argv[1:]}
    multimedia = _find_multimedia_root().resolve()
    print("Using MULTIMEDIA root:", multimedia)

    media_multimedia = (Path("media") / "MULTIMEDIA TEATRO OCULTO").resolve()
    if media_multimedia.exists() and media_multimedia.is_dir():
        print("Using MEDIA MULTIMEDIA root:", media_multimedia)

    created = 0

    # Carousel (hero) images
    carousel_spec = ThumbSpec(max_size=(1000, 1000), quality=82)

    carousel_dir = multimedia / "carousel"
    for src in _iter_images(carousel_dir):
        dst = carousel_dir / "thumbs" / src.name
        if _ensure_thumb(src, dst, carousel_spec, force=force):
            created += 1

    media_carousel_dir = media_multimedia / "carousel"
    for src in _iter_images(media_carousel_dir):
        dst = media_carousel_dir / "thumbs" / src.name
        if _ensure_thumb(src, dst, carousel_spec, force=force):
            created += 1

    # Iniciativas card images
    ini_dir = multimedia / "iniciativas"
    ini_spec = ThumbSpec(max_size=(640, 640), quality=82)
    for src in _iter_images(ini_dir):
        dst = ini_dir / "thumbs" / src.name
        if _ensure_thumb(src, dst, ini_spec, force=force):
            created += 1

    # Legacy obras posters under MULTIMEDIA/obras/<stem>.<ext>
    obras_dir = multimedia / "obras"
    poster_spec = ThumbSpec(max_size=(640, 640), quality=82)
    for src in _iter_images(obras_dir):
        dst = obras_dir / "thumbs" / src.name
        if _ensure_thumb(src, dst, poster_spec, force=force):
            created += 1

    # New obras structure: MULTIMEDIA/obras/<slug>/poster.* and /gallery/*
    gallery_spec = ThumbSpec(max_size=(360, 360), quality=78)
    if obras_dir.exists() and obras_dir.is_dir():
        for obra_folder in sorted(obras_dir.iterdir()):
            if not obra_folder.is_dir():
                continue
            if obra_folder.name.lower() in {"thumbs", "gallery"}:
                continue

            # Poster
            for ext in sorted(RASTER_EXTS):
                poster = obra_folder / f"poster{ext}"
                if poster.exists():
                    dst = obra_folder / "thumbs" / poster.name
                    if _ensure_thumb(poster, dst, poster_spec, force=force):
                        created += 1
                    break

            # Gallery images (Git-tracked)
            gallery_dir = obra_folder / "gallery"
            if gallery_dir.exists() and gallery_dir.is_dir():
                for src in _iter_images(gallery_dir):
                    dst = gallery_dir / "thumbs" / src.name
                    if _ensure_thumb(src, dst, gallery_spec, force=force):
                        created += 1

    # Nosotros page (brand image)
    brand_img = Path("web") / "static" / "web" / "brand" / "ensayo-oculto.jpg"
    if brand_img.exists() and brand_img.is_file():
        brand_spec = ThumbSpec(max_size=(640, 640), quality=82)
        dst = brand_img.parent / "thumbs" / brand_img.name
        if _ensure_thumb(brand_img, dst, brand_spec, force=force):
            created += 1

    print("Thumbs created/updated:", created)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
