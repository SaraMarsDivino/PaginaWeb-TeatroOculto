from __future__ import annotations

import os
import shutil
from pathlib import Path


def _is_image(path: Path) -> bool:
    return path.suffix.lower() in {".jpg", ".jpeg", ".png", ".svg", ".webp"}


def main() -> None:
    project_dir = Path(__file__).resolve().parents[1]
    src_dir = Path(os.getenv("CAROUSEL_SRC", project_dir / "MULTIMEDIA TEATRO OCULTO" / "carousel"))
    dst_dir = Path(
        os.getenv(
            "CAROUSEL_DST",
            project_dir / "media" / "MULTIMEDIA TEATRO OCULTO" / "carousel",
        )
    )

    if not src_dir.exists():
        raise SystemExit(f"Source folder not found: {src_dir}")

    dst_dir.mkdir(parents=True, exist_ok=True)

    # Build the desired set (relative paths)
    desired: set[Path] = set()
    for path in src_dir.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(src_dir)
        parts_lower = {p.lower() for p in rel.parts}
        if "thumbs" in parts_lower:
            continue
        if any(p.startswith(".") for p in rel.parts):
            continue
        if rel.name.startswith("_"):
            continue
        if not _is_image(path):
            continue
        desired.add(rel)

    # Delete extra files (mirror)
    for existing in dst_dir.rglob("*"):
        if existing.is_dir():
            continue
        rel = existing.relative_to(dst_dir)
        if rel not in desired:
            existing.unlink(missing_ok=True)

    # Copy/update desired files
    for rel in sorted(desired):
        src = src_dir / rel
        dst = dst_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    print(f"Synced {len(desired)} image(s)")
    print(f"Source: {src_dir}")
    print(f"Dest:   {dst_dir}")


if __name__ == "__main__":
    main()
