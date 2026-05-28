from __future__ import annotations

from typing import Any

from .models import Iniciativa, Obra


def footer_lists(request) -> dict[str, Any]:
    """Site-wide footer content (kept lightweight)."""

    footer_obras = (
        Obra.objects.filter(active=True)
        .order_by("-created_at")
        .only("id", "title", "release_date")[:3]
    )
    footer_iniciativas = (
        Iniciativa.objects.order_by("-created_at")
        .only("id", "title", "category")[:3]
    )

    return {
        "footer_obras": footer_obras,
        "footer_iniciativas": footer_iniciativas,
    }
