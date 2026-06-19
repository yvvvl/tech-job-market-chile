import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { tanstackStart } from "@tanstack/react-start/plugin/vite";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig(async ({ mode }) => {
  const plugins = [
    tsconfigPaths(),
    tailwindcss(),
    tanstackStart({ server: { entry: "server" } }),
    react(),
  ];

  if (mode === "demo") {
    const { cloudflare } = await import("@cloudflare/vite-plugin");
    plugins.unshift(cloudflare());
  }

  return {
    plugins,
  };
});
