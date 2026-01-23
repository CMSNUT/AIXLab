// 状态管理 Pinia 主文件
/**
 * Pinia Store 管理入口文件
 * 提供统一的状态管理导出和工具函数
 */

import { createPinia } from 'pinia'

// 创建 Pinia 实例
const pinia = createPinia()

// Pinia 插件示例(如果需要)
pinia.use(({ store }) => {
  // 添加自定义方法到所有 store
  store.$reset = () => {
    // 如果 store 有 reset 方法, 则调用
    if (typeof store.reset === 'function') {
      store.reset()
    } else {
      // 否则重置状态到初始值
      const initialState = store.$state
      Object.keys(initialState).forEach(key => {
        store[key] = initialState[key]
      })
    }
  }

  // 添加持久化示例
  store.$persist = (key = null) => {
    const storageKey = key || store.$id
    
    // 从 localStorage 加载
    const savedState = localStorage.getItem(storageKey)
    if (savedState) {
      try {
        const parsed = JSON.parse(savedState)
        Object.assign(store.$state, parsed)
      } catch (e) {
        console.warn(`Failed to load state for ${storageKey}:`, e)
      }
    }

    // 监听状态变化并保存
    store.$subscribe((mutation, state) => {
      localStorage.setItem(storageKey, JSON.stringify(state))
    })
  }
})

// 导出所有 store
export * from './plot'
export * from './health'

// 导出 Pinia 实例
export { pinia }

// 工具函数
export const createStoreHelpers = () => {
  return {
    /**
     * 重置所有 store
     * @param {Object} stores - store 对象集合
     */
    resetAllStores(stores) {
      Object.values(stores).forEach(store => {
        if (store && store.$reset) {
          store.$reset()
        }
      })
    },

    /**
     * 持久化所有 store
     * @param {Object} stores - store 对象集合
     */
    persistAllStores(stores) {
      Object.entries(stores).forEach(([key, store]) => {
        if (store && store.$persist) {
          store.$persist(key)
        }
      })
    },

    /**
     * 获取 store 状态快照
     * @param {Object} store - store 实例
     * @returns {Object} 状态快照
     */
    getStoreSnapshot(store) {
      return JSON.parse(JSON.stringify(store.$state))
    },

    /**
     * 恢复 store 状态
     * @param {Object} store - store 实例
     * @param {Object} snapshot - 状态快照
     */
    restoreStore(store, snapshot) {
      if (store && snapshot) {
        Object.assign(store.$state, snapshot)
      }
    }
  }
}

// 状态存储类型定义(用于 TypeScript 或文档)
export const StoreTypes = {
  PLOT: 'plot',
  HEALTH: 'health'
}

// 默认导出 Pinia 实例
export default pinia