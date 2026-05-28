from __future__ import annotations

import re
import sys
from pathlib import Path

from pypdf import PdfReader

DEFAULT_PDF_PATH = Path(r"C:\Users\rocha\Downloads\Comentarios de Pagina web - teatro oculto.pdf")
DEFAULT_OUT_PATH = Path(__file__).resolve().parent / "feedback_extracted.txt"


def _parse_args(argv: list[str]) -> tuple[Path, Path]:
    pdf_path = DEFAULT_PDF_PATH
    out_path = DEFAULT_OUT_PATH

    if len(argv) >= 2 and argv[1].strip():
        pdf_path = Path(argv[1]).expanduser()

    if len(argv) >= 3 and argv[2].strip():
        out_path = Path(argv[2]).expanduser()

    return pdf_path, out_path


def main() -> None:
    pdf_path, out_path = _parse_args(sys.argv)
    reader = PdfReader(str(pdf_path))

    chunks: list[str] = []
    chunks.append(f"source: {pdf_path}")
    chunks.append(f"pages: {len(reader.pages)}")

    for idx, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        chunks.append(f"\n--- page {idx} ---\n")
        chunks.append(text)

    out_path.write_text("\n".join(chunks).strip() + "\n", encoding="utf-8")
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
