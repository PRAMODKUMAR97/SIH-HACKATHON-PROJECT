/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        command: {
          bg: '#0b0f19',
          card: '#111827',
          hover: '#1f2937',
          border: '#1e293b',
          accent: '#06b6d4',
          accentHover: '#0891b2',
          emerald: '#10b981',
          danger: '#ef4444',
          warning: '#f59e0b',
        }
      }
    },
  },
  plugins: [],
}
