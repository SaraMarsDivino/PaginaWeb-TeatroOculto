#!/bin/sh
# Usage: run on the Raspberry Pi as the deploy user (pablo)

set -e

PROJECT_DIR=${1:-/home/pablo/teatro_project}
# Static + media live inside the cloned repo now (bind-mounted into the containers).
STATIC_DIR=${2:-"$PROJECT_DIR/staticfiles"}
MEDIA_DIR=${3:-"$PROJECT_DIR/media"}

echo "Creating directories"
mkdir -p "$PROJECT_DIR" "$STATIC_DIR" "$MEDIA_DIR"

echo "Ensure proper permissions"
chown -R $(whoami):$(whoami) "$PROJECT_DIR" "$STATIC_DIR" "$MEDIA_DIR"

echo "If Docker and docker-compose are installed, clone the repo into $PROJECT_DIR or pull latest"
echo "Example commands to run locally on Pi (do not run as root):"
echo "  git clone https://github.com/YOURUSER/YOURREPO.git $PROJECT_DIR"
echo "  cd $PROJECT_DIR"
echo "  cp .env.example .env   # then edit .env with proper values"
echo "  docker-compose up -d --build"

echo "Setup complete (manual steps remain: edit .env, add secret keys, set domain in nginx config)"
