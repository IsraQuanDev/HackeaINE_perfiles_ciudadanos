import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        ine: {
          dark: "#5A1236",
          primary: "#8B1D52",
          accent: "#B8296B",
          neutral: "#1E293B",
          light: "#F8FAFC",
        },
      },
    },
  },
  plugins: [],
};
export default config;
