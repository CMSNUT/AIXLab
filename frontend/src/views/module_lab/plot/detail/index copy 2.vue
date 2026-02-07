<template>
  <div class="pair-plot-container">
    <!-- 页面头部 -->
    <div class="header">
      <div class="header-content">
        <div class="title-section">
          <h1>基础绘图 - 类别比较 - 配对图</h1>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧参数配置区域 -->
      <div class="params-section">
        <!-- 数据参数 -->
        <el-card class="params-card">
          <template #header>
            <div class="card-header">
              <span>数据参数</span>
              <el-button type="text" icon="RefreshLeft">重置参数</el-button>
            </div>
          </template>
          
          <div class="upload-section">
            <div class="upload-header">
              <span>上传文件</span>
              <el-tooltip content="上传数据文件" placement="top">
                <el-icon><QuestionFilled /></el-icon>
              </el-tooltip>
            </div>
            <div class="file-info">
              <span class="filename">配对图.xlsx</span>
              <el-link type="primary" :underline="false">下载示例数据</el-link>
            </div>
            <p class="upload-tips">支持.xlsx,.csv,.txt格式数据（<4M）</p>
            <div class="verify-status">
              <el-button type="success" icon="Check">验证成功</el-button>
            </div>
          </div>
        </el-card>

        <!-- 主要参数 -->
        <el-card class="params-card">
          <template #header>
            <div class="card-header">
              <span>主要参数</span>
              <div class="header-actions">
                <el-button type="text" icon="Star">保存参数</el-button>
                <el-button type="text" icon="RefreshLeft">重置参数</el-button>
              </div>
            </div>
          </template>

          <el-collapse v-model="activeCollapse">
            <!-- 统计分析 -->
            <el-collapse-item title="统计分析" name="statistics">
              <div class="param-item">
                <div class="param-label">统计方法</div>
                <el-select v-model="statMethod" placeholder="选择统计方法">
                  <el-option label="配对样本T检验" value="t-test" />
                  <el-option label="Wilcoxon signed rank test" value="wilcoxon" />
                  <el-option label="auto" value="auto" />
                </el-select>
              </div>

              <div class="param-item">
                <div class="param-label">分组对比</div>
                <el-select v-model="groupComparison" multiple placeholder="选择分组对比">
                  <el-option label="Before vs After" value="before_after" />
                </el-select>
              </div>

              <div class="param-item">
                <div class="param-label">显著性显示类型</div>
                <el-select v-model="significanceType" placeholder="选择显示类型">
                  <el-option label="星号" value="star" />
                  <el-option label="p值科学计数法" value="scientific" />
                  <el-option label="p值数值(小于0.05自动<)" value="pvalue" />
                </el-select>
              </div>

              <div class="param-item">
                <div class="param-label">显著性大小</div>
                <el-select v-model="significanceSize" placeholder="选择大小">
                  <el-option label="6pt" value="6pt" />
                  <el-option label="8pt" value="8pt" />
                  <el-option label="10pt" value="10pt" />
                </el-select>
              </div>
            </el-collapse-item>

            <!-- 间距设置 -->
            <el-collapse-item title="间距设置" name="spacing">
              <div class="param-item">
                <div class="param-label">组间距离</div>
                <el-input 
                  v-model="groupSpacing" 
                  placeholder="两组之间的聚类，0-1之间"
                  clearable
                />
              </div>
            </el-collapse-item>

            <!-- 点设置 -->
            <el-collapse-item title="点" name="points">
              <div class="param-item">
                <div class="param-label">填充色</div>
                <div class="color-group">
                  <el-color-picker v-model="pointFillColor1" />
                  <el-color-picker v-model="pointFillColor2" />
                </div>
              </div>

              <div class="param-item">
                <div class="param-label">描边色</div>
                <div class="color-group">
                  <el-color-picker v-model="pointStrokeColor1" />
                  <el-color-picker v-model="pointStrokeColor2" />
                </div>
              </div>

              <div class="param-item">
                <div class="param-label">样式</div>
                <el-select v-model="pointStyle" placeholder="选择点样式">
                  <el-option label="圆形" value="circle" />
                  <el-option label="方形" value="square" />
                  <el-option label="三角形" value="triangle" />
                </el-select>
              </div>

              <div class="param-item">
                <div class="param-label">大小</div>
                <el-input v-model="pointSize" placeholder="点的大小" clearable />
              </div>

              <div class="param-item">
                <div class="param-label">不透明度</div>
                <el-input v-model="pointOpacity" placeholder="0-1之间，1代表完全不透明" clearable />
              </div>
            </el-collapse-item>

            <!-- 连线设置 -->
            <el-collapse-item title="连线" name="lines">
              <div class="param-item">
                <div class="param-label">颜色</div>
                <el-color-picker v-model="lineColor" />
              </div>

              <div class="param-item">
                <div class="param-label">类型</div>
                <el-select v-model="lineType" placeholder="选择线类型">
                  <el-option label="实线" value="solid" />
                  <el-option label="虚线" value="dashed" />
                  <el-option label="点线" value="dotted" />
                </el-select>
              </div>

              <div class="param-item">
                <div class="param-label">粗细</div>
                <el-select v-model="lineWidth" placeholder="选择线粗细">
                  <el-option label="0.75pt" value="0.75pt" />
                  <el-option label="1pt" value="1pt" />
                  <el-option label="1.5pt" value="1.5pt" />
                </el-select>
              </div>
            </el-collapse-item>

            <!-- 箱设置 -->
            <el-collapse-item title="箱" name="box">
              <div class="param-item">
                <div class="param-label">展示</div>
                <el-switch v-model="showBox" />
              </div>

              <div class="param-item">
                <div class="param-label">填充色</div>
                <div class="color-group">
                  <el-color-picker v-model="boxFillColor1" />
                  <el-color-picker v-model="boxFillColor2" />
                </div>
              </div>

              <div class="param-item">
                <div class="param-label">描边色</div>
                <div class="color-group">
                  <el-color-picker v-model="boxStrokeColor1" />
                  <el-color-picker v-model="boxStrokeColor2" />
                </div>
              </div>

              <div class="param-item">
                <div class="param-label">描边粗细</div>
                <el-select v-model="boxStrokeWidth" placeholder="选择描边粗细">
                  <el-option label="0.75pt" value="0.75pt" />
                  <el-option label="1pt" value="1pt" />
                  <el-option label="1.5pt" value="1.5pt" />
                </el-select>
              </div>

              <div class="param-item">
                <div class="param-label">不透明度</div>
                <el-input v-model="boxOpacity" placeholder="0-1之间，1代表完全不透明" clearable />
              </div>

              <div class="param-item">
                <div class="param-label">箱子宽度</div>
                <el-input v-model="boxWidth" placeholder="宽度，0-1之间" clearable />
              </div>
            </el-collapse-item>

            <!-- 标题设置 -->
            <el-collapse-item title="标题" name="titles">
              <div class="param-item">
                <div class="param-label">大标题</div>
                <el-input v-model="mainTitle" placeholder="大标题内容" clearable />
              </div>

              <div class="param-item">
                <div class="param-label">x轴标题</div>
                <el-input v-model="xAxisTitle" placeholder="x轴标题内容" clearable />
              </div>

              <div class="param-item">
                <div class="param-label">y轴标题</div>
                <el-input v-model="yAxisTitle" placeholder="y轴标题内容" clearable />
              </div>
            </el-collapse-item>

            <!-- 图注设置 -->
            <el-collapse-item title="图注" name="legend">
              <div class="param-item">
                <div class="param-label">是否展示</div>
                <el-switch v-model="showLegend" />
              </div>

              <div class="param-item">
                <div class="param-label">图注标题</div>
                <el-input v-model="legendTitle" placeholder="图注标题内容" clearable />
              </div>

              <div class="param-item">
                <div class="param-label">图注位置</div>
                <el-select v-model="legendPosition" placeholder="选择图注位置">
                  <el-option label="默认" value="default" />
                  <el-option label="顶部" value="top" />
                  <el-option label="底部" value="bottom" />
                  <el-option label="左侧" value="left" />
                  <el-option label="右侧" value="right" />
                </el-select>
              </div>
            </el-collapse-item>

            <!-- 坐标轴设置 -->
            <el-collapse-item title="坐标轴" name="axes">
              <div class="param-item">
                <div class="param-label">x轴分组名</div>
                <el-input v-model="xAxisLabels" placeholder=",+空格隔开" clearable />
              </div>

              <div class="param-item">
                <div class="param-label">x轴标注旋转</div>
                <el-select v-model="xAxisRotation" placeholder="选择旋转角度">
                  <el-option label="0" value="0" />
                  <el-option label="45" value="45" />
                  <el-option label="90" value="90" />
                </el-select>
              </div>

              <div class="param-item">
                <div class="param-label">y轴范围+刻度</div>
                <el-input v-model="yAxisRange" placeholder="()包裹,内容用','+空格隔开" clearable />
              </div>
            </el-collapse-item>

            <!-- 风格设置 -->
            <el-collapse-item title="风格" name="style">
              <div class="param-item">
                <div class="param-label">边框</div>
                <el-switch v-model="showBorder" />
              </div>

              <div class="param-item">
                <div class="param-label">网格</div>
                <el-switch v-model="showGrid" />
              </div>

              <div class="param-item">
                <div class="param-label">xy颠倒</div>
                <el-switch v-model="swapAxes" />
              </div>

              <div class="param-item">
                <div class="param-label">文字大小</div>
                <el-select v-model="fontSize" placeholder="选择文字大小">
                  <el-option label="7pt" value="7pt" />
                  <el-option label="8pt" value="8pt" />
                  <el-option label="9pt" value="9pt" />
                  <el-option label="10pt" value="10pt" />
                </el-select>
              </div>
            </el-collapse-item>

            <!-- 图片设置 -->
            <el-collapse-item title="图片" name="image">
              <div class="param-item">
                <div class="param-label">宽度 (cm)</div>
                <el-input v-model="imageWidth" placeholder="设置图片宽度" clearable />
              </div>

              <div class="param-item">
                <div class="param-label">高度 (cm)</div>
                <el-input v-model="imageHeight" placeholder="设置图片高度" clearable />
              </div>

              <div class="param-item">
                <div class="param-label">字体</div>
                <el-select v-model="fontFamily" placeholder="选择字体">
                  <el-option label="Arial" value="Arial" />
                  <el-option label="Times New Roman" value="Times New Roman" />
                  <el-option label="Helvetica" value="Helvetica" />
                  <el-option label="SimSun" value="SimSun" />
                </el-select>
              </div>
            </el-collapse-item>
          </el-collapse>
        </el-card>

        <!-- 提交按钮 -->
        <div class="submit-section">
          <el-button type="primary" size="large" @click="generatePlot">确认</el-button>
        </div>
      </div>

      <!-- 右侧结果展示区域 -->
      <div class="result-section">
        <div class="result-header">
          <div class="result-tabs">
            <div 
              v-for="tab in tabs" 
              :key="tab.id"
              :class="['result-tab', { 'tab-active': activeTab === tab.id }]"
              @click="activeTab = tab.id"
            >
              {{ tab.label }}
            </div>
          </div>
          <div class="result-actions">
            <el-button type="primary" plain @click="saveResult">保存结果</el-button>
            <el-button type="primary" plain @click="downloadReport">下载整份报告</el-button>
          </div>
        </div>

        <!-- 主要结果 -->
        <div v-show="activeTab === 'main'" class="result-content">
          <div class="result-block">
            <div class="result-title">配对图</div>
            <div class="result-intro">
              <div><strong>配对图</strong>: 将有配对关系的样本进行可视化的一种方式</div>
              <div>当前所选的统计方法: <strong>{{ statMethodLabel }}</strong></div>
              <div><strong>注意</strong>: 统计要求<u>每组样本都要满足3个样本以上</u>，并且<u>每组样本的方差不能为0</u>，如果不满足条件，就不会进行统计分析</div>
            </div>
            
            <div class="result-image">
              <el-image 
                :src="plotImage" 
                :preview-src-list="[plotImage]"
                fit="contain"
                class="plot-image"
              >
                <template #error>
                  <div class="image-error">
                    <el-icon><Picture /></el-icon>
                    <span>图片加载失败</span>
                  </div>
                </template>
              </el-image>
            </div>
            
            <div class="result-actions">
              <el-button type="primary" plain @click="downloadPDF">配对图.pdf</el-button>
              <el-button type="primary" plain @click="downloadTIFF">配对图.tiff</el-button>
            </div>
          </div>
        </div>

        <!-- 补充结果 -->
        <div v-show="activeTab === 'supplementary'" class="result-content">
          <!-- 统计描述表格 -->
          <div class="result-block">
            <div class="result-title">统计描述</div>
            <div class="result-intro">各个组常见「统计描述指标」</div>
            
            <el-table :data="statDescription" border class="result-table">
              <el-table-column prop="group" label="组别" />
              <el-table-column prop="count" label="数目" />
              <el-table-column prop="min" label="最小值" />
              <el-table-column prop="max" label="最大值" />
              <el-table-column prop="median" label="中位数(Median)" />
              <el-table-column prop="iqr" label="四分位距(IQR)" />
              <el-table-column prop="q1" label="下四分位" />
              <el-table-column prop="q3" label="上四分位" />
              <el-table-column prop="mean" label="均值(Mean)" />
              <el-table-column prop="sd" label="标准差(SD)" />
              <el-table-column prop="se" label="标准误(SE)" />
            </el-table>
            
            <div class="result-actions">
              <el-button type="primary" plain @click="exportStatDescription">统计描述.xlsx</el-button>
            </div>
          </div>

          <!-- 异常值分析 -->
          <div class="result-block">
            <div class="result-title">异常值分析</div>
            <div class="result-intro">
              <div>离群值 = Q1(下四分位) - 1.5*IQR(四分位间距) 或者 Q3(上四分位) + 1.5*IQR(四分位间距)</div>
              <div>异常值 = Q1(下四分位) - 3.0*IQR(四分位间距) 或者 Q3(上四分位) + 3.0*IQR(四分位间距)</div>
            </div>
            
            <el-table :data="outlierAnalysis" border class="result-table">
              <el-table-column prop="group" label="组别" />
              <el-table-column prop="outliers" label="离群值" />
              <el-table-column prop="anomalies" label="异常值" />
            </el-table>
            
            <div class="result-explain">
              <div>各组离群值和异常值如上所示，如数据确认非人为记录错误，可不进行处理</div>
            </div>
          </div>

          <!-- 正态性检验 -->
          <div class="result-block">
            <div class="result-title">正态性检验</div>
            <div class="result-intro">检验方法: Shapiro-Wilk normality test</div>
            
            <el-table :data="normalityTest" border class="result-table">
              <el-table-column prop="df" label="自由度(df)" />
              <el-table-column prop="statistic" label="统计量" />
              <el-table-column prop="pValue" label="p值" />
            </el-table>
            
            <div class="result-explain">
              <div>正态性检验结果显示，各组配对样本<差值>接近正态分布(P > 0.05)，建议选择用参数检验的方法</div>
            </div>
          </div>

          <!-- 配对样本T检验 -->
          <div class="result-block">
            <div class="result-title">配对样本T检验</div>
            <div class="result-intro">应用条件: 各组内两两配对样本差值满足正态性检验</div>
            
            <el-table :data="tTestResults" border class="result-table">
              <el-table-column prop="groupI" label="组别I" />
              <el-table-column prop="groupJ" label="组别J" />
              <el-table-column prop="df" label="自由度(df)" />
              <el-table-column prop="tStatistic" label="统计量t" />
              <el-table-column prop="difference" label="差值(J-I)" />
              <el-table-column prop="confidenceInterval" label="置信区间(95%CI)" />
              <el-table-column prop="pValue" label="p值" />
            </el-table>
            
            <div class="result-explain">
              <div>p值满足<0.05时，可认为两组存在统计学上差异</div>
            </div>
          </div>
        </div>

        <!-- 方法学 -->
        <div v-show="activeTab === 'methodology'" class="result-content">
          <div class="result-block">
            <div class="result-title">方法学</div>
            <div class="methodology-content">
              <div><strong>软件</strong>: R (4.2.1)版本</div>
              <div><strong>R包</strong>: ggplot2[3.4.4], stats[4.2.1], car[3.1-0]</div>
              <div>
                <p><strong>处理过程:</strong></p>
                <p>· 根据数据格式特征情况选择合适的统计方法进行统计(stats包以及car包)(如果不满足统计要求将不会进行统计分析)，用ggplot2包对数据进行可视化</p>
              </div>
              <div>
                <p><strong>补充说明:</strong></p>
                <p>· 统计方法: 配对样本T检验</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  Document,
  Refresh,
  QuestionFilled,
  RefreshLeft,
  Star,
  Check,
  Picture
} from '@element-plus/icons-vue'

