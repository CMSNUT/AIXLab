<template>
  <div class="paired-plot-app">
    <!-- 顶部标题与文档 -->
    <el-page-header title="返回" @back="goBack">
      <template #content>
        <div class="page-title">
          <h1>基础绘图 - 类别比较 - 配对图</h1>
          <div class="doc-links">
            <el-link type="primary" :underline="false" href="#" target="_blank" :icon="Document">GITHUB文档</el-link>
            <el-divider direction="vertical" />
            <el-link type="primary" :underline="false" href="#" target="_blank" :icon="CollectionTag">更新情况</el-link>
            <el-divider direction="vertical" />
            <el-link type="primary" :underline="false" href="#" target="_blank" :icon="VideoPlay">教程文档</el-link>
          </div>
        </div>
      </template>
    </el-page-header>

    <el-main>
      <el-row :gutter="20">
        <!-- 左侧：数据与参数配置区 -->
        <el-col :span="8">
          <el-card class="config-card">
            <template #header>
              <div class="card-header">
                <span>数据参数</span>
                <div>
                  <el-button :icon="RefreshRight" @click="resetAllParams">重置参数</el-button>
                </div>
              </div>
            </template>

            <!-- 数据上传区域 -->
            <div class="upload-area">
              <div class="param-section-title">
                <el-icon><Upload /></el-icon> 上传文件
              </div>
              <!-- 核心交互1：点击文本框弹出上传对话框 -->
              <el-input 
                v-model="uploadedFileName" 
                placeholder="请上传数据文件" 
                readonly 
                @click="handleUploadClick"
                class="upload-input-trigger"
              >
                <template #append>
                  <el-button :icon="Upload" @click="handleUploadClick" />
                </template>
              </el-input>
              <div class="upload-tips">
                <el-link type="info" :underline="false" @click="downloadExampleData">
                  <el-icon><Download /></el-icon> 下载示例数据
                </el-link>
                <span class="file-format">支持 .xlsx, .csv, .txt 格式数据（<4M）</span>
                <el-tag v-if="isDataValid" type="success" size="small">验证成功</el-tag>
              </div>
              <!-- 隐藏的文件上传输入框 -->
              <input 
                type="file" 
                ref="fileInputRef" 
                style="display: none;" 
                @change="handleFileChange"
                accept=".xlsx,.csv,.txt"
              />
            </div>

            <!-- 主要参数设置 -->
            <el-collapse v-model="activeCollapse" class="param-collapse">
              <el-collapse-item title="主要参数" name="main">
                <el-form :model="plotParams" label-width="100px">
                  <el-form-item label="统计分析">
                    <el-select v-model="plotParams.statMethod" placeholder="请选择统计方法">
                      <el-option label="配对样本T检验" value="paired_t" />
                      <el-option label="Wilcoxon符号秩检验" value="wilcoxon" />
                    </el-select>
                  </el-form-item>
                  <el-form-item label="间距设置">
                    <el-slider v-model="plotParams.spacing" :min="0" :max="2" :step="0.1" />
                  </el-form-item>
                  <el-form-item label="点">
                    <el-color-picker v-model="plotParams.pointColor" show-alpha />
                    <el-input-number v-model="plotParams.pointSize" :min="1" :max="10" controls-position="right" />
                  </el-form-item>
                  <el-form-item label="连线">
                    <el-switch v-model="plotParams.showLine" />
                    <el-color-picker v-model="plotParams.lineColor" show-alpha :disabled="!plotParams.showLine" />
                  </el-form-item>
                </el-form>
                <div class="param-actions">
                  <el-button type="primary" :icon="Finished" @click="saveParams">保存参数</el-button>
                  <el-button :icon="Refresh" @click="resetCurrentParams">重置参数</el-button>
                </div>
              </el-collapse-item>

              <el-collapse-item title="更多设置" name="more">
                <!-- 此处可扩展：箱、标题、图注、坐标轴、风格等设置 -->
                <div style="color: #909399; text-align: center; padding: 20px;">
                  更多图形参数设置区域
                </div>
              </el-collapse-item>
            </el-collapse>

            <!-- 核心交互3：点击确认开始分析 -->
            <div class="confirm-action">
              <el-button 
                type="primary" 
                :icon="Check" 
                size="large" 
                :loading="isPlotting"
                @click="generatePlot"
                :disabled="!isDataValid"
              >
                确认分析
              </el-button>
            </div>
          </el-card>
        </el-col>

        <!-- 右侧：结果展示区 -->
        <el-col :span="16">
          <!-- 核心交互4：分析完成后显示结果区 -->
          <div v-if="showResults">
            <!-- 结果标签页 -->
            <el-card class="results-card">
              <template #header>
                <div class="card-header">
                  <el-tabs v-model="activeResultTab" @tab-click="handleTabClick">
                    <el-tab-pane label="主要结果" name="main"></el-tab-pane>
                    <el-tab-pane label="补充结果" name="supplementary"></el-tab-pane>
                    <el-tab-pane label="方法学" name="methodology"></el-tab-pane>
                  </el-tabs>
                  <div class="result-actions">
                    <el-button :icon="Document" @click="saveResults">保存结果</el-button>
                    <el-button type="primary" :icon="Download" @click="downloadReport">下载整份报告</el-button>
                  </div>
                </div>
              </template>

              <!-- 主要结果：配对图 -->
              <div v-if="activeResultTab === 'main'">
                <div class="plot-description">
                  <h3>配对图</h3>
                  <p>配对图：将有配对关系的样本进行可视化的一种方式</p>
                  <el-alert type="info" :closable="false">
                    <div class="alert-content">
                      <div>当前所选的统计方法：{{ plotParams.statMethod === 'paired_t' ? '配对样本T检验' : 'Wilcoxon符号秩检验' }}</div>
                      <div class="alert-detail">
                        注意：统计要求每组样本都要满足3个样本以上，并且每组样本的方差不能为0，如果不满足条件，就不会进行统计分析
                      </div>
                    </div>
                  </el-alert>
                </div>
                <!-- 图表容器 -->
                <div ref="chartContainer" class="chart-container"></div>
                <div class="chart-downloads">
                  <el-link type="primary" :underline="false" :icon="Download">配对图.pdf</el-link>
                  <el-link type="primary" :underline="false" :icon="Download">配对图.tiff</el-link>
                </div>
              </div>

              <!-- 补充结果：统计表格 -->
              <div v-if="activeResultTab === 'supplementary'">
                <div class="supplementary-content">
                  <h3>统计描述</h3>
                  <p class="section-subtitle">各个组常见「统计描述指标」</p>
                  
                  <!-- 核心交互5：点击“补充结果”显示统计表格 -->
                  <el-table :data="statDescriptionData" border style="width: 100%; margin-bottom: 20px;">
                    <el-table-column prop="group" label="组别" width="100" />
                    <el-table-column prop="count" label="数目" width="80" />
                    <el-table-column prop="min" label="最小值" width="90" />
                    <el-table-column prop="max" label="最大值" width="90" />
                    <el-table-column prop="median" label="中位数(Median)" width="120" />
                    <el-table-column prop="iqr" label="四分位距(IQR)" width="110" />
                    <el-table-column prop="q1" label="下四分位" width="100" />
                    <el-table-column prop="q3" label="上四分位" width="100" />
                    <el-table-column prop="mean" label="均值(Mean)" width="100" />
                    <el-table-column prop="sd" label="标准差(SD)" width="100" />
                    <el-table-column prop="se" label="标准误(SE)" width="100" />
                  </el-table>
                  
                  <el-divider />
                  
                  <div class="file-download">
                    <el-link type="primary" :underline="false" :icon="Document">统计描述.xlsx</el-link>
                  </div>
                  
                  <el-divider />
                  
                  <h4>异常值分析</h4>
                  <div class="outlier-formula">
                    <p>离群值 = Q1(下四分位) - 1.5*IQR(四分位间距) 或者 Q3(上四分位) + 1.5*IQR(四分位间距)</p>
                    <p>异常值 = Q1(下四分位) - 3.0*IQR(四分位间距) 或者 Q3(上四分位) + 3.0*IQR(四分位间距)</p>
                  </div>
                  
                  <el-table :data="outlierData" border style="width: 300px; margin: 15px 0;">
                    <el-table-column prop="group" label="组别" width="100" />
                    <el-table-column prop="outliers" label="离群值" width="100" />
                    <el-table-column prop="extremes" label="异常值" width="100" />
                  </el-table>
                  
                  <el-alert type="info" :closable="false">
                    各组离群值和异常值如上所示，如数据确认非人为记录错误，可不进行处理。
                  </el-alert>
                  
                  <h4 style="margin-top: 25px;">正态性检验</h4>
                  <!-- 正态性检验内容占位 -->
                  <div style="padding: 30px; text-align: center; color: #909399;">
                    正态性检验结果将在此显示
                  </div>
                </div>
              </div>

              <!-- 方法学 -->
              <div v-if="activeResultTab === 'methodology'">
                <!-- 核心交互6：点击“方法学”显示内容 -->
                <div class="methodology-content">
                  <h3>分析方法学说明</h3>
                  
                  <el-alert type="info" title="编程语言选择" style="margin-bottom: 20px;">
                    <template #default>
                      <el-radio-group v-model="selectedLanguage" size="small">
                        <el-radio-button label="R">R 语言实现</el-radio-button>
                        <el-radio-button label="Python">Python 实现</el-radio-button>
                      </el-radio-group>
                    </template>
                  </el-alert>
                  
                  <div v-if="selectedLanguage === 'R'">
                    <h4>R 语言实现 - 配对样本T检验</h4>
                    <pre class="code-block"><code># 配对样本T检验 R代码示例
