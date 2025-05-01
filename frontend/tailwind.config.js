
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#42a5f5',
          DEFAULT: '#1976d2',
          dark: '#1565c0',
        },
        secondary: {
          light: '#ffb74d',
          DEFAULT: '#ff9800',
          dark: '#f57c00',
        },
      },
      boxShadow: {
        card: '0 4px 12px 0 rgba(0,0,0,0.05)',
      },
    },
  },
  plugins: [],
}