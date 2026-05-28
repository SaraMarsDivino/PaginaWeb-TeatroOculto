from django.db import models
from django.utils.text import slugify


class Iniciativa(models.Model):
    CREACION = 'Creación'
    FORMACION = 'Formación'
    COMUNIDAD = 'Comunidad'
    CATEGORY_CHOICES = [
        (CREACION, 'Creación'),
        # Updated labels requested by client (Mar 2026)
        (FORMACION, 'Formación de audiencia y comunidad'),
        (COMUNIDAD, 'Formación de audiencia'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, blank=True, db_index=True)
    description = models.TextField()
    image = models.ImageField(upload_to='iniciativas/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or 'iniciativa'
            self.slug = base[:220]
        super().save(*args, **kwargs)

        if Iniciativa.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{self.slug[:200]}-{self.pk}"
            super().save(update_fields=['slug'])

    def __str__(self):
        return self.title


class Obra(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, blank=True, db_index=True)
    synopsis = models.TextField()
    poster_image = models.ImageField(upload_to='obras/', blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or 'obra'
            self.slug = base[:220]
        super().save(*args, **kwargs)

        if Obra.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{self.slug[:200]}-{self.pk}"
            super().save(update_fields=['slug'])

    def __str__(self):
        return self.title


class Suscriptor(models.Model):
    name = models.CharField(max_length=150, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class MensajeContacto(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.name} <{self.email}>"


class Equipo(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=220, blank=True, db_index=True)
    role = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='equipo/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} — {self.role}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or 'equipo'
            self.slug = base[:220]
        super().save(*args, **kwargs)

        if Equipo.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{self.slug[:200]}-{self.pk}"
            super().save(update_fields=['slug'])
