# Deploy to Raspberry Pi (manual)

Steps to deploy the project to the Raspberry Pi (manual method):

1. On the Pi (as user `pablo`), prepare the project directory:

```bash
# run on Pi
mkdir -p /home/pablo/teatro_project
```

2. Clone the repo into the project dir (or pull if already cloned):

```bash
cd /home/pablo
git clone https://github.com/SaraMarsDivino/PaginaWeb-TeatroOculto.git teatro_project
cd teatro_project
```

## Fast updates (recommended)

After you already have containers running, you can update everything (pull + migrate + collectstatic + restart web) with:

```bash
cd /home/pablo/teatro_project
sh scripts/pi_update.sh
```

If the script previously failed with "working tree has local tracked changes":

- Make sure you're in the repo folder: `cd /home/pablo/teatro_project`
- Run `git status` to see what's modified.
- Normally you should not edit tracked files directly on the Pi. If the only file that changes is `db.sqlite3` (SQLite DB), the update script now ignores it.

If you ever need to run the steps manually:

```bash
cd /home/pablo/teatro_project
git pull --ff-only
docker compose up -d
docker compose exec -T web python manage.py migrate --noinput
docker compose exec -T web python manage.py collectstatic --noinput
docker compose restart web nginx
```

Important: fixture changes (like `web/fixtures/sample_data.json`) do not update the production database automatically.
To update content that lives in the DB (e.g. an Obra's release date), change it in `/admin/` or run a one-off command like:

```bash
docker compose exec -T web python manage.py shell -c "from datetime import date; from web.models import Obra; o=Obra.objects.filter(active=True).order_by('-created_at').first(); print('Before:', o.title, o.release_date); o.release_date=date(2026,4,1); o.save(update_fields=['release_date']); print('After:', o.title, o.release_date)"
```

## Local preview (Windows / runserver)

When running locally with Django `runserver`, `/media/` is served from `teatro_project/media/` (MEDIA_ROOT).
So to preview the carousel locally, sync the repo carousel folder into local media:

```powershell
Set-Location .\teatro_project

# One-command local dev (sync carousel + migrate + load sample data + runserver)
PowerShell -ExecutionPolicy Bypass -File .\scripts\local_dev.ps1

# Optional: don’t start server (only prep DB + media)
PowerShell -ExecutionPolicy Bypass -File .\scripts\local_dev.ps1 -NoRunserver
```

3. Create `.env` from `.env.example` and update values:

```bash
cp .env.example .env
# Edit .env: set DJANGO_SECRET_KEY, ALLOWED_HOSTS (your domain or Pi IP), DEBUG=0
```

4. Ensure `docker-compose` is installed and running on the Pi. Then run:

```bash
cd /home/pablo/teatro_project
docker-compose up -d --build
```

5. Check logs and containers:

```bash
docker-compose ps
docker-compose logs -f web
```

6. After the first run, collectstatic output is stored in `./staticfiles/` (inside the cloned repo). User uploads (if any) go to `./media/`.

## Multimedia in Git (recommended)

The curated multimedia (carousel, posters, initiatives, placeholders) lives in the repo under `MULTIMEDIA TEATRO OCULTO/` and is served via `/static/` after `collectstatic`.

So for normal updates:

- `git pull`
- restart the `web` container (entrypoint runs `migrate` + `collectstatic`)

No external media sync is required for the carousel when using the Git-tracked workflow.

### Legacy note (optional)

There is a script `scripts/sync_carousel_to_volume.sh` from an older approach that mirrored carousel images into a separate `/media/` volume. Keep it only if you intentionally serve carousel from `/media/`.

Notes & security:
- We removed the GitHub Actions workflow per request; for automated deploy you can either add a CI workflow later or run `git pull` on the Pi manually.
- For TLS in production, configure Cloudflare or Let's Encrypt on the Pi and update `nginx/teatro.conf` with your domain.
- Prefer SSH key auth instead of passwords when running remote scripts.
