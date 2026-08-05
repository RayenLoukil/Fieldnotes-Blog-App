/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        steel: {
          50: '#f4f7f9',
          100: '#e9eff3',
          500: '#527c9f', // Corey's classic brand color
          600: '#41637f',
          700: '#355067',
        },
        bg: {
          light: '#fafafa',
          dark: '#1a1a1a',
          cardLight: '#ffffff',
          cardDark: '#2d2d2d',
        }
      },
      fontFamily: {
        heading: ["Montserrat", "sans-serif"],
        body: ["Nunito", "sans-serif"],
      }
    },
  },
  plugins: [],
}