// 折叠面板状态
const activeCollapse = ref(['statistics', 'points', 'lines', 'box', 'titles'])

// 参数数据
const statMethod = ref('t-test')
const groupComparison = ref(['before_after'])
const significanceType = ref('star')
const significanceSize = ref('6pt')
const groupSpacing = ref('0.5')
const pointFillColor1 = ref('#4DBBD5')
const pointFillColor2 = ref('#E64B35')
const pointStrokeColor1 = ref('#4DBBD5')
const pointStrokeColor2 = ref('#E64B35')
const pointStyle = ref('circle')
const pointSize = ref('4')
const pointOpacity = ref('1')
const lineColor = ref('#000000')
const lineType = ref('solid')
const lineWidth = ref('0.75pt')
const showBox = ref(true)
const boxFillColor1 = ref('#4DBBD5')
const boxFillColor2 = ref('#E64B35')
const boxStrokeColor1 = ref('#000000')
const boxStrokeColor2 = ref('#000000')
const boxStrokeWidth = ref('0.75pt')
const boxOpacity = ref('1')
const boxWidth = ref('0.5')
const mainTitle = ref('')
const xAxisTitle = ref('')
const yAxisTitle = ref('')
const showLegend = ref(true)
const legendTitle = ref('')
const legendPosition = ref('default')
const xAxisLabels = ref('Before, After')
const xAxisRotation = ref('0')
const yAxisRange = ref('')
const showBorder = ref(false)
const showGrid = ref(false)
const swapAxes = ref(false)
const fontSize = ref('7pt')
const imageWidth = ref('')
const imageHeight = ref('')
const fontFamily = ref('Arial')

