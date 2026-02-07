<template>
  <div class="analysis-tool">
    <!-- 主要内容区域 -->
    <el-main class="main-content">

      <el-row :gutter="20">


        <!-- 右侧参数设置 -->
        <el-col :span="18">
          <div class="analysis-workspace">
            <!-- 工具标题和操作 -->
            <div class="tool-header">
              <h2>基础绘图 - 类别比较 - 配对图</h2>
            </div>

            <!-- 参数设置 -->
            <el-card class="params-card">
              <!-- 数据参数 -->
              <div class="params-section">
                <div class="section-header">
                  <h3>数据参数</h3>
                  <el-button type="text" @click="resetDataParams">
                    <el-icon><Refresh /></el-icon>
                    重置参数
                  </el-button>
                </div>
                <el-form :model="dataParams" label-width="120px">
                  <el-form-item label="上传文件">
                    <el-upload
                      class="upload-demo"
                      action="/api/upload"
                      :on-success="handleUploadSuccess"
                      :before-upload="beforeUpload"
                    >
                      <el-button type="primary">点击上传</el-button>
                      <template #tip>
                        <div class="el-upload__tip">
                          支持 .xlsx, .csv, .txt 格式数据（<4M）
                          <a href="#" @click="downloadExample">下载示例数据</a>
                        </div>
                      </template>
                    </el-upload>
                  </el-form-item>
                </el-form>
              </div>

              <!-- 主要参数 -->
              <div class="params-section">
                <div class="section-header">
                  <h3>主要参数</h3>
                  <div>
                    <el-button type="text" @click="saveParams">
                      <el-icon><Download /></el-icon>
                      保存参数
                    </el-button>
                    <el-button type="text" @click="resetMainParams">
                      <el-icon><Refresh /></el-icon>
                      重置参数
                    </el-button>
                  </div>
                </div>
                
                <el-collapse v-model="activeParamSections">
                  <!-- 统计分析 -->
                  <el-collapse-item title="统计分析" name="statistics">
                    <el-form :model="mainParams" label-width="150px">
                      <el-form-item label="统计方法">
                        <el-select v-model="mainParams.statMethod" placeholder="请选择">
                          <el-option label="auto" value="auto" />
                        </el-select>
                      </el-form-item>
                      <el-form-item label="分组对比">
                        <el-select v-model="mainParams.groupComparison" multiple placeholder="请选择">
                          <el-option label="all" value="all" />
                        </el-select>
                      </el-form-item>
                      <el-form-item label="显著性显示类型">
                        <el-select v-model="mainParams.significanceType" placeholder="请选择">
                          <el-option label="星号" value="star" />
                          <el-option label="p值科学计数法" value="scientific" />
                          <el-option label="p值数值" value="numeric" />
                        </el-select>
                      </el-form-item>
                      <el-form-item label="显著性大小">
                        <el-select v-model="mainParams.significanceSize" placeholder="请选择">
                          <el-option label="6pt" value="6pt" />
                          <el-option label="7pt" value="7pt" />
                          <el-option label="8pt" value="8pt" />
                        </el-select>
                      </el-form-item>
                    </el-form>
                  </el-collapse-item>

                  <!-- 点设置 -->
                  <el-collapse-item title="点" name="points">
                    <el-form :model="mainParams.points" label-width="150px">
                      <el-form-item label="填充色">
                        <el-color-picker v-model="mainParams.points.fillColor1" />
                        <el-color-picker v-model="mainParams.points.fillColor2" />
                      </el-form-item>
                      <el-form-item label="描边色">
                        <el-color-picker v-model="mainParams.points.borderColor1" />
                        <el-color-picker v-model="mainParams.points.borderColor2" />
                      </el-form-item>
                      <el-form-item label="样式">
                        <el-select v-model="mainParams.points.style" placeholder="请选择">
                          <el-option label="圆形" value="circle" />
                          <el-option label="正方形" value="square" />
                          <el-option label="菱形" value="diamond" />
                        </el-select>
                      </el-form-item>
                      <el-form-item label="大小">
                        <el-input v-model="mainParams.points.size" placeholder="点的大小" />
                      </el-form-item>
                      <el-form-item label="不透明度">
                        <el-input v-model="mainParams.points.opacity" placeholder="0-1之间" />
                      </el-form-item>
                    </el-form>
                  </el-collapse-item>

                  <!-- 更多参数设置... -->
                </el-collapse>
              </div>
            </el-card>

            <!-- 提交按钮 -->
            <div class="submit-section">
              <el-button type="primary" size="large" @click="handleSubmit">
                确认生成
              </el-button>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-main>

    <!-- 页脚 -->
    <el-footer class="footer">
      <div class="footer-content">
        <div class="footer-links">
          <a href="/literatures">文献检索</a>
          <a href="/writings">写作工具</a>
          <a href="/products">生信工具</a>
          <a href="/gds">数据集检索</a>
          <a href="/about">关于我们</a>
          <a href="/contact">联系我们</a>
          <a href="https://www.helixlife.cn/main/helps">帮助中心</a>
        </div>
        <div class="footer-info">
          <p>© 2026 解螺旋集团 版权所有 所有权利保留</p>
          <p>沪ICP备15007276号-32</p>
        </div>
        <div class="footer-contact">
          <div class="contact-item">
            <el-icon><ChatDotSquare /></el-icon>
            <span>客服咨询</span>
          </div>
          <div class="contact-item">
            <el-icon><Location /></el-icon>
            <span>上海市徐汇区苍梧路37号越界锦和尚城T2栋15F&16F</span>
          </div>
          <div class="contact-item">
            <el-icon><Message /></el-icon>
            <span>service@helixlife.com.cn</span>
          </div>
        </div>
      </div>
    </el-footer>

    <!-- 全局设置对话框 -->
    <el-dialog v-model="showSettings" title="全局设置" width="600px">
      <!-- 设置内容 -->
      <div>全局设置内容...</div>
      <template #footer>
        <el-button @click="showSettings = false">取消</el-button>
        <el-button type="primary" @click="saveSettings">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import {
  Setting,
  Clock,
  HotWater,
  Star,
  StarFilled,
  Document,
  Refresh,
  Help,
  Download,
  ChatDotSquare,
  Location,
  Message
} from '@element-plus/icons-vue'

