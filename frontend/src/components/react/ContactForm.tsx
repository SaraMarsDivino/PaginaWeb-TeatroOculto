'use client';
import { useState } from 'react';
import { motion } from 'framer-motion';

type Status = 'idle' | 'sending' | 'success' | 'error';

const FORMSPREE_ENDPOINT = 'https://formspree.io/f/mzdwyjke';

const inputClass =
  'w-full bg-white/03 border border-white/10 rounded-xl px-4 py-3 text-sm text-white placeholder-white/30 outline-none transition-all duration-200 focus:border-white/30 focus:bg-white/05 focus:ring-2 focus:ring-white/08';

export default function ContactForm() {
  const [status, setStatus] = useState<Status>('idle');
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = (data: FormData) => {
    const errs: Record<string, string> = {};
    if (!String(data.get('name')).trim()) errs.name = 'El nombre es requerido.';
    const email = String(data.get('email')).trim();
    if (!email) errs.email = 'El correo es requerido.';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) errs.email = 'Correo no válido.';
    if (!String(data.get('message')).trim()) errs.message = 'El mensaje es requerido.';
    return errs;
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const data = new FormData(form);
    const errs = validate(data);
    if (Object.keys(errs).length) {
      setErrors(errs);
      return;
    }
    setErrors({});
    setStatus('sending');

    try {
      const res = await fetch(FORMSPREE_ENDPOINT, {
        method: 'POST',
        body: data,
        headers: { Accept: 'application/json' },
      });
      if (res.ok) {
        setStatus('success');
        form.reset();
      } else {
        setStatus('error');
      }
    } catch {
      setStatus('error');
    }
  };

  if (status === 'success') {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.96 }}
        animate={{ opacity: 1, scale: 1 }}
        className="text-center py-16 px-8 rounded-3xl border border-white/08 card-glass"
      >
        <div className="w-14 h-14 rounded-full bg-green-500/15 border border-green-500/30 flex items-center justify-center mx-auto mb-5">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" className="text-green-400">
            <path d="M20 6L9 17l-5-5" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </div>
        <h3 className="text-xl font-black text-white mb-2">Mensaje enviado</h3>
        <p className="text-sm text-white/75">Gracias por contactarnos. Te responderemos a la brevedad.</p>
        <button onClick={() => setStatus('idle')} className="mt-6 btn-ghost text-xs">
          Enviar otro mensaje
        </button>
      </motion.div>
    );
  }

  return (
    <form onSubmit={handleSubmit} noValidate className="space-y-5">
      {status === 'error' && (
        <div className="px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/25 text-sm text-red-300">
          Hubo un error al enviar. Por favor inténtalo nuevamente.
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
        {/* Name */}
        <div>
          <label htmlFor="name" className="text-xs font-bold uppercase tracking-widest text-white/65 block mb-2">
            Nombre *
          </label>
          <input
            id="name"
            name="name"
            type="text"
            placeholder="Tu nombre"
            className={inputClass}
            aria-describedby={errors.name ? 'name-error' : undefined}
          />
          {errors.name && (
            <p id="name-error" className="mt-1.5 text-xs text-red-400">{errors.name}</p>
          )}
        </div>

        {/* Email */}
        <div>
          <label htmlFor="email" className="text-xs font-bold uppercase tracking-widest text-white/65 block mb-2">
            Correo *
          </label>
          <input
            id="email"
            name="email"
            type="email"
            placeholder="tu@correo.cl"
            className={inputClass}
            aria-describedby={errors.email ? 'email-error' : undefined}
          />
          {errors.email && (
            <p id="email-error" className="mt-1.5 text-xs text-red-400">{errors.email}</p>
          )}
        </div>
      </div>

      {/* Message */}
      <div>
        <label htmlFor="message" className="text-xs font-bold uppercase tracking-widest text-white/65 block mb-2">
          Mensaje *
        </label>
        <textarea
          id="message"
          name="message"
          rows={5}
          placeholder="¿En qué podemos ayudarte?"
          className={inputClass + ' resize-none'}
          aria-describedby={errors.message ? 'message-error' : undefined}
        />
        {errors.message && (
          <p id="message-error" className="mt-1.5 text-xs text-red-400">{errors.message}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={status === 'sending'}
        className="btn-primary w-full justify-center disabled:opacity-60 disabled:cursor-not-allowed"
      >
        {status === 'sending' ? (
          <>
            <motion.div
              className="w-4 h-4 rounded-full border-2 border-white/30 border-t-white"
              animate={{ rotate: 360 }}
              transition={{ duration: 0.8, repeat: Infinity, ease: 'linear' }}
            />
            Enviando…
          </>
        ) : (
          <>
            Enviar mensaje
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M22 2L11 13M22 2L15 22l-4-9-9-4 20-7z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </>
        )}
      </button>

      <p className="text-xs text-white/30 text-center">
        También puedes escribirnos a{' '}
        <a href="mailto:gestion@teatrooculto.cl" className="text-white/50 hover:text-white/80 transition-colors underline underline-offset-2">
          gestion@teatrooculto.cl
        </a>
      </p>
    </form>
  );
}
