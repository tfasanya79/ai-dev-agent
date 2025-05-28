import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/setupTests.ts',
    // you can include test match patterns if needed:
    include: ['src/**/*.{test,spec}.{js,ts,jsx,tsx}'],
  },
})
