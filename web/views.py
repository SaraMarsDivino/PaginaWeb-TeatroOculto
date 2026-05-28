import os
from pathlib import Path
from urllib.parse import quote

from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.utils.http import url_has_allowed_host_and_scheme
from django.templatetags.static import static as static_url

from .models import Obra, Iniciativa, Suscriptor, MensajeContacto, Equipo
from .forms import SuscriptorForm, ContactoForm


NEWSLETTER_RECIPIENTS = [
    'rochaulin2@gmail.com',
    'plnvalenciafernandez@gmail.com',
]


def _newsletter_notify_enabled() -> bool:
    return os.getenv('NEWSLETTER_NOTIFY', '').strip().lower() in {'1', 'true', 'yes', 'on'}


def _get_contact_recipients() -> list[str]:
    raw = os.getenv('CONTACT_RECIPIENTS', '').strip()
    if not raw:
        return ['gestion@teatrooculto.cl']

    recipients = [p.strip() for p in raw.split(',')]
    return [r for r in recipients if r]


def _collect_gallery_images(base_dir, url_prefix):
    images = []
    try:
        if not base_dir.exists() or not base_dir.is_dir():
            return []

        for fname in sorted(os.listdir(base_dir)):
            lower = fname.lower()
            if fname.startswith(('.', '_')):
                continue
            if lower == 'thumbs' or lower.startswith('thumbs'):
                continue
            if not lower.endswith(('.jpg', '.jpeg', '.png', '.svg', '.webp')):
                continue
            images.append(settings.MEDIA_URL + quote(f"{url_prefix}/{fname}"))
    except Exception:
        return []

    return images


_IMAGE_EXTS = ('.jpg', '.jpeg', '.png', '.svg', '.webp')


def _candidate_stems_for_obra(obra) -> list[str]:
    stems: list[str] = []

    poster_name = getattr(getattr(obra, 'poster_image', None), 'name', '') or ''
    poster_stem = Path(poster_name).stem.strip() if poster_name else ''
    if poster_stem:
        stems.append(poster_stem)

    slug = (getattr(obra, 'slug', '') or '').strip()
    if slug and slug not in stems:
        stems.append(slug)

    title_stem = slugify(getattr(obra, 'title', '') or '')
    if title_stem and title_stem not in stems:
        stems.append(title_stem)

    return stems


def _candidate_stems_for_iniciativa(ini) -> list[str]:
    stems: list[str] = []

    image_name = getattr(getattr(ini, 'image', None), 'name', '') or ''
    image_stem = Path(image_name).stem.strip() if image_name else ''
    if image_stem:
        stems.append(image_stem)

    slug = (getattr(ini, 'slug', '') or '').strip()
    if slug and slug not in stems:
        stems.append(slug)

    title_stem = slugify(getattr(ini, 'title', '') or '')
    if title_stem and title_stem not in stems:
        stems.append(title_stem)

    return stems


def _find_git_static_by_stem(multimedia_root: Path, rel_dir: str, stem: str) -> str | None:
    """Return a /static/... URL for the first existing file matching stem+ext in rel_dir."""
    if not stem:
        return None

    base_dir = multimedia_root / rel_dir
    if not base_dir.exists() or not base_dir.is_dir():
        return None

    for ext in _IMAGE_EXTS:
        candidate = base_dir / f"{stem}{ext}"
        if candidate.exists() and candidate.is_file():
            rel_path = f"{rel_dir}/{candidate.name}"
            return static_url(quote(rel_path, safe='/'))
    return None


def _find_git_static_with_thumb_by_stem(
    multimedia_root: Path,
    rel_dir: str,
    stem: str,
) -> tuple[str | None, str | None]:
    """Return (full_url, thumb_url) for the first existing file matching stem+ext.

    If a thumbnail exists under rel_dir/thumbs/ with the same filename, include it.
    """
    if not stem:
        return None, None

    base_dir = multimedia_root / rel_dir
    if not base_dir.exists() or not base_dir.is_dir():
        return None, None

    thumbs_dir = base_dir / 'thumbs'
    for ext in _IMAGE_EXTS:
        candidate = base_dir / f"{stem}{ext}"
        if not (candidate.exists() and candidate.is_file()):
            continue

        rel_path = f"{rel_dir}/{candidate.name}"
        full_url = static_url(quote(rel_path, safe='/'))

        thumb_url = None
        thumb_candidate = thumbs_dir / candidate.name
        if thumb_candidate.exists() and thumb_candidate.is_file():
            thumb_rel_path = f"{rel_dir}/thumbs/{thumb_candidate.name}"
            thumb_url = static_url(quote(thumb_rel_path, safe='/'))

        return full_url, thumb_url

    return None, None


