import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import cesium from "vite-plugin-cesium"; // <-- הוספה שלנו

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    cesium(), // <-- הפעלת הפלאגין
  ],
});
