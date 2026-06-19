# Teatro Oculto — Contexto de Proyecto

> Documento de referencia para continuar el trabajo en sesiones futuras.  
> **No hacer push a git sin indicación explícita del usuario.**

---

## Resumen ejecutivo

Sitio web de **Teatro Oculto**, compañía de artes escénicas con sede en La Calera, Región de Valparaíso, Chile. El proyecto tiene dos capas:

1. **Backend Django (legacy)** — en disco, no eliminar, no tocar.
2. **Frontend Astro (activo)** — reconstrucción Jamstack estática. **Ya desplegado en producción.**

---

## Repositorio Git

- **URL:** https://github.com/SaraMarsDivino/PaginaWeb-TeatroOculto
- **Rama principal:** `main`
- **Último commit:** `67c8352` — fix(obras): parse release_date in local time to avoid UTC offset showing wrong month
- **Git config local:** user `SaraMarsDivino`, email `rochaulin2@gmail.com`

---

## Servidor de producción (Raspberry Pi)

- **IP local:** `192.168.1.24`
- **Usuario SSH:** `pablo`
- **Ruta del proyecto:** `/home/pablo/teatro_project/`
- **Stack:** Docker Compose — nginx (443/80) + gunicorn (Django, puerto 8000 interno)
- **Node.js:** instalado vía `apt` (para builds futuros)
- **nvm:** también instalado en `~/.nvm` pero NO usar para builds (usar `node` directo de apt)

### Comandos clave en el servidor

```bash
# Ver estado
cd ~/teatro_project && docker compose ps

# Reiniciar todo
cd ~/teatro_project && docker compose down && docker compose up -d

# Reiniciar solo nginx (para cambios de config)
cd ~/teatro_project && docker compose restart nginx

# Rebuild frontend y redeploy
cd ~/teatro_project/frontend && npm install && npm run build
cd ~/teatro_project && docker compose restart nginx
```

### Flujo de deploy

1. Hacer cambios localmente en `D:\PROYECTOS PROGRAMADOR\PaginaWeb-TeatroOculto-main\frontend\`
2. Probar en `http://localhost:4321/`
3. Push a GitHub: `git add . && git commit -m "..." && git push origin main`
4. En el servidor vía SSH:
   ```bash
   cd ~/teatro_project && git pull && cd frontend && npm install && npm run build && cd .. && docker compose restart nginx
   ```

---

## Rutas clave

```
D:\PROYECTOS PROGRAMADOR\PaginaWeb-TeatroOculto-main\   ← raíz del repositorio
│
├── frontend\                  ← PROYECTO ACTIVO (Astro)
│   ├── src\
│   │   ├── components\
│   │   │   ├── react\         ← SpotlightHero, HeroCarousel, ObrasGrid, ContactForm
│   │   │   ├── Navbar.astro
│   │   │   └── Footer.astro
│   │   ├── content\
│   │   │   ├── obras\         ← Markdown: sobre-el-dano, cuidado-con-el-vigilante
│   │   │   └── iniciativas\   ← Markdown: creacion, formacion, colaboracion
│   │   ├── data\
│   │   │   └── equipo.ts      ← 4 integrantes hardcodeados
│   │   ├── layouts\
│   │   │   └── BaseLayout.astro  ← spotlight global + orbs animados aquí
│   │   ├── pages\             ← index, nosotros, iniciativas, obras, contacto
│   │   └── styles\
│   │       └── global.css     ← Tailwind + variables CSS + componentes globales
│   ├── public\
│   │   └── images\            ← imágenes copiadas desde MULTIMEDIA TEATRO OCULTO
│   └── dist\                  ← build output (en .gitignore, se genera en el servidor)
│
├── nginx\
│   └── teatro.conf            ← configuración nginx (SSL + WebP + cache)
├── MULTIMEDIA TEATRO OCULTO\  ← fuente original de imágenes (NO MOVER, en .gitignore)
├── web\                       ← app Django legacy
├── teatro_project\            ← settings Django
└── manage.py
```

---

## Stack tecnológico (frontend Astro)

| Capa | Tecnología | Versión |
|---|---|---|
| Framework | Astro | 4.16.x (estático) |
| Estilos | Tailwind CSS | 3.4.x |
| Animaciones | Framer Motion | 11.x |
| Smooth scroll | Lenis | 1.1.x |
| Componentes React | React 18 | 18.3.x |
| Contenido | Astro Content Collections | nativo |
| Formularios | Formspree | endpoint: `mzdwyjke` |

**Formspree endpoint completo:** `https://formspree.io/f/mzdwyjke`  
Configurado en `frontend/src/components/react/ContactForm.tsx` línea 7

---

## Diseño / UI

### Paleta de colores
```css
--bg:          #060810        /* negro azulado profundo */
--accent:      #e04242        /* carmesí teatral */
--gold:        #d7b36a        /* oro teatral */
--text:        rgba(255,255,255,0.92)
--muted:       rgba(255,255,255,0.55)
--border:      rgba(255,255,255,0.08)
```

