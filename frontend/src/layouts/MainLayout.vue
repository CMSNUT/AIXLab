<!-- 主布局组件 -->
 <template>
  <div class="main-layout">
    <el-container style="height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
      <el-header class="header">
        <div class="header-content">
          <div class="brand">
            <el-icon size="32"><DataAnalysis /></el-icon>
            <div>
              <h1 class="title">AIXLab 绘图平台</h1>
              <p class="subtitle">Python & R 在线绘图演示</p>
            </div>
          </div>
          <div class="spacer"></div>
          <ServiceStatus />
        </div>
      </el-header>
      
      <el-main class="main-content">
        <slot />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { DataAnalysis } from '@element-plus/icons-vue'
import ServiceStatus from '@/components/layout/ServiceStatus.vue'
</script>

<style scoped>
.main-layout {
  width: 100%;
  height: 100vh;
}

.header {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  backdrop-filter: blur(10px);
}

.header-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.brand {
  display: flex;
  align-items: center;
}

.brand .el-icon {
  margin-right: 15px;
}

.title {
  margin: 0;
  font-size: 24px;
}

.subtitle {
  margin: 5px 0 0 0;
  font-size: 14px;
  opacity: 0.8;
}

.spacer {
  flex-grow: 1;
}

.main-content {
  padding: 20px;
  overflow: auto;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}
</style>