def _list_git_static_gallery(multimedia_root: Path, rel_dir: str) -> list[str]:
    """Return sorted /static/... URLs for image files inside rel_dir."""
    base_dir = multimedia_root / rel_dir
    if not base_dir.exists() or not base_dir.is_dir():
        return []

    urls: list[str] = []
    for fname in sorted(os.listdir(base_dir)):
        lower = fname.lower()
        if fname.startswith(('.', '_')):
            continue
        if lower == 'thumbs' or lower.startswith('thumbs'):
            continue
        if not lower.endswith(_IMAGE_EXTS):
            continue
        rel_path = f"{rel_dir}/{fname}"
        urls.append(static_url(quote(rel_path, safe='/')))
    return urls


def _list_git_static_gallery_items(multimedia_root: Path, rel_dir: str) -> list[dict]:
    """Return sorted gallery items with optional thumbs.

    Each item is: {"full": <url>, "thumb": <url or None>}.
    """
    base_dir = multimedia_root / rel_dir
    if not base_dir.exists() or not base_dir.is_dir():
        return []

    thumbs_dir = base_dir / 'thumbs'
    items: list[dict] = []
    for fname in sorted(os.listdir(base_dir)):
        lower = fname.lower()
        if fname.startswith(('.', '_')):
            continue
        if lower == 'thumbs' or lower.startswith('thumbs'):
            continue
        if not lower.endswith(_IMAGE_EXTS):
            continue

        rel_path = f"{rel_dir}/{fname}"
        full_url = static_url(quote(rel_path, safe='/'))

        thumb_url = None
        thumb_candidate = thumbs_dir / fname
        if thumb_candidate.exists() and thumb_candidate.is_file():
            thumb_rel_path = f"{rel_dir}/thumbs/{fname}"
            thumb_url = static_url(quote(thumb_rel_path, safe='/'))

        items.append({'full': full_url, 'thumb': thumb_url})

    return items


def _send_subscribers_snapshot_email() -> None:
    subscribers = Suscriptor.objects.order_by('created_at')
    lines = [
        'Listado de suscriptores (Mantente atento):',
        '',
        'Nombre | Edad | Correo',
        '----------------------',
    ]
    for item in subscribers:
        name = (item.name or '').strip() or '-'
        age = str(item.age) if item.age is not None else '-'
        lines.append(f'{name} | {age} | {item.email}')

    lines.extend(['', f'Total suscriptores: {subscribers.count()}'])

    subject = 'Teatro Oculto - Lista actualizada de suscriptores'
    message = '\n'.join(lines)
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@teatrooculto.local')
    send_mail(subject, message, from_email, NEWSLETTER_RECIPIENTS, fail_silently=True)


def root_view(request):
    """
    Root URL: redirect to /inicio/.
    """
    return redirect('home')


def skip_intro_view(request):
    """
    Sets the 'seen_intro' cookie and redirects to home.
    """
    response = redirect('home')
    max_age = 365 * 24 * 60 * 60  # 1 year
    response.set_cookie('seen_intro', '1', max_age=max_age, httponly=True, samesite='Lax')
    return response