# 读取数据
data <- read.csv("paired_data.csv")

# 执行配对t检验
t_test_result <- t.test(data$Before, data$After, paired = TRUE)

# 输出结果
print(t_test_result)

# 计算效应量 (Cohen's d)
library(effsize)
cohen_d <- cohen.d(data$Before, data$After, paired = TRUE)
print(cohen_d)</code></pre>
                    
                    <h4>相关R包参考文献</h4>
                    <ul class="reference-list">
                      <li>R Core Team (2023). R: A language and environment for statistical computing. R Foundation for Statistical Computing, Vienna, Austria.</li>
                      <li>Wickham, H. (2016). ggplot2: Elegant Graphics for Data Analysis. Springer-Verlag New York.</li>
                    </ul>
                  </div>
                  
                  <div v-if="selectedLanguage === 'Python'">
                    <h4>Python 实现 - 配对样本T检验</h4>
                    <pre class="code-block"><code># 配对样本T检验 Python代码示例
import pandas as pd
import scipy.stats as stats
import numpy as np

# 读取数据
data = pd.read_csv('paired_data.csv')

# 执行配对t检验
t_stat, p_value = stats.ttest_rel(data['Before'], data['After'])

# 输出结果
print(f"t统计量: {t_stat:.4f}")
print(f"P值: {p_value:.4f}")

