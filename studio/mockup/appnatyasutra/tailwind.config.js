/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ["./index.html", "./components/**/*.html", "./sections/**/*.html", "./layouts/**/*.html", "./*.html", "./src/**/*.html"],
  theme: {
    extend: {
      colors: {
        brand: {
          pink: {
            DEFAULT: '#C2185B',
            light: '#E91E63',
            dark: '#880E4F',
            soft: '#FCE4EC',
          },
          purple: {
            DEFAULT: '#2D0B2A',
            light: '#4A148C',
            dark: '#1A0518',
            bg: '#0A0A0A',
          },
          gold: {
            DEFAULT: '#F59E0B',
            light: '#F1C40F',
            dark: '#B8860B',
          },
          cream: '#FDFBF7',
        },
        neutral: {
          950: '#0A0A0A',
        }
      },
      fontFamily: {
        serif: ['"Inter"', 'sans-serif'],
        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
      },
      fontWeight: {
        black: '600',
      },
      scale: {
        '102': '1.02',
      },
      backgroundImage: {
        'hero-gradient': 'linear-gradient(to bottom, rgba(45, 11, 42, 0.7), rgba(45, 11, 42, 0.9))',
      }
    },
  },
  plugins: [],
}