### Convención de opacidad de texto (Tailwind)
| Clase | Uso |
|---|---|
| `text-white/90`+ | Base del body, títulos |
| `text-white/80`–`/82` | Texto de cuerpo principal (párrafos largos) |
| `text-white/75` | Descripciones de sección, sinopsis, taglines, bio |
| `text-white/70` | Texto secundario (previews, credenciales) |
| `text-white/65` | Labels de formulario, texto expandible secundario |
| `text-white/40`–`/35` | Labels decorativos, etiquetas pequeñas en mayúsculas |
| `text-white/30` | Placeholder de inputs, elementos muy sutiles |

### Fuente
**Montserrat** (Google Fonts) — cargada vía `<link>` en `BaseLayout.astro`, NO en CSS.

### Componentes visuales clave
- **SpotlightHero** — hero con spotlight que sigue el mouse, título animado con curtain reveal, background beams diagonales. Sin indicador "Scroll" (fue eliminado).
- **HeroCarousel** — carrusel con blur+scale+ken-burns, autoplay 5.5s, difuminado en bordes izquierdo y derecho.
- **ObrasGrid** — cards con hover lift, modal cinematográfico con `AnimatePresence`.
- **ContactForm** — validación client-side, spinner, estado success animado. Usa Formspree.
- **Navbar** — glassmorphism al scroll, hamburger animado, logo `h-28`, ícono Instagram `24×24`.
- **BaseLayout** — incluye dos orbs animados (carmesí + dorado) y spotlight global que sigue el cursor en todas las páginas.

---

## Nginx en producción

Archivo: `/home/pablo/teatro_project/nginx/teatro.conf`

- Redirige HTTP → HTTPS
- SSL con certs en `/home/pablo/certs/`
- Sirve `frontend/dist/` como raíz estática
- Gzip activado para SVG, CSS, JS
- Imágenes con cache 30 días + header `immutable`
- Sirve `.webp` automáticamente cuando el navegador lo soporta (map `$http_accept`)
- Las imágenes WebP fueron generadas con `cwebp -q 82` directamente en el dist del servidor

---

## Contenido gestionado

### Obras (Astro Content Collections)
Archivos en `frontend/src/content/obras/*.md`

```yaml
title: string
synopsis: string (multiline)
poster: "/images/obras/{slug}/poster.png"
release_date: "YYYY-MM-DD"
active: boolean
gallery: string[]
duration: string
cast: string[]
```

Obras actuales:
1. `sobre-el-dano-que-causa-el-tabaco.md` — Estreno mayo 2026 · 45 min · 13 fotos en galería
2. `cuidado-con-el-vigilante.md` — Estreno mar 2026 · 20 min · 16 fotos en galería

**Textos:** aprobados por el cliente. Fuente original en `Obras - web teatro oculto.docx` (raíz del repo).

**Obra pendiente (NO subir aún):** "Algo de Ricardo" — hay consultas de derechos de autor sin resolver.

### Galería de imágenes
Imágenes en `frontend/public/images/obras/{slug}/gallery/` — archivos `.JPG` y `.png`.
- Nombres con espacios o paréntesis fueron renombrados con `_` (ej: `13 (1).JPG` → `13_1.JPG`).
- Archivos `.CR2` (RAW) no son compatibles con web — exportar como JPG antes de agregar.
- Al agregar fotos nuevas: copiar a la carpeta gallery correspondiente y agregar la ruta en el `.md` de la obra.

### Iniciativas
Archivos en `frontend/src/content/iniciativas/*.md`

```yaml
title: string
category: "Creación" | "Formación" | "Comunidad"
image: "/images/iniciativas/{filename}.png"
order: number
```

### Equipo
`frontend/src/data/equipo.ts` — Pablo Valencia Fernández, Estefania Villalobos, Fabián Zúñiga, Camila Estay Ancieta.

---

## Servidor de desarrollo local

```bash
cd "D:\PROYECTOS PROGRAMADOR\PaginaWeb-TeatroOculto-main\frontend"
npm run dev -- --host
# → http://localhost:4321
```

---

## Estado actual del proyecto

