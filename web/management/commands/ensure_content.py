from django.core.management.base import BaseCommand
from django.utils.text import slugify
from datetime import date

from web.models import Iniciativa, Obra


TABACO_SYNOPSIS = (
    "En esta adaptación libre del texto de Antón Chéjov, la obra se presenta como una "
    "conferencia aparentemente informativa sobre los daños que causa el tabaco, dictada "
    "por un hombre mayor convocado más por obediencia familiar que por verdadera vocación. "
    "A medida que el discurso avanza, la conferencia se fragmenta y deja al descubierto la "
    "fragilidad emocional del personaje, su relación distante con su hijo y una profunda "
    "sensación de soledad e incomunicación. El relato transita entre el humor, la nostalgia "
    "y la reflexión, incorporando quiebres escénicos y recursos del teatro gestual que "
    "transforman la charla en un viaje íntimo hacia la necesidad humana de ser escuchado.\n\n"
    "Trabajar con un autor fundamental de la literatura universal y referente clave en la "
    "formación teatral representa tanto un privilegio como un desafío artístico. Esta versión "
    "propone volver a convocar a Chéjov desde una mirada fresca, rescatando la profundidad de "
    "su escritura y actualizando sus temas para dialogar con el presente. La adaptación busca "
    "generar un puente intergeneracional, conectando especialmente con una población adulta "
    "mayor en crecimiento, sin dejar de interpelar a jóvenes audiencias, invitándolas a "
    "reflexionar sobre la comunicación, la escucha y los vínculos humanos en la sociedad actual."
)


