<template>
  <!-- 参数设置 -->
  <el-card class="plot-card">
    <template #header>
      <div class="plot-card-header">
        <span>绘图参数</span>
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
          <div class="result-container">
            <!-- 行容器：仅保留el-row标签，清除所有Element默认布局属性 -->
            <el-row class="result-row">
              <!-- 列容器：仅保留el-col+key，无任何原生属性 -->
              <el-col v-for="item in plotStore.historicalResults" :key="item.id" class="result-col">
                <!-- 折叠面板：原有逻辑不变，样式自适应 -->
                <el-collapse class="result-collapse" accordion>
                  <el-collapse-item :title="item.title" name="1">
                    <div class="collapse-content">
                      <p>结果ID：{{ item.id }}</p>
                      <p>结果详情：{{ item.content }}</p>
                      <p>生成时间：{{ item.createTime }}</p>
                      <div class="result-actions">
                        <el-button type="text" size="small" @click="viewResult(item)">查看</el-button>
                        <el-button type="text" size="small" @click="deleteResult(item.id)">删除</el-button>
                      </div>
                    </div>
                  </el-collapse-item>
                </el-collapse>
              </el-col>
            </el-row>
          </div>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { usePlotStoreHook } from '@/store';
import { Refresh } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';

const plotStore = usePlotStoreHook();

// 重置数据
const resetData = () => {
  plotStore.clearUploadData();
  plotStore.resetPlotParams();
  ElMessage.success('数据已重置');
};

// 查看结果
const viewResult = (result: any) => {
  console.log('查看结果:', result);
  ElMessage.info(`查看结果 ${result.id}`);
};

// 删除结果
const deleteResult = (id: number) => {
  plotStore.removeHistoricalResult(id);
  ElMessage.success('结果已删除');
};
</script>

<style scoped>
/* 整体容器：和你原有页面风格统一，限制最大宽度 */
.result-container {
  width: 100%;
  max-width: 1400px;
  margin: 20px auto;
  padding: 0 16px;
  box-sizing: border-box;
}

/* 核心：行容器 - Flex布局+强制换行，彻底清除Element默认样式 */
:deep(.result-row) {
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 20px !important;
  /* 列之间的间距（4列=3个间距） */
  margin: 0 !important;
  /* 清除Element el-row默认外边距 */
  padding: 0 !important;
}

/* 核心：列容器 - 固定宽度+彻底清除默认样式，严格每行4个 */
:deep(.result-col) {
  /* Flex固定尺寸：不拉伸、不压缩，宽度精准计算（4列核心公式） */
  flex: 0 0 calc((100% - 3 * 20px) / 4) !important;
  margin-bottom: 20px !important;
  /* 行之间的间距 */
  padding: 0 !important;
  /* 彻底清除Element el-col默认内边距 */
  margin: 0 0 20px 0 !important;
  box-sizing: border-box !important;
  /* 防止内边距撑宽列 */
}

/* 折叠面板：100%继承列宽，样式和你原有橙色卡片呼应 */
:deep(.result-collapse) {
  width: 100% !important;
  border-radius: 8px !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
  border: 1px solid #e6e6e6 !important;
}

/* 折叠面板标题：浅橙色，和你之前的卡片头部风格统一 */
:deep(.result-collapse .el-collapse-item__header) {
  background: #fef7f0 !important;
  font-weight: 500 !important;
  padding: 12px 16px !important;
  margin: 0 !important;
}

/* 折叠面板内容：避免文字贴边，行高优化 */
.collapse-content {
  padding: 12px 16px;
  font-size: 14px;
  color: #606266;
  line-height: 1.8;
}

.collapse-content p {
  margin: 6px 0;
}

.result-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

/* 清除折叠面板默认间距，防止布局错位 */
:deep(.el-collapse-item) {
  margin-bottom: 0 !important;
}

:deep(.el-collapse-item__content) {
  padding: 0 !important;
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

.plot-header-actions {
  display: flex;
  gap: 10px;
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
:deep(.el-collapse-item__plot-header) {
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
</style>