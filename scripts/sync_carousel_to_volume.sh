#!/usr/bin/env sh
# Sync carousel images from the repo folder into the Pi media volume.
# This ensures nginx can serve them at /media/... (mounted from /home/pablo/teatro_media).
#
# Usage on Pi:
#   cd /home/pablo/teatro_project
#   sh scripts/sync_carousel_to_volume.sh
#
# Optional env:
#   CAROUSEL_SRC=...   (default: ./MULTIMEDIA TEATRO OCULTO/carousel)
#   CAROUSEL_DST=...   (default: /home/pablo/teatro_media/MULTIMEDIA TEATRO OCULTO/carousel)
#   DRY_RUN=1          (show what would change)

set -eu

CAROUSEL_SRC=${CAROUSEL_SRC:-"./MULTIMEDIA TEATRO OCULTO/carousel"}
CAROUSEL_DST=${CAROUSEL_DST:-"/home/pablo/teatro_media/MULTIMEDIA TEATRO OCULTO/carousel"}

if [ ! -d "$CAROUSEL_SRC" ]; then
  echo "[sync_carousel] Source folder not found: $CAROUSEL_SRC" >&2
  echo "[sync_carousel] Tip: keep your carousel images in 'MULTIMEDIA TEATRO OCULTO/carousel/' inside the repo." >&2
  exit 1
fi

mkdir -p "$CAROUSEL_DST"

# Safety guard: never allow syncing into a dangerous destination
case "$CAROUSEL_DST" in
  "/"|""|"/home"|"/home/pablo"|"/home/pablo/teatro_media"|"/home/pablo/teatro_media/"|"/home/pablo/teatro_media/MULTIMEDIA TEATRO OCULTO"|"/home/pablo/teatro_media/MULTIMEDIA TEATRO OCULTO/")
    echo "[sync_carousel] Refusing to sync into unsafe destination: $CAROUSEL_DST" >&2
    exit 2
    ;;
esac

RSYNC_FLAGS="-av"
if [ "${DRY_RUN:-}" = "1" ]; then
  RSYNC_FLAGS="$RSYNC_FLAGS --dry-run"
fi

# Exclude thumbnails and hidden/disabled images.
# Note: files starting with '_' are ignored by the Django view as well.
rsync $RSYNC_FLAGS \
  --delete \
  --exclude "thumbs/" \
  --exclude ".*" \
  --exclude "_*" \
  "$CAROUSEL_SRC/" \
  "$CAROUSEL_DST/"

# Ensure nginx can read the files
find "$(dirname "$CAROUSEL_DST")" -type d -exec chmod 755 {} \; 2>/dev/null || true
find "$(dirname "$CAROUSEL_DST")" -type f -exec chmod 644 {} \; 2>/dev/null || true

echo "[sync_carousel] Done. Served path will be: /media/MULTIMEDIA%20TEATRO%20OCULTO/carousel/<file>"
