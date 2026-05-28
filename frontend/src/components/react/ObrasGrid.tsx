'use client';
import { useState } from 'react';
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';

export interface Obra {
  id: string;
  title: string;
  synopsis: string;
  poster: string;
  release_date?: string;
  gallery?: string[];
  duration?: string;
  cast?: string[];
}

interface Props {
  obras: Obra[];
}

const overlayVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.25 } },
  exit: { opacity: 0, transition: { duration: 0.2 } },
};

const modalVariants = {
  hidden: { opacity: 0, scale: 0.95, y: 20 },
  visible: { opacity: 1, scale: 1, y: 0, transition: { duration: 0.35, ease: [0.22, 1, 0.36, 1] } },
  exit: { opacity: 0, scale: 0.97, y: 10, transition: { duration: 0.2 } },
};

export default function ObrasGrid({ obras }: Props) {
  const [selected, setSelected] = useState<Obra | null>(null);
  const reduced = useReducedMotion();

  const close = () => setSelected(null);

  return (
    <>
      {/* ── Grid ───────────────────────────────────────────────────── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {obras.map((obra, i) => (
          <motion.article
            key={obra.id}
            initial={reduced ? false : { opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-60px' }}
            transition={{ duration: 0.55, ease: [0.22, 1, 0.36, 1], delay: i * 0.1 }}
            className="card-glass cursor-pointer group"
            onClick={() => setSelected(obra)}
            role="button"
            tabIndex={0}
            aria-label={`Ver detalles de ${obra.title}`}
            onKeyDown={(e) => e.key === 'Enter' && setSelected(obra)}
          >
            {/* Poster */}
            <div className="overflow-hidden rounded-t-2xl" style={{ height: '260px' }}>
              <img
                src={obra.poster}
                alt={`Afiche — ${obra.title}`}
                className="card-img h-full w-full"
                style={{ height: '260px' }}
                loading="lazy"
                decoding="async"
                onError={(e) => {
                  (e.target as HTMLImageElement).src = '/images/placeholder-poster.svg';
                }}
              />
            </div>

            {/* Info */}
            <div className="p-5">
              <h3
                className="text-lg font-bold text-white mb-2 leading-tight text-balance"
                style={{ textWrap: 'balance' } as React.CSSProperties}
              >
                {obra.title}
              </h3>
              <p className="text-sm text-white/55 leading-relaxed line-clamp-3 mb-4">
                {obra.synopsis.split('\n')[0]}
              </p>

              {obra.release_date && (
                <p className="text-xs text-white/35 font-medium mb-3">
                  Estreno:{' '}
                  {new Date(obra.release_date).toLocaleDateString('es-CL', {
                    month: 'long',
                    year: 'numeric',
                  })}
                </p>
              )}

              <span className="text-xs font-bold uppercase tracking-widest text-crimson group-hover:text-crimson-hover transition-colors flex items-center gap-1.5">
                Más información
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </span>
            </div>
          </motion.article>
        ))}
      </div>

      {/* ── Modal ──────────────────────────────────────────────────── */}
      <AnimatePresence>
        {selected && (
          <>
            {/* Backdrop */}
            <motion.div
              key="backdrop"
              variants={overlayVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              className="fixed inset-0 z-[100] bg-black/80 backdrop-blur-sm"
              onClick={close}
              aria-hidden="true"
            />

            {/* Modal panel */}
            <motion.div
              key="modal"
              role="dialog"
              aria-modal="true"
              aria-labelledby="modal-title"
              variants={modalVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              className="fixed inset-4 sm:inset-8 lg:inset-16 z-[101] overflow-y-auto rounded-3xl border border-white/08"
              style={{
                background: 'linear-gradient(145deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01)) , #0a0c14',
                boxShadow: '0 32px 80px rgba(0,0,0,0.7)',
                maxHeight: 'calc(100vh - 4rem)',
              }}
            >
              {/* Close button */}
              <button
                onClick={close}
                className="absolute top-4 right-4 z-10 w-9 h-9 flex items-center justify-center rounded-full border border-white/20 bg-black/50 text-white/60 hover:text-white hover:border-white/40 transition-all"
                aria-label="Cerrar"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                </svg>
              </button>

              <div className="grid lg:grid-cols-[380px_1fr] gap-0 h-full">
                {/* Left: poster */}
                <div className="relative overflow-hidden rounded-t-3xl lg:rounded-l-3xl lg:rounded-tr-none" style={{ minHeight: '280px' }}>
                  <img
                    src={selected.poster}
                    alt={`Afiche — ${selected.title}`}
                    className="w-full h-full object-cover"
                    style={{ minHeight: '280px', maxHeight: '100%' }}
                    loading="eager"
                    decoding="async"
                    onError={(e) => {
                      (e.target as HTMLImageElement).src = '/images/placeholder-poster.svg';
                    }}
                  />
                  <div
                    className="absolute inset-0 pointer-events-none"
                    style={{
                      background: 'linear-gradient(to right, transparent 60%, #0a0c14 100%), linear-gradient(to top, #0a0c14 0%, transparent 30%)',
                    }}
                  />
                </div>

                {/* Right: content */}
                <div className="p-7 lg:p-10 overflow-y-auto">
                  <h2 id="modal-title" className="text-2xl sm:text-3xl font-black text-white mb-1 leading-tight">
                    {selected.title}
                  </h2>
                  <div className="h-px w-12 my-3" style={{ background: 'linear-gradient(90deg, #e04242, transparent)' }} />

                  {selected.release_date && (
                    <p className="text-xs text-white/40 font-medium uppercase tracking-widest mb-5">
                      Estreno:{' '}
                      {new Date(selected.release_date).toLocaleDateString('es-CL', {
                        month: 'long',
                        year: 'numeric',
                      })}
                      {selected.duration && ` · ${selected.duration}`}
                    </p>
                  )}

                  <div className="prose prose-invert prose-sm max-w-none text-white/70 leading-relaxed mb-8">
                    {selected.synopsis.split('\n\n').map((para, i) => (
                      <p key={i} className="mb-3 last:mb-0">{para}</p>
                    ))}
                  </div>

                  {selected.cast && selected.cast.length > 0 && (
                    <div className="mb-8">
                      <p className="text-xs font-black uppercase tracking-theater text-white/40 mb-3">Elenco</p>
                      <div className="flex flex-wrap gap-2">
                        {selected.cast.map((actor) => (
                          <span
                            key={actor}
                            className="text-xs px-3 py-1 rounded-full border border-white/10 text-white/65"
                          >
                            {actor}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Gallery */}
                  {selected.gallery && selected.gallery.length > 0 && (
                    <div>
                      <p className="text-xs font-black uppercase tracking-theater text-white/40 mb-3">Galería</p>
                      <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                        {selected.gallery.map((img, i) => (
                          <a
                            key={i}
                            href={img}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="overflow-hidden rounded-lg border border-white/05 hover:border-white/20 transition-colors"
                          >
                            <img
                              src={img}
                              alt={`Galería ${i + 1} — ${selected.title}`}
                              className="w-full object-cover hover:scale-105 transition-transform duration-300"
                              style={{ height: '100px' }}
                              loading="lazy"
                              decoding="async"
                            />
                          </a>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