# 计算效应量 (Cohen's d)
mean_diff = np.mean(data['Before'] - data['After'])
std_diff = np.std(data['Before'] - data['After'], ddof=1)
cohen_d = mean_diff / std_diff if std_diff != 0 else 0
print(f"Cohen's d: {cohen_d:.4f}")</code></pre>
                    
                    <h4>相关Python包参考文献</h4>
                    <ul class="reference-list">
                      <li>Virtanen, P., et al. (2020). SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python. Nature Methods, 17, 261-272.</li>
                      <li>McKinney, W. (2010). Data Structures for Statistical Computing in Python. Proceedings of the 9th Python in Science Conference.</li>
                    </ul>
                  </div>
                  
                  <h4>统计方法参考文献</h4>
                  <ul class="reference-list">
                    <li>Student (1908). The probable error of a mean. Biometrika, 6(1), 1-25.</li>
                    <li>Wilcoxon, F. (1945). Individual comparisons by ranking methods. Biometrics Bulletin, 1(6), 80-83.</li>
                    <li>Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences (2nd ed.). Hillsdale, NJ: Lawrence Erlbaum Associates.</li>
                  </ul>
                </div>
              </div>
            </el-card>
          </div>
          
          <!-- 分析前的占位提示 -->
          <div v-else class="empty-results">
            <el-empty description="等待分析结果" :image-size="200">
              <template #image>
                <el-icon :size="80"><DataAnalysis /></el-icon>
              </template>
              <p>请先在左侧配置参数并点击"确认分析"按钮</p>
              <p>分析完成后，结果将显示在此区域</p>
            </el-empty>
          </div>
        </el-col>
      </el-row>
    </el-main>
  </div>
</template>

<script setup>
defineOptions({
  name: "DouJiaTu", // 关键：改掉和列表页重复的BasicPlot，避免冲突
  inheritAttrs: false,
});

