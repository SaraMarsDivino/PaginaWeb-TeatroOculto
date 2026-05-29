'use client';
import { useRef, useState, useEffect } from 'react';
import { motion, useReducedMotion } from 'framer-motion';

const WORDS = ['Teatro', 'Oculto'] as const;

const containerVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.18, delayChildren: 0.1 } },
};

const lineVariants = {
  hidden: { y: '110%', opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: { duration: 0.85, ease: [0.22, 1, 0.36, 1] },
  },
};

const fadeUp = {
  hidden: { opacity: 0, y: 18 },
  visible: (delay = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.7, ease: [0.22, 1, 0.36, 1], delay },
  }),
};

export default function SpotlightHero() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [mouse, setMouse] = useState({ x: 0, y: 0 });
  const [hasEntered, setHasEntered] = useState(false);
  const reducedMotion = useReducedMotion();

  useEffect(() => {
    // small delay so entrance animation feels deliberate
    const t = setTimeout(() => setHasEntered(true), 80);
    return () => clearTimeout(t);
  }, []);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = containerRef.current?.getBoundingClientRect();
    if (!rect) return;
    setMouse({ x: e.clientX - rect.left, y: e.clientY - rect.top });
  };

  return (
    <section
      ref={containerRef}
      onMouseMove={handleMouseMove}
      className="relative min-h-[calc(100vh-5rem)] flex flex-col items-center justify-center overflow-hidden select-none"
      aria-label="Hero — Teatro Oculto"
    >
      {/* ── Ambient background ───────────────────────────────────── */}
      <div
        className="absolute inset-0 pointer-events-none z-0"
        style={{
          background:
            'radial-gradient(ellipse 80% 60% at 50% -10%, rgba(224,66,66,0.22), transparent 60%), radial-gradient(ellipse 60% 50% at 80% 90%, rgba(215,179,106,0.12), transparent 55%)',
        }}
      />

      {/* ── Mouse-tracking spotlight (Aceternity style) ───────────── */}
      {!reducedMotion && hasEntered && (
        <div
          className="absolute inset-0 pointer-events-none z-10 transition-none"
          style={{
            background: `radial-gradient(700px circle at ${mouse.x}px ${mouse.y}px, rgba(224,66,66,0.13), transparent 40%)`,
          }}
        />
      )}

      {/* ── Background beams (diagonal light shafts) ──────────────── */}
      {!reducedMotion && (
        <div className="absolute inset-0 overflow-hidden pointer-events-none z-0" aria-hidden="true">
          {[...Array(8)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute h-px"
              style={{
                top: `${10 + i * 11}%`,
                left: '-20%',
                right: '-20%',
                background:
                  'linear-gradient(90deg, transparent 0%, rgba(215,179,106,0.06) 40%, rgba(215,179,106,0.10) 50%, rgba(215,179,106,0.06) 60%, transparent 100%)',
                transform: `rotate(${-35 + i * 2}deg)`,
                transformOrigin: 'center',
              }}
              animate={{ x: ['0%', '30%', '0%'] }}
              transition={{
                duration: 12 + i * 3,
                repeat: Infinity,
                ease: 'easeInOut',
                delay: i * 1.4,
              }}
            />
          ))}
        </div>
      )}

      {/* ── Film grain ────────────────────────────────────────────── */}
      <div className="grain" aria-hidden="true" />

      {/* ── Main content ──────────────────────────────────────────── */}
      <div className="relative z-20 text-center px-4 max-w-5xl w-full">

        {/* Pre-title tag */}
        <motion.div
          variants={fadeUp}
          custom={0}
          initial="hidden"
          animate={hasEntered ? 'visible' : 'hidden'}
          className="flex items-center justify-center gap-3 mb-8"
        >
          <span
            className="h-px w-12"
            style={{ background: 'linear-gradient(90deg, transparent, #d7b36a)' }}
          />
          <span className="text-[10px] font-black uppercase tracking-theater text-white/45">
            Artes Escénicas · La Calera, Valparaíso
          </span>
          <span
            className="h-px w-12"
            style={{ background: 'linear-gradient(90deg, #d7b36a, transparent)' }}
          />
        </motion.div>

        {/* ── TEATRO OCULTO in huge type ─────────────────────────── */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate={hasEntered ? 'visible' : 'hidden'}
          aria-label="Teatro Oculto"
        >
          {WORDS.map((word, wi) => (
            <div key={word} className="overflow-hidden leading-none">
              <motion.h1
                variants={lineVariants}
                className="font-black text-white tracking-tight"
                style={{
                  fontSize: 'clamp(4.5rem, 17vw, 14rem)',
                  lineHeight: 0.9,
                  letterSpacing: '-0.02em',
                  ...(wi === 1 && {
                    WebkitTextStroke: '1px rgba(255,255,255,0.12)',
                    color: 'rgba(255,255,255,0.92)',
                  }),
                }}
              >
                {word === 'Oculto' ? (
                  <>
                    <span style={{ color: '#e04242' }}>O</span>culto
                  </>
                ) : (
                  word
                )}
              </motion.h1>
            </div>
          ))}
        </motion.div>

        {/* Tagline */}
        <motion.p
          variants={fadeUp}
          custom={0.55}
          initial="hidden"
          animate={hasEntered ? 'visible' : 'hidden'}
          className="mt-8 text-sm sm:text-base text-white/75 font-medium max-w-md mx-auto leading-relaxed"
        >
          Compañía de teatro independiente comprometida con la creación escénica,
          la formación de audiencias y la vinculación comunitaria.
        </motion.p>

        {/* CTA buttons */}
        <motion.div
          variants={fadeUp}
          custom={0.75}
          initial="hidden"
          animate={hasEntered ? 'visible' : 'hidden'}
          className="mt-10 flex flex-wrap items-center justify-center gap-4"
        >
          <a href="/obras" className="btn-primary">
            Explorar obras
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </a>
          <a href="/nosotros" className="btn-ghost">
            Conócenos
          </a>
        </motion.div>
      </div>

    </section>
  );
}