// 响应式数据
const activeNav = ref('products')
const activeTab = ref('all')
const activeCategories = ref(['all'])
const activeParamSections = ref(['statistics', 'points'])
const showSettings = ref(false)

// 用户数据
const userAvatar = ref('https://static.helixlife.cn/V4/avatar/default50.png')

// 参数数据
const dataParams = reactive({
  file: null
})

const mainParams = reactive({
  statMethod: 'auto',
  groupComparison: ['all'],
  significanceType: 'star',
  significanceSize: '6pt',
  points: {
    fillColor1: '#4DBBD5',
    fillColor2: '#E64B35',
    borderColor1: '#4DBBD5',
    borderColor2: '#E64B35',
    style: 'circle',
    size: '',
    opacity: ''
  }
  // 其他参数...
})

// 方法
const handleNavSelect = (key) => {
  console.log('导航选择:', key)
  // 实际应用中这里应该进行路由跳转
}

const handleTabClick = (tab) => {
  console.log('标签切换:', tab.props.name)
}

const handleUploadSuccess = (response, file) => {
  dataParams.file = file
  console.log('文件上传成功:', file)
}

const beforeUpload = (file) => {
  const isLt4M = file.size / 1024 / 1024 < 4
  if (!isLt4M) {
    ElMessage.error('文件大小不能超过4MB')
    return false
  }
  return true
}

const downloadExample = () => {
  console.log('下载示例数据')
  // 实际应用中这里应该触发文件下载
}

const resetDataParams = () => {
  dataParams.file = null
  ElMessage.success('数据参数已重置')
}

const resetMainParams = () => {
  Object.assign(mainParams, {
    statMethod: 'auto',
    groupComparison: ['all'],
    significanceType: 'star',
    significanceSize: '6pt',
    points: {
      fillColor1: '#4DBBD5',
      fillColor2: '#E64B35',
      borderColor1: '#4DBBD5',
      borderColor2: '#E64B35',
      style: 'circle',
      size: '',
      opacity: ''
    }
  })
  ElMessage.success('主要参数已重置')
}

const saveParams = () => {
  console.log('保存参数:', mainParams)
  ElMessage.success('参数保存成功')
}

const handleSubmit = () => {
  console.log('提交参数:', { dataParams, mainParams })
  ElMessage.success('正在生成图表...')
  // 实际应用中这里应该调用API生成图表
}

const saveSettings = () => {
  console.log('保存全局设置')
  showSettings.value = false
  ElMessage.success('设置保存成功')
}
</script>

<style scoped>
.analysis-tool {
  min-width: 1200px;
  background-color: #f5f7fa;
}

.header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1400px;
  margin: 0 auto;
}

.logo img {
  height: 40px;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.username {
  margin-left: 8px;
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.nav-switch {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  background-color: #fff;
  padding: 10px 20px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
}

.tool-category {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.tool-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tool-item {
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tool-item:hover {
  background-color: #f5f7fa;
}

.hot-icon {
  color: #f56c6c;
}

.new-icon {
  color: #67c23a;
}

.favorite-icon {
  color: #e6a23c;
}

.category-title {
  font-weight: bold;
  margin-bottom: 10px;
  padding-bottom: 5px;
  border-bottom: 1px solid #ebeef5;
}

.analysis-workspace {
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  padding: 20px;
}

.tool-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.tool-actions {
  display: flex;
  gap: 15px;
}

.params-card {
  margin-bottom: 20px;
}

.params-section {
  margin-bottom: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.submit-section {
  text-align: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.footer {
  background-color: #fff;
  border-top: 1px solid #ebeef5;
  margin-top: 40px;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 15px;
}

.footer-links a {
  color: #606266;
  text-decoration: none;
}

.footer-links a:hover {
  color: #409eff;
}

.footer-info {
  text-align: center;
  color: #909399;
  font-size: 12px;
  margin-bottom: 15px;
}

.footer-contact {
  display: flex;
  justify-content: center;
  gap: 30px;
  color: #606266;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.global-settings {
  margin-left: 20px;
}
</style>