import { createPinia } from 'pinia'
import { markRaw } from 'vue'
import type { Router } from 'vue-router'

export default createPinia()

// 在 main.ts 中注入 router
declare module 'pinia' {
  export interface PiniaCustomProperties {
    router: Router
  }
}