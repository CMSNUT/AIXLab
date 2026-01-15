<template>
  <div class="plot-demo">
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card class="result-card" shadow="always">
          <template #header>
            <div class="card-header">
              <el-icon><Picture /></el-icon>
              <span>绘图结果</span>
            </div>
          </template>
          
          <div v-if="loading" class="loading-container">
            <el-icon class="loading-icon"><Loading /></el-icon>
            <p>正在生成图表...</p>
            <p class="loading-desc">使用 {{ currentLanguage === 'python' ? 'Python Matplotlib' : 'R ggplot2' }} 生成 {{ currentPlotType }} 图表</p>
          </div>
          
          <div v-else-if="plotResult && plotResult.success" class="plot-result">
            <div class="plot-image-container">
              <img :src="`data:image/png;base64,${plotResult.image}`" alt="绘图结果" />
            </div>
            
            <div class="plot-info">
              <el-tag :type="plotResult.language === 'python' ? 'primary' : 'success'" size="large">
                <el-icon>
                  <component :is="plotResult.language === 'python' ? 'Platform' : 'Monitor'" />
                </el-icon>
                {{ plotResult.language.toUpperCase() }}
              </el-tag>
              <el-tag type="info" size="large">
                <el-icon><Histogram /></el-icon>
                {{ plotTypeNames[plotResult.plot_type] || plotResult.plot_type }}
              </el-tag>
              <el-tag size="large">
                <el-icon><Crop /></el-icon>
                {{ plotResult.image_info.width }} × {{ plotResult.image_info.height }}
              </el-tag>
              <el-tag v-if="plotResult.data_info" size="large">
                <el-icon><DataLine /></el-icon>
                {{ plotResult.data_info.rows }}行 × {{ plotResult.data_info.columns }}列
              </el-tag>
            </div>
          </div>
          
          <div v-else-if="plotResult && !plotResult.success" class="error-container">
            <el-alert
              title="绘图失败"
              type="error"
              :description="plotResult.error || '未知错误'"
              show-icon
              :closable="false"
            />
            <div style="margin-top: 20px; text-align: center;">
              <el-button type="primary" @click="runTest(currentLanguage)">
                运行测试图表
              </el-button>
            </div>
          </div>
          
          <div v-else class="empty-result">
            <el-empty description="请选择语言和绘图类型，然后点击生成图表" />
            <div style="text-align: center; margin-top: 20px;">
              <el-button type="success" @click="generatePlot" :disabled="!currentLanguage">
                快速示例
              </el-button>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="control-card" shadow="always">
          <template #header>
            <div class="card-header">
              <el-icon><Operation /></el-icon>
              <span>控制面板</span>
            </div>
          </template>
          
          <div class="control-group">
            <h3><el-icon><Monitor /></el-icon> 选择语言</h3>
            <div class="language-buttons">
              <el-button 
                :type="currentLanguage === 'python' ? 'primary' : ''" 
                @click="selectLanguage('python')"
                size="large"
                class="language-btn"
              >
                <el-icon><Platform /></el-icon>
                Python
              </el-button>
              <el-button 
                :type="currentLanguage === 'r' ? 'success' : ''" 
                @click="selectLanguage('r')"
                size="large"
                class="language-btn"
              >
                <el-icon><Monitor /></el-icon>
                R
              </el-button>
            </div>
          </div>
          
          <div class="control-group">
            <h3><el-icon><Histogram /></el-icon> 绘图类型</h3>
            <div class="plot-type-buttons">
              <el-button 
                v-for="type in plotTypes" 
                :key="type.value"
                :type="currentPlotType === type.value ? 'primary' : ''"
                @click="selectPlotType(type.value)"
                class="plot-type-btn"
              >
                <el-icon>
                  <component :is="type.icon" />
                </el-icon>
                {{ type.label }}
              </el-button>
            </div>
          </div>
          
          <div class="control-group">
            <h3><el-icon><VideoPlay /></el-icon> 操作</h3>
            <el-button 
              type="primary" 
              @click="generatePlot" 
              :loading="loading"
              :disabled="!currentLanguage"
              size="large"
              class="action-btn"
            >
              <el-icon><VideoPlay /></el-icon>
              生成图表
            </el-button>
            
            <div style="margin-top: 15px; display: flex; gap: 10px;">
              <el-button 
                type="info" 
                @click="runTest('python')"
                :loading="testingPython"
                class="test-btn"
              >
                <el-icon><Platform /></el-icon>
                测试Python
              </el-button>
              <el-button 
                type="warning" 
                @click="runTest('r')"
                :loading="testingR"
                class="test-btn"
              >
                <el-icon><Monitor /></el-icon>
                测试R
              </el-button>
            </div>
          </div>
          
          <div class="control-group" v-if="plotResult && plotResult.success">
            <h3><el-icon><InfoFilled /></el-icon> 图表信息</h3>
            <div class="info-box">
              <div class="info-item">
                <span class="info-label">语言:</span>
                <span class="info-value">{{ plotResult.language === 'python' ? 'Python (Matplotlib)' : 'R (ggplot2)' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">类型:</span>
                <span class="info-value">{{ plotTypeNames[plotResult.plot_type] || plotResult.plot_type }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">状态:</span>
                <el-tag type="success" size="small">成功</el-tag>
              </div>
              <div class="info-item" v-if="plotResult.data_info">
                <span class="info-label">数据:</span>
                <span class="info-value">{{ plotResult.data_info.rows }}行 × {{ plotResult.data_info.columns }}列</span>
              </div>
              <div class="info-item">
                <span class="info-label">图像:</span>
                <span class="info-value">{{ plotResult.image_info.width }} × {{ plotResult.image_info.height }} {{ plotResult.image_info.format }}</span>
              </div>
            </div>
          </div>
        </el-card>
        
        <el-card class="description-card" shadow="always" style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <el-icon><HelpFilled /></el-icon>
              <span>使用说明</span>
            </div>
          </template>
          
          <div class="instructions">
            <h3>快速开始:</h3>
            <ol>
              <li>选择编程语言（Python或R）</li>
              <li>选择绘图类型（散点图、折线图等）</li>
              <li>点击"生成图表"按钮</li>
              <li>查看右侧生成的图表</li>
            </ol>
            
            <h3>服务说明:</h3>
            <ul>
              <li><strong>主后端服务</strong>: 端口 8000，协调所有服务</li>
              <li><strong>Python分析服务</strong>: 端口 8001，使用Matplotlib绘图</li>
              <li><strong>R分析服务</strong>: 端口 8002，使用ggplot2绘图</li>
            </ul>
            
            <h3>数据源:</h3>
            <p>使用鸢尾花(Iris)数据集进行演示，包含150个样本，5个特征。</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const currentLanguage = ref('python')
const currentPlotType = ref('scatter')
const loading = ref(false)
const testingPython = ref(false)
const testingR = ref(false)
const plotResult = ref(null)

const plotTypes = reactive([
  { value: 'scatter', label: '散点图', icon: 'ScatterPlot' },
  { value: 'line', label: '折线图', icon: 'TrendCharts' },
  { value: 'histogram', label: '直方图', icon: 'Histogram' },
  { value: 'boxplot', label: '箱线图', icon: 'BoxPlot' }
])

const plotTypeNames = {
  scatter: '散点图',
  line: '折线图',
  histogram: '直方图',
  boxplot: '箱线图'
}

// 选择语言
const selectLanguage = (language) => {
  currentLanguage.value = language
  plotResult.value = null
}

// 选择绘图类型
const selectPlotType = (type) => {
  currentPlotType.value = type
}

// 生成图表
const generatePlot = async () => {
  if (!currentLanguage.value) {
    ElMessage.warning('请先选择编程语言')
    return
  }
  
  loading.value = true
  plotResult.value = null
  
  try {
    const response = await axios.post('/api/plot', {
      language: currentLanguage.value,
      plot_type: currentPlotType.value
    })
    
    plotResult.value = response.data
    
    if (response.data.success) {
      ElMessage.success(`${currentLanguage.value.toUpperCase()} ${plotTypeNames[currentPlotType.value]} 生成成功！`)
    } else {
      ElMessage.error('图表生成失败: ' + (response.data.error || '未知错误'))
    }
    
  } catch (error) {
    ElMessage.error('请求失败: ' + error.message)
    plotResult.value = {
      success: false,
      error: error.message
    }
  } finally {
    loading.value = false
  }
}

// 测试服务
const runTest = async (language) => {
  if (language === 'python') {
    testingPython.value = true
  } else {
    testingR.value = true
  }
  
  plotResult.value = null
  
  try {
    const endpoint = language === 'python' ? '/api/test/python-plot' : '/api/test/r-plot'
    const response = await axios.get(endpoint)
    
    plotResult.value = response.data
    currentLanguage.value = language
    
    if (response.data.success) {
      ElMessage.success(`${language.toUpperCase()} 服务测试成功！`)
    } else {
      ElMessage.error(`${language.toUpperCase()} 测试失败: ` + (response.data.error || '未知错误'))
    }
    
  } catch (error) {
    ElMessage.error(`${language} 测试请求失败: ` + error.message)
  } finally {
    if (language === 'python') {
      testingPython.value = false
    } else {
      testingR.value = false
    }
  }
}
</script>

<style scoped>
.plot-demo {
  height: 100%;
}

.card-header {
  display: flex;
  align-items: center;
  font-weight: bold;
  font-size: 18px;
}

.card-header .el-icon {
  margin-right: 8px;
}

.result-card {
  height: 100%;
  min-height: 600px;
}

.control-card, .description-card {
  height: auto;
}

.control-group {
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.control-group:last-child {
  border-bottom: none;
}

.control-group h3 {
  margin-bottom: 15px;
  color: #333;
  font-size: 16px;
  display: flex;
  align-items: center;
}

.control-group h3 .el-icon {
  margin-right: 8px;
}

.language-buttons {
  display: flex;
  gap: 10px;
}

.language-btn {
  flex: 1;
  height: 50px;
  font-size: 16px;
}

.plot-type-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.plot-type-btn {
  height: 45px;
}

.action-btn {
  width: 100%;
  height: 50px;
  font-size: 16px;
}

.test-btn {
  flex: 1;
}

.info-box {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e8e8e8;
}

.info-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.info-label {
  font-weight: bold;
  color: #666;
}

.info-value {
  color: #333;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 500px;
  text-align: center;
}

.loading-icon {
  font-size: 60px;
  color: #409eff;
  margin-bottom: 20px;
  animation: rotating 2s linear infinite;
}

.loading-desc {
  color: #666;
  margin-top: 10px;
  font-size: 14px;
}

@keyframes rotating {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.plot-result {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.plot-image-container {
  margin-bottom: 20px;
  text-align: center;
}

.plot-image-container img {
  max-width: 100%;
  max-height: 450px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.plot-image-container img:hover {
  transform: scale(1.01);
}

.plot-info {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin-top: 15px;
}

.error-container {
  padding: 20px;
  text-align: center;
}

.empty-result {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 500px;
}

.instructions {
  font-size: 14px;
  line-height: 1.6;
  color: #555;
}

.instructions h3 {
  margin: 15px 0 10px 0;
  color: #333;
  font-size: 15px;
}

.instructions ol, .instructions ul {
  padding-left: 20px;
  margin: 10px 0;
}

.instructions li {
  margin: 5px 0;
}
</style>