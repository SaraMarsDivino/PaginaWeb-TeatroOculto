'use client';
import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';

interface CarouselItem {
  src: string;
  thumb?: string;
  alt?: string;
}

interface Props {
  items: CarouselItem[];
  autoPlayMs?: number;
}

const slideVariants = {
  enter: (dir: number) => ({
    x: dir > 0 ? '6%' : '-6%',
    opacity: 0,
    scale: 1.04,
    filter: 'blur(8px)',
  }),
  center: {
    x: 0,
    opacity: 1,
    scale: 1,
    filter: 'blur(0px)',
    transition: { duration: 1.0, ease: [0.32, 0.72, 0, 1] },
  },
  exit: (dir: number) => ({
    x: dir > 0 ? '-6%' : '6%',
    opacity: 0,
    scale: 0.97,
    filter: 'blur(4px)',
    transition: { duration: 0.65, ease: [0.32, 0.72, 0, 1] },
  }),
};

export default function HeroCarousel({ items, autoPlayMs = 5500 }: Props) {
  const [[index, direction], setSlide] = useState([0, 1]);
  const reducedMotion = useReducedMotion();

  const go = useCallback((dir: number) => {
    setSlide(([i]) => {
      const next = (i + dir + items.length) % items.length;
      return [next, dir];
    });
  }, [items.length]);

  useEffect(() => {
    if (reducedMotion) return;
    const id = setInterval(() => go(1), autoPlayMs);
    return () => clearInterval(id);
  }, [go, autoPlayMs, reducedMotion]);

  if (!items.length) return null;

  const current = items[index];

  return (
    <div className="relative overflow-hidden rounded-3xl aspect-[4/3] sm:aspect-[16/9] md:aspect-[16/7]">

      {/* Edge fade — left */}
      <div
        className="absolute inset-y-0 left-0 z-20 pointer-events-none"
        style={{ width: 'clamp(24px, 8vw, 120px)', background: 'linear-gradient(to right, #060810 0%, transparent 100%)' }}
      />
      {/* Edge fade — right */}
      <div
        className="absolute inset-y-0 right-0 z-20 pointer-events-none"
        style={{ width: 'clamp(24px, 8vw, 120px)', background: 'linear-gradient(to left, #060810 0%, transparent 100%)' }}
      />

      {/* Slides */}
      <AnimatePresence initial={false} custom={direction} mode="popLayout">
        <motion.div
          key={index}
          custom={direction}
          variants={reducedMotion ? {} : slideVariants}
          initial={index === 0 ? false : 'enter'}
          animate="center"
          exit="exit"
          className="absolute inset-0"
        >
          <img
            src={current.src}
            srcSet={current.thumb ? `${current.thumb} 640w, ${current.src} 1920w` : undefined}
            sizes="100vw"
            alt={current.alt ?? `Slide ${index + 1}`}
            className="w-full h-full object-cover"
            style={{
              filter: 'contrast(1.1) saturate(1.05) brightness(1.1)',
              animation: reducedMotion ? undefined : 'ken-burns 10s ease-out both',
            }}
            loading={index === 0 ? 'eager' : 'lazy'}
            fetchpriority={index === 0 ? 'high' : 'auto'}
            decoding={index === 0 ? 'sync' : 'async'}
          />

          {/* Gradient overlays */}
          <div
            className="absolute inset-0 pointer-events-none"
            style={{
              background:
                'linear-gradient(180deg, rgba(6,8,16,0.72) 0%, rgba(6,8,16,0.28) 30%, rgba(6,8,16,0.28) 65%, rgba(6,8,16,0.88) 100%)',
            }}
          />

          {/* Film grain */}
          <div
            className="absolute inset-0 pointer-events-none opacity-[0.06] mix-blend-overlay"
            style={{
              backgroundImage:
                "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")",
            }}
          />
        </motion.div>
      </AnimatePresence>

      {/* Cinema tag */}
      <div className="absolute bottom-5 left-5 z-10 flex items-center gap-3" aria-label="Teatro Oculto">
        <div
          className="h-[2px] w-12 animate-bar-sheen"
          style={{
            background: 'linear-gradient(90deg, #e04242, #d7b36a, #e04242)',
            backgroundSize: '200% 100%',
          }}
        />
        <span className="text-[10px] font-black uppercase tracking-theater text-white/85">
          Teatro Oculto
        </span>
      </div>

      {/* Slide counter */}
      <div className="absolute bottom-5 right-5 z-10 flex items-center gap-1.5">
        <span className="text-[10px] font-black text-white tabular-nums">{String(index + 1).padStart(2, '0')}</span>
        <span className="text-white/30 text-[10px]">/</span>
        <span className="text-[10px] text-white/40 tabular-nums">{String(items.length).padStart(2, '0')}</span>
      </div>

      {/* Nav buttons */}
      <div className="absolute inset-y-0 left-0 right-0 flex items-center justify-between px-3 z-10 pointer-events-none">
        <button
          onClick={() => go(-1)}
          className="pointer-events-auto w-9 h-9 flex items-center justify-center rounded-full border border-white/20 bg-black/30 text-white/70 hover:text-white hover:border-white/40 hover:bg-black/50 backdrop-blur-sm transition-all"
          aria-label="Imagen anterior"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M15 19l-7-7 7-7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
        <button
          onClick={() => go(1)}
          className="pointer-events-auto w-9 h-9 flex items-center justify-center rounded-full border border-white/20 bg-black/30 text-white/70 hover:text-white hover:border-white/40 hover:bg-black/50 backdrop-blur-sm transition-all"
          aria-label="Imagen siguiente"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M9 5l7 7-7 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>

      {/* Dot indicators */}
      <div className="absolute bottom-5 left-1/2 -translate-x-1/2 z-10 flex gap-1.5" role="tablist" aria-label="Slides">
        {items.map((_, i) => (
          <button
            key={i}
            role="tab"
            aria-selected={i === index}
            aria-label={`Ir al slide ${i + 1}`}
            onClick={() => setSlide([i, i > index ? 1 : -1])}
            className="transition-all duration-300 rounded-full"
            style={{
              width: i === index ? '20px' : '6px',
              height: '6px',
              background: i === index ? '#e04242' : 'rgba(255,255,255,0.3)',
            }}
          />
        ))}
      </div>
    </div>
  );
}