// 标签页状态
const activeTab = ref('main')
const tabs = [
  { id: 'main', label: '主要结果' },
  { id: 'supplementary', label: '补充结果' },
  { id: 'methodology', label: '方法学' }
]

// 计算属性
const statMethodLabel = computed(() => {
  const methods = {
    't-test': '配对样本T检验',
    'wilcoxon': 'Wilcoxon signed rank test',
    'auto': 'auto'
  }
  return methods[statMethod.value] || '配对样本T检验'
})

// 示例数据
const plotImage = ref('https://via.placeholder.com/800x400/4DBBD5/FFFFFF?text=配对图+示例')

const statDescription = ref([
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

const outlierAnalysis = ref([
  { group: 'After', outliers: '337', anomalies: '' }
])

const normalityTest = ref([
  { df: 9, statistic: 0.96751, pValue: 0.8669 }
])

const tTestResults = ref([
  {
    groupI: 'Before',
    groupJ: 'After',
    df: 9,
    tStatistic: 25.546,
    difference: 199.48,
    confidenceInterval: '181.82 – 217.14',
    pValue: '1.04e-09'
  }
])

// 方法
const generatePlot = () => {
  console.log('生成配对图...')
  // 这里应该调用API生成图表
  activeTab.value = 'main'
}

const saveResult = () => {
  console.log('保存结果...')
  ElMessage.success('结果保存成功')
}

const downloadReport = () => {
  console.log('下载整份报告...')
  ElMessage.success('开始下载报告')
}

const downloadPDF = () => {
  console.log('下载PDF...')
  ElMessage.success('开始下载PDF')
}

const downloadTIFF = () => {
  console.log('下载TIFF...')
  ElMessage.success('开始下载TIFF')
}

const exportStatDescription = () => {
  console.log('导出统计描述...')
  ElMessage.success('开始导出统计描述')
}
</script>

<style scoped>
.pair-plot-container {
  min-width: 1200px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

/* 头部样式 */
.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px 0;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.title-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
}

.title-section h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.action-buttons {
  display: flex;
  gap: 20px;
}

.action-buttons .el-button {
  color: white;
  font-size: 14px;
}

/* 主要内容布局 */
.main-content {
  max-width: 1400px;
  margin: 20px auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 20px;
}

/* 参数卡片样式 */
.params-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 10px;
}

/* 上传区域样式 */
.upload-section {
  padding: 16px;
}

.upload-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-weight: 500;
}

