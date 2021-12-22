import { defineNuxtConfig } from 'nuxt3'

export default defineNuxtConfig({
  build: {
    transpile: [
      /echarts/
    ],
    postcss: {
        postcssOptions: {
          plugins: {
            tailwindcss: {},
            autoprefixer: {},
          }
        }
      },
  }
})
