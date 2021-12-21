import { defineNuxtConfig } from 'nuxt3'

export default defineNuxtConfig({
  buildModules: [
    'nuxt-windicss',
  ],
  build: {
    transpile: [
      /echarts/
    ]
  }
})
