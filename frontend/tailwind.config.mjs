/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        crimson: {
          DEFAULT: '#e04242',
          hover: '#ff5a5a',
          dim: 'rgba(224,66,66,0.15)',
        },
        gold: {
          DEFAULT: '#d7b36a',
          soft: 'rgba(215,179,106,0.20)',
          muted: 'rgba(215,179,106,0.08)',
        },
        surface: {
          DEFAULT: 'rgba(255,255,255,0.03)',
          hover: 'rgba(255,255,255,0.06)',
        },
        border: {
          DEFAULT: 'rgba(255,255,255,0.08)',
          hover: 'rgba(215,179,106,0.24)',
        },
      },
      fontFamily: {
        sans: ['Montserrat', 'system-ui', '-apple-system', 'sans-serif'],
      },
      fontSize: {
        'display-xl': 'clamp(5rem, 14vw, 13rem)',
        'display-lg': 'clamp(3.5rem, 9vw, 8rem)',
        'display-md': 'clamp(2.5rem, 5vw, 4.5rem)',
      },
      letterSpacing: {
        widest: '0.18em',
        theater: '0.28em',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'grain': "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E\")",
      },
      keyframes: {
        'ken-burns': {
          from: { transform: 'scale(1.0)' },
          to: { transform: 'scale(1.08)' },
        },
        'bar-sheen': {
          '0%': { backgroundPosition: '0% 50%', opacity: '0.9' },
          '50%': { backgroundPosition: '100% 50%', opacity: '1' },
          '100%': { backgroundPosition: '0% 50%', opacity: '0.9' },
        },
        'spotlight-drift': {
          '0%': { transform: 'translate3d(0,0,0)' },
          '50%': { transform: 'translate3d(-1.5%,1.2%,0)' },
          '100%': { transform: 'translate3d(1.2%,-1%,0)' },
        },
      },
      animation: {
        'ken-burns': 'ken-burns 10s ease-out both',
        'bar-sheen': 'bar-sheen 3.2s ease-in-out infinite',
        'spotlight-drift': 'spotlight-drift 18s ease-in-out infinite alternate',
      },
      borderRadius: {
        '4xl': '2rem',
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
};
