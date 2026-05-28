# Teatro Oculto — Frontend (Astro)

Sitio web estático de Teatro Oculto. Stack: **Astro 4** + **Tailwind CSS 3** + **Framer Motion** + **Lenis**.

## Instalación

```bash
cd frontend
npm install
npm run dev        # http://localhost:4321
npm run build      # genera dist/
npm run preview    # previsualizar el build
```

## Estructura

```
src/
  components/
    react/            # Componentes interactivos (React + Framer Motion)
      SpotlightHero   # Hero de inicio con spotlight y animaciones
      HeroCarousel    # Carrusel de imágenes cinematográfico
      ObrasGrid       # Grid de obras con modal detalle
      ContactForm     # Formulario con validación
    Navbar.astro
    Footer.astro
  content/
    obras/            # Markdown de cada obra (frontmatter + sinopsis)
    iniciativas/      # Markdown de cada eje/iniciativa
  data/
    equipo.ts         # Datos del equipo (TypeScript)
  layouts/
    BaseLayout.astro  # HTML base, Lenis, meta tags
  pages/
    index.astro       # Inicio
    nosotros.astro    # Nosotros + equipo
    iniciativas.astro # Ejes expandibles
    obras.astro       # Grid de obras + modal
    contacto.astro    # Formulario de contacto
  styles/
    global.css        # Tailwind + variables + componentes globales
```

## 1. Copiar imágenes

Las imágenes provienen del proyecto Django anterior. Cópialas así:

```
MULTIMEDIA TEATRO OCULTO/carousel/        → public/images/carousel/
MULTIMEDIA TEATRO OCULTO/carousel/thumbs/ → public/images/carousel/thumbs/
MULTIMEDIA TEATRO OCULTO/iniciativas/     → public/images/iniciativas/
MULTIMEDIA TEATRO OCULTO/obras/           → public/images/obras/
MULTIMEDIA TEATRO OCULTO/nosotros/bw/     → public/images/nosotros/
web/static/web/brand/                     → public/images/brand/
```

Convención de nombres (sin tildes y en minúsculas):
```
nosotros/pablo-valencia.jpg
nosotros/estefania-villalobos.jpg
nosotros/fabian-zuniga.jpg
nosotros/camila-emilce.jpg
brand/logo.png
brand/isotipo.png
brand/ensayo-oculto.jpg
brand/favicon-16.png  favicon-32.png  favicon-180.png
```

## 2. Configurar el formulario de contacto

El componente `ContactForm.tsx` usa [Formspree](https://formspree.io) (gratuito, sin backend).

1. Crea una cuenta en formspree.io
2. Crea un formulario y copia el ID (ej: `xrgvkpqz`)
3. Reemplaza en dos archivos:
   - `src/components/react/ContactForm.tsx` línea 7: `YOUR_FORM_ID`
   - `src/pages/index.astro` en el form del newsletter: `YOUR_FORM_ID`

## 3. Agregar obras o iniciativas

**Nueva obra:** crear `src/content/obras/mi-obra.md`:
```markdown
---
title: "Título de la obra"
synopsis: "Sinopsis completa..."
poster: "/images/obras/mi-obra/poster.jpg"
release_date: "2025-06-01"
active: true
gallery:
  - "/images/obras/mi-obra/gallery/img1.jpg"
duration: "60 minutos"
cast:
  - "Actor 1"
---
```

**Nueva iniciativa:** crear `src/content/iniciativas/mi-eje.md`:
```markdown
---
title: "Nombre del eje"
category: "Creación"   # Creación | Formación | Comunidad
image: "/images/iniciativas/mi-imagen.png"
order: 4
---

Descripción completa en Markdown...
```

## 4. Despliegue

**Netlify** (recomendado):
```toml
# netlify.toml
[build]
  base = "frontend"
  command = "npm run build"
  publish = "dist"
```

**Cloudflare Pages:** build command `npm run build`, output `dist`.

**Servidor propio:** subir el contenido de `dist/` a cualquier hosting estático (Apache, Nginx, etc.).
