import path from 'path';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/client',
  resolve: {
    alias: {
      '~app': path.resolve('src/app'),
      '~pages': path.resolve('src/pages'),
      '~widgets': path.resolve('src/widgets'),
      '~entities': path.resolve('src/entities'),
      '~features': path.resolve('src/features'),
      '~shared': path.resolve('src/shared'),
      '~root': path.resolve('src/app/root'),
      '~layout': path.resolve('src/app/layout'),
      '~lazyPages': path.resolve('src/app/lazyPages.tsx'),
      '~icons': path.resolve('src/shared/ui/Icon/icons/'),
    },
  },
});