.file-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  padding: 8px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.filename {
  font-weight: 500;
  color: #409eff;
}

.upload-tips {
  font-size: 12px;
  color: #909399;
  margin-bottom: 16px;
}

.verify-status {
  text-align: center;
}

/* 参数项样式 */
.param-item {
  margin-bottom: 16px;
}

.param-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
  font-weight: 500;
}

.param-label.tips-text {
  color: #909399;
}

.color-group {
  display: flex;
  gap: 12px;
}

/* 折叠面板样式 */
:deep(.el-collapse-item__header) {
  font-weight: 600;
  color: #303133;
}

:deep(.el-collapse-item__content) {
  padding: 20px;
  background-color: #fafafa;
  border-radius: 0 0 4px 4px;
}

/* 提交按钮区域 */
.submit-section {
  text-align: center;
  margin: 20px 0;
}

.submit-section .el-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  background: linear-gradient(135deg, #f46e2f 0%, #ff8c00 100%);
  border: none;
}

.submit-section .el-button:hover {
  background: linear-gradient(135deg, #e55e1f 0%, #e67c00 100%);
}

/* 结果区域样式 */
.result-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
}

.result-tabs {
  display: flex;
  gap: 30px;
}

.result-tab {
  padding: 8px 0;
  cursor: pointer;
  color: #888;
  font-weight: 600;
  position: relative;
  transition: color 0.3s;
}