import { ref, reactive, nextTick, onMounted } from 'vue'
import * as echarts from 'echarts'
import {
  Document,
  CollectionTag,
  VideoPlay,
  Upload,
  Download,
  RefreshRight,
  Refresh,
  Check,
  Finished,
  DataAnalysis
} from '@element-plus/icons-vue'

// 数据状态
const uploadedFileName = ref('')
const isDataValid = ref(false)
const isPlotting = ref(false)
const showResults = ref(false)
const activeCollapse = ref(['main'])
const activeResultTab = ref('main')
const selectedLanguage = ref('R')
const fileInputRef = ref(null)
const chartContainer = ref(null)
let chartInstance = null

// 图表参数
const plotParams = reactive({
  statMethod: 'paired_t',
  spacing: 0.5,
  pointColor: '#409EFF',
  pointSize: 5,
  showLine: true,
  lineColor: '#409EFF80'
})

// 统计描述数据
const statDescriptionData = ref([
  {
    group: 'Before',
    count: 10,
    min: 172.4,
    max: 235,
    median: 197.35,
    iqr: 19.15,
    q1: 187.8,
    q3: 206.95,
    mean: 200.56,
    sd: 20.028,
    se: 6.3335
  },
  {
    group: 'After',
    count: 10,
    min: 337,
    max: 445.8,
    median: 405,
    iqr: 28.3,
    q1: 384.53,
    q3: 412.83,
    mean: 400.04,
    sd: 30.087,
    se: 9.5143
  }
])

// 异常值数据
const outlierData = ref([
  { group: 'Before', outliers: '', extremes: '' },
  { group: 'After', outliers: '337', extremes: '' }
])

// 交互方法
const handleUploadClick = () => {
  fileInputRef.value.click()
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    uploadedFileName.value = file.name
    // 这里可以添加文件验证逻辑
    isDataValid.value = true
  }
}

const downloadExampleData = () => {
  // 实际应用中这里会触发文件下载
  ElMessage.success('示例数据下载开始')
  // 模拟下载
  setTimeout(() => {
    ElMessage.success('示例数据下载完成')
    uploadedFileName.value = '配对图示例数据.xlsx'
    isDataValid.value = true
  }, 500)
}

const saveParams = () => {
  ElMessage.success('参数已保存')
}

const resetCurrentParams = () => {
  Object.assign(plotParams, {
    statMethod: 'paired_t',
    spacing: 0.5,
    pointColor: '#409EFF',
    pointSize: 5,
    showLine: true,
    lineColor: '#409EFF80'
  })
  ElMessage.info('当前参数已重置')
}

const resetAllParams = () => {
  resetCurrentParams()
  uploadedFileName.value = ''
  isDataValid.value = false
  showResults.value = false
  activeResultTab.value = 'main'
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  ElMessage.info('所有参数已重置')
}

const generatePlot = () => {
  if (!isDataValid.value) {
    ElMessage.warning('请先上传有效数据')
    return
  }
  
  isPlotting.value = true
  
  // 模拟分析过程
  setTimeout(() => {
    isPlotting.value = false
    showResults.value = true
    
    // 确保DOM已更新后初始化图表
    nextTick(() => {
      initChart()
    })
    
    ElMessage.success('分析完成！')
  }, 1500)
}

