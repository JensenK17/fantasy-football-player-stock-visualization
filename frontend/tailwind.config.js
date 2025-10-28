/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        success: '#10B981',      // Green for over-performance
        danger: '#EF4444',       // Red for under-performance
        primary: '#3B82F6',      // Blue for primary actions
      },
    },
  },
  plugins: [],
}