.result-tab:hover {
  color: #f46e2f;
}

.tab-active {
  color: #f46e2f;
}

.tab-active::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -1px;
  width: 100%;
  height: 2px;
  background: #f46e2f;
}

.result-actions {
  display: flex;
  gap: 10px;
}

/* 结果内容样式 */
.result-content {
  padding: 20px;
}

.result-block {
  margin-bottom: 30px;
}

.result-title {
  position: relative;
  padding-left: 12px;
  margin-bottom: 16px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.result-title::after {
  content: "";
  position: absolute;
  left: 0;
  top: 2px;
  width: 5px;
  height: 20px;
  background: #f46e2f;
}

.result-intro {
  padding: 16px;
  background: #f7f7f7;
  border-radius: 4px;
  margin-bottom: 16px;
  font-size: 14px;
  color: #555;
  line-height: 1.6;
}

.result-intro div {
  margin-bottom: 8px;
}

.result-intro strong {
  color: #303133;
}

.result-image {
  text-align: center;
  background: #f7f7f7;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.plot-image {
  max-width: 100%;
  height: 400px;
  object-fit: contain;
}

.image-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #909399;
}

.image-error .el-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

/* 表格样式 */
.result-table {
  margin: 16px 0;
  border-radius: 4px;
  overflow: hidden;
}

:deep(.result-table .el-table__header) {
  background-color: #f5f7fa;
}

:deep(.result-table th) {
  background-color: #f5f7fa;
  color: #303133;
  font-weight: 600;
}

/* 解释说明样式 */
.result-explain {
  padding: 16px;
  background: #f7f7f7;
  border-radius: 4px;
  margin-top: 16px;
  font-size: 14px;
  color: #555;
}

/* 方法学内容样式 */
.methodology-content {
  padding: 16px;
  background: #f7f7f7;
  border-radius: 4px;
  font-size: 14px;
  color: #555;
  line-height: 1.6;
}

.methodology-content > div {
  margin-bottom: 16px;
}

.methodology-content p {
  margin: 8px 0;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .header-content,
  .main-content {
    padding: 0 12px;
  }
  
  .title-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .action-buttons {
    width: 100%;
    justify-content: space-between;
  }
  
  .result-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .result-tabs {
    width: 100%;
    justify-content: space-between;
    gap: 10px;
  }
  
  .result-actions {
    width: 100%;
    justify-content: center;
  }
}
</style>