class Command(BaseCommand):
    help = "Ensure baseline content exists (non-destructive)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print what would be created without writing to DB.",
        )

    def handle(self, *args, **options):
        dry_run = bool(options.get("dry_run"))

        desired_iniciativas = [
            {
                "title": "Función de “Al Caer la Noche” — Obra de teatro performance.",
                "description": (
                    "Obra de teatro performance realizada por laboratorio ecoanonimo e Ignacio Romero "
                    "en el vagón multi espacio, junto con ejecución de estudio de público."
                ),
                "category": "Formación",
                "image": "iniciativas/al-caer-la-noche.jpg",
            },
            {
                "title": "Taller de Teatro Performance",
                "description": "Taller orientado a explorar la performance y el entrenamiento actoral.",
                "category": "Formación",
                "image": "iniciativas/teatro-perfomance.png",
            }
            ,
            {
                "title": "Gestión de funciones: Algo de Ricardo",
                "description": "Gestión y presentación de funciones en Multiespacio El Vagón.",
                "category": "Comunidad",
                "image": "iniciativas/gestion-de-funciones-algo-de-ricardo.jpg",
            }
        ]

        desired_obras = [
            {
                "title": "Cuidado con el Vigilante",
                "release_date": date(2026, 3, 1),
                "synopsis": (
                    "¡Cuidado con el Vigilante! es una intervención callejera de Teatro Oculto que activa espacios públicos a través del humor físico, la música en vivo y el juego de máscaras inspirado en la tradición de la commedia dell’arte. En escena, un autoproclamado “vigilante comunitario” intenta demostrar su heroísmo frente a Colombina, una mujer de feria que no se deja impresionar fácilmente, dando lugar a un encuentro lleno de equívocos, fanfarronerías y situaciones cómicas.\n"
                    "\n"
                    "En apenas quince minutos, el espectáculo despliega un romance inesperado que cuestiona los roles de poder y cuidado: quien dice proteger termina necesitando ser cuidado. Con esta propuesta, la compañía retoma el espíritu del antiguo teatro itinerante, acercando el teatro al público en su propio entorno y recordando que los arquetipos clásicos de la comedia siguen vivos en las historias cotidianas que ocurren en nuestras calles."
                ),
                "active": True,
            },
            {
                "title": "Sobre el daño que causa el tabaco",
                "release_date": None,
                "synopsis": TABACO_SYNOPSIS,
                "active": True,
            }
        ]

        created = 0
        skipped = 0

        for ini in desired_iniciativas:
            title = ini["title"].strip()
            desired_slug = (slugify(title) or "iniciativa")[:220]

            existing = (
                Iniciativa.objects.filter(slug=desired_slug).first()
                or Iniciativa.objects.filter(title__iexact=title).first()
            )

            if existing:
                updated_fields = []

                desired_image = (ini.get("image") or "").strip()
                current_image = existing.image.name if (existing.image and existing.image.name) else ""
                allow_image_overwrite = False
                if (existing.title or "").strip() == "Taller de Teatro Performance":
                    allow_image_overwrite = current_image in {"", "iniciativas/ensayo.jpg"}
                elif (existing.title or "").strip() == "Gestión de funciones: Algo de Ricardo":
                    allow_image_overwrite = current_image in {"", "iniciativas/ricardo.jpg"}
                else:
                    allow_image_overwrite = current_image == ""

                if desired_image and allow_image_overwrite and current_image != desired_image:
                    if dry_run:
                        self.stdout.write(f"WOULD UPDATE image: {existing.title} -> {desired_image}")
                    else:
                        existing.image.name = desired_image
                        updated_fields.append("image")

                desired_desc = (ini.get("description") or "").strip()
                current_desc = (existing.description or "").strip()
                allow_desc_overwrite = not current_desc
                if (existing.title or "").strip() == "Taller de Teatro Performance":
                    allow_desc_overwrite = (not current_desc) or ("escena contempor" in current_desc.lower())

                if desired_desc and allow_desc_overwrite and current_desc != desired_desc:
                    if dry_run:
                        self.stdout.write(f"WOULD UPDATE description: {existing.title}")
                    else:
                        existing.description = desired_desc
                        updated_fields.append("description")

                desired_cat = (ini.get("category") or "").strip()
                if desired_cat and not (existing.category or "").strip():
                    if dry_run:
                        self.stdout.write(f"WOULD UPDATE category: {existing.title} -> {desired_cat}")
                    else:
                        existing.category = desired_cat
                        updated_fields.append("category")

                if updated_fields and not dry_run:
                    existing.save(update_fields=updated_fields)
                    self.stdout.write(self.style.SUCCESS(f"UPDATED: {existing.title} ({', '.join(updated_fields)})"))
                else:
                    skipped += 1
                    self.stdout.write(f"OK (exists): {existing.title}")
                continue

            if dry_run:
                created += 1
                self.stdout.write(f"WOULD CREATE: {title}")
                continue

            Iniciativa.objects.create(
                title=title,
                description=ini["description"],
                category=ini["category"],
                image=(ini.get("image") or "") or None,
            )
            created += 1
            self.stdout.write(self.style.SUCCESS(f"CREATED: {title}"))

        for obra in desired_obras:
            title = obra["title"].strip()
            desired_slug = (slugify(title) or "obra")[:220]

            existing = (
                Obra.objects.filter(slug=desired_slug).first()
                or Obra.objects.filter(title__iexact=title).first()
            )

            if existing is None and "tabaco" in title.lower():
                existing = Obra.objects.filter(title__icontains="tabaco").first()

            if existing:
                updated_fields = []

                # If we matched the historic "tabaco" obra with an old title/slug
                # (e.g. "... del tabaco"), normalize the slug so Git-tracked posters
                # under MULTIMEDIA TEATRO OCULTO/obras/<slug>/poster.* are found.
                if "tabaco" in title.lower():
                    current_slug = (existing.slug or "").strip()
                    if current_slug and current_slug != desired_slug:
                        slug_taken = Obra.objects.filter(slug=desired_slug).exclude(pk=existing.pk).exists()
                        if not slug_taken:
                            if dry_run:
                                self.stdout.write(f"WOULD UPDATE slug: {existing.title} -> {desired_slug}")
                            else:
                                existing.slug = desired_slug
                                updated_fields.append("slug")

                    # Optionally normalize the title if it's a known typo variant.
                    current_title = (existing.title or "").strip()
                    if current_title.lower() == "sobre el daño que causa del tabaco" and current_title != title:
                        if dry_run:
                            self.stdout.write(f"WOULD UPDATE title: {current_title} -> {title}")
                        else:
                            existing.title = title
                            updated_fields.append("title")

                desired_synopsis = (obra.get("synopsis") or "").strip()
                current_synopsis = (existing.synopsis or "").strip()
                allow_synopsis_overwrite = (not current_synopsis) or ("Sinopsis pendiente" in current_synopsis)
                if desired_synopsis and allow_synopsis_overwrite and current_synopsis != desired_synopsis:
                    if dry_run:
                        self.stdout.write(f"WOULD UPDATE synopsis: {existing.title}")
                    else:
                        existing.synopsis = desired_synopsis
                        updated_fields.append("synopsis")

                desired_date = obra.get("release_date")
                if desired_date and (existing.release_date is None) and existing.release_date != desired_date:
                    if dry_run:
                        self.stdout.write(f"WOULD UPDATE release_date: {existing.title} -> {desired_date}")
                    else:
                        existing.release_date = desired_date
                        updated_fields.append("release_date")

                desired_active = bool(obra.get("active", True))
                if existing.active != desired_active:
                    if dry_run:
                        self.stdout.write(f"WOULD UPDATE active: {existing.title} -> {int(desired_active)}")
                    else:
                        existing.active = desired_active
                        updated_fields.append("active")

                if updated_fields and not dry_run:
                    existing.save(update_fields=updated_fields)
                    self.stdout.write(self.style.SUCCESS(f"UPDATED: {existing.title} ({', '.join(updated_fields)})"))
                else:
                    skipped += 1
                    self.stdout.write(f"OK (exists): {existing.title}")
                continue

            if dry_run:
                created += 1
                self.stdout.write(f"WOULD CREATE: {title}")
                continue

            Obra.objects.create(
                title=title,
                synopsis=obra["synopsis"],
                active=bool(obra.get("active", True)),
                release_date=obra.get("release_date"),
            )
            created += 1
            self.stdout.write(self.style.SUCCESS(f"CREATED: {title}"))

        self.stdout.write(
            f"Done. created={created} skipped={skipped} dry_run={int(dry_run)}"
        )