def home_view(request):
    """
    Home page: shows active obras in carousel and iniciativas.
    Handles Suscriptor form (newsletter) POST.
    """
    obras = Obra.objects.filter(active=True).order_by('-release_date')
    iniciativas = Iniciativa.objects.all().order_by('-id')[:2]

    # Prefer Git-tracked static images when present.
    multimedia_root = settings.BASE_DIR / 'MULTIMEDIA TEATRO OCULTO'
    for ini in iniciativas:
        ini.git_image_url = None
        ini.git_image_thumb_url = None
        for stem in _candidate_stems_for_iniciativa(ini):
            full_url, thumb_url = _find_git_static_with_thumb_by_stem(multimedia_root, 'iniciativas', stem)
            if full_url:
                ini.git_image_url = full_url
                ini.git_image_thumb_url = thumb_url
                break

    for obra in obras:
        obra.git_poster_url = None
        obra.git_poster_thumb_url = None
        for stem in _candidate_stems_for_obra(obra):
            full_url, thumb_url = _find_git_static_with_thumb_by_stem(multimedia_root, f'obras/{stem}', 'poster')
            if not full_url:
                full_url, thumb_url = _find_git_static_with_thumb_by_stem(multimedia_root, 'obras', stem)

            if full_url:
                obra.git_poster_url = full_url
                obra.git_poster_thumb_url = thumb_url
                break

    # Collect carousel images.
    # Default to Git-tracked static multimedia so a simple git pull reproduces the same carousel.
    # Optionally, set CAROUSEL_SOURCE=media to prefer MEDIA_ROOT content.
    # Files starting with '_' are ignored so we can keep images on disk without showing them.
    carousel_images = []
    carousel_items = []
    try:
        source_dir = None
        thumbs_dir = None
        full_url_prefix = None
        thumbs_url_prefix = None

        carousel_source = os.getenv('CAROUSEL_SOURCE', '').strip().lower() or 'static'

        def _try_media_carousel():
            nonlocal source_dir, thumbs_dir, full_url_prefix, thumbs_url_prefix
            media_root = settings.MEDIA_ROOT
            if not media_root:
                return
            media_multimedia_root = Path(media_root) / 'MULTIMEDIA TEATRO OCULTO'
            media_carousel_dir = media_multimedia_root / 'carousel'
            if not (media_carousel_dir.exists() and media_carousel_dir.is_dir()):
                return
            imgs = [
                f for f in sorted(os.listdir(media_carousel_dir))
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.svg', '.webp'))
            ]
            if not imgs:
                return
            source_dir = media_carousel_dir
            thumbs_dir = media_carousel_dir / 'thumbs'
            full_url_prefix = settings.MEDIA_URL + quote('MULTIMEDIA TEATRO OCULTO/carousel/')
            thumbs_url_prefix = settings.MEDIA_URL + quote('MULTIMEDIA TEATRO OCULTO/carousel/thumbs/')

        def _try_static_carousel():
            nonlocal source_dir, thumbs_dir, full_url_prefix, thumbs_url_prefix
            multimedia_root = settings.BASE_DIR / 'MULTIMEDIA TEATRO OCULTO'
            static_carousel_dir = multimedia_root / 'carousel'
            if not (static_carousel_dir.exists() and static_carousel_dir.is_dir()):
                return
            imgs = [
                f for f in sorted(os.listdir(static_carousel_dir))
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.svg', '.webp'))
            ]
            if not imgs:
                return
            source_dir = static_carousel_dir
            thumbs_dir = static_carousel_dir / 'thumbs'
            full_url_prefix = settings.STATIC_URL + quote('carousel/')
            thumbs_url_prefix = settings.STATIC_URL + quote('carousel/thumbs/')

        if carousel_source == 'media':
            _try_media_carousel()
            if source_dir is None:
                _try_static_carousel()
        else:
            _try_static_carousel()
            if source_dir is None:
                _try_media_carousel()

        # 3) STATIC fallback: BASE_DIR/MULTIMEDIA TEATRO OCULTO/* (legacy)
        if source_dir is None:
            multimedia_root = settings.BASE_DIR / 'MULTIMEDIA TEATRO OCULTO'
            if multimedia_root.exists() and multimedia_root.is_dir():
                imgs = [
                    f for f in sorted(os.listdir(multimedia_root))
                    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.svg', '.webp'))
                ]
                if imgs:
                    source_dir = multimedia_root
                    thumbs_dir = multimedia_root / 'thumbs'
                    full_url_prefix = settings.STATIC_URL
                    thumbs_url_prefix = settings.STATIC_URL + quote('thumbs/')

        carousel_max_raw = os.getenv('CAROUSEL_MAX', '').strip()
        carousel_max = None
        if carousel_max_raw.isdigit():
            carousel_max = max(1, int(carousel_max_raw))

        if source_dir and full_url_prefix and thumbs_url_prefix:
            seen_names: set[str] = set()
            for fname in sorted(os.listdir(source_dir)):
                dedupe_key = fname.strip().lower()
                if dedupe_key in seen_names:
                    continue
                seen_names.add(dedupe_key)
                lower = fname.lower()
                if fname.startswith(('.', '_')):
                    continue
                if lower == 'thumbs' or lower.startswith('thumbs'):
                    continue
                if not lower.endswith(('.jpg', '.jpeg', '.png', '.svg', '.webp')):
                    continue
                full_url = full_url_prefix + quote(fname)
                thumb_path = thumbs_dir / fname if thumbs_dir else None
                thumb_url = (thumbs_url_prefix + quote(fname)) if (thumb_path and thumb_path.exists()) else None

                version = None
                try:
                    version = str(int((source_dir / fname).stat().st_mtime))
                except Exception:
                    version = None

                carousel_images.append(full_url)
                carousel_items.append({'full': full_url, 'thumb': thumb_url, 'v': version})

            if carousel_max:
                carousel_images = carousel_images[:carousel_max]
                carousel_items = carousel_items[:carousel_max]
    except Exception:
        carousel_images = []
        carousel_items = []

    suscribed = False
    suscriptor_form = SuscriptorForm()
    if request.method == 'POST':
        suscriptor_form = SuscriptorForm(request.POST)
        if suscriptor_form.is_valid():
            try:
                suscriptor_form.save()
                if _newsletter_notify_enabled():
                    _send_subscribers_snapshot_email()
                suscribed = True
                suscriptor_form = SuscriptorForm()
            except Exception:
                suscriptor_form.add_error('email', 'Este correo ya está suscrito.')

    context = {
        'obras': obras,
        'iniciativas': iniciativas,
        'suscribed': suscribed,
        'suscriptor_form': suscriptor_form,
        'carousel_images': carousel_images,
        'carousel_items': carousel_items,
    }
    return render(request, 'web/home.html', context)


