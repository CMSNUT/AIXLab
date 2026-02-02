<template>
  <div>
    <!-- 根据 code 动态显示不同组件 -->
    <component :is="currentModule" />
  </div>
</template>

<script setup lang="ts">
import { computed, defineAsyncComponent } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const code = computed(() => route.params.code as string)

// 动态导入组件
const currentModule = computed(() => {
  return defineAsyncComponent(() => 
    import(`./${code.value}/index.vue`).catch(() => 
      import("@/views/error/404.vue")
    )
  )
})
</script>