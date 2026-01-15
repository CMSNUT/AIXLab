<template>
  <div id="app">
    <el-container style="height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
      <el-header style="background: rgba(255, 255, 255, 0.1); color: white; backdrop-filter: blur(10px);">
        <div style="display: flex; align-items: center; height: 100%;">
          <el-icon size="32" style="margin-right: 15px;"><DataAnalysis /></el-icon>
          <div>
            <h1 style="margin: 0; font-size: 24px;">AIXLab 绘图平台</h1>
            <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.8;">Python & R 在线绘图演示</p>
          </div>
          <div style="flex-grow: 1;"></div>
          <div style="display: flex; gap: 10px;">
            <el-tag :type="mainStatus === 'healthy' ? 'success' : 'danger'">
              主服务: {{ mainStatus }}
            </el-tag>
            <el-tag :type="pythonStatus === 'healthy' ? 'success' : 'danger'">
              Python: {{ pythonStatus }}
            </el-tag>
            <el-tag :type="rStatus === 'healthy' ? 'success' : 'danger'">
              R: {{ rStatus }}
            </el-tag>
          </div>
        </div>
      </el-header>
      
      <el-main style="padding: 20px; overflow: auto;">
        <PlotDemo />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import PlotDemo from './components/PlotDemo.vue'

const mainStatus = ref('检查中...')
const pythonStatus = ref('检查中...')
const rStatus = ref('检查中...')

// 检查服务状态
const checkServices = async () => {
  try {
    // 检查主后端
    const response = await axios.get('/api/health')
    const status = response.data
    
    mainStatus.value = status.main_backend === 'healthy' ? '正常' : '异常'
    pythonStatus.value = status.python_service === 'healthy' ? '正常' : 
                        status.python_service === 'unreachable' ? '未启动' : '异常'
    rStatus.value = status.r_service === 'healthy' ? '正常' : 
                   status.r_service === 'unreachable' ? '未启动' : '异常'
  } catch (error) {
    mainStatus.value = '异常'
    pythonStatus.value = '未知'
    rStatus.value = '未知'
  }
}

onMounted(() => {
  checkServices()
  // 每30秒检查一次服务状态
  setInterval(checkServices, 30000)
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: #f5f7fa;
}

#app {
  width: 100%;
  height: 100vh;
}

.el-main {
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}
</style>