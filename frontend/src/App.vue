<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useHealthStore } from '@/stores/health'

const healthStore = useHealthStore()

onMounted(() => {
  // 启动自动健康检查
  healthStore.startAutoCheck()
})

onUnmounted(() => {
  // 清理自动检查定时器
  healthStore.stopAutoCheck()
})
</script>

<style>
@import '@/assets/css/base.css';
@import '@/assets/css/element.css';
</style>