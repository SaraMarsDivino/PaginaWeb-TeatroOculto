from django.db import migrations


TABACO_SYNONYMS = [
    "sobre los daños que causa el tabaco",
    "sobre el daño que causa el tabaco",
    "sobre el daño que causa del tabaco",
]


NEW_SYNOPSIS = (
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


def forwards(apps, schema_editor):
    Obra = apps.get_model("web", "Obra")

    # Prefer exact title matches, but fall back to a relaxed lookup.
    for title in TABACO_SYNONYMS:
        updated = Obra.objects.filter(title__iexact=title).update(synopsis=NEW_SYNOPSIS)
        if updated:
            return

    candidates = Obra.objects.filter(title__icontains="tabaco")
    if candidates.exists():
        candidates.update(synopsis=NEW_SYNOPSIS)


def backwards(apps, schema_editor):
    # Non-destructive: keep whatever synopsis is currently in the DB.
    return


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0002_suscriptor_age"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
