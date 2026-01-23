<template>
  <div class="app-container">
    <h1>用户列表</h1>

    <div class="content">
      <!-- 页面内容 -->
      <el-table :data="userList" stripe>
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="status" label="状态" />
      </el-table>

    </div>

  </div>

</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义页面name, 用于keep-alive缓存
defineOptions({
  name: 'TestUser'
})

const userList = ref([
  { username: 'admin', email: 'admin@example.com', status: '启用' }
])
</script>

<style lang="scss" scoped>
.app-container {
  padding: 20px;
}

.content {
  margin-top: 20px;
}
</style>