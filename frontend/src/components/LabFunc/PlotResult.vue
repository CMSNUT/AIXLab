<template>
  <div class="result-section">
    <div class="result-header">
      <div class="result-tabs">
        <div 
          v-for="tab in plotStore.tabs" 
          :key="tab.id"
          :class="['result-tab', { 'tab-active': plotStore.activeTab === tab.id }]"
          @click="plotStore.setActiveTab(tab.id)"
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
    <div v-show="plotStore.activeTab === 'main'" class="result-content">
      <div class="result-block">
        <div class="result-title">配对图</div>
        <div class="result-intro">
          <div><strong>配对图</strong>: 将有配对关系的样本进行可视化的一种方式</div>
          <div>当前所选的统计方法: <strong>{{ plotStore.statMethodLabel }}</strong></div>
          <div><strong>注意</strong>: 统计要求<u>每组样本都要满足3个样本以上</u>，并且<u>每组样本的方差不能为0</u>，如果不满足条件，就不会进行统计分析</div>
        </div>
        
        <div class="result-image">
          <el-image 
            :src="plotStore.plotResult.imageUrl" 
            :preview-src-list="[plotStore.plotResult.imageUrl]"
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
          <el-button type="primary" plain @click="downloadPPTX">配对图.pptx</el-button>
        </div>
      </div>
    </div>

    <!-- 补充结果 -->
    <div v-show="plotStore.activeTab === 'supplementary'" class="result-content">
      <!-- 统计描述表格 -->
      <div class="result-block">
        <div class="result-title">统计描述</div>
        <div class="result-intro">各个组常见「统计描述指标」</div>
        
        <el-table :data="plotStore.plotResult.statDescription" border class="result-table">
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
        
        <el-table :data="plotStore.plotResult.outlierAnalysis" border class="result-table">
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
        
        <el-table :data="plotStore.plotResult.normalityTest" border class="result-table">
          <el-table-column prop="df" label="自由度(df)" />
          <el-table-column prop="statistic" label="统计量" />
          <el-table-column prop="pValue" label="p值" />
        </el-table>
        
        <div class="result-explain">
          <div v-if="plotStore.plotResult.normalityTest && plotStore.plotResult.normalityTest.length > 0">
            正态性检验结果显示，各组配对样本<差值>接近正态分布(P > 0.05)，建议选择用参数检验的方法
          </div>
          <div v-else>
            暂无正态性检验数据
          </div>
        </div>
      </div>

      <!-- 配对样本T检验 -->
      <div class="result-block">
        <div class="result-title">配对样本T检验</div>
        <div class="result-intro">应用条件: 各组内两两配对样本差值满足正态性检验</div>
        
        <el-table :data="plotStore.plotResult.tTestResults" border class="result-table">
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
    <div v-show="plotStore.activeTab === 'methodology'" class="result-content">
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
            <p>· 统计方法: {{ plotStore.statMethodLabel }}</p>
            <p>· 当前图表: {{ plotStore.plotName }}</p>
            <p>· 图表ID: {{ plotStore.plotId }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { usePlotStoreHook } from '@/store';
import { Picture } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';

const plotStore = usePlotStoreHook();

// 保存结果
const saveResult = () => {
  plotStore.saveResult();
  ElMessage.success('结果保存成功');
  
  // 添加到历史记录
  plotStore.addHistoricalResult({
    title: `${plotStore.plotName} - 分析结果`,
    content: `使用${plotStore.statMethodLabel}方法进行分析`,
    createTime: new Date().toLocaleString('zh-CN'),
  });
};

// 下载整份报告
const downloadReport = () => {
  console.log('下载整份报告...');
  ElMessage.success('开始下载报告');
};

// 下载PDF
const downloadPDF = () => {
  console.log('下载PDF...');
  ElMessage.success('开始下载PDF');
};

// 下载TIFF
const downloadTIFF = () => {
  console.log('下载TIFF...');
  ElMessage.success('开始下载TIFF');
};

// 下载TIFF
const downloadPPTX = () => {
  console.log('下载PPTX...');
  ElMessage.success('开始下载PPTX');
};


// 导出统计描述
const exportStatDescription = () => {
  console.log('导出统计描述...');
  ElMessage.success('开始导出统计描述');
};
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