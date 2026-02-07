<template>
  <!-- 数据读取 -->
  <el-card class="plot-card">
    <template #header>
      <div class="plot-card-header">
        <span>绘图数据</span>
        <div class="plot-card-header-right">
          <el-button type="text" @click="resetData">
            <el-icon class="plot-card-header-reset-icon">
              <Refresh />
            </el-icon>
            <span class="plot-card-header-title">重置数据</span>
          </el-button>
        </div>
      </div>
    </template>

    <div class="plot-data-box">
      <div class="plot-data-params-box">
        <div class="plot-data-params-box-title">
          <!-- 上传区域 -->
          <div class="upload-plot-header">
            <span>上传数据</span>
            <el-tooltip content="支持上传CSV、Excel、TXT格式的数据文件" placement="top">
              <el-icon>
                <InfoFilled />
              </el-icon>
            </el-tooltip>
          </div>

          <!-- 上传组件 -->
          <div class="upload-container">
            <el-upload ref="uploadRef" class="upload-demo" drag action="" :multiple="true" :show-file-list="false"
              :accept="'.csv,.xlsx,.xls,.txt'" :on-change="handleFileChange" :auto-upload="false">
              <el-icon class="el-icon--upload">
                <UploadFilled />
              </el-icon>
              <div class="el-upload__text">
                拖拽文件到此处或 <em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  支持 CSV、Excel、TXT 格式，单个文件不超过 10MB
                </div>
              </template>
            </el-upload>

            <!-- 文件列表 -->
            <div v-if="hasUploadedFiles" class="file-list-container">
              <div class="file-list-header">
                <span>已选择 {{ uploadedFiles.length }} 个文件</span>
                <el-button type="text" @click="clearAllFiles">清空</el-button>
              </div>
              <div class="file-list">
                <div v-for="(file, index) in uploadedFiles" :key="index" class="file-item">
                  <div class="file-info">
                    <el-icon class="file-icon">
                      <Document />
                    </el-icon>
                    <div class="file-details">
                      <div class="file-name">{{ file.name }}</div>
                      <div class="file-size">{{ formatFileSize(file.size) }}</div>
                    </div>
                  </div>
                  <div class="file-actions">
                    <el-button type="text" size="small" @click="removeFile(index)">删除</el-button>
                  </div>
                </div>
              </div>
            </div>

            <!-- 上传状态 -->
            <div v-if="uploadStatus === 'uploading'" class="upload-status">
              <el-progress :percentage="uploadProgress" :stroke-width="8" />
              <div class="progress-text">上传中... {{ uploadProgress }}%</div>
            </div>

            <div v-if="uploadStatus === 'success'" class="status-success">
              <el-icon>
                <CircleCheck />
              </el-icon>
              <span>上传成功！</span>
            </div>

            <div v-if="uploadStatus === 'error'" class="status-error">
              <el-icon>
                <CircleClose />
              </el-icon>
              <span>上传失败，请重试</span>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="upload-actions">
            <el-button type="primary" :disabled="!hasUploadedFiles || uploadStatus === 'uploading'"
              @click="handleUpload">
              {{ uploadStatus === 'uploading' ? '上传中...' : '确认上传数据' }}
            </el-button>

            <el-button type="warning" @click="handelDownloadPlotSampleData">
              <el-icon>
                <Download />
              </el-icon>
              下载示例数据
            </el-button>

            <el-button v-if="uploadStatus === 'success' && dataValidated" type="success" disabled>
              <el-icon>
                <CircleCheckFilled />
              </el-icon>
              验证成功
            </el-button>

            <el-button v-else-if="hasUploadedFiles" type="info" @click="validateData">
              <el-icon>
                <Check />
              </el-icon>
              验证数据
            </el-button>
          </div>

          <!-- 数据预览 -->
          <div v-if="dataPreview.length > 0" class="data-preview">
            <div class="preview-header">
              <span>数据预览 (前5行)</span>
              <el-button type="text" size="small" @click="showFullData">查看完整数据</el-button>
            </div>
            <el-table :data="dataPreview" border height="200" style="width: 100%">
              <el-table-column v-for="column in dataColumns" :key="column" :prop="column" :label="column" />
            </el-table>
          </div>
        </div>
      </div>
    </div>
  </el-card>
  <!-- 数据结束-->
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { usePlotStoreHook } from '@/store'
import {
  Refresh,
  InfoFilled,
  UploadFilled,
  Document,
  CircleCheck,
  CircleClose,
  CircleCheckFilled,
  Download,
  Check
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
// import LabPlotAPI from '@/api/module_lab/plot'
import ResourceAPI from '@/api/module_monitor/resource'

const plotStore = usePlotStoreHook()
const uploadRef = ref()

// 计算属性
const uploadedFiles = computed(() => plotStore.uploadData.files || [])
const hasUploadedFiles = computed(() => uploadedFiles.value.length > 0)
const uploadStatus = computed(() => plotStore.uploadData.status || 'idle')
const uploadProgress = computed(() => plotStore.uploadData.progress || 0)
const dataValidated = computed(() => plotStore.uploadData.options?.validated || false)

// 数据预览
const dataPreview = ref<any[]>([])
const dataColumns = ref<string[]>([])

// 处理文件变化
const handleFileChange = (file: any) => {
  if (file.raw) {
    plotStore.addUploadFiles([file.raw])
    // 重置验证状态
    plotStore.updateUploadData({
      options: { ...plotStore.uploadData.options, validated: false }
    })
    // 清除数据预览
    dataPreview.value = []
    dataColumns.value = []
  }
}

// 移除文件
const removeFile = (index: number) => {
  plotStore.removeUploadFile(index)
  if (uploadedFiles.value.length === 0) {
    dataPreview.value = []
    dataColumns.value = []
  }
}

// 清空所有文件
const clearAllFiles = () => {
  ElMessageBox.confirm('确定要清空所有文件吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    plotStore.clearUploadData()
    dataPreview.value = []
    dataColumns.value = []
    ElMessage.success('已清空所有文件')
  })
}

