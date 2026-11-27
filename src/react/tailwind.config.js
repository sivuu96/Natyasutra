/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        // Placeholder palette. Replace with the brand colours from the design system.
        brand: {
          50: "#fdf6ee",
          500: "#b45309",
          700: "#78350f",
        },
      },
      fontFamily: {
        display: ["Georgia", "serif"],
      },
    },
  },
  plugins: [],
};
