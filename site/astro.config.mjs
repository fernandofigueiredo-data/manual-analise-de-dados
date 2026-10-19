// @ts-check
import { defineConfig } from 'astro/config';

// URL pública: defina SITE_URL no deploy (ex.: https://manual-analise-de-dados.vercel.app)
export default defineConfig({
  site: process.env.SITE_URL || undefined,
  trailingSlash: 'always',
  build: { format: 'directory', inlineStylesheets: 'always' },
  compressHTML: true,
  prefetch: { prefetchAll: false, defaultStrategy: 'hover' },
  devToolbar: { enabled: false },
});
