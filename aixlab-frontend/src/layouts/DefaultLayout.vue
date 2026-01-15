<template>
  <div class="default-layout">
    <el-container class="layout-container">
      <!-- 侧边栏 -->
      <el-aside width="240px" class="layout-sidebar">
        <div class="sidebar-header">
          <h2 class="logo">
            <el-icon><Menu /></el-icon>
            AIXLab
          </h2>
        </div>
        
        <el-menu
          :default-active="$route.path"
          router
          class="sidebar-menu"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
        >
          <el-menu-item index="/">
            <el-icon><Odometer /></el-icon>
            <span>仪表盘</span>
          </el-menu-item>
          
          <el-sub-menu index="data">
            <template #title>
              <el-icon><DataAnalysis /></el-icon>
              <span>数据管理</span>
            </template>
            <el-menu-item index="/datasets">我的数据集</el-menu-item>
            <el-menu-item index="/datasets/upload">上传数据</el-menu-item>
          </el-sub-menu>
          
          <el-sub-menu index="analysis">
            <template #title>
              <el-icon><Cpu /></el-icon>
              <span>数据分析</span>
            </template>
            <el-menu-item index="/analysis">分析中心</el-menu-item>
            <el-menu-item index="/analysis/r">R 分析</el-menu-item>
            <el-menu-item index="/analysis/python">Python 分析</el-menu-item>
            <el-menu-item index="/analysis/tasks">任务列表</el-menu-item>
          </el-sub-menu>
          
          <el-menu-item index="/public-data">
            <el-icon><Share /></el-icon>
            <span>公共数据</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <!-- 主内容区 -->
      <el-container class="main-container">
        <!-- 顶部导航 -->
        <el-header class="layout-header">
          <div class="header-left">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item v-for="item in breadcrumbs" :key="item.path">
                {{ item.meta.title }}
              </el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          
          <div class="header-right">
            <el-dropdown @command="handleCommand">
              <span class="user-info">
                <el-avatar :size="32" :src="authStore.user?.avatar">
                  {{ authStore.user?.username?.charAt(0) }}
                </el-avatar>
                <span class="username">{{ authStore.user?.username }}</span>
                <el-icon><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">
                    <el-icon><User /></el-icon>
                    个人中心
                  </el-dropdown-item>
                  <el-dropdown-item command="settings">
                    <el-icon><Setting /></el-icon>
                    系统设置
                  </el-dropdown-item>
                  <el-dropdown-item divided command="logout">
                    <el-icon><SwitchButton /></el-icon>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        
        <!-- 主要内容 -->
        <el-main class="layout-main">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  Menu,
  Odometer,
  DataAnalysis,
  Cpu,
  Share,
  ArrowDown,
  User,
  Setting,
  SwitchButton
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const breadcrumbs = computed(() => {
  const matched = route.matched.filter(item => item.meta.title)
  return matched.map(item => ({
    path: item.path,
    meta: item.meta
  }))
})

const handleCommand = (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/settings')
      break
    case 'settings':
      router.push('/settings')
      break
    case 'logout':
      authStore.logout()
      router.push('/login')
      break
  }
}
</script>

<style lang="scss" scoped>
.default-layout {
  height: 100vh;
  
  .layout-container {
    height: 100%;
  }
  
  .layout-sidebar {
    background-color: #304156;
    transition: width 0.3s;
    
    .sidebar-header {
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      
      .logo {
        color: #fff;
        font-size: 18px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 0;
      }
    }
    
    .sidebar-menu {
      border-right: none;
      height: calc(100vh - 60px);
    }
  }
  
  .main-container {
    display: flex;
    flex-direction: column;
  }
  
  .layout-header {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    border-bottom: 1px solid var(--border-color);
    background: #fff;
    
    .header-left {
      .el-breadcrumb {
        font-size: 14px;
      }
    }
    
    .header-right {
      .user-info {
        display: flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
        
        .username {
          font-size: 14px;
          color: var(--text-color);
        }
      }
    }
  }
  
  .layout-main {
    padding: 20px;
    background: var(--bg-color);
    overflow-y: auto;
    
    :deep(.el-card) {
      margin-bottom: 20px;
      
      &:last-child {
        margin-bottom: 0;
      }
    }
  }
}
</style>