### ✅ Completado
- Estructura completa del proyecto Astro
- Todas las páginas: Inicio, Nosotros, Iniciativas, Obras, Contacto
- Componentes React animados con Framer Motion
- Lenis smooth scroll integrado
- Tailwind CSS con paleta teatral personalizada
- Content collections configuradas (obras + iniciativas)
- Imágenes organizadas en `public/images/`
- Formspree configurado (`mzdwyjke`)
- Logo navbar grande (`h-28`), ícono Instagram grande (`24×24`)
- Indicador "Scroll" eliminado del hero
- Difuminado en bordes del carrusel
- Efecto spotlight global + orbs animados en todas las páginas
- CSS warning corregido (`@import` duplicado eliminado)
- Git inicializado y conectado a GitHub
- **Desplegado en producción** en Raspberry Pi con Docker + nginx
- Imágenes convertidas a WebP en el servidor
- Nginx optimizado (gzip + cache + WebP condicional)
- **Contraste de textos mejorado** — opacidad de cuerpo subida +20 en toda la web
- **Iniciativas grid fix** — `items-start` evita que cards cerradas se estiren al abrir una vecina
- **Textos de obras corregidos** — sinopsis, título y fechas aprobados por el cliente (sesión 2026-06-05)
- **Galería de fotos** — 16 fotos en Vigilante, 13 en Tabaco. Rutas en cada `.md`
- **Lightbox en galería** — clic en foto abre vista de pantalla completa con botón "Volver" y flechas ← → para navegar entre imágenes
- **Deploy 2026-06-07** — git pull + npm run build + docker compose restart nginx en Raspberry Pi. Imágenes de galería convertidas a WebP con cwebp -q 82 en dist/ y redimensionadas a máximo 1920px con ImageMagick (reducción ~83% en peso, ej: 9_1.JPG pasó de 18MB → 419KB)
- **Deploy 2026-06-09** — Obra "Sobre el daño...": fecha → mayo 2026, duración → 45 min. Eliminado párrafo descriptivo bajo título "Obras". Fix bug zona horaria en parseo de fechas (UTC → local) en ObrasGrid.tsx
- **Sesión 2026-06-19 — Performance + Mobile fixes** (pendiente de deploy):
  - `HeroCarousel.tsx`: primer slide arranca visible (`initial={false}` en `motion.div`) en vez de `opacity:0`. Agrega `fetchpriority="high"` y `loading="eager"` a la primera imagen. Aspect ratio responsivo: `4/3` mobile → `16/9` sm → `16/7` md. Fade lateral responsivo: `clamp(24px, 8vw, 120px)` en vez de 120px fijo.
  - `BaseLayout.astro`: Google Fonts cambiado de `rel="stylesheet"` (bloqueante) a `rel="preload" as="style" onload=...` (asíncrono, ahorro ~1,480ms render-blocking). Agrega slot `<slot name="head">` para preloads por página.
  - `index.astro`: `<link rel="preload" as="image" href="/images/carousel/ensayo 1.jpg" fetchpriority="high">` en `<head>` vía slot.
  - `Navbar.astro`: Hamburguesa mobile corregida — líneas dentro de wrapper `<span class="flex flex-col items-start gap-[5px] w-5">` para alineación correcta. Animación X limpiada con `translateY(±6px) rotate(±45deg)`.

### 🔲 Pendiente / por hacer
- [ ] **CRÍTICO — Deploy pendiente**: hacer `git push` + deploy en servidor (sesión 2026-06-19 tiene 4 archivos modificados listos)
- [ ] **CRÍTICO — Imágenes carrusel en servidor**: convertir a WebP y redimensionar después del próximo deploy (son JPEGs sin optimizar de 3–7 MB cada uno, causa principal del LCP lento en producción):
  ```bash
  cd ~/teatro_project/frontend/dist/images/carousel
  for f in *.jpg *.JPG; do convert "$f" -resize "1920x1920>" "$f"; done
  for f in *.jpg *.JPG; do cwebp -q 82 "$f" -o "${f%.*}.webp"; done
  ```
- [ ] Agregar más imágenes al carousel
- [ ] OG image para redes sociales (`public/images/brand/og-image.jpg`)
- [ ] Dominio: verificar que `teatrooculto.cl` apunta correctamente al servidor
- [ ] Decidir si eliminar/archivar el backend Django
- [ ] "Algo de Ricardo" — agregar cuando se resuelvan los derechos de autor
- [ ] **Nota deploy futuro**: tras cada `npm run build`, regenerar WebP (`cwebp -q 82`) y redimensionar (`convert -resize "1920x1920>"`) las imágenes nuevas en `dist/images/obras/` Y `dist/images/carousel/`

---

## Contacto / identidad del proyecto

- **Web:** teatrooculto.cl
- **Email gestión:** gestion@teatrooculto.cl
- **Email comunicaciones:** comunicaciones@teatrooculto.cl (Zoho Mail)
- **Instagram:** @teatro.oculto_
- **Facebook:** Teatro Oculto (La Calera)
- **Sede:** La Calera, Región de Valparaíso, Chile

---

## Notas de desarrollo

- `MULTIMEDIA TEATRO OCULTO/` en la raíz **no mover ni eliminar** — fuente original de imágenes, en `.gitignore`.
- El backend Django (`manage.py`, `web/`, `teatro_project/`) está intacto pero no se usa en el frontend.
- Tailwind Intellisense en VSCode requiere abrir `frontend/` como workspace raíz.
- Los componentes React usan `client:load` (SpotlightHero, ContactForm) o `client:visible` (HeroCarousel, ObrasGrid).
- `useReducedMotion()` implementado en todos los componentes animados.
- La fuente Montserrat se carga en `BaseLayout.astro` vía `<link>`, no en `global.css`.
- Al hacer cambios en imágenes locales, hay que volver a convertir a WebP en el servidor después del `git pull`.
- La sección iniciativas usa `<details>` HTML nativo con animación CSS (`grid-template-rows: 0fr → 1fr`). El grid tiene `items-start` para que cada card sea independiente en altura.
- No modificar opacidades de texto por debajo de `/65` salvo labels decorativos intencionales (ver tabla de convención arriba).