const initChart = () => {
  if (!chartContainer.value) return
  
  // 如果已有图表实例，先销毁
  if (chartInstance) {
    chartInstance.dispose()
  }
  
  // 初始化ECharts实例
  chartInstance = echarts.init(chartContainer.value)
  
  // 模拟配对图数据
  const beforeData = [172.4, 185.2, 195.0, 187.8, 200.5, 235.0, 190.3, 206.9, 198.7, 192.1]
  const afterData = [337.0, 384.5, 412.8, 390.2, 405.0, 445.8, 398.7, 420.3, 401.5, 395.2]
  
  const option = {
    title: { text: '配对图', left: 'center' },
    grid: { top: 60, right: 40, bottom: 60, left: 60 },
    xAxis: {
      type: 'category',
      data: ['Before', 'After'],
      axisLabel: { fontSize: 14 }
    },
    yAxis: {
      type: 'value',
      name: 'Value',
      axisLabel: { fontSize: 12 }
    },
    series: [
      {
        type: 'scatter',
        data: beforeData.map((val, idx) => [0, val]),
        symbolSize: plotParams.pointSize,
        itemStyle: { color: plotParams.pointColor },
        name: 'Before'
      },
      {
        type: 'scatter',
        data: afterData.map((val, idx) => [1, val]),
        symbolSize: plotParams.pointSize,
        itemStyle: { color: '#F56C6C' },
        name: 'After'
      },
      {
        type: 'line',
        data: beforeData.map((val, idx) => [
          [0, val],
          [1, afterData[idx]]
        ]),
        lineStyle: {
          color: plotParams.showLine ? plotParams.lineColor : 'transparent',
          width: 1.5,
          opacity: 0.6
        },
        show: plotParams.showLine
      },
      {
        type: 'boxplot',
        data: [
          [172.4, 187.8, 197.35, 206.95, 235.0],
          [337.0, 384.53, 405.0, 412.83, 445.8]
        ],
        itemStyle: { color: '#909399', borderColor: '#606266' }
      }
    ],
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        if (params.seriesType === 'scatter') {
          return `${params.seriesName}<br/>值: ${params.value[1].toFixed(1)}`
        }
        return ''
      }
    },
    legend: { top: 10, data: ['Before', 'After'] }
  }
  
  chartInstance.setOption(option)
  
  // 响应窗口大小变化
  window.addEventListener('resize', () => {
    chartInstance.resize()
  })
}

const handleTabClick = (tab) => {
  // 切换到方法学标签页时，如果图表存在，确保重新渲染
  if (tab.props.name === 'main' && chartInstance && chartContainer.value) {
    nextTick(() => {
      chartInstance.resize()
    })
  }
}

const saveResults = () => {
  ElMessage.success('分析结果已保存')
}

const downloadReport = () => {
  ElMessage.success('整份报告下载开始')
  // 模拟下载过程
  setTimeout(() => {
    ElMessage.success('报告下载完成')
  }, 1000)
}

const goBack = () => {
  // 返回上一页的逻辑
  ElMessage.info('返回上一页')
}

// 组件挂载时的初始化
onMounted(() => {
  // 可以在这里进行一些初始化操作
})
</script>

<style scoped>
.paired-plot-app {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.page-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.page-title h1 {
  margin: 0;
  color: #303133;
}

.doc-links {
  display: flex;
  align-items: center;
  gap: 10px;
}

.config-card, .results-card {
  height: 100%;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
}

.upload-area {
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e4e7ed;
}

.param-section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-weight: 500;
  color: #606266;
}

.upload-input-trigger {
  cursor: pointer;
  margin-bottom: 10px;
}

.upload-tips {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}

.file-format {
  flex-grow: 1;
}

.param-collapse {
  margin: 20px 0;
}

.param-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  justify-content: center;
}

.confirm-action {
  margin-top: 30px;
  text-align: center;
}

.confirm-action .el-button {
  width: 80%;
  height: 48px;
  font-size: 16px;
}

.results-card .card-header {
  padding-bottom: 0;
}

.result-actions {
  display: flex;
  gap: 10px;
}

.plot-description {
  margin-bottom: 25px;
}

.plot-description h3 {
  margin-top: 0;
  color: #303133;
}

.plot-description p {
  color: #606266;
  margin-bottom: 15px;
}

.alert-detail {
  font-size: 13px;
  margin-top: 5px;
}

.chart-container {
  width: 100%;
  height: 450px;
  margin: 20px 0;
}

.chart-downloads {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-top: 15px;
}

.empty-results {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 600px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.supplementary-content h3 {
  margin-top: 0;
  color: #303133;
}

.section-subtitle {
  color: #606266;
  font-size: 14px;
  margin-bottom: 15px;
}

.outlier-formula {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  margin: 15px 0;
  font-size: 13px;
  color: #606266;
}

.file-download {
  margin: 15px 0;
}

.methodology-content {
  line-height: 1.6;
}

.code-block {
  background-color: #f6f8fa;
  padding: 15px;
  border-radius: 4px;
  overflow-x: auto;
  border-left: 4px solid #409EFF;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.5;
  margin: 15px 0;
}

.reference-list {
  padding-left: 20px;
  color: #606266;
}

.reference-list li {
  margin-bottom: 8px;
  font-size: 13px;
}

.el-divider {
  margin: 20px 0;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .el-col-8, .el-col-16 {
    width: 100%;
  }
  
  .page-title {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>




