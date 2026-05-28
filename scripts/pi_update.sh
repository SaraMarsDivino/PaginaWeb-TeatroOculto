#!/usr/bin/env sh
# One-command update flow for the Raspberry Pi.
#
# What it does:
# - git pull (fast-forward)
# - sync carousel images into the media volume
# - run Django migrations
# - collectstatic
# - restart the web service (Gunicorn)
#
# Usage on Pi:
#   cd /home/pablo/teatro_project
#   sh scripts/pi_update.sh

set -eu

PROJECT_DIR=${PROJECT_DIR:-"/home/pablo/teatro_project"}
BRANCH=${BRANCH:-"main"}
REMOTE=${REMOTE:-"origin"}

cd "$PROJECT_DIR"

echo "[pi_update] Project: $PROJECT_DIR"

if command -v docker-compose >/dev/null 2>&1; then
  DC="docker-compose"
else
  DC="docker compose"
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "[pi_update] ERROR: not a git repository: $PROJECT_DIR" >&2
  exit 1
fi

# Only block if there are tracked changes. Untracked files like .env are fine.
# NOTE: db.sqlite3 is currently tracked in this repo and will be modified by the app.
# We explicitly ignore it here so updates don't get blocked.
DIRTY_TRACKED=$(git status --porcelain --untracked-files=no | grep -v 'db\.sqlite3$' || true)
if [ -n "$DIRTY_TRACKED" ]; then
  echo "[pi_update] ERROR: working tree has local tracked changes." >&2
  echo "[pi_update] Run 'git status' and stash/commit those changes, then retry." >&2
  exit 2
fi

echo "[pi_update] Pulling latest changes..."
git fetch "$REMOTE" "$BRANCH"
git pull --ff-only "$REMOTE" "$BRANCH"

echo "[pi_update] Syncing carousel images into media volume..."
sh scripts/sync_carousel_to_volume.sh

echo "[pi_update] Ensuring containers are up..."
$DC up -d

echo "[pi_update] Running migrations..."
$DC exec -T web python manage.py migrate

echo "[pi_update] Collecting static..."
$DC exec -T web python manage.py collectstatic --noinput

echo "[pi_update] Restarting web service..."
$DC restart web

echo "[pi_update] Done."