// 格式化文件大小
const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 处理上传
const handleUpload = async () => {
  if (!hasUploadedFiles.value) {
    ElMessage.warning('请先选择文件')
    return
  }

  try {
    // 开始上传
    plotStore.updateUploadData({ status: 'uploading', progress: 0 })

    // 模拟上传进度
    const interval = setInterval(() => {
      const progress = uploadProgress.value + 10
      plotStore.updateUploadData({ progress })

      if (progress >= 100) {
        clearInterval(interval)
        plotStore.updateUploadData({
          status: 'success',
          options: { ...plotStore.uploadData.options, validated: false }
        })

        // 解析并预览数据
        parseAndPreviewData()

        ElMessage.success('文件上传成功！')
      }
    }, 200)

  } catch (error) {
    plotStore.updateUploadData({ status: 'error' })
    ElMessage.error('文件上传失败：' + (error as Error).message)
  }
}

// 解析并预览数据（模拟）
const parseAndPreviewData = () => {
  // 这里应该是实际解析文件的逻辑
  // 模拟一些示例数据用于预览
  dataColumns.value = ['样本ID', '组别', '处理前', '处理后', '差值']
  dataPreview.value = [
    { '样本ID': 'S001', '组别': 'A组', '处理前': 150.2, '处理后': 210.5, '差值': 60.3 },
    { '样本ID': 'S002', '组别': 'A组', '处理前': 168.7, '处理后': 225.1, '差值': 56.4 },
    { '样本ID': 'S003', '组别': 'B组', '处理前': 142.3, '处理后': 198.7, '差值': 56.4 },
    { '样本ID': 'S004', '组别': 'B组', '处理前': 155.6, '处理后': 215.3, '差值': 59.7 },
    { '样本ID': 'S005', '组别': 'C组', '处理前': 160.8, '处理后': 220.1, '差值': 59.3 },
  ]
}

// 验证数据
const validateData = () => {
  if (!hasUploadedFiles.value) {
    ElMessage.warning('请先上传文件')
    return
  }

  // 模拟验证过程
  
  plotStore.updateUploadData({ status: 'uploading', progress: 0 })

  const interval = setInterval(() => {
    const progress = uploadProgress.value + 20
    plotStore.updateUploadData({ progress })

    if (progress >= 100) {
      clearInterval(interval)
      plotStore.updateUploadData({
        status: 'success',
        options: { ...plotStore.uploadData.options, validated: true }
      })

      ElMessage.success('数据验证通过！数据格式正确，可以进行绘图分析。')
    }
  }, 300)
}


// 文件下载
async function handelDownloadPlotSampleData () {
  try {
    // 使用file_url字段
    const name = plotStore.currentPlot?.code + '.xlsx';
    // const base_path = "http://127.0.0.1:8000/api/v1/static/sample/plot/"
    const full_path = "http://127.0.0.1:8000/api/v1/static/sample/plot/" + name
    // const parent_path = "static/sample/plot";
    // const response = await ResourceAPI.downloadFile(name, parent_path);
    const response = await ResourceAPI.downloadFile(full_path);
    const blob = response.data;
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Download error:", error);
  }
}