def newsletter_subscribe_view(request):
    """Subscribe from footer (or anywhere) and return to the originating page."""

    if request.method != 'POST':
        return redirect('home')

    form = SuscriptorForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            if _newsletter_notify_enabled():
                _send_subscribers_snapshot_email()
            messages.success(request, 'Gracias por suscribirte.')
        except Exception:
            messages.info(request, 'Este correo ya está suscrito.')
    else:
        messages.error(request, 'Revisa el correo e intenta nuevamente.')

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
    if next_url and url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=not settings.DEBUG,
    ):
        return redirect(next_url)

    return redirect(reverse('home'))


def contacto_view(request):
    """
    Contact page: handle contact form POST -> save MensajeContacto.
    """
    sent = False
    contacto_form = ContactoForm()
    if request.method == 'POST':
        contacto_form = ContactoForm(request.POST)
        if contacto_form.is_valid():
            contacto_form.save()
            sent = True
            # Send notification email with contact contents. For development the
            # email backend is the console backend so the message will be printed
            # to the runserver console. To send real email, configure SMTP in
            # `settings.py` and restart the server.
            try:
                data = contacto_form.cleaned_data
                subject = f"Nuevo mensaje de contacto: {data.get('name','(sin nombre)')}"
                message = f"Nombre: {data.get('name')}\nEmail: {data.get('email')}\n\nMensaje:\n{data.get('message')}"
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@teatrooculto.local')
                send_mail(subject, message, from_email, _get_contact_recipients(), fail_silently=True)
            except Exception:
                # Fail silently in development; the form was already saved.
                pass
            contacto_form = ContactoForm()
    return render(request, 'web/contacto.html', {'sent': sent, 'contacto_form': contacto_form})


def nosotros_view(request):
    equipo = Equipo.objects.all()
    multimedia_root = settings.BASE_DIR / 'MULTIMEDIA TEATRO OCULTO'
    for member in equipo:
        stem = (getattr(member, 'slug', '') or '').strip() or slugify(getattr(member, 'name', '') or '')
        member.git_photo_url = _find_git_static_by_stem(multimedia_root, 'nosotros', stem)
    mission = {
        'mision': "Nuestra misión es democratizar el acceso al teatro y fomentar la creación contemporánea.",
        'vision': "Ser un referente cultural que inspire transformación social a través de las artes escénicas.",
    }
    return render(request, 'web/nosotros.html', {'equipo': equipo, 'mission': mission})


