/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        celestial: {
          void: "#0B0F19",
          slate: "#0F172A",
          amber: "#F59E0B",
          cyan: "#38BDF8",
          violet: "#8B5CF6",
        },
      },
    },
  },
  plugins: [],
};
