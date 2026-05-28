from __future__ import annotations

import os
import sys
from pathlib import Path

# Ensure project root is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teatro_project.settings")
# Allow Django test client host
os.environ.setdefault("ALLOWED_HOSTS", "testserver")

import django

django.setup()

from django.test import Client
from django.test.utils import setup_test_environment


def main() -> None:
    setup_test_environment()
    client = Client()
    resp = client.get("/inicio/")
    print("/inicio/ ->", resp.status_code)

    ctx = getattr(resp, "context", None)
    images = []
    if ctx is not None:
        # Django may return ContextList when multiple templates render
        try:
            raw = ctx.get("carousel_images")
        except Exception:
            raw = None
            try:
                raw = ctx[-1].get("carousel_images")
            except Exception:
                raw = None
        images = list(raw or [])

    print("carousel_images:", len(images))
    if images:
        print("sample:", images[:3])


if __name__ == "__main__":
    main()
