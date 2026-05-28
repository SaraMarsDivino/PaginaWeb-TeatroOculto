from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teatro_project.settings")
os.environ.setdefault("ALLOWED_HOSTS", "testserver")

import django

django.setup()

from django.test import Client


def main() -> None:
    client = Client()
    resp = client.get("/inicio/")
    print("/inicio/ ->", resp.status_code)

    ctx = getattr(resp, "context", None)
    print("context type:", type(ctx))

    if ctx is None:
        print("No context attached; templates not captured")
        return

    # Django may return a ContextList when multiple templates render.
    try:
        images = ctx.get("carousel_images")
    except Exception:
        # try last context in list
        try:
            images = ctx[-1].get("carousel_images")
        except Exception:
            images = None

    images = list(images or [])
    print("carousel_images:", len(images))
    print("sample:", images[:3])


if __name__ == "__main__":
    main()
