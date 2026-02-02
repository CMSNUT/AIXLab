<template>
  <div class="module-container">
    <!-- 动态加载的模块 -->
    <component :is="currentModule" v-if="currentModule" />
    
    <!-- 加载状态 -->
    <div v-else-if="loading" class="loading-state">
      加载中...
    </div>
    
    <!-- 错误状态 -->
    <div v-else-if="error" class="error-state">
      模块加载失败
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, defineAsyncComponent } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const currentModule = ref<any>(null)
const loading = ref(false)
const error = ref(false)

// 动态加载模块
const loadModule = async () => {
  const category = route.params.category as string
  const code = route.params.code as string
  
  if (!category || !code) {
    error.value = true
    return
  }
  
  try {
    loading.value = true
    error.value = false
    
    // 动态导入对应模块
    const module = await import(
      /* webpackChunkName: "plot-module-[request]" */
      `./${category}/${code}/index.vue`
    )
    
    currentModule.value = defineAsyncComponent(() => Promise.resolve(module.default || module))
    
  } catch (err) {
    console.error('模块加载失败:', err)
    error.value = true
  } finally {
    loading.value = false
  }
}

// 监听路由参数变化
watch(
  () => [route.params.category, route.params.code],
  () => {
    loadModule()
  }
)

// 初始化加载
onMounted(() => {
  loadModule()
})
</script>

<style scoped>
.module-container {
  min-height: 400px;
}
.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
  font-size: 18px;
  color: #666;
}
.error-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
  font-size: 18px;
  color: #f56c6c;
}
</style>