/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        instagram: {
          purple: "#833AB4",
          pink: "#FD1D1D",
          orange: "#F56040",
          yellow: "#FCAF45",
        }
      }
    },
  },
  plugins: [],
}
