from pathlib import Path
import shutil

# Try several likely locations for the multimedia folder
candidates = [Path('MULTIMEDIA TEATRO OCULTO'), Path('teatro_project') / 'MULTIMEDIA TEATRO OCULTO', Path.cwd() / 'teatro_project' / 'MULTIMEDIA TEATRO OCULTO']
# image extensions
raster_exts = ('.jpg', '.jpeg', '.png', '.webp')
vector_exts = ('.svg',)
allowed_exts = raster_exts + vector_exts

SRC = None
# Prefer a candidate that actually contains image files (excluding placeholders)
for c in candidates:
    if c.exists() and c.is_dir():
        imgs = [p for p in c.iterdir() if p.is_file() and p.suffix.lower() in allowed_exts and 'placeholder' not in p.name.lower()]
        if imgs:
            SRC = c
            break
# otherwise pick the first existing candidate
if SRC is None:
    for c in candidates:
        if c.exists() and c.is_dir():
            SRC = c
            break
if SRC is None:
    SRC = Path('MULTIMEDIA TEATRO OCULTO')

print('DEBUG: candidate dirs:', [str(c) for c in candidates])
print('DEBUG: using SRC=', SRC.resolve())
print('DEBUG: SRC exists:', SRC.exists())
print('DEBUG: items in SRC:', [p.name for p in SRC.iterdir()] if SRC.exists() else [])
DST = SRC / 'carousel'
THUMBS = DST / 'thumbs'

DST.mkdir(parents=True, exist_ok=True)
THUMBS.mkdir(parents=True, exist_ok=True)

raster_exts = ('.jpg', '.jpeg', '.png', '.webp')
vector_exts = ('.svg',)
allowed_exts = raster_exts + vector_exts

moved = []
for p in sorted(SRC.iterdir()):
    if p.is_file() and p.suffix.lower() in allowed_exts and 'placeholder' not in p.name.lower():
        # skip files already inside carousel
        if p.parent == DST:
            continue
        dest = DST / p.name
        try:
            shutil.move(str(p), str(dest))
            moved.append(p.name)
        except Exception as e:
            print('move error', p.name, e)

# generate thumbnails for raster images using Pillow if available
thumbs = []
try:
    from PIL import Image
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

if PIL_AVAILABLE:
    for f in sorted(DST.iterdir()):
        if f.is_file() and f.suffix.lower() in raster_exts:
            tpath = THUMBS / f.name
            try:
                if not tpath.exists():
                    img = Image.open(f)
                    img.thumbnail((1000, 1000))
                    img.save(tpath, optimize=True, quality=85)
                    thumbs.append(tpath.name)
            except Exception as e:
                print('thumb error', f.name, e)
else:
    print('Pillow not installed. Run: python -m pip install --upgrade pillow')

print('moved:', moved)
print('thumbnails created:', thumbs)