// 查看完整数据
const showFullData = () => {
  ElMessageBox.alert(
    '完整数据预览功能正在开发中...',
    '数据预览',
    {
      confirmButtonText: '确定',
    }
  )
}

// 重置数据
const resetData = () => {
  ElMessageBox.confirm('确定要重置所有数据吗？这将清除所有上传的文件和设置。', '重置确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    plotStore.clearUploadData()
    dataPreview.value = []
    dataColumns.value = []
    ElMessage.success('数据已重置')
  })
}

// 组件挂载时检查是否有现有数据
onMounted(() => {
  if (hasUploadedFiles.value && uploadStatus.value === 'success') {
    // 如果已有成功上传的文件，显示数据预览
    parseAndPreviewData()
  }
})
</script>

<style scoped lang="scss">
/* 上传区域样式 */
.plot-data-box {
  width: 100%;
  padding: 0 30px 30px 25px;
  box-sizing: border-box;
  background: #fff;
}

.plot-data-params-box {
  width: 100%;
  padding-top: 40px;
}

.plot-data-params-box-title {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.upload-plot-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-weight: 500;
  font-size: 16px;
  color: #303133;
}

.upload-plot-header .el-icon {
  color: #909399;
  cursor: help;
}

/* 上传容器 */
.upload-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 文件列表 */
.file-list-container {
  border: 1px solid #ebeef5;
  border-radius: 6px;
  overflow: hidden;
}

.file-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
  font-size: 14px;
  color: #606266;
}

.file-list {
  max-height: 200px;
  overflow-y: auto;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;

  &:last-child {
    border-bottom: none;
  }

  &:hover {
    background-color: #fafafa;
  }
}

.file-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.file-icon {
  font-size: 20px;
  color: #409eff;
}

.file-details {
  flex: 1;
  min-width: 0;
}

.file-name {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-size {
  font-size: 12px;
  color: #909399;
  margin-top: 2px;
}

.file-actions {
  flex-shrink: 0;
}

/* 上传状态 */
.upload-status {
  width: 100%;
}

.progress-text {
  text-align: center;
  font-size: 12px;
  color: #606266;
  margin-top: 8px;
}

.status-success {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  background-color: #f0f9eb;
  border-radius: 4px;
  color: #67c23a;
  gap: 8px;
}

.status-error {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  background-color: #fef0f0;
  border-radius: 4px;
  color: #f56c6c;
  gap: 8px;
}

/* 操作按钮 */
.upload-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 16px;
}

.upload-actions .el-button {
  min-width: 120px;
}

/* 数据预览 */
.data-preview {
  margin-top: 24px;
  border: 1px solid #ebeef5;
  border-radius: 6px;
  overflow: hidden;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
  font-size: 14px;
  color: #606266;
}

:deep(.data-preview .el-table) {
  font-size: 12px;
}

:deep(.data-preview .el-table th) {
  background-color: #f8f9fa;
  font-weight: 600;
}

/* 参数卡片样式 */
:deep(.plot-card) {
  width: 100%;
  padding: 0 !important;
  margin: 10px 0 !important;
  margin-bottom: 25px !important;
  border-radius: 10px 10px 0 0;
  overflow: hidden;
}

/* 清除卡片默认头部内边距 */
:deep(.plot-card .el-card__header) {
  padding: 0;
  margin: 0;
}

/* 清除卡片默认主体内边距 */
:deep(.plot-card .el-card__body) {
  padding: 0;
}

/* 卡片头部样式 */
.plot-card-header {
  font-weight: 700;
  font-size: 14px;
  color: white;
  width: 100%;
  height: 35px;
  background: #F19F55;
  display: flex;
  align-items: center;
  padding: 0 15px;
  box-sizing: border-box;
  justify-content: space-between;
}

.plot-card-header-right {
  height: 100%;
  display: flex;
  align-items: center;
}

.plot-card-header-reset-icon {
  color: white;
  font-size: 18px;
  margin-right: 2px;
}

.plot-card-header-title {
  font-size: 12px;
  font-weight: 400;
  color: #fff;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .plot-data-box {
    padding: 0 16px 20px 16px;
  }

  .upload-actions {
    flex-direction: column;
  }

  .upload-actions .el-button {
    width: 100%;
    min-width: auto;
  }
}
</style>