def obras_view(request):
    obras = list(Obra.objects.filter(active=True).order_by('-release_date'))

    multimedia_root = settings.BASE_DIR / 'MULTIMEDIA TEATRO OCULTO'
    for obra in obras:
        stems = _candidate_stems_for_obra(obra)

        obra.git_poster_url = None
        obra.git_poster_thumb_url = None
        for stem in stems:
            full_url, thumb_url = _find_git_static_with_thumb_by_stem(multimedia_root, f'obras/{stem}', 'poster')
            if not full_url:
                full_url, thumb_url = _find_git_static_with_thumb_by_stem(multimedia_root, 'obras', stem)

            if full_url:
                obra.git_poster_url = full_url
                obra.git_poster_thumb_url = thumb_url
                break

        obra.git_gallery_items = []
        obra.git_gallery_images = []
        for stem in stems:
            obra.git_gallery_items = _list_git_static_gallery_items(multimedia_root, f'obras/{stem}/gallery')
            if obra.git_gallery_items:
                break

        if obra.git_gallery_items:
            obra.git_gallery_images = [item.get('full') for item in obra.git_gallery_items if item.get('full')]

    # Smart gallery: drop images into MEDIA_ROOT/obras_galeria/<obra.id>/
    for obra in obras:
        base = settings.MEDIA_ROOT / 'obras_galeria' / str(obra.id)
        obra.gallery_images = _collect_gallery_images(
            base_dir=base,
            url_prefix=f'obras_galeria/{obra.id}',
        )

    return render(request, 'web/obras.html', {'obras': obras})


def iniciativas_view(request):
    iniciativas = Iniciativa.objects.order_by('-id')

    multimedia_root = settings.BASE_DIR / 'MULTIMEDIA TEATRO OCULTO'
    for ini in iniciativas:
        ini.git_image_url = None
        ini.git_image_thumb_url = None
        for stem in _candidate_stems_for_iniciativa(ini):
            full_url, thumb_url = _find_git_static_with_thumb_by_stem(multimedia_root, 'iniciativas', stem)
            if full_url:
                ini.git_image_url = full_url
                ini.git_image_thumb_url = thumb_url
                break

    return render(request, 'web/iniciativas.html', {'iniciativas': iniciativas})


@staff_member_required
def mensajes_view(request):
    allowed_sorts = {
        'orden': '-created_at',
        'correo': 'email',
        'nombre': 'name',
        'mensaje': 'message',
    }

    sort_key = (request.GET.get('sort') or 'orden').strip().lower()
    direction = (request.GET.get('dir') or 'desc').strip().lower()
    sort_field = allowed_sorts.get(sort_key, allowed_sorts['orden'])

    if sort_key == 'orden':
        ordering = 'created_at' if direction == 'asc' else '-created_at'
    else:
        ordering = sort_field
        if direction == 'desc':
            ordering = '-' + ordering

    qs = MensajeContacto.objects.all().order_by(ordering, '-created_at')

    per_page_raw = (request.GET.get('per_page') or '').strip()
    per_page = 25
    if per_page_raw.isdigit():
        per_page = max(5, min(200, int(per_page_raw)))

    paginator = Paginator(qs, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'web/mensajes.html',
        {
            'mensajes': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'sort': sort_key,
            'dir': direction,
            'per_page': per_page,
        },
    )


@staff_member_required
def listas_view(request):
    allowed_sorts = {
        'orden': '-created_at',
        'correo': 'email',
        'nombre': 'name',
        'edad': 'age',
    }

    sort_key = (request.GET.get('sort') or 'orden').strip().lower()
    direction = (request.GET.get('dir') or 'desc').strip().lower()
    sort_field = allowed_sorts.get(sort_key, allowed_sorts['orden'])

    if sort_key == 'orden':
        # Keep a stable default: newest first unless explicitly asc.
        ordering = 'created_at' if direction == 'asc' else '-created_at'
    else:
        ordering = sort_field
        if direction == 'desc':
            ordering = '-' + ordering

    qs = Suscriptor.objects.all().order_by(ordering, '-created_at')

    export = (request.GET.get('export') or '').strip().lower()
    if export in {'csv', 'excel', 'xlsx'}:
        # Excel-compatible CSV (UTF-8 with BOM)
        lines = ['Correo,Nombre,Edad']
        for s in qs:
            email = (s.email or '').replace('"', '""')
            name = (s.name or '').replace('"', '""')
            age = '' if s.age is None else str(s.age)
            lines.append(f'"{email}","{name}","{age}"')

        content = '\ufeff' + '\n'.join(lines) + '\n'
        resp = HttpResponse(content, content_type='text/csv; charset=utf-8')
        resp['Content-Disposition'] = 'attachment; filename="suscriptores.csv"'
        return resp

    per_page_raw = (request.GET.get('per_page') or '').strip()
    per_page = 25
    if per_page_raw.isdigit():
        per_page = max(5, min(200, int(per_page_raw)))

    paginator = Paginator(qs, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'web/listas.html',
        {
            'suscriptores': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'sort': sort_key,
            'dir': direction,
            'per_page': per_page,
        },
    )

